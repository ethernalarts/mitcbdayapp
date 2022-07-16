
from rest_framework import serializers
from birthday.models import staffDetails


class StaffDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = staffDetails
        fields = [
            'staff_image', 'first_name', 'middle_name', 'last_name', 
            'gender_text', 'level', 'step', 'email', 'cadre', 'department'
            ]