from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import InternetData, HealthCenterData
from .serializers import InternetDataSerializer,HealthCenterDataSerializer
from .logic import updateHealthData, updaateInternetData, calculateScore
from django.db.models import Func
from django.contrib.gis.db.models import GeometryField
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
class Simplify(Func):
    function = "ST_SimplifyPreserveTopology"
    output_field = GeometryField()
class LocationDataView(APIView):
    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        updateHealthData()
        updaateInternetData()
        InternetDatas = InternetData.objects.annotate(simple_geom=Simplify('mpoly', 0.01)).all()[:100000]
        HealthCenterDatas = HealthCenterData.objects.all()
        SerializedInternetData = InternetDataSerializer(InternetDatas,many=True)
        SerializedHealthCenterData = HealthCenterDataSerializer(HealthCenterDatas,many=True)
        return Response({
            'internet': SerializedInternetData.data,
            'health':SerializedHealthCenterData.data
        },status = status.HTTP_200_OK)
class ScoreCalculationView(APIView):
    def post(self,request,*args,**kwargs):
        longtiude = request.data.get("longtiude")
        latitiude = request.data.get("latitiude")
        radius = request.data.get("MapRadius")
        res = calculateScore(latitiude,longtiude,radius)
        return Response({
            "result":res
        },status = status.HTTP_200_OK)