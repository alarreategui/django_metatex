from .models import Role
from .permissions import IsUserActivate
from .serializers import *
from apps.tareo.models import BaseMachinery
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from exceptions.utils import log_exception_with_object
from precotex_db.settings_api import REQUESTS, URL
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import re
import requests
from apps.kanban.models import Route, Process, RoutePoint
def create_users(employees):
    for employee in employees:
        try:
            username = employee['cod_Usuario'].rstrip()
            if not User.objects.filter(username=username).exists():
                nuevo_usuario = User.objects.create_user(username=username, password='1234')
                nuevo_usuario.save()
                print(f"Usuario {username} creado")
            else:
                print(f"El usuario {username} ya existe")
        except Exception as e:
            if e:
                print(str(e))
            # log_exception_with_object(e, employee)
            print(f"Error en Empleado : {employee}")
       
def create_base_machineries(machineries):
    for machinery in machineries:
        try:
            maq_base = machinery['maq_base'].rstrip()
            des_Maquina = machinery['des_Maquina'].rstrip().split(' ')
            if not BaseMachinery.objects.filter(code=maq_base).exists():
                if len(des_Maquina) > 0:
                    base_machinery = BaseMachinery(code=maq_base, name=des_Maquina[0])
                else:
                    base_machinery = BaseMachinery(code=maq_base)
                base_machinery.save()
                print(f"Maquinaria base '{maq_base}' creada")
        except Exception as e:
            if e:
                print(str(e))

def make_request(key):
    payload = {}
    headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiIyODgiLCJuYmYiOjE3MDYwMzg4NDQsImV4cCI6MTcwNjA0MDY0NCwiaWF0IjoxNzA2MDM4ODQ0fQ.oF3KQKpt_ZYuPawm5SFJ8dE3UZUU938PdXa1GlzeoN4'
    }
    url = f'{URL}{key}'
    response = requests.request("GET", url, headers=headers, data=payload)
    return response

def make_dictionary(data, base_dictionary):
    new_dictionary = {}
    for key, value in base_dictionary.items():
        new_dictionary[value] = data[key]
    return new_dictionary

def validate_datetime_format(cadena):
    patron = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}"
    if re.match(patron, cadena):
        return True
    else:
        return False
    
def filter_data(base_dictionary, data):
    foreign_keys = {}
    # Obtener un diccionario con las claves foraneas
    for key, value in base_dictionary.items():
        if not type(value) == str:
            foreign_keys[key] = {}
    print(f"Foreign keys: {foreign_keys.keys()}")
    new_data = []
    # Recorrer el arreglo de datos
    for obj in data:
        new_dictionary = {}
        # Por cada objeto de datos hacer un nuevo diccionrio
        for key, value in base_dictionary.items():
            if type(obj[key]) == str:
                try:
                    obj[key] = obj[key].rstrip()
                except Exception as e:
                    print(e)
            if key in foreign_keys.keys():
                # Si la clave forane se encuentra ya en el diccionario foreign_keys comprobamos que sea valida
                if obj[key] in foreign_keys[key].keys():
                    # si es valida enconces se añade al nuevo diccionario
                    if foreign_keys[key][obj[key]]:
                        new_dictionary[base_dictionary[key]['value']] = foreign_keys[key][obj[key]]
                    # en caso de no ser valida se rompe el for y se ignora el dato
                    else:
                        break
                # Si no esta en foreign_keys la buscamos en la base de datos
                else:
                    # obtenemos el valor de la clave foranea
                    if not type(base_dictionary[key]['pk']) == str:
                        primary_key = { pk[1]: obj[pk[0]] for pk in base_dictionary[key]['pk'] }
                    else:
                        primary_key = { base_dictionary[key]['pk']: obj[key] }
                    model = base_dictionary[key]['model']
                    try:
                        instance = model.objects.get(**primary_key)
                        foreign_keys[key][obj[key]] = instance
                        new_dictionary[base_dictionary[key]['value']] = instance
                    except ObjectDoesNotExist:
                        foreign_keys[key][obj[key]] = None
                        print(f"Error, no existe el Modelo: {str(model)} - con la primary key:{primary_key}")
                        break
                    except Exception as e:
                        if e:
                            print(str(e))
                        print(f"Error, en Modelo: {str(model)} - primary key:{primary_key}")
                        # log_exception_with_object(e, primary_key)
            else:
                try:
                    new_dictionary[value] = obj[key]
                except TypeError:
                    print('TypeError')
                    print(value, key, obj)
                    break
        new_data.append(new_dictionary)
    return new_data


def first_request(request):
    # recorrer todos los endpoints
    print("Iniciando sincronizacion")
    for key in REQUESTS.keys():
        print(f"Endpoint actual: {key} \nModelo actual: {str(REQUESTS[key]['model'])}")
        try:
            response = make_request(key)
            if response.status_code == 200:
                response = response.json()
                if key == '/api/Empleado/ConsultaEmpleados':
                    create_users(response)
                elif key == '/api/Maquina/ConsultaMaquinas':
                    create_base_machineries(response)
                response = filter_data(REQUESTS[key]['attributes'], response)
                model =  REQUESTS[key]['model']
                for res in response:
                    try:
                        instance = model(**res)
                        instance.save()
                    except IntegrityError:
                        pass
                    except Exception as error:
                        pass
                        # log_exception_with_object(error, res)
            else:
                print('Error: Status code: %d' % response.status_code)
                # log_exception_with_object('Error: Status code: %d' % response.status_code)
        except Exception as e:
            print(e)
            log_exception_with_object(e)
    return JsonResponse({'mensaje': 'Operación ejecutada con éxito'}, status=202)

def get_all_routes(request):
    # recorrer todos los endpoints
    # all_routes = Route.objects.all()
    all_code_routes = {route.code for route in Route.objects.all()}
    print("Iniciando sincronizacion")
    for code in all_code_routes:
        print(f"Ruta actual: {code}")
        try:
            response = make_request(f"/api/Tela/ConsultaRutaProceso?Cod_Ruta={code}")
            if response.status_code == 200:
                route_points_data = response.json()
                for point_data in route_points_data:
                    process_code = point_data['cod_Proceso']
                    route_code = point_data['cod_Ruta']
                    if Process.objects.filter(code=process_code).exists() and Route.objects.filter(code=route_code).exists():
                        route_point = RoutePoint(
                            process_code=Process.objects.filter(code=process_code).first(),
                            route_code=Route.objects.filter(code=route_code).first(),
                            sequence=point_data['secuencia']
                        )
                        route_point.save()
                    else:
                        print(f"Could not find associated process or route for the point: {point_data}")
            else:
                print('Error: Status code: %d' % response.status_code)
                # log_exception_with_object('Error: Status code: %d' % response.status_code)
        except Exception as e:
            print(e)
            log_exception_with_object(e)
    return JsonResponse({'mensaje': 'Operación ejecutada con éxito'}, status=202)

class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                    },
                },200)
            except Exception as e:
                return Response({'error': str(e)}, 500)
        else:
            return Response(serializer.errors, 400)
        
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = request.user
        try:
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                return Response({
                    'isAuthenticated': 'successfully',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                             },
                },200)
            else:
                return Response({'isAuthenticated': 'error'}, 400)
        except:
                return Response({'isAuthenticated': 'error'}, 500)
        
class LogoutView(APIView):
    permission_classes = (IsUserActivate,)
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class RoleListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            roles = Role.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            roles = Role.objects.filter(updated_at__gte=start_datetime)
        else:
            roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'code'
    
class EmployeeListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            employee = Employee.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            employee = Employee.objects.filter(updated_at__gte=start_datetime)
        else:
            employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'code'