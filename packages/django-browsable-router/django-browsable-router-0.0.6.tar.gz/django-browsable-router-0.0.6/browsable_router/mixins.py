"""
Mixin classes to be used with BaseAPIView.
"""

from django.urls import NoReverseMatch

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.reverse import reverse

from .utils import translate


__all__ = [
    "GetMixin",
    "PostMixin",
    "PutMixin",
    "PatchMixin",
    "DeleteMixin",
    "RootMixin",
    "HeadMixin",
    "OptionsMixin",
    "TraceMixin",
]


class GetMixin:

    @translate
    def get(self, request: Request, *args, **kwargs) -> Response:
        data = {key: value for key, value in request.query_params.items()}
        # Update data from extra options.
        # https://docs.djangoproject.com/en/3.2/topics/http/urls/#passing-extra-options-to-view-functions
        data.update(**kwargs)
        return self._process_request(data=data)


class PostMixin:

    @translate
    def post(self, request: Request, *args, **kwargs) -> Response:
        data = {key: value for key, value in request.data.items()}
        data.update(**kwargs)
        return self._process_request(data=data)


class PutMixin:

    @translate
    def put(self, request: Request, *args, **kwargs) -> Response:
        data = {key: value for key, value in request.data.items()}
        data.update(**kwargs)
        return self._process_request(data=data)


class PatchMixin:

    @translate
    def patch(self, request: Request, *args, **kwargs) -> Response:
        data = {key: value for key, value in request.data.items()}
        data.update(**kwargs)
        return self._process_request(data=data)


class DeleteMixin:

    @translate
    def delete(self, request: Request, *args, **kwargs) -> Response:
        data = {key: value for key, value in request.data.items()}
        data.update(**kwargs)
        return self._process_request(data=data)


class HeadMixin:

    @translate
    def head(self, request: Request, *args, **kwargs) -> Response:
        data = {key: value for key, value in request.data.items()}
        data.update(**kwargs)
        return self._process_request(data=data)


class OptionsMixin:

    @translate
    def options(self, request: Request, *args, **kwargs) -> Response:
        data = {key: value for key, value in request.data.items()}
        data.update(**kwargs)
        return self._process_request(data=data)


class TraceMixin:

    @translate
    def trace(self, request: Request, *args, **kwargs) -> Response:
        data = {key: value for key, value in request.data.items()}
        data.update(**kwargs)
        return self._process_request(data=data)


class RootMixin:

    api_root_dict = {}

    @translate
    def get(self, request: Request, *args, **kwargs) -> Response:
        routes = {}
        namespace = request.resolver_match.namespace
        for key, url_name in self.api_root_dict.items() or {}:  # noqa
            if namespace:
                url_name = namespace + ':' + url_name
            try:
                routes[key] = reverse(
                    url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get('format', None)
                )
            except NoReverseMatch:
                continue

        return Response(routes)