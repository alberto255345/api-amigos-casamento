# Api Amigos do Casamentoe

API to help a friend create a wedding photo gallery.:

## Stack used
* Python
* Django
* Django Rest Framewrok
* PostgreSQL (neon.tech)
* Cloud Run GCP

* Only allows the groups to approve the photos: "noivos" and "amigos".
* Support CSV impoty of guestlist
    * Import a CSV of guests and the following data:
      * Full Name
      * Email
      * Password
      * Groups

# Getting started

1. Initialise Django's database; from the project's root directory, run:

``` 
python manage.py check
python manage.py makemigrations
python manage.py migrate
```
2. Create an account and load initial data; still from the project's root directory, 
run:
```
python manage.py createsuperuser
python manage.py loaddata main/initial_data.json
``` 

3. *(Optional): import sample data to play with the database: go to
   localhost:8000/upload, pick "Upload csv" and upload upload_data.csv*

Upload CSV:

Nome: Upload CSV
Método: POST
Autenticação: Bearer Token
Corpo: Form Data
Tipo: Arquivo (file)
Chave: "file"
URL: http://localhost:8000/upload/
Objetivo: Fazer upload de um arquivo CSV.
Photos:

Nome: Photos
Método: POST
Autenticação: Bearer Token
Corpo: Form Data
Tipo: Arquivo (file)
Chave: "image"
URL: http://localhost:8000/photos/
Objetivo: Enviar uma foto para ser processada.
TOKEN:

Nome: TOKEN
Método: POST
Autenticação: Sem autenticação
Corpo: Form Data
Tipo: Texto
Chave: "username"
Valor: Endereço de e-mail
Chave: "password"
Valor: Senha
URL: http://localhost:8000/token/
Objetivo: Autenticar e obter um token de acesso.
Aprovação:

Nome: Aprovação
Método: POST
Autenticação: Bearer Token
URL: http://localhost:8000/approved/1/
Objetivo: Enviar uma solicitação de aprovação para um item identificado como "1".
Like:

Nome: Like
Método: POST
Autenticação: Bearer Token
URL: http://localhost:8000/like/1/
Objetivo: Enviar um "like" para um item identificado como "1".
Comentar:

Nome: Comentar
Método: POST
Autenticação: Bearer Token
Corpo: Form Data
Tipo: Texto
Chave: "comment"
Valor: Texto do comentário
URL: http://localhost:8000/comment/1/
Objetivo: Enviar um comentário para um item identificado como "1".
