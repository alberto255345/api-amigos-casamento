# Api Amigos do Casamentoe

A Django project to help you wrangle a wedding's guests. Wedding Wrangle will:

* Import a CSV of guests and the following data:
    * Full Name
    * Email
    * Password
    * Groups

## Stack used
* Python
* Django
* Django Rest Framewrok
* PostgreSQL (neon.tech)
* Cloud Run GCP
* Swagger

* Allow users (wedding organisers) to log in and see a dashboard of their guests, as
  well as update each guest's details and partnerships (one-to-one relationship with
  another guest)
* Send emails to guests asking them to RSVP using a random string-encoded URL 
    * Guests' partners are emailed at the same time, with both links for convenience
* Serve random string-encoded URLs to allow guests to mark boolean attendance and
  complex dietary requirements (many-to-many)
* Support CSV export of guestlist
    * This will allow for mail-merging of physical invites and placecards
* Support export of QR codes as an alternative RSVP option

The project will mostly store and return text. It will return images too: QR codes.
Logged-in users will have the ability to interactively edit guest details.

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

