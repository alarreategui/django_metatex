from .serializers import *
from datetime import datetime
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
# from .models import Client 
from apps.kanban.models import Client

# MODELO DE SELECCION 
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd

warchivo= "SelecciónPartida2.xlsx"

class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100
      
class ClientListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            client = Client.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            client = Client.objects.filter(updated_at__gte=start_datetime)
        else:
            client = Client.objects.all()
        serializer = ClientSerializer(client, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView): 
    permission_classes = (AllowAny,)
    queryset = Client.objects.all() 
    serializer_class = ClientSerializer
    lookup_field = 'code'

class pruebaView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):      
        seleccion()
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            client = Client.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            client = Client.objects.filter(updated_at__gte=start_datetime)
        else:
            client = Client.objects.all()
        serializer = ClientSerializer(client, many=True)
        return Response(serializer.data)

 
def seleccion():  
  #lectura de datos
  print("----------------------------------------------------------------------")
  dfRPartidas = pd.read_excel(warchivo, sheet_name="PARTIDAS" )
  dfRMaquinas = pd.read_excel(warchivo, sheet_name="MAQUINAS" )
  dfRMaquinasStockMinimo = pd.read_excel(warchivo, sheet_name="MAQUINAS STOCK MINIMO" )
  dfPreferenciasReceta = pd.read_excel(warchivo, sheet_name="Preferencia Receta" )
  dfPreferenciasGama = pd.read_excel(warchivo, sheet_name="Preferencia Gama" )

  #calculo de la matriz de preferencias de receta
  dfPreferenciasReceta.iloc[:,1:]=dfPreferenciasReceta.iloc[:,1:]/len(dfPreferenciasReceta)
  print(dfPreferenciasReceta)
  #calculo de la matriz de preferencias de gama
  dfPreferenciasGama.iloc[:,1:]=dfPreferenciasGama.iloc[:,1:]/len(dfPreferenciasGama)
  print(dfPreferenciasGama)

  fecha_actual = '2024-2-1 00:00:00'
  dfRPartidas['FechaActual']= fecha_actual
  dfRPartidas['HumedoMaxHoras'] = pd.to_timedelta(dfRPartidas['HumedoMax'], unit='h')
  dfRPartidas['HorasPendienteHumedaHoras'] = pd.to_timedelta(dfRPartidas['HorasPendienteHumeda'], unit='h')
  dfRPartidas['HorasPendientesHoras'] = pd.to_timedelta(dfRPartidas['HorasPendientes'], unit='h')

  dfRPartidas['TiempoEnRiesgo'] = pd.to_datetime(dfRPartidas['FechaActual']) + dfRPartidas['HorasPendienteHumedaHoras']  - pd.to_datetime( dfRPartidas['FinTinto'] )  - dfRPartidas['HumedoMaxHoras']
  hora0 = 0
  dfRPartidas['hora0']= hora0
  dfRPartidas['hora0'] = pd.to_timedelta(dfRPartidas['hora0'], unit='h')
  dfRPartidas['Conjunto1'] = (dfRPartidas['TiempoEnRiesgo']>dfRPartidas['hora0']) & (dfRPartidas['Humedo']==1)
  dfRPartidas['Conjunto3'] = pd.to_datetime(dfRPartidas['FechaActual']) + dfRPartidas['HorasPendientesHoras'] >= pd.to_datetime(dfRPartidas['FechaObjetivo'])

  dfPartidasPrioridad2 = dfRPartidas[dfRPartidas['Prioridad']==1]

  def obtenerPartidasPorMaquina(maquina):

    return dfRPartidas[dfRPartidas['Maquina']==maquina]

  def obtenerPreferenciasMaquina(maquina):
    maquinaSeleccionada = dfRMaquinas[dfRMaquinas['CODIGO_MAQUINA']==maquina]
    partidasPorMaquina = obtenerPartidasPorMaquina(maquina)
    parametrosUlt = ['Receta-ult','Temperatura-ult','Velocidad-ult','Gama-ult','Ancho Cadena-ult']
    parametros = ['Receta','Temperatura','Velocidad','Gama','Ancho Cadena']
    ultimaReceta = maquinaSeleccionada.iloc[0]['Receta-ult']
    ultimaGama = maquinaSeleccionada.iloc[0]['Gama-ult']
    ultimaTemperatura = maquinaSeleccionada.iloc[0]['Temperatura-ult']
    ultimaVelocidad = maquinaSeleccionada.iloc[0]['Velocidad-ult']
    ultimaAnchoCadena = maquinaSeleccionada.iloc[0]['Ancho Cadena-ult']
    # Recetas
    for index, partida in partidasPorMaquina.iterrows():
      valor = dfPreferenciasReceta[dfPreferenciasReceta['Receta'] == partida['Receta']].iloc[0][ultimaReceta]
      partidasPorMaquina.loc[index,'Preferencia'] = valor * maquinaSeleccionada.iloc[0]['Receta']
    # Gama
    for index, partida in partidasPorMaquina.iterrows():
      valor = dfPreferenciasGama[dfPreferenciasGama['Gama'] == partida['Gama']].iloc[0][ultimaGama]
      partidasPorMaquina.loc[index,'Preferencia'] += valor * maquinaSeleccionada.iloc[0]['Receta']
    # Temperatura
    partidasPorMaquina['Preferencia'] += maquinaSeleccionada.iloc[0]['Temperatura']  *  abs(1- (partidasPorMaquina['Temperatura'] -ultimaTemperatura) / ultimaTemperatura)
    # Velocidad
    partidasPorMaquina['Preferencia'] += maquinaSeleccionada.iloc[0]['Velocidad']  *  abs(1- (partidasPorMaquina['Velocidad'] -ultimaVelocidad) / ultimaVelocidad)
    # AnchoCadena
    partidasPorMaquina['Preferencia'] += maquinaSeleccionada.iloc[0]['Ancho Cadena']  *  abs(1- (partidasPorMaquina['Ancho Cadena'] -ultimaAnchoCadena) / ultimaAnchoCadena)
    return partidasPorMaquina
  # obtenerPreferenciasMaquina('PTX-17')

  def obtenerValorStockActual(maquina):
    # RECETA
    stockActualRecetaMaquina = dfRPartidas[dfRPartidas['Maquina']==maquina].groupby("Receta").sum().reset_index()[['Receta','Peso']]
    stockActualRecetaMaquina['Maquina'] = maquina
    stockActualRecetaMaquina['Parametro']='Receta'
    stockActualRecetaMaquina.rename(columns={'Receta': 'Valor'}, inplace=True)
    # TEMPERATURA
    stockActualTemperaturaMaquina = dfRPartidas[dfRPartidas['Maquina']==maquina].groupby("Temperatura").sum().reset_index()[['Temperatura','Peso']]
    stockActualTemperaturaMaquina['Maquina'] = maquina
    stockActualTemperaturaMaquina['Parametro']='Temperatura'
    stockActualTemperaturaMaquina.rename(columns={'Temperatura': 'Valor'}, inplace=True)
    # Gama
    stockActualGamaMaquina = dfRPartidas[dfRPartidas['Maquina']==maquina].groupby("Gama").sum().reset_index()[['Gama','Peso']]
    stockActualGamaMaquina['Maquina'] = maquina
    stockActualGamaMaquina['Parametro']='Gama'
    stockActualGamaMaquina.rename(columns={'Gama': 'Valor'}, inplace=True)

    result_concat = pd.concat([stockActualRecetaMaquina,stockActualTemperaturaMaquina,stockActualGamaMaquina]).reset_index()
    del result_concat['index']
    dfStockActualMaquina =pd.merge(result_concat,
      dfRMaquinasStockMinimo,
      how='left',
      left_on=['Maquina','Parametro' ],
      right_on=['Maquina','Parametro' ]
    )
    dfStockActualMaquina['Porcentaje']= (dfStockActualMaquina['Stock de Satisfaccion']-  dfStockActualMaquina['Peso']) /  dfStockActualMaquina['Stock de Satisfaccion']
    return(dfStockActualMaquina)

  # obtenerValorStockActual('PTX-17')

  def esContinuo(partida,num):
    if(partida['Conjunto1']==1):
      print("PARTIDA #",num," SELECCIONADA y ES CONTINUO")
      print(partida)
    else:
      print("PARTIDA #",num," SELECCIONADA y ES CONTINUO")
      print(partida)

  def evaluarContinuo(partida,longitud):
    if(longitud== 1):
      esContinuo(partida,0)
    else:
      for i in range(longitud):
        # Verificar si funciona
        esContinuo(partida.iloc[i],i)

  def evaluarParalelos(partida,maquina):
    print("evaluarParalelos")
    dfMaquinaSeleccionada = dfRMaquinas[dfRMaquinas['CODIGO_MAQUINA']== str(maquina)].iloc[0]
    anchoMaquina = dfMaquinaSeleccionada['Ancho Maquina']
    if(dfMaquinaSeleccionada['ProcesoParalelo']==1):
      dfParametroParalelos = dfMaquinaSeleccionada[['RecetaP','TemperaturaP','VelocidadP','GamaP','Ancho CadenaP']]
      partidasPorMaquina = obtenerPartidasPorMaquina(maquina)
      dfParametroPorPartidas =partidasPorMaquina[['Partida','Receta','Temperatura','Velocidad','Gama','Ancho Cadena']]
      dfParametroPartida = partida[['Partida','Receta','Temperatura','Velocidad','Gama','Ancho Cadena']]
      condicion  = True
      condicion2 = True
      condicion3 = True
      condicion4 = True
      if(dfParametroParalelos['RecetaP']==1):
        condicion = ( dfParametroPorPartidas['Receta'] == dfParametroPartida['Receta'])
      if(dfParametroParalelos['TemperaturaP']==1):
        condicion2 = ( dfParametroPorPartidas['Temperatura'] == dfParametroPartida['Temperatura'])
      if(dfParametroParalelos['GamaP']==1):
        condicion3 = ( dfParametroPorPartidas['Gama'] == dfParametroPartida['Gama'])
      if(dfParametroParalelos['VelocidadP']==1):
        condicion4 = ( dfParametroPorPartidas['Velocidad'] == dfParametroPartida['Velocidad'])
      condicion5 = ( dfParametroPorPartidas['Partida'] != partida['Partida'])
      dfPartidasCompatible = dfParametroPorPartidas[condicion & condicion2 & condicion3 & condicion4 & condicion5 ]
      if(dfPartidasCompatible.empty):
        print("--------------")
        evaluarContinuo(partida,1)
      else:
        suma_acumulada = 0 + partida['Ancho Cadena']
        suma = suma_acumulada
        indices_filas= []
        for index in range(len(dfPartidasCompatible)):
          indice = dfPartidasCompatible.index[index]
          # Sumar el valor de la columna correspondiente a la suma acumulada
          suma = suma_acumulada
          suma_acumulada += dfPartidasCompatible.loc[indice]['Ancho Cadena']

          # Verificar si la suma acumulada supera 10
          if suma_acumulada <= anchoMaquina:
              # Agregar el índice de la fila a la lista
              indices_filas.append(indice)
              suma = suma_acumulada
          else:
              # Detener la iteración si la suma acumulada supera 10
              break
        if(len(indices_filas)==0):
          evaluarContinuo(partida,1)
        else:
          dfPartidasCompatibleSeleccionados = partidasPorMaquina.loc[indices_filas]
          result_concat = pd.concat([partidasPorMaquina[~condicion5],dfPartidasCompatibleSeleccionados])
          print("Hay casos paralelos para la partida ", partida['Partida'])
          print("Índices de las filas de Partidas adicionales cuya suma de ancho no supera ",anchoMaquina," cm:", indices_filas)
          print("Suma de anchos: ", suma)
          evaluarContinuo(result_concat,len(result_concat))
    else:
      evaluarContinuo(partida,1)
  # evaluarParalelos(dfRPartidas.loc[1],'PTX-17')

  def evaluarReceta(partidasSeleccionada, partidasPorMaquina,maquina):
    print("evaluarReceta")
    maquinaSeleccionada = dfRMaquinas[dfRMaquinas['CODIGO_MAQUINA']==maquina]
    # print(maquinaSeleccionada)
    if(maquinaSeleccionada.iloc[0]['MinReceta']== 0):
      evaluarParalelos(partidasSeleccionada,maquina)
      return 1 #fin
    ultimaReceta = maquinaSeleccionada.iloc[0]['Receta-ult']
    partida = partidasSeleccionada['Partida']
    recetaPartida = partidasSeleccionada['Receta']
    if(ultimaReceta == recetaPartida):
      evaluarParalelos(partidasSeleccionada,maquina)
      return 1 #fin
    else:
      minReceta = maquinaSeleccionada.iloc[0]['MinReceta']
      peso =  partidasSeleccionada['Peso']
      if (peso >= minReceta ):
        evaluarParalelos(partidasSeleccionada,maquina)
        return 1 #fin
      else:
        partidasPorMaquinaByReceta = partidasPorMaquina[(partidasPorMaquina['Receta'] == ultimaReceta) & (partidasPorMaquina['Partida'] != partida)]
        suma_acumulada = 0 + partidasSeleccionada['Peso']
        print("suma_acumulada")
        print(suma_acumulada)
        suma = suma_acumulada
        indices_filas= []
        for index in range(len(partidasPorMaquinaByReceta)):
          indice = partidasPorMaquinaByReceta.index[index]
          # Sumar el valor de la columna correspondiente a la suma acumulada
          suma = suma_acumulada
          suma_acumulada += partidasPorMaquinaByReceta.loc[indice]['Peso']

          # Verificar si la suma acumulada supera 10
          if suma_acumulada <= minReceta:
              # Agregar el índice de la fila a la lista
              indices_filas.append(indice)
              suma = suma_acumulada
          else:
              indices_filas.append(indice)
              # Detener la iteración si la suma acumulada supera 10
              break
        if(len(indices_filas)==0):
          # Este caso es que la partida seleccionada superó el minimo de receta
          evaluarParalelos(partidasSeleccionada,maquina)
          return 1
        else:
          #agregar partida seleccionada al concatenar
          if( suma_acumulada >= minReceta):
            print("Enviar en cola las siguientes partidas")
            dfPartidasCompatibleSeleccionados = partidasPorMaquinaByReceta.loc[indices_filas]
            result_concat = pd.concat([partidasPorMaquina[partidasPorMaquina['Partida'] == partida],dfPartidasCompatibleSeleccionados])
            print("Hay casos en cola para la partida ", partidasSeleccionada['Partida'])
            print("Índices de las filas de Partidas adicionales cuya suma de peso supera ",minReceta," kg:", indices_filas)
            print("Suma de pesos: ", suma_acumulada)
            print(result_concat)
            evaluarContinuo(result_concat,len(result_concat))
            # enviar en cola
            return 1 #fin
          else:
            return 0 #siguiente partida
      return 0

            # remover partida actual
  # evaluarMatrizPreferencias(dfRPartidas,'PTX-17')

  def evaluarMatrizPreferencias(dfPartidas,maquina):
    print("evaluar Matriz preferencias")
    dfPartidasCopia = dfPartidas
    dfPartidasCopia['index1'] = 0
    dfPartidasCopia['index2'] = 0
    dfPartidasCopia['index3'] = 0
    dfPartidasCopia['index4'] = 0
    dfPartidasCopia['index5'] = 0
    dfPartidasCopia['index1Percent'] = 0
    dfPartidasCopia['index2Percent'] = 0
    dfPartidasCopia['index3Percent'] = 0
    dfPartidasCopia['index4Percent'] = 0
    dfPartidasCopia['index5Percent'] = 0

    ##ORDENAR POR INDEX Y PORCENTAJE
    indice = dfRMaquinas[dfRMaquinas['CODIGO_MAQUINA']== str(maquina)].index[0]
    dfMaquinaSeleccionada = dfRMaquinas.loc[indice]
    data = obtenerValorStockActual(maquina)
    dfPreferenciasMaquina =dfMaquinaSeleccionada[['Receta','Temperatura','Velocidad','Gama','Ancho Cadena']].sort_values( ascending = False).reset_index()
    # preferenciasYvalor = []
    result_concat = pd.DataFrame()
    for i in range(len(dfPreferenciasMaquina)):
      columna = dfPreferenciasMaquina['index'].loc[i]
      orden = dfPreferenciasMaquina.iloc[i][indice]
      dfParametroFiltrado = data[(data['Parametro']== columna) & ( data['Porcentaje'] > 0)].sort_values(by=['Porcentaje'], ascending=[False])
      dfParametroFiltrado['index'] = orden
      result_concat = pd.concat([result_concat,dfParametroFiltrado])
    if(result_concat.empty):
      return 0
    for i in range(len(dfPreferenciasMaquina)):
      result_concatFiltrado = result_concat[result_concat['index']==(len(dfPreferenciasMaquina)-i)]
      if not(result_concatFiltrado.empty):


        for index,parametroValor in result_concatFiltrado.iterrows():
          columna= parametroValor['Parametro']
          valor = parametroValor['Valor']
          porcentaje = parametroValor['Porcentaje']
          dfPartidasCopia.loc[dfPartidasCopia[columna]==valor, 'index'+str(len(dfPreferenciasMaquina) - i)] = 1
          dfPartidasCopia.loc[dfPartidasCopia[columna]==valor, 'index'+str(len(dfPreferenciasMaquina) - i)+'Percent'] = porcentaje

    dfPartidasCopiaOrdenadas = dfPartidasCopia.sort_values(by=['index1','index1Percent','index2','index2Percent','index3','index3Percent','index4','index4Percent','index5','index5Percent'], ascending=False)

    dfPartidasConPreferencia = obtenerPreferenciasMaquina(maquina)
    for index, partida in dfPartidasCopiaOrdenadas.iterrows():
      resultadoEvaluarReceta = evaluarReceta(partida, dfPartidasConPreferencia,maquina)
      if(resultadoEvaluarReceta==1):
        return 1
    return 0

  # evaluarMatrizPreferencias(dfRPartidas,'PTX-17')

  def evaluarPrioridadAutomatica(dfPartidas,maquina):

    print("evaluarPrioridadAutomatica")
    print("dfPartidas =>")
    print(dfPartidas)
    dfPartidasPrioridad3 = dfPartidas[dfPartidas['Conjunto3']==1]
    dfPartidasConPreferencia = obtenerPreferenciasMaquina(maquina)
    dfPartidasPrioridad3ConPreferencia =  pd.merge(dfPartidasPrioridad3, dfPartidasConPreferencia[['Partida','Preferencia']], on='Partida', how='left')
    if (dfPartidasPrioridad3.empty):
      # Analisis de Preferencias
      indice = dfRMaquinas[dfRMaquinas['CODIGO_MAQUINA']== str(maquina)].index[0]
      dfMaquinaSeleccionada = dfRMaquinas.loc[indice]
      if not(pd.isna(dfMaquinaSeleccionada['MAESTRO']) ):
        print("evaluando maquina maestro")
        # Tiene maestro
        resultadoPreferenciasMaestro = evaluarMatrizPreferencias(dfPartidas,maquina)
        if(resultadoPreferenciasMaestro == 1):
          return 1
      # No tiene maestro
      print("evaluando maquina actual")
      print(dfPartidas)
      sinPartidas = False
      for index, partida in dfPartidas.iterrows():
        resultado = evaluarReceta(partida, dfPartidasConPreferencia,maquina)
        if(resultado == 1):
          sinPartidas = True
          break
      if not(sinPartidas):
        print("No hay Partidas con priorización")
        return 0
      else:
        return 1
    else:
      if(len(dfPartidasPrioridad3ConPreferencia)==1):
        # Analisis terminado
        evaluarParalelos(dfPartidasPrioridad3ConPreferencia.iloc[0],maquina)
        return 0
      else:
        indice = dfRMaquinas[dfRMaquinas['CODIGO_MAQUINA']== str(maquina)].index[0]
        dfMaquinaSeleccionada = dfRMaquinas.loc[indice]
        if not(pd.isna(dfMaquinaSeleccionada['MAESTRO']) ):
          print("evaluando maquina maestro")
          # Tiene maestro
          resultadoPreferenciasMaestro = evaluarMatrizPreferencias(dfPartidasPrioridad3ConPreferencia,maquina)
          if(resultadoPreferenciasMaestro == 1):
            return 1
        # No tiene maestro
        print("evaluando maquina actual")
        print(dfPartidasPrioridad3ConPreferencia)
        sinPartidas = False
        for index, partida in dfPartidasPrioridad3ConPreferencia.iterrows():
          resultado = evaluarReceta(partida, dfPartidasConPreferencia,maquina)
          if(resultado == 1):
            sinPartidas = True
            break
        if not(sinPartidas):
          print("No hay Partidas con priorización")
          return 0
    return 0

  # evaluarPrioridadAutomatica(dfRPartidas,'PTX-17')

  def evaluarPrioridad(dfPartidas,maquina):
    print("Evaluar Prioridad")
    dfPartidasPrioridad2 = dfPartidas[dfPartidas['Conjunto1']==1]
    if (dfPartidasPrioridad2.empty):
      # Analisis de 3da Prioridad
      evaluarPrioridadAutomatica(dfPartidas,maquina)
      return 0
    else:
      if(len(dfPartidasPrioridad2)==1):
        evaluarParalelos(dfPartidasPrioridad2.iloc[0],maquina)
        # Analisis terminado
        return 0
      else:
        # Analisis de 3da Prioridad en base a la 2da prioridad
        evaluarPrioridadAutomatica(dfPartidasPrioridad2,maquina)

  def evaluarCalidad(dfRPartidas,maquina):
    print("Evaluar Calidad")
    dfPartidasPrioridad1 = dfRPartidas[dfRPartidas['Conjunto1']]
    if (dfPartidasPrioridad1.empty):
      # Analisis de 2da Prioridad
      evaluarPrioridad(dfRPartidas,maquina)
      return 0
    else:
      if(len(dfPartidasPrioridad1)==1):
        evaluarParalelos(dfPartidasPrioridad1.iloc[0],maquina)
        # Analisis terminado
        return 0
      else:
        # Obtener el mayor riesgo
        indexMayorRiesgo = dfPartidasPrioridad1['TiempoEnRiesgo'].idxmax()
        MayorTiempoRiesgo =  dfPartidasPrioridad1.loc[indexMayorRiesgo]['TiempoEnRiesgo']
        partidasCoincidencias =  dfPartidasPrioridad1[dfPartidasPrioridad1['TiempoEnRiesgo']==MayorTiempoRiesgo]

        if(len(partidasCoincidencias)==1):
          evaluarParalelos(dfPartidasPrioridad1.loc[indexMayorRiesgo],maquina)
          # Analisis terminado
          return 0
        else:
          # Analisis de 2da Prioridad en base a la primera prioridad
          evaluarPrioridad(partidasCoincidencias,maquina)
        return 0

  maquina = 'PTX-17'
  dfPartidasPorMaquina = obtenerPartidasPorMaquina(maquina)
  evaluarCalidad(dfPartidasPorMaquina,maquina)
