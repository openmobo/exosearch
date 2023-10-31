from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.exceptions import AuthenticationFailed
from django.core.files.storage import FileSystemStorage
from backendApp.serializers import LogUploadSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import LogUpload, ForwarderData, User, APIKey
from .serializers import LogUploadSerializer, ForwarderDataSerializer, UserSerializer, APIKeySerializer
from rest_framework import status
import jwt, datetime
from django.http import HttpRequest
from rest_framework.pagination import PageNumberPagination
from rest_framework import pagination
from django.utils.dateparse import parse_date
import re
from datetime import datetime as datetimestamp
from django.contrib.auth import authenticate




class APIKeyViewSet(viewsets.ModelViewSet):
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer
    # permission_classes = [permissions.IsAuthenticated]

    # user = User.objects.filter(email=email).first()

    # def perform_create(self, serializer):
    #     # Automatically set the user of the API key to the currently authenticated user.
    #     print(self.request.user)
    #     serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(name='admin').exists():
            return APIKey.objects.all()
        return APIKey.objects.filter(user=user, is_user_key=True)


class change_password(APIView): 
    def post(self, request):
        email = request.data['email']
        current_password = request.data['currentPassword']
        confirmed_password = request.data['password']

        print(email)
        print(confirmed_password)
        print(current_password)

        
        user = User.objects.filter(email=email).first()
        print(user)

        if user is None:
            raise AuthenticationFailed("User not found!")

        # Authenticate the user using the current password
        if not authenticate(request, username=email, password=current_password):
            raise AuthenticationFailed("Incorrect current password")

        # Change the user's password
        user.set_password(confirmed_password)
        user.save()


        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
   


#register and login part start from here

class RegisterView(APIView):
    def post(self, request):
        print("aaya")
        print(request.data)
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
       
        serializer.save()
        return Response(serializer.data)




class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        # print("aaya")
     #with email we are finding the user bcoz email is unique
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed("User not found!")
        
     #as password is hashed      this fxn already provided by django
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
                
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=240),    #we will keep this token for 4 hours
            'iat': datetime.datetime.utcnow()   #date when token is created
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response =  Response()
        # response.set_cookie(key='jwt', value=token, httponly=True)
        response.set_cookie(key='jwt', value=token, samesite='none', secure=True, httponly=True)
        # response.set_cookie(key='jwt', value=token, samesite='none', secure=True)         #it works fine , but not for production mode 
             #it works fine , but not for production mode 
        # response.set_cookie(key='jwt', value=token, secure=True)  # Remove samesite='none'

        # response.set_cookie(key='jwt', value=token,samesite='None', httponly=True)
        # response.set_cookie(key='jwt', value='token', samesite='None', httponly=True)
        response.data = {
            'jwt': token,
        }
        print(response.data)

        return response


class UserView(APIView):

    def get(self, request):
        print("chala user")
        # print(request.COOKIES)
        token = request.COOKIES.get('jwt')     #retrieve from cookie
        print(token)

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
        print("chala logout")
        response = Response()
        response.delete_cookie(key='jwt',samesite='none')        #not suitable for production     

        response.data = {
            'message': 'success'
        }
        return response


# data forwarder technique start from here

# class LargeResultsSetPagination(PageNumberPagination):
#     page_size = 1000
#     page_size_query_param = 'page_size'
#     max_page_size = 10000

class ForwarderDataViewSet(viewsets.ModelViewSet):
    queryset = ForwarderData.objects.all()
    serializer_class = ForwarderDataSerializer
    # pagination_class = PageNumberPagination  # Enable pagination
    # pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        email = self.request.query_params.get('email', '')  # Get the email parameter from the query string

        queryappend = query
        print(query)
        print(email)
        from_date = self.request.query_params.get('from', '')
        to_date = self.request.query_params.get('to', '')
        print(from_date)
        print(to_date)
        queryset = ForwarderData.objects.filter(email=email, log_data__icontains=query)

        print(queryset)

        

        fileArrays = []
        dataArray = []

        for query in queryset:
            print(query.log_data)
            print("haaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            
            log_entries = query.log_data.split('\n')

            log_entry_pattern = re.compile(r'\[([^\]]+)\] (.+)')

            for log_entry in log_entries:
                match = log_entry_pattern.match(log_entry)
                if match:
                    # log_datetime = datetime.strptime(match.group(1), '%a %b %d %H:%M:%S.%f %Y')
                    log_datetime = datetimestamp.strptime(match.group(1), '%a %b %d %H:%M:%S.%f %Y')
                    from_datetime = datetimestamp.strptime(from_date, '%Y-%m-%d')
                    to_datetime = datetimestamp.strptime(to_date, '%Y-%m-%d')

                  
                        

                    log_data = match.group(2)

                    print(log_datetime)
                    print(log_data)
                    
                    print(from_datetime <= log_datetime <= to_datetime)

                    if queryappend in log_data:
                        if from_datetime <= log_datetime <= to_datetime:
                            dataArray.append({
                        'log_datetime': log_datetime,
                        'log_data': log_data
            })


            print("\n \n \n")
            print(dataArray)
            fileArrays.append( {
                'log_data' : dataArray,
                'file_name': query.file_name,

            })

            dataArray = []

        # if from_date:
        #     from_date = parse_date(from_date)
        #     queryset = queryset.filter(received_at__gte=from_date)

        # if to_date:
        #     to_date = parse_date(to_date)
        #     to_date = datetime.datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59)  # Set the time to end of the day
        #     queryset = queryset.filter(received_at__lte=to_date)
        
       
        print('\n\n\\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        print(fileArrays[0]['file_name'])

        print('\n\n\\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

        # return queryset  # Filter based on email and query
        return fileArrays
    
# standard  implementation for handling HTTP GET requests to retrieve a list of objects
    def list(self, request):
        queryset = self.get_queryset()               
        # serializer = ForwarderDataSerializer(queryset, many=True)
        # print(serializer.data)
        return Response(queryset)


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
        email=request.POST['email']

        user = User.objects.filter(email=email).first()
        print(user.role)



         # Capture the host information
        host = request.META.get('HTTP_HOST')

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
            "email": email,
            "host": host,

        }
        if user.role == "admin":
            forwarder, created = ForwarderData.objects.get_or_create(
                file_name=forwarder_data['file_name'],
                email=forwarder_data['email'],
                host=forwarder_data['host'],
                defaults={'log_data': forwarder_data['log_data']}
            )

            if not created:
                # If the entry already exists, update it
                forwarder.log_data = forwarder_data['log_data']
                forwarder.save()

            return Response({'message': 'Log uploaded successfully'}, status=201)

        return Response({'error': 'Unauthorized or invalid user'}, status=403)    
    