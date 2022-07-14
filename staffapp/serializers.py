
from rest_framework import serializers


class StaffDetailsSerializer(serializers.Serializer):
    staff_image = serializers.ImageField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.IntegerField()
    level = serializers.IntegerField()
    step = serializers.IntegerField()
    email = serializers.EmailField()
    cadre = serializers.CharField()
    department = serializers.CharField()