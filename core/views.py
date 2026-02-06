from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Prova, Materia, Questao
from .forms import ProvaForm, MateriaForm, QuestaoForm

def provas(request):
    
    provas = Prova.objects.all()
    
    return render(request, 'core/provas.html', {
        'provas': provas
    })
    
def criarProva(request):
    
    form = ProvaForm()
    
    if request.method == "POST":
        form = ProvaForm(request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/provas")
    
    return render(request, 'core/criar_prova.html', {
        'model': form
    })

def editarProva(request, id):
    
    model = Prova.objects.filter(id=id).first()
    
    if request.method == 'POST':
        form = ProvaForm(request.POST, instance=model)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return HttpResponseRedirect(f"/provas")
    else:
        form = ProvaForm(instance=model)
    
    return render(request, 'core/editar_prova.html', {
        "form": form,
        "prova": model,
    })
    
    
    
def verProva(request, id):
    
    model = Prova.objects.filter(id = id).first()
    materias = Materia.objects.filter(prova_fk=id).prefetch_related('questao_set')
    totais = model.obterTotais()
    
    return render(request, 'core/ver_prova.html', {
        'model': model,
        'materias': materias,
        'totais': totais
    })
    
def criarMateria(request, id):
    
    prova = Prova.objects.filter(id=id).first()
    form = MateriaForm()
    
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        
        if form.is_valid():
            form = form.save(commit=False)
            form.prova_fk_id = id
            form.save()
            return HttpResponseRedirect(f'/provas/ver/{id}')
    
    return render(request, 'core/criar_materia.html', {
        'form': form,
        'prova': prova,
    })
    
    
def carga(request):
 
    prova = Prova.objects.filter(nome="CGM").first()
    
    provaModel = Prova()
    
    
    for key, item in provaModel.QUESTOES.items():
        
        materiaModel = Materia()
        materiaModel.nome = key
        materiaModel.prova_fk_id = prova.id
        materiaModel.save()
        
        for numero, valor in item.items():
            questao = Questao()
            questao.numero = numero
            questao.valor = valor
            questao.materia_fk_id = materiaModel.id
            questao.save()        

    return HttpResponse('Funcionou')
    
       
    
def cgm(request):
    
    prova = Prova()
    totais = prova.obterTotais()
    
    return render(request, 'core/main.html', {
        "prova": prova,
        "totais": totais
    })
    


def verMateria(request, provaId):
    
    prova = Prova.objects.filter(id=provaId).first()
    materias = Materia.objects.filter(prova_fk=provaId).all()
    
    return render(request, 'core/ver_materia.html', {
        "prova": prova,
        "materias": materias
    })
    
def editarMateria(request, id):
    model = Materia.objects.get(id=id)

    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=model)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.prova_fk = model.prova_fk
            materia.save()
            return HttpResponseRedirect(f"/provas/ver_materias/{materia.prova_fk_id}")
    else:
        form = MateriaForm(instance=model)

    return render(request, 'core/editar_materia.html', {
        "form": form,
        "model": model
    })
    
def excluirMateria(request, id):
    
    model = Materia.objects.filter(id=id).first()
    model.delete()
    
    return HttpResponseRedirect(f"/provas/ver_materias/{model.prova_fk_id}")
    
    
def verQuestao(request, materiaId):
    materia = Materia.objects.filter(id=materiaId).first()
    questoes = Questao.objects.filter(materia_fk=materiaId).all()
    
    return render(request, 'core/ver_questoes.html', {
        "materia": materia,
        "questoes": questoes
    })
    
def adicionarQuestao(request, materiaId):
    
    form = QuestaoForm()
    
    if request.method == 'POST':
        form = QuestaoForm(data=request.POST)
        
        if form.is_valid():
            form = form.save(commit=False)
            form.materia_fk_id = materiaId
            form.save()
            return HttpResponseRedirect(f"/provas/ver_questoes/{form.materia_fk_id}")
        
    
    return render(request, 'core/criar_questao.html', {
        "form": form
    })

def editarQuestao(request, id):
    model = Questao.objects.get(id=id)

    if request.method == 'POST':
        form = QuestaoForm(request.POST, instance=model)
        if form.is_valid():
            form = form.save(commit=False)
            form.materia_fk_id = model.materia_fk_id
            form.save()
            return HttpResponseRedirect(f"/provas/ver_questoes/{form.materia_fk_id}")
    else:
        form = QuestaoForm(instance=model)

    return render(request, 'core/editar_questao.html', {
        "form": form,
        "model": model
    })

def excluirQuestao(request, id):
    model = Questao.objects.filter(id=id).first()
    model.delete()
    
    return HttpResponseRedirect(f"/provas/ver_questoes/{model.materia_fk_id}")
