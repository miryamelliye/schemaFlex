from django.core.cache import cache
from django.db import models, connection

from .models import *


def generate_model(table_id):
    table = Table.objects.get(pk=table_id)
    fields = Field.objects.filter(table=table)

    attrs = {
        "Meta": type(
            "Meta",
            (),
            {"app_label": "schema_manager"}
        ),
        "__module__": "schema_manager.models"
    }

    for field in fields:
        if field.type == 'text':
            attrs[field.name] = models.CharField(max_length=255)
        elif field.type == 'integer':
            attrs[field.name] = models.IntegerField()
        elif field.type == 'boolean':
            attrs[field.name] = models.BooleanField()
        elif field.type == 'date':
            attrs[field.name] = models.DateField()
        elif field.type == 'datetime':
            attrs[field.name] = models.DateTimeField()


    GeneratedModel = type(
        f"Table{table_id}",
        (models.Model,),
        attrs
    )

    return GeneratedModel


def create_table(table_id):
    GeneratedModel = generate_model(table_id)

    table_name = f"schema_manager_table{table_id}"

    if table_name in connection.introspection.table_names():
        print(f"Table {table_name} already exists. Skipping table creation.")
        return

    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(GeneratedModel)

    if hasattr(GeneratedModel, 'name'):
        GeneratedModel.objects.create(name="Sample Data")


def update_table_schema(table_id, field):
    GeneratedModel = generate_model(table_id)
    table_name = f"schema_manager_table{table_id}"

    if table_name not in connection.introspection.table_names():
        raise ValueError(f"Table {table_name} does not exist!")

    if field.type == 'text':
        new_field = models.CharField(max_length=255)
    elif field.type == 'integer':
        new_field = models.IntegerField()
    elif field.type == 'boolean':
        new_field = models.BooleanField()
    elif field.type == 'date':
        new_field = models.DateField()
    elif field.type == 'datetime':
        new_field = models.DateTimeField()

    new_field.set_attributes_from_name(field.name)
    new_field.model = GeneratedModel

    with connection.schema_editor() as schema_editor:
        schema_editor.add_field(GeneratedModel, new_field)


def get_model_from_cache(table_id):
    cached_attrs = cache.get(f"table_model_cache_{table_id}")
    if cached_attrs:
        return type(f"Table{table_id}", (models.Model,), cached_attrs)
    else:
        GeneratedModel = generate_model(table_id)
        cache.set(f"table_model_cache_{table_id}", GeneratedModel._meta.get_fields(), timeout=None)
        return GeneratedModel