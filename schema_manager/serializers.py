from rest_framework import serializers
from .models import Table, Field


class DynamicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, required=False)

    class Meta:
        model = Table
        fields = '__all__'

    def create(self, validated_data):
        fields_data = validated_data.pop('fields', [])
        table = Table.objects.create(**validated_data)
        for field_data in fields_data:
            Field.objects.create(table=table, **field_data)
        return table

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', [])
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        for field_data in fields_data:
            field_id = field_data.get('id')
            if field_id:
                field = Field.objects.get(id=field_id)
                field.name = field_data.get('name', field.name)
                field.type = field_data.get('type', field.type)
                field.save()
            else:
                Field.objects.create(table=instance, **field_data)
        return instance