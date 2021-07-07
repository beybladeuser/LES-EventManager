# LES-EventManager
The source for the final project of LES

How to run this:

1º install django and all other libs:

```
  c:\folder_example> python -m venv Django
  
  c:\folder_example> Django\Scripts\activate.bat
  
  (Django) c:\folder_example> python -m pip install --upgrade pip
  
  (Django) c:\folder_example> python -m pip install Django
  
  (Django) c:\folder_example> python -m pip install django-crispy-forms
  
  (Django) c:\folder_example> python -m pip install mysqlclient

  (Django) c:\folder_example> python -m pip install django-tables2

  (Django) c:\folder_example> python -m pip install django-filter

  (Django) c:\folder_example> python -m pip install django-notifications-latest
  
  (Django) c:\folder_example> python -m pip install django-notifications-hq

  (Django) c:\folder_example> python -m pip install django-clear-cache
```

2º clone this rep:
  Sugestion: have the files like this
  ```
    c:\folder_example\
      Django\
      LES-EventManager\
  ```

  Where Django contains the django install and LES-EventManager contains this rep

  Note:
  after you clone the repo, you could install all dependencies using the following:
  ```
    (Django) c:\folder_example\LES-EventManager> python -m pip install -r requirements.txt
  ```

3º follow this to setup the db:
  just a cool tutorial:
  https://medium.com/@sonuyohannan/django-and-mysql-how-to-connect-mysql-database-with-django-project-ee3c695fe7c5

  install xampp

  in LES-EventManager\EventManager\EventManager\settings.py make sure the following code uses your xampp settings:

```  
    DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'eventmanager',
          'USER' : 'root',
          'PASSWORD' : '',
          'HOST' : '127.0.0.1',
          'PORT' : '3306',
          'OPTIONS' : {
              'init_command':"SET sql_mode='STRICT_TRANS_TABLES'"
          }
      }
    }
```

   next do the following:
```
    c:\folder_example> Django\Scripts\activate.bat
    
    (Django) c:\folder_example> cd LES-EventManager\EventManager\
    
    (Django) c:\folder_example\LES-EventManager\EventManager> python manage.py makemigrations
    
    (Django) c:\folder_example\LES-EventManager\EventManager> python manage.py migrate
```

4º: load default values
```
  python manage.py loaddata basic_fixtures.json
```
  this adds all the types of forms, events, assets, etc
  the user groups
  and a superuser of the admin group with the credentials:
    username: admin
    password: alaridodameianoite

5º: run the server
```    
    c:\folder_example> Django\Scripts\activate.bat
    
    (Django) c:\folder_example> cd LES-EventManager\EventManager\
    
    (Django) c:\folder_example\LES-EventManager\EventManager> python manage.py runserver
```
 should be working fine
    


