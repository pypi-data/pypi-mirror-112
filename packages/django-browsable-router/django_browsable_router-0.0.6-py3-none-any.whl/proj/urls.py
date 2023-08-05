
from uuid import uuid4

from django.contrib import admin
from django.urls import path, include

from rest_framework import serializers

from browsable_router.views import BaseAPIView
from browsable_router.mixins import PostMixin, GetMixin
from browsable_router.router import APIRouter



class InputSerializer(serializers.Serializer):

    class OutputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        id = serializers.UUIDField()

    name = serializers.CharField()
    age = serializers.IntegerField()





def test_method(name: str, age: int):
    return {"email": "matti.lamppu@vincit.fi", "id": str(uuid4())}


class TestView(PostMixin, BaseAPIView):

    pipelines = {
        "POST": (InputSerializer, test_method, InputSerializer.OutputSerializer),
    }



a = APIRouter()
a.register(r"test1", TestView, "test1")
a.register(r"test2", TestView, "test2")

b = APIRouter(name="Folder 2", docstring="This is folder 2.")
b.register(r"test3", TestView, "test3")
b.register(r"test4", TestView, "test4")

c = APIRouter(name="Folder 1", docstring="This is folder 1.")
c.register(r"test5", TestView, "test5")
c.register(r"test6", TestView, "test6")



a.navigation_routes = {"folder2": b}
b.navigation_routes = {"folder1": c}


urlpatterns = [
    path("", include(a.urls)),
    path('admin/', admin.site.urls),
]
