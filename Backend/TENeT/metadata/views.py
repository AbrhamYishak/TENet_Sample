from django.shortcuts import render
from .models import MetaData
# Create your views here.
def updateMetadata(lastupdate):
    MetaData.objects.update_or_create(pk =  1,LastUpdate = lastupdate)
    MetaData.save()
def getLastupdate():
    return MetaData.objects.get(id = 1).Lastupdated