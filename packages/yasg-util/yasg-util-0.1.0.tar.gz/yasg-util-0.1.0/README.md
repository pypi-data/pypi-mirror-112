# yasg-util

Injecting parameters through annotations based on drf-yasg

## Requirements

- Python 3.6+
- drf-yasg

## Installation

```shell
$ pip install yasg-util
```

## Start

settings.py

```python
INSTALLED_APPS = [
   ...
   'django.contrib.staticfiles',  # required for serving swagger ui's css/js files
   'drf_yasg',
   ...
]
```

urls.py

```python
from django.urls import path, re_path
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework.fields import IntegerField, CharField, DictField
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from yasg_util import Response, restapi, Location

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


class DemoSerializer(Serializer):
    name = CharField(required=True, min_length=2, max_length=20, help_text='姓名')
    age = IntegerField(required=True, min_value=0, max_value=150, help_text='年龄')

    class Meta:
        location = Location.BODY


class ResponseSerializer(Serializer):
    code = IntegerField(default=200, help_text='状态码')
    msg = CharField(default='success', help_text='响应消息')
    data = DictField(help_text='响应数据')


class DemoAPIView(APIView):
    @restapi()
    def post(self, request, pk: int, serializer: DemoSerializer) -> Response[ResponseSerializer]:
        res = serializer.data
        res['id'] = pk
        return Response({'code': 0, 'msg': 'success', 'data': res})


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # type:ignore
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # type:ignore
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # type:ignore
    path('demo/<int:pk>', DemoAPIView.as_view()),
]
```

go to http://127.0.0.1:8000/doc
