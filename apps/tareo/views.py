from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Machinery
from .serializers import MachinerySerializer
from rest_framework.permissions import AllowAny

class MachineryListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        machineries = Machinery.objects.all()
        serializer = MachinerySerializer(machineries, many=True)
        return Response(serializer.data)