
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from birthday.models import staffDetails
from .serializers import StaffDetailsSerializer


class AllStaff(ListAPIView): 
    queryset = staffDetails.objects.all()
    serializer_class = StaffDetailsSerializer
