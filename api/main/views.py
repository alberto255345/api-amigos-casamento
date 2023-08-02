import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from .serializers import FileUploadSerializer, UserSerializer
from .models import User  # Importe o seu modelo User
from django.contrib.auth.models import Group


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
                user = User.objects.create_user(
                    name=row['name'],
                    email=row['email'], 
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
