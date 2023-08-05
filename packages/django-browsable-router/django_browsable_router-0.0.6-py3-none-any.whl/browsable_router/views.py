"""Base API view that can be used with the router."""

from collections.abc import Callable
from typing import Dict, Any, Type, Union, Literal, Tuple

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.serializers import Serializer

from .meta import APIMetadata
from .mixins import RootMixin
from .serializers import MockSerializer


__all__ = ["BaseAPIView", "APIRootView"]


method = Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS', 'TRACE']
input_serializer = Type["Serializer"]
logic = Callable[..., Dict[str, Any]]
output_serializer = Type["Serializer"]


class BaseAPIView(APIView):
    """Base view for browsable API.

    Generate views by inheriting this class and any number of the included mixins.
    Set the 'input_serializer_classes' 'output_serializer_classes',
    and 'logic_methods' with the appropriate keys for the HTTP methods used,
    and your custom serializers as the values. This way the class can have
    different serializers for different HTTP methods with both input and output
    verification.
    """

    pipelines: Dict[method, Tuple[input_serializer, logic, output_serializer]] = {}
    """Dictionary describing the HTTP method pipelines.
    Key is the name of the HTTP method in all caps.
    Values is a tuple of the input serializer, main logic function,
    and output serializer used for that method.
    """

    metadata_class = APIMetadata
    """Metadata cass that provides automatic documentation.
    Make an OPTIONS request to see what inputs and outputs each
    HTTP endpoint takes and outputs.
    """

    def _process_request(self, data: Dict[str, Any]) -> Response:
        """Process request in a pipeline-fashion.

        :param data: Data coming in from the request.
        """

        data = self._run_serializer(data=data)
        data = self._run_logic(data=data)
        data = self._run_serializer(data=data, output=True)

        if data:
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def _run_serializer(self, data: Dict[str, Any], output: bool = False) -> Dict[str, Any]:
        """Build and validate input or output serializer.

        :param data: Data to initialize serializer with.
        :param output: Use output serializers instead of input serializers for the HTTP method.
        """

        self._output_ = output  # noqa
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        self._output_ = False  # noqa
        return data

    def _run_logic(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Main part of the internal logic for the request.

        :param data: Data to pass to the function.
        """

        try:
            logic_method = self.pipelines[self.request.method][1]
        except KeyError:
            raise KeyError(f"No logic configured for HTTP method '{self.request.method}'")

        return logic_method(**data)

    def get_serializer(self, *args, **kwargs) -> "Serializer":
        """Initialize serializer for current request HTTP method.
        Use output serializers if self._output_ == True, else input serializers.
        """

        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        kwargs.setdefault("many", getattr(serializer_class, "many", False))
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self) -> Type["Serializer"]:
        """Get serializer class based on current request HTTP method.

        :raises KeyError: If serializer for a method was not setup in either
                          'input_serializer_classes' and/or 'output_serializer_classes'.
        """

        output = getattr(self, "_output_", False)
        try:
            if output:
                return self.pipelines[self.request.method][2]
            else:
                return self.pipelines[self.request.method][0]
        except KeyError:
            direction = "Output" if output else "Input"
            raise KeyError(f"{direction} serializer is not configured for HTTP method '{self.request.method}'")

    def get_serializer_context(self) -> Dict[str, Union[Request, "BaseAPIView"]]:
        """Return serializer context, mainly for browerable api."""
        return {"request": self.request, "view": self}


class APIRootView(RootMixin, BaseAPIView):
    """Welcome! This is the API root."""

    pipelines = {
        "GET": (
            type("Input", (MockSerializer,), {"_format": "Nothing."}),
            lambda: None,
            type("Output", (MockSerializer,), {"_format": "URLs in this root."}),
        ),
    }
