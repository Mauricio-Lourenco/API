from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Documentação API Voos",
        default_version='v1',
        description="API contém CRUD com todas as suas funcionalidades(GET, POST, PUT e DELETE)",
        terms_of_service="https://www.apivoos.com/terms/",
        contact=openapi.Contact(email="contact@apivoos.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.get_voos, name='get_all_voos'),
    path('voos/<int:id>', views.get_by_id),
    path('data/', views.voos_manager),
    path('consultar_flight/<str:flight>/', views.consultar_flight),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
