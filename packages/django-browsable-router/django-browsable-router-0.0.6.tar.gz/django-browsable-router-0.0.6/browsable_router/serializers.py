""""""

from typing import Union, Dict, List

from rest_framework.serializers import Serializer


__all__ = ["MockSerializer"]


class MockSerializer(Serializer):
    """Serializer that allows passing a custom output format."""

    _format: Union[Dict, List, str] = {}

    def to_representation(self, instance):
        many = getattr(self, "many", False)
        is_dict = isinstance(self._format, dict)
        return self._format if is_dict else [self._format] if many else {"description": self._format}
