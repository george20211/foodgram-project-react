from recept.models import Ingridient
from rest_framework import serializers


class IngridientSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    measurement_unit = serializers.StringRelatedField()

    class Meta:
        model = Ingridient
        fields = ('__all__')
