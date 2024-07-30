from django.shortcuts import render
from rest_framework import viewsets
from .models import ToDo
from .serializers import ToDoSerializer


class ToDoViewSet(viewsets.ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer


def index(request):
    return render(request, "todoapp/index.html")
