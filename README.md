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
```

2º clone this rep:
  Sugestion: have the files like this
  ```
    c:\folder_example\
      Django\
      LES-EventManager\
  ```

  Where Django contains the django install and LES-EventManager contains this rep

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
4º: add a super user
```
    c:\folder_example> Django\Scripts\activate.bat
    
    (Django) c:\folder_example> cd LES-EventManager\EventManager\
    
    (Django) c:\folder_example\LES-EventManager\EventManager> python manage.py createsuperuser
```
  put the credetials that you want

5º: dar load dos valores default

```
  python manage.py loaddata fixtures.json
```

6º: run the server
```    
    c:\folder_example> Django\Scripts\activate.bat
    
    (Django) c:\folder_example> cd LES-EventManager\EventManager\
    
    (Django) c:\folder_example\LES-EventManager\EventManager> python manage.py runserver
```
 should be working fine
    


