from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import AccountSerializer
from rest_framework.authtoken.models import Token
from .models import Account
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def login(request):
    user = get_object_or_404(Account, email = request.data["email"])
    if not user.check_password(request.data["password"]):
        return Response({"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)
    token, create = Token.objects.get_or_create(user=user)
    serializer = AccountSerializer(instance=user)
    return Response({"token":token.key, "user":serializer.data})
    
@api_view(['POST'])
def signup(request):
    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = Account.objects.get(email= request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token":token.key, "user":serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    user = AccountSerializer(request.user).data
    return Response(user)