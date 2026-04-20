from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import InternetData, HealthCenterData
import json
class InternetDataSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = InternetData
        geo_field = "mpoly" 
        fields = [
            'id', 'brandname', 'technology', 'minup', 'mindown', 
            'frn', 'providerid', 'minsignal', 'environmnt', 'h3_res9_id'
        ]
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.mpoly:
            simplified_geom = instance.mpoly.simplify(0.001)
            ret['geometry'] = json.loads(simplified_geom.geojson)
        return ret
class HealthCenterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCenterData
        fields = ['id','name','location']
    