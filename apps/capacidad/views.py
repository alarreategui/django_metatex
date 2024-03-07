from .serializers import *
from datetime import datetime
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
# from .models import Client 
from apps.kanban.models import Machinery, Client, Fabric, RoutePoint,Process,ProcessMachinery,FabricProcess,Stop

# MODELO DE SELECCION 
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
from django.http import JsonResponse
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
        # ARTICULOS RUTAS
        resultado_fabric = Fabric.objects.filter(route_code__in=['RU101', 'RU021']).values(
            'code',
            'route_code_id',
        ) 
        dfTelas = pd.DataFrame(list(resultado_fabric))
        print("dfTelas")
        print(dfTelas)
        print("_----------------------")
        # Extrae los IDs de ruta de la primera consulta
        route_code_ids = resultado_fabric.values_list('route_code_id', flat=True)
        # Utiliza los IDs de ruta en la segunda consulta
        resultado_routepoint = RoutePoint.objects.filter(route_code_id__in=route_code_ids).values(
          "process_code_id",
          "route_code_id",
          "sequence",
        )
        dfPuntoRuta= pd.DataFrame(list(resultado_routepoint))
        print("dfPuntoRuta")
        print(dfPuntoRuta)
        print("_----------------------")
        dfArticulosRutas = dfTelas.merge(
            dfPuntoRuta,
            how='left',
            left_on=['route_code_id' ],
            right_on=['route_code_id' ]
        )
        dfArticulosRutas.rename(columns={'code': 'ARTICULO'}, inplace=True)
        dfArticulosRutas.rename(columns={'process_code_id': 'CODIGO_PROCESO'}, inplace=True)
        print("dfArticulosRutas")
        print(dfArticulosRutas)
        print("_----------------------")
        # PARTIDA TELA
        
        resultado_fabricBatch = FabricBatch.objects.filter(fabric_code__in=['IN000227','JE003384','JE003375','JE003383','JE002999']).values(
            'code',
            'target_date',
            'process_quantity',
            'fabric_code'
            
        )

        # Corregir para que venga con la zona horaria adecuada
        for item in resultado_fabricBatch:
          item['target_date'] = item['target_date'].replace(tzinfo=None) if item['target_date'] else None

        dfPartidaTela_bd= pd.DataFrame(list(resultado_fabricBatch))
        dfPartidaTela_bd.rename(columns={'code': 'PARTIDAS'}, inplace=True)
        dfPartidaTela_bd.rename(columns={'target_date': 'FECHA OBJETIVO'}, inplace=True)
        dfPartidaTela_bd.rename(columns={'process_quantity': 'CANTIDAD'}, inplace=True) 

        dfPartidaTela = dfPartidaTela_bd.merge(
            dfTelas[["code", "route_code_id"]],
            how='left',
            left_on=['fabric_code' ],
            right_on=['code' ]
        )  
        dfPartidaTela = dfPartidaTela.merge(
            dfPuntoRuta,
            how='left',
            left_on=['route_code_id' ],
            right_on=['route_code_id' ]
        )    
  
        print("dfPartidaTela")
        print(dfPartidaTela)
        print("_----------------------")
        def concat_proceso_codigo(group):
          return ','.join(group['process_code_id'])

        # Agrupa por las columnas especificadas y aplica la función personalizada
        grouped_df = dfPartidaTela.groupby(['PARTIDAS', 'FECHA OBJETIVO', 'CANTIDAD', 'fabric_code', 'route_code_id']).apply(concat_proceso_codigo).reset_index(name='Secuencia_Proceso')
        grouped_df.rename(columns={'fabric_code': 'ARTICULO'}, inplace=True) 

        print("grouped_df")
        print(grouped_df)
        print(len(grouped_df))
        print("_----------------------")


        resultado_machinery = Machinery.objects.values(
            'code',
            'description',
        ) 
        dfMaquinas = pd.DataFrame(list(resultado_machinery))
        dfMaquinas.rename(columns={'code': 'CODIGO_MAQUINA'}, inplace=True) 
        dfMaquinas.rename(columns={'description': 'DETALLE_MAQUINA'}, inplace=True) 
        print("dfMaquinas")
        print(dfMaquinas)
        print("_----------------------")


        resultado_process = Process.objects.values(
            'code',
            'name',
        ) 
        dfProcesos = pd.DataFrame(list(resultado_process))
        dfProcesos.rename(columns={'code': 'CODIGO_PROCESO'}, inplace=True) 
        dfProcesos.rename(columns={'name': 'DETALLE_PROCESO'}, inplace=True) 
        print("dfProcesos")
        print(dfProcesos)
        print("_----------------------")
        resultado_processMachinery = ProcessMachinery.objects.values(
            'code',
            'machinery_code',
            'fabric_process_code',
            'speed_kg',
        ) 
        resultado_fabricProcess = FabricProcess.objects.values(
            'code',
            'process_code',
            'fabric_code',
        ) 
        dfprocesoMaquinaria = pd.DataFrame(list(resultado_processMachinery))
        
        dfprocesoMaquinaria.rename(columns={'code': 'CODIGO_MAQUINAxPROCESO'}, inplace=True) 
        print("dfprocesoMaquinaria")
        print(dfprocesoMaquinaria)
        print("_----------------------")
        dfprocesoTela = pd.DataFrame(list(resultado_fabricProcess))
        print("dfprocesoTela")
        print(dfprocesoTela)
        print("_----------------------")
        dfprocesoMaquinariaCompleto = dfprocesoMaquinaria.merge(
            dfprocesoTela,
            how='left',
            left_on=['fabric_process_code' ],
            right_on=['code' ]
        )
        dfprocesoMaquinariaCompleto.rename(columns={'process_code': 'CODIGO_PROCESO'}, inplace=True) 
        dfprocesoMaquinariaCompleto.rename(columns={'speed_kg': 'VELOCIDADES'}, inplace=True) 
        dfprocesoMaquinariaCompleto.rename(columns={'fabric_code': 'ARTICULO'}, inplace=True) 
        dfprocesoMaquinariaCompleto.rename(columns={'machinery_code': 'CODIGO_MAQUINA'}, inplace=True) 
        print("dfprocesoMaquinariaCompleto")
        print(dfprocesoMaquinariaCompleto)
        print("_----------------------")
        resultadoStop= Stop.objects.filter(code=0).values(
            'code',
        )  
        dfParadas = pd.DataFrame(list(resultadoStop))
        print("dfParadas")
        print(dfParadas)
        print("_----------------------")
        fecha_inicial = '2023-07-19 00:00:00'
        dataTrayectoSeleccionado = capacidad(grouped_df,dfProcesos,dfprocesoMaquinariaCompleto,dfArticulosRutas,dfMaquinas,fecha_inicial) 

        print(dataTrayectoSeleccionado.columns) 
        dataTrayectoSeleccionado = dataTrayectoSeleccionado.merge(
            dfprocesoMaquinariaCompleto[['ARTICULO', 'CODIGO_PROCESO','CODIGO_MAQUINA', 'CODIGO_MAQUINAxPROCESO']],
            how='left',
            left_on=['CODIGO_TELA', 'CODIGO_PROCESO','CODIGO_MAQUINA'],
            right_on=['ARTICULO','CODIGO_PROCESO','CODIGO_MAQUINA' ]
        ) 
        print("dataTrayectoSeleccionado")
        print(dataTrayectoSeleccionado) 
        print(dataTrayectoSeleccionado.columns) 
        print("_----------------------")
        # return JsonResponse(dataTrayectoSeleccionado.to_dict(), safe=False)
        for index, row in dataTrayectoSeleccionado.iterrows():
          fabricProcess = FabricProcess.objects.get(code=row['CODIGO_MAQUINAxPROCESO'])
          nuevo_objeto = SelectedPath(
              machinery_process_code=fabricProcess.code,
              # Agrega más campos según tu modelo Django y DataFrame
          )
          serializer = SelectedPathSerializer(data=nuevo_objeto)
          if serializer.is_valid():
              serializer.save() 
          else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # start_timestamp = request.query_params.get('start_timestamp', None)
        # end_timestamp = request.query_params.get('end_timestamp', None)
        # start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        # end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        # if start_datetime and end_datetime:
        #     client = Client.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        # elif start_timestamp:
        #     start_datetime = datetime.fromtimestamp(int(start_timestamp))
        #     client = Client.objects.filter(updated_at__gte=start_datetime)
        # else:
        #     client = Client.objects.all()
        # serializer = ClientSerializer(client, many=True)
        # return Response(serializer.data)

 
def capacidad(dfPartidas,dfProcesos,dfMaquinasProcesos,ArticulosRutas,dfMaquinas,fecha_inicial):  

  # fecha_inicial = '2023-8-6 08:00:00'
  # warchivo= "PlanCapacidad NUEVA DATA PRUEBA 5 POR FECHA.xlsx"
  # NumeroPartidas = 10
  # dfPartidas = pd.read_excel(warchivo, sheet_name="Partidas", nrows=NumeroPartidas)
  # dfProcesos = pd.read_excel(warchivo,sheet_name="Procesos")
  # dfMaquinasProcesos = pd.read_excel(warchivo,sheet_name="MaquinasProcesos")
  # ArticulosRutas = pd.read_excel(warchivo,sheet_name="ArticulosRutas")
  # dfMaquinas = pd.read_excel(warchivo,sheet_name="Maquinas")

  dfPartidas['Secuencia_Proceso'] = dfPartidas['Secuencia_Proceso'].apply(lambda x: x.split(','))
  dfPartidas['codProcesoSiguiente'] = dfPartidas['Secuencia_Proceso'].apply(lambda x: x[0] if len(x) > 0 else None)
  dfPartidas['horaFinMax'] = np.nan

  dfPartidas2 = dfPartidas.merge(
      ArticulosRutas,
      how='inner',
      left_on=['ARTICULO' ],
      right_on=['ARTICULO' ]
  )
  dfPartidas2['estaDisponible']= False
  dfPartidas2['estaDisponible']= dfPartidas2['CODIGO_PROCESO']== dfPartidas2['codProcesoSiguiente']
  dfPartidas3 =pd.merge(dfPartidas2,
      dfMaquinasProcesos,
      how='left',
      left_on=['ARTICULO','CODIGO_PROCESO' ],
      right_on=['ARTICULO','CODIGO_PROCESO' ]
  )
  dfPartidas3['CodPlan'] = pd.Series(range(1, 1 + dfPartidas3.shape[0]))
  dfPartidas3['Tiempo_Procesar(h)']= dfPartidas3['CANTIDAD']/dfPartidas3['VELOCIDADES']
  dfPlan=dfPartidas3

  prueba = dfPlan.groupby(['CODIGO_MAQUINA'])[['CANTIDAD','horaFinMax','estaDisponible','CODIGO_MAQUINAxPROCESO', 'VELOCIDADES','CodPlan','Tiempo_Procesar(h)']].sum()
  prueba2 = pd.merge(prueba, dfMaquinas, on='CODIGO_MAQUINA', how='right').sort_values(by='CANTIDAD', ascending = False).reset_index()
  dfMaquinas = prueba2[['CODIGO_MAQUINA','DETALLE_MAQUINA']]
  # print(dfMaquinas)
  totalMaquinas = dfMaquinas.shape[0]

  #Para reemplazar la hoja DisponibilidadMaquina
  filas= 60*24*31*5
  df = pd.DataFrame(index=range(filas))
  df['TiempoI'] = np.arange(0,filas)
  df['TiempoF(min)'] = np.arange(1,filas+1)
  encabezados = dfMaquinas['CODIGO_MAQUINA'].to_list()
  # Agregar encabezados a las columnas
  for encabezado in encabezados:
      df[encabezado] = np.nan

  dfDisponibilidadMaquina = df
  dfDisponibilidadMaquinaAtrasados = dfDisponibilidadMaquina.copy()
  print(filas)

  dfDisponibilidadMaquina.head(10)

  # dfParadasProgramadas = pd.read_excel(warchivo,sheet_name="PARADAS_PROGRAMADAS")
  # dfParadasProgramadas['FechaEjecucion'] = fecha_inicial
  # dfParadasProgramadas['FechaHoraInicioTime'] = pd.to_datetime(dfParadasProgramadas['FechaHoraInicio']) -pd.to_datetime( dfParadasProgramadas['FechaEjecucion'] )
  # dfParadasProgramadas['FechaHoraFinTime'] = pd.to_datetime(dfParadasProgramadas['FechaHoraFin']) -pd.to_datetime( dfParadasProgramadas['FechaEjecucion'] )

  # # Convertir a minutos y luego a segundos
  # dfParadasProgramadas['FechaHoraInicioMinutos'] = (dfParadasProgramadas['FechaHoraInicioTime'].dt.total_seconds())/60
  # dfParadasProgramadas['FechaHoraFinMinutos'] = dfParadasProgramadas['FechaHoraFinTime'].dt.total_seconds()/60

  # # Ahora puedes acceder a las columnas TotalMinutos y TotalMinutos
  # dfParadasProgramadas['FechaHoraInicioMinutos']=dfParadasProgramadas['FechaHoraInicioMinutos'].astype(int)
  # dfParadasProgramadas['FechaHoraFinMinutos']=dfParadasProgramadas['FechaHoraFinMinutos'].astype(int)
  # longitud = dfParadasProgramadas.shape[0]

  # for i in range(longitud):
  #   item = dfParadasProgramadas.loc[i]
  #   dfDisponibilidadMaquina.loc[item.FechaHoraInicioMinutos:item.FechaHoraFinMinutos, str(item.CODIGO_MAQUINA)	] = "-1"

  dfPartidasYsecuencias = pd.merge(dfPartidas, ArticulosRutas, on='ARTICULO', how='left')
  dfPartidasYsecuencias
  dfPartidasYsecuencias['Inicio'] = np.nan
  dfPartidasYsecuencias['DuracionEnMaquina'] = np.nan
  dfPartidasYsecuencias['CODIGO_MAQUINA'] = None
  dfPartidasYsecuencias['CodPlan'] = np.nan
  dfPartidasYsecuencias['estuvo_en_espera'] = False

  # Todos los procesos disponibles segun el Plan de Capacidad
  def seleccionarPosiblesProceso(Inicio,CODIGO_MAQUINA):
    filtro = (dfPlan['estaDisponible'] == True) & (dfPlan['CODIGO_MAQUINA'] == CODIGO_MAQUINA)
    dfFiltrado = dfPlan.loc[filtro]
    dfFiltrado = dfFiltrado[(pd.isna(dfFiltrado['horaFinMax'])) | (dfFiltrado['horaFinMax'] <= Inicio)]
    return dfFiltrado

  def agregarHoras(dataFrame,Inicio): 
    dataFrameLoc = dataFrame.iloc[0]
    codMaquina= str(dataFrameLoc['CODIGO_MAQUINA'])
    tiempo = int(dataFrameLoc['Tiempo_Procesar(h)'])
    CodPlan = int(dataFrameLoc['CodPlan'])
    PARTIDAS = int(dataFrameLoc['PARTIDAS'])
    CODIGO_PROCESO = str(dataFrameLoc['CODIGO_PROCESO'])
    CANTIDAD = dataFrameLoc['CANTIDAD'] 
    indice = dfPartidas.loc[dfPartidas['PARTIDAS'] == PARTIDAS].index 
    dfPartidas.loc[indice[0], 'horaFinMax'] =int(Inicio + tiempo)
    filtro = (dfPlan['PARTIDAS'] == PARTIDAS)
    dfPlan.loc[filtro, 'estaDisponible'] = False
    dfPlan.loc[filtro, 'horaFinMax'] =int(Inicio + tiempo)
    procesoActual = dataFrameLoc['Secuencia_Proceso'].index(CODIGO_PROCESO)
    if (procesoActual + 1) != len(dataFrameLoc['Secuencia_Proceso']):
        filtro = (dfPlan['PARTIDAS'] == PARTIDAS) & (dfPlan['CODIGO_PROCESO'] == dataFrameLoc['Secuencia_Proceso'][procesoActual + 1])
        dfPlan.loc[filtro, 'estaDisponible'] = True


    #PARA EL REPORTE
    dfPartidasYsecuencias.loc[(dfPartidasYsecuencias['PARTIDAS'] == PARTIDAS) &
                            (dfPartidasYsecuencias['CODIGO_PROCESO'] == CODIGO_PROCESO),
                            ['Inicio', 'DuracionEnMaquina','CODIGO_MAQUINA','CANTIDAD','CodPlan']] = [int(Inicio), int(tiempo),str(codMaquina),CANTIDAD,CodPlan]
    dfDisponibilidadMaquina.loc[Inicio:(Inicio + tiempo - 1), codMaquina] = str(PARTIDAS)+" "+CODIGO_PROCESO
    data1 = dfPartidasYsecuencias.loc[(dfPartidasYsecuencias['PARTIDAS'] == PARTIDAS) &
                            (dfPartidasYsecuencias['CODIGO_PROCESO'] == CODIGO_PROCESO)].index
    data2 = dfPartidasYsecuencias.loc[data1[0]]
    if data2['codProcesoSiguiente']!=CODIGO_PROCESO:
      data3 = dfPartidasYsecuencias.loc[data1[0]-1]

      if(data3['DuracionEnMaquina']+data3['Inicio']<Inicio):
        dfDisponibilidadMaquinaAtrasados.loc[Inicio, codMaquina] = Inicio-data3['DuracionEnMaquina']-data3['Inicio']
        dfPartidasYsecuencias.loc[(dfPartidasYsecuencias['PARTIDAS'] == PARTIDAS) &
                            (dfPartidasYsecuencias['CODIGO_PROCESO'] == CODIGO_PROCESO),
                            ['estuvo_en_espera']] = [True]

    return 0

  def indice_primer_menos_uno(columna):
      return columna.eq("-1").idxmax()

  def comprobarMaquinaPorTiempo(Inicio):
    for i in range(totalMaquinas):
      #Evaluar Maquina i
      analizarCasosEnProceso=True
      while(analizarCasosEnProceso):

        partidasYprocesos= seleccionarPosiblesProceso(Inicio,str(dfMaquinas.iloc[i]['CODIGO_MAQUINA']))

        if not(partidasYprocesos.empty):
          partidaSeleccionado = partidasYprocesos.iloc[0]
          filtro = (dfPlan['PARTIDAS'] == partidaSeleccionado['PARTIDAS']) & (dfPlan['CODIGO_PROCESO'] == partidaSeleccionado['CODIGO_PROCESO'])
          maquinas_procesables = dfPlan.loc[filtro]

          first_row = dfDisponibilidadMaquina.loc[Inicio]
          processed_items = []
          for idx, item in enumerate(first_row):
            if not(isinstance(item, str)):
              processed_items.append(dfDisponibilidadMaquina.columns[idx])

          df_procesado = pd.DataFrame(processed_items[2:], columns=['CODIGO_MAQUINA'])

          df_procesado_Partidas = pd.merge(maquinas_procesables,df_procesado, on='CODIGO_MAQUINA', how='inner')

          if(df_procesado_Partidas.empty):
            analizarCasosEnProceso = False
          else:
            prueba = dfDisponibilidadMaquina[Inicio:]
            indices_primer_menos_uno = prueba.apply(indice_primer_menos_uno)
            dfPrueba = pd.DataFrame(list(indices_primer_menos_uno.items()), columns=['CODIGO_MAQUINA', 'countLibre'])

            df_procesado_Partidas2 = pd.merge(df_procesado_Partidas,dfPrueba, on='CODIGO_MAQUINA', how='left')

            df_procesado_Partidas3 = df_procesado_Partidas2[(df_procesado_Partidas2['Tiempo_Procesar(h)'] < (abs(Inicio - df_procesado_Partidas2['countLibre'])) )|( Inicio == df_procesado_Partidas2['countLibre']) ]
            if(df_procesado_Partidas3.empty):
              analizarCasosEnProceso = False
            else:
              primera_procesable_menor_tiempo = df_procesado_Partidas3.nsmallest(1, 'Tiempo_Procesar(h)')
              agregarHoras(primera_procesable_menor_tiempo,Inicio)
        else:
          analizarCasosEnProceso = False
    return 0

  def saltoTiempo(time): 
    first_row = dfDisponibilidadMaquina.loc[time] 

    # Inicializar una lista para almacenar los elementos procesados
    processed_items = []

    # Iterar a través de los elementos de la primera fila
    for item in first_row:
      if isinstance(item, int):
        if(item!="-1"):
          processed_items.append(item.split()[0])
        else:
          return (time+1) 
    if(len(processed_items)==0):
      return (time+1)
    else:
      # Crear un nuevo DataFrame a partir de los elementos procesados
      df_procesado = pd.DataFrame(processed_items, columns=['PARTIDAS'])
      

      # Mostrar el nuevo DataFrame o hacer lo que necesites con él

      df_procesado_Partidas = pd.merge(df_procesado, dfPartidas, on='PARTIDAS', how='left')

      indice_primero_menos_uno = (dfDisponibilidadMaquina.loc[time:] == "-1").idxmax()
      df_indice_primero_menos_uno = pd.DataFrame(indice_primero_menos_uno)
      prueba = (totalMaquinas+2)*time
      if df_indice_primero_menos_uno.sum().values[0]==prueba:
        return int(df_procesado_Partidas['horaFinMax'].min())



      indice_segundo_menor = df_indice_primero_menos_uno[df_indice_primero_menos_uno != df_indice_primero_menos_uno.min()].min()
      if (int(df_procesado_Partidas['horaFinMax'].min()) <= int(indice_segundo_menor)):
        return int(df_procesado_Partidas['horaFinMax'].min())
      else:
        return int(indice_segundo_menor)

  print(dfPartidasYsecuencias['Inicio'].isnull().sum())

  def main():
    hayProcesosPendientes = True
    Inicio = 0
    # Inicio = 37694
    while(hayProcesosPendientes):
      # cantidad_nulos = dfPartidasYsecuencias['Inicio'].isnull().sum()
      print("----- MINUTO ",Inicio," EJECUTADO---- PROCESOS RESTANTES: ",dfPartidasYsecuencias['Inicio'].isnull().sum(),"----------")
      comprobarMaquinaPorTiempo(Inicio)
      filas_filtradas = dfPartidasYsecuencias['Inicio']
      if filas_filtradas.notnull().all():
        print("No hay partidas por Procesar")
        # print(dfPartidasYsecuencias)
        hayProcesosPendientes = False

      Inicio=saltoTiempo(Inicio)
      # Comentar estas dos lineas
      # if Inicio >= 23 :
      #   hayProcesosPendientes = False
      # Inicio=Inicio+1

    return 0
 
  main() 

  resultado_left = pd.merge(dfPartidasYsecuencias, dfProcesos, on='CODIGO_PROCESO', how='left')
  resultado_left2 = pd.merge(resultado_left, dfMaquinas, on='CODIGO_MAQUINA', how='left')
  resultado_left2['Fin']=resultado_left2['Inicio']+resultado_left2['DuracionEnMaquina']
  resultado_left2['FechaEjecucion'] = fecha_inicial
  resultado_left2['FechaEjecucion'] = pd.to_datetime(resultado_left2['FechaEjecucion'])
  resultado_left2['InicioMinutos'] = pd.to_timedelta(resultado_left2['Inicio'], unit='m')
  resultado_left2['FinMinutos'] = pd.to_timedelta(resultado_left2['Fin'], unit='m')
  resultado_left2['Hora_estimada_Inicial'] = resultado_left2['FechaEjecucion'] + resultado_left2['InicioMinutos']
  resultado_left2['Hora_estimada_final'] = resultado_left2['FechaEjecucion'] + resultado_left2['FinMinutos']
  resultado_left2['total_ParTelPro_atrasadas'] = resultado_left2['Hora_estimada_final'] > resultado_left2['FECHA OBJETIVO']
  resultado_left2['SECUENCIA'] = resultado_left2.sort_values(by='Inicio' ).groupby('CODIGO_MAQUINA').cumcount() + 1
  resultado_left2['ParTelPro_Atrasado_Y_en_Espera'] = resultado_left2['total_ParTelPro_atrasadas'] &  resultado_left2['estuvo_en_espera']

  del resultado_left2['codProcesoSiguiente']
  del resultado_left2['horaFinMax']
  resultado_left2['SECUENCIA'] = resultado_left2.sort_values(by='Inicio' ).groupby('CODIGO_MAQUINA').cumcount() + 1
  del resultado_left2['CodPlan']
  del resultado_left2['FechaEjecucion']
  # del resultado_left2['Color_Representativo']
  resultado_left2.rename(columns={'Inicio': 'Inicio (min)'}, inplace=True)
  resultado_left2.rename(columns={'DuracionEnMaquina': 'DuracionEnMaquina (min)'}, inplace=True)
  resultado_left2.rename(columns={'Fin': 'Fin (min)'}, inplace=True)
  resultado_left2.rename(columns={'ARTICULO': 'CODIGO_TELA'}, inplace=True)
  print(" --------------------- resultado_left2 ------------ ")
  print(resultado_left2)
  resultado_left2.to_excel("salida.xlsx", index=False)
  return resultado_left2
