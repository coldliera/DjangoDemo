from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="接口文档",
        default_version='v1',
        license=openapi.License(name="BSD License")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# 请注意此处两种路由方式：通过 urlpatterns 和 router。这是因为 AT1View 没有使用 ModelViewSet, router 没法自动补全所有的端口类型，因此需要手动添加路由。
urlpatterns = [
    path(r'docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'at1/', AT1View.as_view()),
]

router = routers.DefaultRouter()

router.register('t1', T1View)
router.register('t2', T2View)
router.register('pt', PTView)

urlpatterns += router.urls
