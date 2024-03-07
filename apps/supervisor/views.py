
from .serializers import *
from datetime import datetime
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

# from .models import 
from apps.kanban.models import Client
from apps.supervisor.models import Disponibilidad, Maquinaparada, Motivocambiovalorparametro, Motivocambiovalorparametroxpartelcolsecpromaqpar, Motivoprioridad, Motivoprioridadxpartida, Partidatelacolorsecuenciaprocesomaquinaparametro
# MODELO DE SELECCION 
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
from django.http import JsonResponse
import json

warchivo= "SelecciónPartida2.xlsx"

class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100
      
class ListaPartidaListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        try:
            # Datos del modelo Partidatelacolorsecuenciaprocesomaquinarealizado
            resultados_ptcspmr = Partidatelacolorsecuenciaprocesomaquinarealizado.objects.all().values()
            # Convierte los resultados en un DataFrame de Pandas
            df_ptcspmr = pd.DataFrame(list(resultados_ptcspmr))
            df_ptcspmr = df_ptcspmr[['codpartidatelacolorsecuenciaprocesomaquinarealizado', 'secuencia', 'partidacodpartida_id', 'colorcodcolor_id', 'procesocodproceso_id','maquinacodmaquina_id','telacodtela']]
            # Datos del modelo Partidatelacolorsecuenciaproceso
            resultados_ptcsp = Partidatelacolorsecuenciaproceso.objects.all().values()
            # Convierte los resultados en un DataFrame de Pandas
            df_ptcsp = pd.DataFrame(list(resultados_ptcsp))
            df_ptcsp = df_ptcsp[['codpartida_id','codtela_id','codcolor_id','secuencia','codproceso_id','estado','cantidadkg','cantidadmt','procesoestandar','estadocalidad','estadobloqueo']]
            df_combinado = df_ptcspmr.merge(df_ptcsp, 
                                            how='inner', 
                                            left_on=['partidacodpartida_id', 'telacodtela', 'colorcodcolor_id', 'secuencia', 'procesocodproceso_id'],
                                            right_on=['codpartida_id', 'codtela_id', 'codcolor_id', 'secuencia', 'codproceso_id'])
            resultados_partida = Partida.objects.all().values()
            df_partida = pd.DataFrame(list(resultados_partida))
            df_combinado_2 = df_combinado.merge(df_partida[['codpartida', 'prioridad']],
                                                how='left',
                                                left_on=['partidacodpartida_id'],
                                                right_on=['codpartida'])
            resultados_mpxp = Motivoprioridadxpartida.objects.all().values()
            if resultados_mpxp.__len__() == 0:
                columnas = ['codmotivoprioridadxpartida', 'motivoprioridadcodmotivoprioridad_id', 'partidacodpartida_id']
                # Crea un DataFrame vacío con las columnas especificadas
                df_mpxp = pd.DataFrame(columns=columnas)
            else:
                df_mpxp = pd.DataFrame(list(resultados_mpxp))
                df_mpxp = df_mpxp[['codmotivoprioridadxpartida','motivoprioridadcodmotivoprioridad_id','partidacodpartida_id']]
            resultados_mp = Motivoprioridad.objects.all().values()
            df_mp = pd.DataFrame(list(resultados_mp)) 
            df_mpxp = df_mpxp.merge(df_mp[['codmotivoprioridad','descripcion']],
                                                  how='left',
                                                  left_on=['motivoprioridadcodmotivoprioridad_id'],
                                                  right_on=['codmotivoprioridad'])
            df_combinado_3 = df_combinado_2.merge(df_mpxp,
                                                  how='left',
                                                  left_on=['partidacodpartida_id'],
                                                  right_on=['partidacodpartida_id']) 
            json_data = df_combinado_3.to_json(orient='records')
            # Cargar el JSON en un objeto Python
            data = json.loads(json_data)
            # Retornar la respuesta JSON
            return Response(data, status=status.HTTP_200_OK)
        except Partidatelacolorsecuenciaprocesomaquinarealizado.DoesNotExist:
            return Response({"message": "No se encontraron partidas realizadas"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = PartidatelacolorsecuenciaprocesorealizadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class ListaPartidasListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, partidacodpartida):
        try:
            # Datos del modelo Partidatelacolorsecuenciaprocesomaquinarealizado
            resultados_ptcspmr = Partidatelacolorsecuenciaprocesomaquinarealizado.objects.filter(partidacodpartida=partidacodpartida).values()
            if resultados_ptcspmr.__len__() == 0:
                return Response([], status=status.HTTP_200_OK)
            # Convierte los resultados en un DataFrame de Pandas
            df_ptcspmr = pd.DataFrame(list(resultados_ptcspmr))
            df_ptcspmr = df_ptcspmr[['codpartidatelacolorsecuenciaprocesomaquinarealizado', 'secuencia', 'partidacodpartida_id', 'colorcodcolor_id', 'procesocodproceso_id','maquinacodmaquina_id','telacodtela']]
            # Datos del modelo Partidatelacolorsecuenciaproceso
            resultados_ptcsp = Partidatelacolorsecuenciaproceso.objects.all().values()
            # Convierte los resultados en un DataFrame de Pandas
            df_ptcsp = pd.DataFrame(list(resultados_ptcsp))
            df_ptcsp = df_ptcsp[['codpartida_id','codtela_id','codcolor_id','secuencia','codproceso_id','estado','cantidadkg','cantidadmt','procesoestandar','estadocalidad','estadobloqueo']]
            df_combinado = df_ptcspmr.merge(df_ptcsp, 
                                            how='inner', 
                                            left_on=['partidacodpartida_id', 'telacodtela', 'colorcodcolor_id', 'secuencia', 'procesocodproceso_id'],
                                            right_on=['codpartida_id', 'codtela_id', 'codcolor_id', 'secuencia', 'codproceso_id'])
            resultados_partida = Partida.objects.all().values()
            df_partida = pd.DataFrame(list(resultados_partida))
            df_combinado_2 = df_combinado.merge(df_partida[['codpartida', 'prioridad']],
                                                how='left',
                                                left_on=['partidacodpartida_id'],
                                                right_on=['codpartida'])
            resultados_mpxp = Motivoprioridadxpartida.objects.all().values()
            if resultados_mpxp.__len__() == 0:
                columnas = ['codmotivoprioridadxpartida', 'motivoprioridadcodmotivoprioridad_id', 'partidacodpartida_id']
                # Crea un DataFrame vacío con las columnas especificadas
                df_mpxp = pd.DataFrame(columns=columnas)
            else:
                df_mpxp = pd.DataFrame(list(resultados_mpxp))
                df_mpxp = df_mpxp[['codmotivoprioridadxpartida','motivoprioridadcodmotivoprioridad_id','partidacodpartida_id']]
            resultados_mp = Motivoprioridad.objects.all().values()
            df_mp = pd.DataFrame(list(resultados_mp)) 
            df_mpxp = df_mpxp.merge(df_mp[['codmotivoprioridad','descripcion']],
                                                  how='left',
                                                  left_on=['motivoprioridadcodmotivoprioridad_id'],
                                                  right_on=['codmotivoprioridad'])
            df_combinado_3 = df_combinado_2.merge(df_mpxp,
                                                  how='left',
                                                  left_on=['partidacodpartida_id'],
                                                  right_on=['partidacodpartida_id']) 
            json_data = df_combinado_3.to_json(orient='records')
            # Cargar el JSON en un objeto Python
            data = json.loads(json_data)
            # Retornar la respuesta JSON
            return Response(data, status=status.HTTP_200_OK)
        except Partidatelacolorsecuenciaprocesomaquinarealizado.DoesNotExist:
            return Response({"message": "No se encontraron partidas realizadas"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, partidacodpartida):
        serializer = PartidatelacolorsecuenciaprocesorealizadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class MaquinasParadasListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            maquinaParada = Maquinaparada.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            maquinaParada = Maquinaparada.objects.filter(updated_at__gte=start_datetime)
        else:
            maquinaParada = Maquinaparada.objects.all()
        maquinaParada = maquinaParada.filter(fechafin__isnull=True) 
        serializer = MaquinaparadaSerializer(maquinaParada, many=True)
        return Response(serializer.data) 
    
    # def post(self, request):
    #     serializer = ClientSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class MotivosPrioridadListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            motivoPrioridad = Motivoprioridad.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            motivoPrioridad = Motivoprioridad.objects.filter(updated_at__gte=start_datetime)
        else:
            motivoPrioridad = Motivoprioridad.objects.all()  
        serializer = MotivoprioridadSerializer(motivoPrioridad, many=True)
        return Response(serializer.data) 
    
    # def post(self, request):
    #     serializer = ClientSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MotivoPrioridadPartidasListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            motivoprioridadxpartida = Motivoprioridadxpartida.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            motivoprioridadxpartida = Motivoprioridadxpartida.objects.filter(updated_at__gte=start_datetime)
        else:
            motivoprioridadxpartida = Motivoprioridadxpartida.objects.all()  
        serializer = MotivoprioridadxpartidaSerializer(motivoprioridadxpartida, many=True)
        return Response(serializer.data) 
    
    def post(self, request):
        serializer = MotivoprioridadxpartidaSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save() 
            partida_id = request.data.get('partidacodpartida')
            partida = Partida.objects.get(codpartida=partida_id)
            partida.prioridad = 1
            partida.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
class MotivoCambioValorParTelasListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            motivocambiovalorparametroxpartelcolsecpromaqpar = Motivocambiovalorparametroxpartelcolsecpromaqpar.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            motivocambiovalorparametroxpartelcolsecpromaqpar = Motivocambiovalorparametroxpartelcolsecpromaqpar.objects.filter(updated_at__gte=start_datetime)
        else:
            motivocambiovalorparametroxpartelcolsecpromaqpar = Motivocambiovalorparametroxpartelcolsecpromaqpar.objects.all()  
        serializer = MotivocambiovalorparametroxpartelcolsecpromaqparSerializer(motivocambiovalorparametroxpartelcolsecpromaqpar, many=True)
        return Response(serializer.data) 
    
    def post(self, request):
        serializer = MotivocambiovalorparametroxpartelcolsecpromaqparSerializer(data = request.data) 
        if serializer.is_valid():
            serializer.save()
            partida_id = request.data.get('codpartidatelacolorsecuenciaprocesomaquinaparametro')
            partida = Partidatelacolorsecuenciaprocesomaquinaparametro.objects.get(codpartidatelacolorsecuenciaprocesomaquinaparametro=partida_id)
            partida.valoractualizado = str(request.data.get('valoractualizado'))
            partida.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
class ParametrosPartidaMaquinaListByCodRealizadoView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request,codigo):
        partidatelacolorsecuenciaproceso = Partidatelacolorsecuenciaprocesomaquinarealizado.objects.filter(codpartidatelacolorsecuenciaprocesomaquinarealizado=codigo)
        if partidatelacolorsecuenciaproceso.__len__() == 0:
            return Response([], status=status.HTTP_200_OK)
        dataParametros = Partidatelacolorsecuenciaprocesomaquinaparametro.objects.all()
        combo = Partidatelacolorsecuenciaprocesomaquinarealizado.objects.get(codpartidatelacolorsecuenciaprocesomaquinarealizado=codigo) 
        dataParametros = dataParametros.filter(secuencia=combo.secuencia).filter(codpartida=combo.partidacodpartida).filter(codtela=combo.codtela).filter(codcolor=combo.colorcodcolor).filter(codproceso=combo.procesocodproceso).filter(codmaquina=combo.maquinacodmaquina)
        serializer = PartidatelacolorsecuenciaprocesomaquinaparametroSerializer(dataParametros, many=True)
        serializer2 = PartidatelacolorsecuenciaprocesorealizadoSerializer(combo, many=False)
        newData = { 'detalle':serializer2.data , 'parametros': serializer.data }
        return Response(newData, status=status.HTTP_200_OK) 
    
    # def post(self, request):
    #     serializer = MotivoprioridadxpartidaSerializer(data = request.data)

    #     if serializer.is_valid(): 
    #         # Obtener el ID de la partida desde el serializer
    #         partida_id = request.data.get('partidacodpartida')
    #         partida = Partida.objects.get(codpartida=partida_id)
    #         partida.prioridad = 1 
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class MotivosCambioListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            motivocambiovalorparametro = Motivocambiovalorparametro.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            motivocambiovalorparametro = Motivocambiovalorparametro.objects.filter(updated_at__gte=start_datetime)
        else:
            motivocambiovalorparametro = Motivocambiovalorparametro.objects.all()  
        serializer = MotivocambioSerializer(motivocambiovalorparametro, many=True)
        return Response(serializer.data) 
    
    # def post(self, request):
    #     serializer = ClientSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaquinasInactivasListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        disponibilidad = Disponibilidad.objects.all()
        serializer = DisponibilidadSerializer(disponibilidad, many=True)
        return Response(serializer.data) 
    def put(self, request, codigo, format=None):
        instance = get_object_or_404(Disponibilidad.objects.all(), pk=codigo) 
        serializer = DisponibilidadSerializerUpdate(instance, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ParadasMotivosListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        parada = Parada.objects.filter(tipoparada='3')
        serializer = ParadaSerializer(parada, many=True)
        return Response(serializer.data)