from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ia_model.funcoes_IA import previsao
import requests

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Voos
from .models import Resultado_ia
from .serializers import VoosSerializer, Resultado_iaSerializer

import json

# Acessando todos os dados


@swagger_auto_schema(
    method='get',
    tags=['Voos'],
    operation_summary='Lista de Voos',
    operation_description='Endpoint para recuperação de lista de Voos aéreos.',
    responses={200: openapi.Response(
        'Success',), 400: openapi.Response('Bad request')},
)
@api_view(['GET'])
def get_voos(request):
    if request.method == 'GET':
        voos = Voos.objects.all()
        serializer = VoosSerializer(voos, many=True)
        formatted_response = {
            'success': True,
            'message': 'Recuperação lista de voos.',
            'data': serializer.data
        }
        return Response(formatted_response, status=status.HTTP_200_OK)
    return Response({'error': 'Requisição inválida'}, status=status.HTTP_400_BAD_REQUEST)


# Acessando por link direto
@swagger_auto_schema(
    method='get',
    tags=['Voos'],
    operation_summary='Buscar usuário por link direto',
    operation_description='Endpoint para recuperação de voo por link direto.',
    responses={200: openapi.Response(
        'Success',), 404: openapi.Response('Not found')},
)
@api_view(['GET'])
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


# Criando dados
@swagger_auto_schema(
    method='post',
    tags=['Voos'],
    operation_summary='Cadastro de Voo',
    operation_description='Endpoint para cadastro de voo',
    responses={201: openapi.Response(
        'Created'), 400: openapi.Response('Bad request')},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['airline', 'flight', 'airpot_from',
                  'airpot_to', 'day_of_week', 'time', 'delay'],
        properties={
            'airline': openapi.Schema(type=openapi.TYPE_STRING),
            'flight': openapi.Schema(type=openapi.TYPE_INTEGER),
            'airpot_from': openapi.Schema(type=openapi.TYPE_STRING),
            'airpot_to': openapi.Schema(type=openapi.TYPE_STRING),
            'day_of_week': openapi.Schema(type=openapi.TYPE_STRING),
            'time': openapi.Schema(type=openapi.TYPE_INTEGER),
            'delay': openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    ),
)
@api_view(['POST'])
def post_create_voo(request):
    if request.method == 'POST':
        new_voos = request.data
        id = new_voos.get('id')

        if Voos.objects.filter(id=id).exists():
            formatted_response = {
                'success': False,
                'message': 'Voo já existente.'
            }
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = VoosSerializer(data=new_voos)

        if serializer.is_valid():
            serializer.save()

            formatted_response = {
                'success': True,
                'message': 'Voo cadastrado com sucesso.',
                'data': serializer.data
            }
            return Response(formatted_response, status=status.HTTP_201_CREATED)
        formatted_response = {
            'success': False,
            'message': 'Erro ao cadastrar Voo.',
            'errors': serializer.errors
        }
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)


# Editando dados
@swagger_auto_schema(
    method='put',
    tags=['Voos'],
    operation_summary=' Atualização de voo',
    operation_description='Endpoint para atualização de voo',
    responses={202: openapi.Response(
        'Created'), 400: openapi.Response('Bad request')},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['airline', 'flight', 'airpot_from',
                  'airpot_to', 'day_of_week', 'time', 'delay'],
        properties={
            'airline': openapi.Schema(type=openapi.TYPE_STRING),
            'flight': openapi.Schema(type=openapi.TYPE_INTEGER),
            'airpot_from': openapi.Schema(type=openapi.TYPE_STRING),
            'airpot_to': openapi.Schema(type=openapi.TYPE_STRING),
            'day_of_week': openapi.Schema(type=openapi.TYPE_STRING),
            'time': openapi.Schema(type=openapi.TYPE_INTEGER),
            'delay': openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    ),
)
@api_view(['PUT'])
def put_edit_user(request, id):
    try:
        update_request = request.data
        update_voo = Voos.objects.get(pk=id)
    except Voos.DoesNotExist:
        formatted_response = {
            'success': False,
            'message': 'Voo não encontrado.'
        }
        return Response(formatted_response, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = VoosSerializer(
            update_voo, data=update_request, partial=True)
        if serializer.is_valid():
            serializer.save()
            formatted_response = {
                'success': True,
                'message': 'Voo editado com sucesso.',
                'data': serializer.data
            }
            return Response(formatted_response, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Deletando dados
@swagger_auto_schema(
    method='delete',
    tags=["Voo"],
    operation_summary='Deletar voo por id',
    operation_description='Endpoint para deleção de voo',
    responses={200: openapi.Response(
        'Sucess'), 404: openapi.Response('Not found')},
)
@api_view(['DELETE'])
def delete_voo(request, id):
    try:
        if request.method == 'DELETE':
            user_exists = Voos.objects.filter(id=id).exists()
            if user_exists:
                Voos.objects.filter(id=id).delete()
                return JsonResponse({'success': True, 'message': 'Voo deletado com sucesso.'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'success': False, 'message': 'Voo não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    except:
        return JsonResponse({'success': False, 'message': 'Erro interno no servidor:'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Resultado IA
@api_view(['GET'])
def get_resultado_ia(request, id):
    try:
        resultado = Resultado_ia.objects.get(usuario=id)
    except:
        formatted_response = {
            'success': False,
            'message': 'Resultado não localizado.'
        }
        return Response(formatted_response, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = Resultado_iaSerializer(resultado)
        formatted_response = {
            'success': True,
            'message': 'Resultado recuperado.',
            'data': serializer.data
        }
        return Response(formatted_response, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    tags=['Voos'],
    operation_summary='Gerar resultado por id',
    operation_description='Endpoint para gerar o resultado do Voo',
    responses={200: openapi.Response(
        'Success',), 404: openapi.Response('Not found')},

)
@api_view(['POST'])
def post_resultado_ia(request, id):
    if request.method == 'POST':
        try:
            voo = Voos.objects.get(pk=id)
            dados = {
                'Airline': [voo.airline],
                'Flight': [voo.flight],
                'Airport_From': [voo.airpot_from],
                'Airport_To': [voo.airpot_to],
                'Day_of_Week': [voo.day_of_week],
                'Time': [voo.time],
                'Delay': [voo.delay]
            }
            resultado = previsao(dados)

            resultado = resultado.tolist()[0]

            serializer = Resultado_iaSerializer(data={
                'resultado': resultado,
                'Voo': voo.id
            })
            if serializer.is_valid():
                serializer.save()

            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except Voos.DoesNotExist:
            return JsonResponse({'error': 'Voo não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Erro interno no servidor: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)


@swagger_auto_schema(
    method='get',
    tags=['Buscar Voo'],
    operation_summary='Buscar os dados por Voo',
    operation_description='Endpoint para recuperação através do Voo.',
    responses={200: openapi.Response(
        'Success',), 500: openapi.Response('Internal server error')},

)
@api_view(['GET'])
def consultar_flight(request, flight):
    if request.method == 'GET':
        url = f"https://viacep.com.br/ws/{flight}/json/"
        response = requests.get(url)

    if response.status_code == 200:
        dados_flight = response.json()
        return JsonResponse(dados_flight)
    else:
        return JsonResponse({'error': 'Erro ao obter informações do Voo'}, status=500)


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
