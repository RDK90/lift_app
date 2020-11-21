from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from workouts.api_support import *

from .models import Profile, PlanVersionTwo, Plan
from .serializers import PlanSerializer


@api_view(['GET'])
def all_plans(request):
    if request.method == "GET":
        workouts = Plan.objects.all()
        plan_serializer = PlanSerializer(workouts, many=True)
        response_data = [{"date":"", "workout":[]}]
        index = 0
        for plan in plan_serializer.data:
            date = plan.pop("date")
            if response_data[index]["date"] == "" or response_data[index]["date"] != date:
                response_data.append({"date":date, "workout":[plan]})
                index = index + 1
            else:
                response_data[index]["workout"].append(plan)
        response_data.pop(0)
        return Response(response_data)

@api_view(['GET','PUT', 'POST', 'DELETE'])
def plans_by_date(request, date):
    date = format_date(date)
    try:
        workouts = Plan.objects.filter(date=date).values()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        if not workouts:
            content = {"Error message": "No plan for date {} found".format(date)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            plan_serializer = PlanSerializer(workouts, many=True)
            for plans in plan_serializer.data:
                plans.pop("date")
            return Response({"date":date, "plan": plan_serializer.data})
    if request.method == "PUT" or request.method == "POST":
        return put_post_workouts_by_id_response(request)
    if request.method == "DELETE":
        plan = Plan.objects.filter(date=date)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def all_plans_version_two(request):
    if request.method == "GET":
        profile_user = Profile.objects.get(user=request.user)
        workouts = PlanVersionTwo.objects.filter(user=profile_user)
        plan_serializer = PlanSerializer(workouts, many=True)
        response_data = [{"date":"", "workout":[]}]
        index = 0
        for plan in plan_serializer.data:
            date = plan.pop("date")
            if response_data[index]["date"] == "" or response_data[index]["date"] != date:
                response_data.append({"date":date, "workout":[plan]})
                index = index + 1
            else:
                response_data[index]["workout"].append(plan)
        response_data.pop(0)
        return Response(response_data)