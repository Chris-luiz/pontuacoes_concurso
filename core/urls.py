"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (
    test,
    index,
    provas, criarProva, verProva, revisarProva, editarProva,
    criarMateria, verMateria, editarMateria, excluirMateria, 
    adicionarQuestao, adicionar_questao_em_lote, verQuestao, editarQuestao, excluirQuestao, alternarValorQuestao,
    gerar_espelho_prova
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test', test),
    path('', index),
    path('provas', provas),
    path('provas/criar/', criarProva),
    path('provas/ver/<int:id>', verProva),
    path('provas/revisar/<int:id>', revisarProva),
    path('provas/editar_prova/<int:id>', editarProva),
   
    path('provas/ver_materias/<int:provaId>', verMateria),
    path('provas/criar-materia/<int:id>', criarMateria),
    path('provas/editar_materia/<int:id>', editarMateria),
    path('provas/excluir_materia/<int:id>', excluirMateria),
    
    path('provas/adicionar_questao/<int:materiaId>', adicionarQuestao),
    path('provas/adicionar_questao_em_lote/<int:materiaId>', adicionar_questao_em_lote),
    path('provas/ver_questoes/<int:materiaId>', verQuestao),
    path('provas/editar_questao/<int:id>', editarQuestao),
    path('provas/alternar_valor_questao/<int:id>', alternarValorQuestao),
    path('provas/excluir_questao/<int:id>', excluirQuestao),
    
    path("provas/pdf/<int:id>/", gerar_espelho_prova),
]
