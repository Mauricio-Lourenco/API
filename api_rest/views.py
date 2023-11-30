from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Voos
from .serializers import VoosSerializer

import json


# Acessando todos os dados
@api_view(['GET'])
def get_voos(request):
    if request.method == 'GET':
        voos = Voos.objects.all()
        serializer = VoosSerializer(voos, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# Acessando por link direto
@api_view(['GET', 'PUT'])
def get_by_id(request, id):

    try:
        voos = Voos.objects.get(pk=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        serializer = VoosSerializer(voos)
        return Response(serializer.data)

    if request.method == 'PUT':

        SERIALIZER = VoosSerializer(voos, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# CRUD
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def voos_manager(request):

    if request.method == 'GET':

        try:
            if request.GET['voos']:

                voos_id = request.GET['id']

                try:
                    voos = Voos.objects.get(pk=voos_id)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                serializer = VoosSerializer(voos)
                return Response(serializer.data)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# Criando dados
    if request.method == 'POST':

        new_voos = request.data

        serializer = VoosSerializer(data=new_voos)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


# Editando dados
    if request.method == 'PUT':
        id = request.data['voos_id']

        try:
            update_voos = Voos.objects.get(pk=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# Deletando dados
    if request.method == 'DELETE':
        try:
            voos_to_delete = Voos.objects.get(pk=request.data['voos_id'])
            voos_to_delete.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
