from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Prova, Materia, Questao
from .forms import ProvaForm, MateriaForm, QuestaoForm, QuestaoLoteForm
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)

def index(request):
    return HttpResponseRedirect("/provas")

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
   
def revisarProva(request, id):

    model = Prova.objects.filter(id=id).first()
    materias = Materia.objects.filter(prova_fk=id).prefetch_related('questao_set')
    
    if request.method == 'POST':
        print(request.POST)
        for materia in materias:
            print(materia)
            for questao in materia.questao_set.all():
                print(questao)
                resposta_correta = request.POST.get(f'resposta_correta_{questao.id}')
                resposta_inserida = request.POST.get(f'resposta_inserida_{questao.id}')
                
                print(resposta_correta)
                print(resposta_inserida)
                
                if resposta_correta:
                    questao.resposta_correta = resposta_correta
                
                if resposta_inserida:
                    questao.resposta_inserida = resposta_inserida
                
                if questao.resposta_correta and questao.resposta_inserida:
                    questao.valor = questao.resposta_correta == questao.resposta_inserida
                
                questao.save()
                
        return HttpResponseRedirect(f'/provas/ver/{id}')

    return render(request, 'core/revisar.html', {
        'model': model,
        'materias': materias,
        'opcoes': Questao.OPCOES_CHOICES,
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
    model = Materia.objects.filter(id=materiaId).first()
    
    if request.method == 'POST':
        form = QuestaoForm(data=request.POST)
            
        if form.is_valid():
            model = form.save(commit=False)
            model.materia_fk_id = materiaId
            model.save()
            return HttpResponseRedirect(f"/provas/ver_questoes/{materiaId}")
        
    return render(request, 'core/criar_questao.html', {
        "form": form,
        "model": model,
    })

def adicionar_questao_em_lote(request, materiaId):
    model = Materia.objects.filter(id=materiaId).first()
    
    if request.method == 'POST':
        form = QuestaoLoteForm(data=request.POST)
            
        if form.is_valid():
            de = form.cleaned_data['de']
            ate = form.cleaned_data['ate']
            
            for i in range(de, ate+1):
                model = form.save(commit=False)
                model.pk = None
                model.numero = i
                model.materia_fk_id = materiaId
                model.save()
                
            return HttpResponseRedirect(f"/provas/ver_questoes/{materiaId}")
        
        print(form.errors)
    else:
        form = QuestaoLoteForm()
    
    return render(request, 'core/criar_questao_em_lote.html', {
        "form": form,
        "model": model,
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

def alternarValorQuestao(request, id):
    
    if not id:
        return JsonResponse({
            "status": False
        })
        
    questao = Questao.objects.filter(id=id).first()
    if not questao:
        return JsonResponse({
            "status": False
        })
        
    questao.valor = False if questao.valor else True
    questao.save()
    
    return JsonResponse({
        "status": True,
        "questaoId": questao.id,
        "valor": questao.valor
    })

def excluirQuestao(request, id):
    model = Questao.objects.filter(id=id).first()
    model.delete()
    
    return HttpResponseRedirect(f"/provas/ver_questoes/{model.materia_fk_id}")

def gerar_espelho_prova(request, id):
    prova = get_object_or_404(Prova, id=id)

    materias = Materia.objects.filter(
        prova_fk=id
    ).prefetch_related('questao_set')

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()

    elementos = []

    # -----------------------------------
    # TÍTULO
    # -----------------------------------

    elementos.append(Paragraph(f"Prova: {prova.nome}", styles["Title"]))

    elementos.append(Spacer(1, 0.5 * cm))

    # -----------------------------------
    # INFORMAÇÕES DA PROVA
    # -----------------------------------

    data_prova = prova.data.strftime("%d/%m/%Y")

    dados_prova = [
        ["Nome da prova", prova.nome],
        ["Data da prova", data_prova],
        ["Link da prova", prova.link_prova or "Não informado"],
        ["Link do gabarito", prova.link_gabarito or "Não informado"],
    ]

    tabela_prova = Table(dados_prova, colWidths=[4 * cm, 13 * cm])

    tabela_prova.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    elementos.append(tabela_prova)

    elementos.append(Spacer(1, 0.8 * cm))

    # -----------------------------------
    # TABELA DE QUESTÕES
    # -----------------------------------

    elementos.append(Paragraph("Questões",styles["Heading2"]))

    elementos.append(Spacer(1, 0.3 * cm))

    dados_questoes = [
        [
            "Questão",
            "Resposta",
            "Resposta do candidato",
            "Acertou",
        ]
    ]

    for materia in materias:

        for questao in materia.questao_set.all():

            resposta_correta = (questao.resposta_correta or "-")

            resposta_candidato = (questao.resposta_inserida or "-")

            acertou = "SIM" if questao.valor else "NÃO"

            dados_questoes.append([
                str(questao.numero),
                resposta_correta,
                resposta_candidato,
                acertou,
            ])

    tabela_questoes = Table(
        dados_questoes,
        colWidths=[
            2.5 * cm,
            4 * cm,
            6 * cm,
            3 * cm,
        ],
        repeatRows=1,
    )

    tabela_questoes.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ])
    )

    elementos.append(tabela_questoes)
    
    totais = prova.obterTotais()
    acertos = totais['total']['acertos']
    total = totais['total']['total']

    elementos.append(Paragraph(f"Total: {acertos}/{total}"))

    # -----------------------------------
    # GERAR PDF
    # -----------------------------------

    documento.build(elementos)

    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")

    response["Content-Disposition"] = (f'inline; filename="prova_{prova.id}.pdf"')

    return response