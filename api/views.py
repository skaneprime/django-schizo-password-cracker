from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth.models import User
from .models import HashRequest
from .serializers import UserSerializer, HashRequestSerializer
from os import getenv


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class HashRequestViewSet(viewsets.ModelViewSet):
    queryset = HashRequest.objects.all()
    serializer_class = HashRequestSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        RATELIMIT_REQ_PER_USER_ENV = getenv("RATELIMIT_REQ_PER_USER")
        
        if RATELIMIT_REQ_PER_USER_ENV is None:
            return Response({
                'error': 'missing env',
                'message': 'RATELIMIT_REQ_PER_USER is not defined in .env'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        ratelimit_req_per_user = int(RATELIMIT_REQ_PER_USER_ENV)
        user_requests_count = self.queryset.filter(user=request.user).count()

        if user_requests_count > ratelimit_req_per_user:
            return Response({
                'error': 'ratelimited',
                'message': 'Max request per user is: ' + str(ratelimit_req_per_user)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(): 
            hash_value = serializer.validated_data['hash_value']
            # Limit to 5 characters lowercase alphabets
            if HashRequest._hash_is_from_limited_alphabet(hash_value) is False:
                return Response({"error": "Invalid characters in hash."}, status=status.HTTP_400_BAD_REQUEST)
            print(request.user)
            serializer.save(user=request.user)
            print(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)