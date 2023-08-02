import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import FileUploadSerializer, UserSerializer, PhotoSerializer
from .models import User, Photo, Like, Comment  # Importe o seu modelo User
from .permissions import CanEditPhotoPermission
from django.contrib.auth.models import Group
from django.contrib.auth.models import User as UserMaster


# ViewSets Define Api
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUploadView(APIView):
    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']

            # Verifique o formato do arquivo (Excel, CSV ou TXT)
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file, header=0)  # Pula a primeira linha (títulos)
            elif file.name.endswith('.csv'):
                df = pd.read_csv(file, header=0, sep=';')  # Pula a primeira linha (títulos)
            elif file.name.endswith('.txt'):
                df = pd.read_csv(file, delimiter='\t', header=0)  # Pula a primeira linha (títulos)
            else:
                return Response({'error': 'Formato de arquivo inválido'}, status=status.HTTP_400_BAD_REQUEST)

            # Itere sobre as linhas do DataFrame e crie os objetos User
            users_to_create = []
            for index, row in df.iterrows():
                user = UserMaster.objects.create_user(
                    first_name=row['name'],
                    email=row['email'], 
                    username=row['email'],
                    password=row['password'],
                )

                # Adicionar os grupos ao usuário usando o método set()
                groups = row['groups'].split(',')  # Supondo que os grupos estão separados por vírgula no CSV
                for group_name in groups:
                    group, created = Group.objects.get_or_create(name=group_name.strip())
                    user.groups.add(group)

            # Crie os objetos User no banco de dados
            User.objects.bulk_create(users_to_create)

            return Response({'message': 'Arquivo processado com sucesso'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [CanEditPhotoPermission]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_photo(request, photo_id):
    try:
        photo = Photo.objects.get(pk=photo_id)
    except Photo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if user.groups.filter(name='noivos').exists() or user.groups.filter(name='amigos').exists():
        print('entrou')
        photo.approve()
        photo.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_photo(request, photo_id):
    try:
        photo = Photo.objects.get(pk=photo_id)
    except Photo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    Like.like_photo(user, photo)
    
    return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_photo(request, photo_id):
    try:
        photo = Photo.objects.get(pk=photo_id)
    except Photo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    text = request.data.get('text', '')  # Obtenha o texto do comentário da solicitação POST
    
    Comment.create_comment(user, photo, text)
    
    return Response(status=status.HTTP_201_CREATED)