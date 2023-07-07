from django.urls import path
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models
from django.apps import AppConfig
from django.core.management import call_command
from django.http import HttpResponse

# Django app configuration
class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

# Django model
class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Django model serializer
class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'

# Django API view
class MyModelList(APIView):
    def get(self, request):
        mymodels = MyModel.objects.all()
        serializer = MyModelSerializer(mymodels, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MyModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Django URL patterns
urlpatterns = [
    path('mymodels/', MyModelList.as_view()),
]

# Django app initialization
def initialize():
    call_command('makemigrations')
    call_command('migrate')
    call_command('runserver')

# Main function
if __name__ == '__main__':
    # Django setup
    import os
    import sys
    import django

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    django.setup()

    # Run app initialization
    initialize()
