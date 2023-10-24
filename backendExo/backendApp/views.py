from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from django.core.files.storage import FileSystemStorage
from backendApp.serializers import LogUploadSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import LogUpload, ForwarderData
from .serializers import LogUploadSerializer
from rest_framework import status


from .serializers import ForwarderDataSerializer

class ForwarderDataViewSet(viewsets.ModelViewSet):
    queryset = ForwarderData.objects.all()
    serializer_class = ForwarderDataSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        print(query)
        return ForwarderData.objects.filter(log_data__icontains=query)
    
# standard  implementation for handling HTTP GET requests to retrieve a list of objects
    def list(self, request):
        queryset = self.get_queryset()               
        serializer = ForwarderDataSerializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)


class LogUploadViewSet(viewsets.ModelViewSet):
    queryset=LogUpload.objects.all()
    serializer_class=LogUploadSerializer


class dataViewSet(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, format=None):
        print("chala")
        upload_log = request.FILES['logFile']
        body = request.POST['logDescription']
        created_at=request.POST['logDate']


        fs = FileSystemStorage(location="event/static") 
        filename=fs.save(upload_log.name,upload_log)
        print(filename)
        log_url=fs.url(filename)
        print(log_url)
        path="event/static/"+filename
        print(path)


        LogUpload.objects.create(uploadedFile_path=path,body=body,created_at=created_at)

        with open(path, 'r') as file:
            log_data = file.read()
            print(log_data)    

        forwarder_data = {
            "file_name": upload_log.name,  
            "log_data": log_data,  
        }

        forwarder_serializer = ForwarderDataSerializer(data=forwarder_data)
        if forwarder_serializer.is_valid():
            forwarder_serializer.save()
            return Response({'message': 'log uploaded successfully'}, status=status.HTTP_201_CREATED)
        return Response(forwarder_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    