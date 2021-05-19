import django_tables2 as django_tables
from utilizadores.models import Administrador, Utilizador
from django.utils.html import format_html
from django.urls import reverse

class formsTable(django_tables.Table) :
	nome = django_tables.Column(empty_values=(), order_by=("first_name", "last_name"))
	email = django_tables.Column('Email')	
	valido = django_tables.Column('Estado', attrs={"th": {"width": "130"}})
	tipo = django_tables.Column(accessor='firstProfile', orderable=False)
	acoes = django_tables.Column('Ações', empty_values=(),orderable=False, attrs={"th": {"width": "150"}})

	class Meta:
		model = Utilizador
    	