from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Prova, Materia, Questao
from .forms import ProvaForm, MateriaForm

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
    
    form = MateriaForm()
    
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        
        if form.is_valid():
            form = form.save(commit=False)
            form.prova_fk_id = id
            form.save()
            return HttpResponseRedirect(f'/provas/ver/{id}')
    
    return render(request, 'core/criar_materia.html', {
        'form': form
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