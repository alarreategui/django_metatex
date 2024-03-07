from .serializers import *
from datetime import datetime
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import ProcessMachinery, FabricRoll, FabricBatch, Fabric, RoutePoint

class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class ProcessListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        processes = Process.objects.all()
        serializer = ProcessSerializer(processes, many=True)
        return Response(serializer.data)


class StopListView(APIView):
    """
    API endpoint to retrieve stops based on start date.

    Parameters:
        start_timestamp (int): The start timestamp.

    Returns:
        list: A list of stop objects with the specified start date or later.

    Example:
        To retrieve stops with a start date on or after '2024-01-15', send a GET request to '/stops/?start_timestamp=1609459200'.
    """
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        if start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            stops = Stop.objects.filter(start_datetime__gte=start_datetime)
        else:
            stops = Stop.objects.all()
        serializer = StopSerializer(stops, many=True)
        return Response(serializer.data)
    
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

class OrderListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            order = Order.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            order = Order.objects.filter(updated_at__gte=start_datetime)
        else:
            order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'code'

class PriorityListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            priority = Priority.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            priority = Priority.objects.filter(updated_at__gte=start_datetime)
        else:
            priority = Priority.objects.all()
        serializer = PrioritySerializer(priority, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PrioritySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PriorityRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    lookup_field = 'code'
    
class FabricTypeListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            fabric_type = FabricType.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            fabric_type = FabricType.objects.filter(updated_at__gte=start_datetime)
        else:
            fabric_type = FabricType.objects.all()
        serializer = FabricTypeSerializer(fabric_type, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FabricTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FabricTypeRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = FabricType.objects.all()
    serializer_class = FabricTypeSerializer
    lookup_field = 'code'

class FabricFamilyListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            fabric_family = FabricFamily.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            fabric_family = FabricFamily.objects.filter(updated_at__gte=start_datetime)
        else:
            fabric_family = FabricFamily.objects.all()
        serializer = FabricFamilySerializer(fabric_family, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FabricFamilySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FabricFamilyRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = FabricFamily.objects.all()
    serializer_class = FabricFamilySerializer
    lookup_field = 'code'
class ColorListView(APIView):
    pagination_class = CustomPagination
    permission_classes = (AllowAny,)

    def get(self, request):
        paginator = self.pagination_class()
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        colors_query = Color.objects.all()
        if start_datetime and end_datetime:
            colors_query = colors_query.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            colors_query = colors_query.filter(updated_at__gte=start_datetime)        
        colors_query = colors_query.order_by('code')
        result_page = paginator.paginate_queryset(colors_query, request)
        serializer = ColorSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ColorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ColorRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    lookup_field = 'code'

class QualityTypeListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            quality_type = QualityType.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            quality_type = QualityType.objects.filter(updated_at__gte=start_datetime)
        else:
            quality_type = QualityType.objects.all()
        serializer = QualityTypeSerializer(quality_type, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = QualityTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QualityTypeRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = QualityType.objects.all()
    serializer_class = QualityTypeSerializer
    lookup_field = 'code'

class QualityFieldListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            quality_field = QualityField.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            quality_field = QualityField.objects.filter(updated_at__gte=start_datetime)
        else:
            quality_field = QualityField.objects.all()
        serializer = QualityFieldSerializer(quality_field, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = QualityFieldSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QualityFieldRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = QualityField.objects.all()
    serializer_class = QualityFieldSerializer
    lookup_field = 'code'
    
class ReasonListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            reasons = Reason.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            reasons = Reason.objects.filter(updated_at__gte=start_datetime)
        else:
            reasons = Reason.objects.all()
        serializer = ReasonSerializer(reasons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReasonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReasonRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer
    lookup_field = 'code'
    
class RouteListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        start_timestamp = request.query_params.get('start_timestamp', None)
        end_timestamp = request.query_params.get('end_timestamp', None)
        start_datetime = datetime.fromtimestamp(int(start_timestamp)) if start_timestamp else None
        end_datetime = datetime.fromtimestamp(int(end_timestamp)) if end_timestamp else None
        if start_datetime and end_datetime:
            routes = Route.objects.filter(updated_at__gte=start_datetime, updated_at__lte=end_datetime)
        elif start_timestamp:
            start_datetime = datetime.fromtimestamp(int(start_timestamp))
            routes = Route.objects.filter(updated_at__gte=start_datetime)
        else:
            routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RouteRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    lookup_field = 'code'
    
class MachineryProcessListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        machinery_processes = ProcessMachinery.objects.all()
        serializer = MachineryProcessSerializer(machinery_processes, many=True)
        return Response(serializer.data)

class FabricRollListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        fabric_code = request.query_params.get('fabric_code', None)
        batch_code = request.query_params.get('batch_code', None)
        fabric_rolls = FabricRoll.objects.all()
        if fabric_code and batch_code:
            fabric_batch = FabricBatch.objects.filter(fabric_code=fabric_code, batch_code=batch_code).first()
            if fabric_batch:
                fabric_rolls = fabric_rolls.filter(fabric_batch_code=fabric_batch.code)
            else:
                return Response([], status=status.HTTP_200_OK)
        elif fabric_code:
            fabric_batchs = FabricBatch.objects.filter(fabric_code=fabric_code)
            if fabric_batchs:
                fabric_rolls = fabric_rolls.filter(fabric_batch_code__in=[fabric_batch.code for fabric_batch in fabric_batchs])
            else:
                return Response([], status=status.HTTP_200_OK)
        elif batch_code:
            fabric_batchs = FabricBatch.objects.filter( batch_code=batch_code)
            if fabric_batchs:
                fabric_rolls = fabric_rolls.filter(fabric_batch_code__in=[fabric_batch.code for fabric_batch in fabric_batchs])
            else:
                return Response([], status=status.HTTP_200_OK)
            # return Response({'error': 'fabric_code and batch_code parameters are required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = FabricRollSerializer(fabric_rolls, many=True)
        return Response(serializer.data)

class FabricRollListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        fabric_code = request.query_params.get('fabric_code', None)
        if fabric_code:
            fabric = Fabric.objects.filter(code=fabric_code).first()
            if fabric:
                route_code = fabric.route_code.code
                print('El codigo de ruta actual es %s'%(route_code))
                route = RoutePoint.objects.filter(route_code=route_code)
                # route = RoutePoint.objects.all()
                serializer = RoutePointSerializer(route, many=True)
                return Response(serializer.data)
            else:
                print('No se encontro el codigo de tela')
                return Response([], status=status.HTTP_200_OK)
        return Response({'error': 'fabric_code parameter is required'}, status=status.HTTP_400_BAD_REQUEST)