from rest_framework import filters, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from .utils import *
from .tasks import import_data_task


class DynamicModelCRUDViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = '__all__'
    ordering_fields = '__all__'
    ordering = ['id']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        table_id = self.kwargs['table_id']
        model = get_model_from_cache(table_id)
        return model.objects.all()

    def get_serializer_class(self):

        class DynamicSerializer(serializers.ModelSerializer):
            class Meta:
                model = get_model_from_cache(self.kwargs['table_id'])
                fields = '__all__'

        return DynamicSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        table_id = response.data['id']
        create_table(table_id)
        return response

class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        table_id = request.data['table']

        field_id = response.data['id']
        field = Field.objects.get(pk=field_id)
        update_table_schema(table_id, field)

        return response


class BulkDataImportAPIView(APIView):
    def post(self, request):
        """
        Handle large data imports asynchronously.
        Example input: {"model_name": "Customer", "data": [{"name": "John", "email": "john@example.com"}, ...]}
        """
        model_name = request.data.get('model_name')
        data = request.data.get('data')
        import_data_task.delay(model_name, data)

        return Response("Import process has started.", status=status.HTTP_202_ACCEPTED)
