from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.exceptions import AuthenticationFailed
from django.core.files.storage import FileSystemStorage
from backendApp.serializers import LogUploadSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import LogUpload, ForwarderData, User
from .serializers import LogUploadSerializer, ForwarderDataSerializer, UserSerializer
from rest_framework import status
import jwt, datetime




#register and login part start from here

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

     #with email we are finding the user bcoz email is unique
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed("User not found!")

     #as password is hashed      this fxn already provided by django
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),    #we will keep this token for 1 hours
            'iat': datetime.datetime.utcnow()   #date when token is created
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')


        response =  Response()

        # response.set_cookie(key='jwt', value=token, httponly=True)
        response.set_cookie(key='jwt', value=token, samesite='none', secure=True)         #it works fine , but not for production mode 

        # response.set_cookie(key='jwt', value=token,samesite='None', httponly=True)
        # response.set_cookie(key='jwt', value='token', samesite='None', httponly=True)


        response.data = {
            'jwt': token,
        }

        print(response.data)

        return response


class UserView(APIView):

    def get(self, request):
        print(request.COOKIES)
        token = request.COOKIES.get('jwt')     #retrieve from cookie

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

        
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


# data forwarder technique start from here

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
    