from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'dynamic-models/(?P<table_id>\w+)', DynamicModelCRUDViewSet, basename='dynamic-model')
router.register(r'tables', TableViewSet)
router.register(r'fields', FieldViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
