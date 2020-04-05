from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from workouts.api_support import *

from .models import Characteristics
from .serializers import CharacteristicsSerializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def characteristics_by_date(request, date):
    date = format_date(date)
    try:
        characteristics = Characteristics.objects.filter(date=date).values()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        if not characteristics:
            content = {"Error Message: Characteristics for date {} not found".format(date)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            characteristics_serializer = CharacteristicsSerializer(characteristics, many=True)
            return Response(characteristics_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST' or request.method == 'PUT':
        return put_post_characteristics_by_date_response(request)
    elif request.method == 'DELETE':
        characteristics = Characteristics.objects.filter(date=date)
        characteristics.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)