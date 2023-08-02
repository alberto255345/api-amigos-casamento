from django.shortcuts import render
from rest_framework import viewsets
from .models import User#, categoryUser
from .serializers import UserSerializer#, CategorySerializer

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# ViewSets Define Api
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = categoryUser.objects.all()
#     serializer_class = CategorySerializer

class UserUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request):
        file_obj = request.data['file']

        # Verifique o tipo de arquivo
        if file_obj.content_type not in ['text/csv', 'text/plain', 'application/vnd.ms-excel']:
            return Response({'error': 'Formato de arquivo inválido'}, status=status.HTTP_400_BAD_REQUEST)

        # Faça a leitura do arquivo e crie instâncias de User
        users = []
        for line in file_obj:
            line = line.decode('utf-8').strip()
            fields = line.split(',')

            if len(fields) != 5:  # Certifique-se de que o arquivo tem o número correto de campos
                return Response({'error': 'Formato de linha inválido'}, status=status.HTTP_400_BAD_REQUEST)

            user_data = {
                'name': fields[0],
                'email': fields[1],
                # Preencha os outros campos de acordo
            }

            serializer = UserSerializer(data=user_data)
            if serializer.is_valid():
                serializer.save()
                users.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Usuários criados com sucesso', 'users': users}, status=status.HTTP_201_CREATED)
