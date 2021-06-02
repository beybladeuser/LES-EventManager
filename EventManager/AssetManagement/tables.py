import django_tables2 as django_tables
from utilizadores.models import Administrador, Utilizador
from django.utils.html import format_html
from django.urls import reverse

class formsTable(django_tables.Table) :
	Nome_Recurso = django_tables.Column("Nome")
	Quantidade = django_tables.Column('Email')	
	Tipo = django_tables.Column('Tipo', attrs={"th": {"width": "130"}})
	Sub_Tipo = django_tables.Column("Sub Tipo")
	
	class Meta:
		model = Utilizador
    	
