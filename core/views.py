from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Prova, Materia
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
    materias = Materia.objects.filter(prova_fk = id)
    
    return render(request, 'core/ver_prova.html', {
        'model': model,
        'materias': materias
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

def cgm(request):
    
    prova = Prova()
    totais = prova.obterTotais()
    
    return render(request, 'core/main.html', {
        "prova": prova,
        "totais": totais
    })