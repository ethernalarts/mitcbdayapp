
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
#from .utils import average_rating
from birthday.models import staffDetails



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['lastname', 'email']
        

class StaffDetailsSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    book = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = staffDetails
        fields = [
            'staff_image', 'first_name', 'middle_name', 'last_name', 
            'gender_text', 'level', 'step', 'email', 'cadre', 'department'
        ]

    def create(self, validated_data):
        request = self.context["request"]
        creator = request.user
        
        if not creator.is_authenticated:
            raise NotAuthenticated('Authentication required.')
        book = Book.objects.get(pk=request.data['book_id'])
        return Review.objects.create(content=validated_data['content'], book=book, creator=creator,
                                     rating=validated_data['rating'])

    def update(self, instance, validated_data):
        request = self.context['request']
        creator = request.user
        if not creator.is_authenticated or instance.creator_id != creator.pk:
            raise PermissionDenied('Permission denied, you are not the creator of this review')
        instance.content = validated_data['content']
        instance.rating = validated_data['rating']
        instance.date_edited = timezone.now()
        instance.save()
        return instance
