"""Metadata classes."""

from rest_framework.serializers import HiddenField, Serializer, ListSerializer
from rest_framework.request import clone_request, Request
from rest_framework.metadata import SimpleMetadata

from .serializers import MockSerializer


__all__ = ["APIMetadata", "SerializerAsOutputMetadata"]


class APIMetadata(SimpleMetadata):
    """Metadata class that adds input and output info for each of the attached views methods based on
    the serializer for that method. """

    recognized_methods = {"GET", "POST", "PUT", "PATCH", "DELETE"}

    def determine_actions(self, request: Request, view):
        """Return information about the fields that are accepted for methods in self.recognized_methods."""
        actions = {}
        for method in self.recognized_methods & set(view.allowed_methods):
            view.request = clone_request(request, method)

            input_serializer = view.get_serializer()
            view._output_ = True
            output_serializer = view.get_serializer()
            view._output_ = False

            actions[method] = {
                "input": self.get_serializer_info(input_serializer),
                "output": self.get_serializer_info(output_serializer),
            }
            view.request = request

        return actions

    def get_serializer_info(self, serializer: Serializer):
        """Given an instance of a serializer, return a dictionary of metadata about its fields."""
        data_serializer = getattr(serializer, "child", serializer)

        if isinstance(data_serializer, MockSerializer):
            return data_serializer._format

        input_data = {
            field_name: self.get_field_info(field)
            for field_name, field in data_serializer.fields.items()
            if not isinstance(field, HiddenField)
        }

        if isinstance(serializer, ListSerializer):
            input_data = [input_data]

        return input_data

    def get_field_info(self, field):
        if getattr(field, "child", False):
            return [self.get_field_info(field.child)]
        elif getattr(field, "fields", False):
            return self.get_serializer_info(field)
        else:
            return super().get_field_info(field)


class SerializerAsOutputMetadata(APIMetadata):
    """Metadata class that presumes that view serializer is used as response data with no request data."""


    def determine_actions(self, request: Request, view):
        """Return information about the fields that are accepted for methods in self.recognized_methods."""
        actions = {}
        for method in self.recognized_methods & set(view.allowed_methods):
            view.request = clone_request(request, method)

            input_serializer = view.get_serializer()

            actions[method] = {
                "input": {},
                "output": self.get_serializer_info(input_serializer),
            }
            view.request = request

        return actions
