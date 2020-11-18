from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from workouts.api_support import *

from .models import Characteristics, CharacteristicsVersionTwo, Profile
from .serializers import CharacteristicsSerializer

@swagger_auto_schema(
    method='GET',
    operation_id='GET Characteristics by <date>',
    operation_description='GET /characteristics/date \n Date in format ddmmyyy \n Example: GET /characteristics/25032019'
)
@swagger_auto_schema(
    method='POST',
    operation_id='POST Characteristics by <date>',
    operation_description='POST /characteristics/date \n Date in format ddmmyyy \n Example: POST /characteristics/25032019'
)
@swagger_auto_schema(
    method='PUT',
    operation_id='PUT Characteristics by <date>',
    operation_description='PUT /characteristics/date \n Date in format ddmmyyy \n Example: PUT /characteristics/25032019'
)
@swagger_auto_schema(
    method='DELETE',
    operation_id='DELETE Characteristics by <date>',
    operation_description='DELETE /characteristics/date \n Date in format ddmmyyy \n Example: DELETE /characteristics/25032019'
)
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

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def characteristics_by_date_version_two(request, date):
    formatted_date = format_date(date)
    try:
        profile_user = Profile.objects.get(user=request.user)
        characteristics = CharacteristicsVersionTwo.objects.filter(user=profile_user, date=formatted_date).values()
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
        characteristics = CharacteristicsVersionTwo.objects.filter(user=profile_user, date=formatted_date)
        characteristics.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)