
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sendmail.models import staffDetails
from .serializers import StaffDetailsSerializer



# @api_view()
# def all_staff(request):
#     staffdetails = staffDetails.objects.all()
#     staffdetails_serializer = StaffDetailsSerializer(staffdetails, many=True)
#     return Response(staffdetails_serializer.data)


class AllStaff(ListAPIView): 
    queryset = staffDetails.objects.all()
    serializer_class = StaffDetailsSerializer
