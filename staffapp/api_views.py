
from rest_framework import generics
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from staffapp.models import staffDetails
from .serializers import StaffDetailsSerializer


class AllStaff(generics.ListAPIView): 
    queryset = staffDetails.objects.all()
    serializer_class = StaffDetailsSerializer
