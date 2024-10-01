from rest_framework import serializers
from .models import Project, Task
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):   #we can perfom this in views.py as well 
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProjectSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'users', 'is_admin', 'is_deleted', 'admin']

    def get_is_admin(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.admin == request.user
        return False

    

class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()  
    class Meta:
        model = Task
        fields = '__all__'

class CreateTaskSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Task
        fields = '__all__'
