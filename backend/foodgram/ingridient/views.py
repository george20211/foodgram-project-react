from recept.models import Ingridient
from .serializers import IngridientSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def ingridient_get(request):
    list_ingredient = Ingridient.objects.all()
    serializer = IngridientSerializer(list_ingredient, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def ingridient_id_get(request, id):
    ingredient = Ingridient.objects.filter(id=id)
    serializer = IngridientSerializer(ingredient, many=True)
    return JsonResponse(serializer.data, safe=False)
