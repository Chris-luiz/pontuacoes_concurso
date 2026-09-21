from django.db import models

class Prova(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    data = models.DateField()
    link_prova = models.CharField(max_length=1024, null=True)
    link_gabarito = models.CharField(max_length=1024, null=True)
    
    class Meta:
        db_table = 'prova'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.id:
            self.obterTotais()
            
    def obterTodasQuestoes(self, provaId=None):
        id = self.id if provaId is None else provaId
        
        return Questao.objects.filter(materia_fk__prova_fk=id)

    def obterTotais(self, provaId=None, materiaNome=None, totalOnly=False):
        
        id = self.id if provaId is None else provaId
        
        materias = Materia.objects.filter(prova_fk=id).prefetch_related('questao_set')

        totais = {}

        total_acertos = 0
        total_questoes = 0
        notaFinal = 0
        notaFinalPossivel = 0
        
        if materiaNome:
            pass

        todasQuestoes = self.obterTodasQuestoes()
        
        # Faz o calculo de todas as pontuações e métricas
        for questao in todasQuestoes:
            notaFinal += (1 * questao.peso) if questao.valor == True else 0
            notaFinalPossivel += (1 * questao.peso)
            total_questoes += 1
            total_acertos += 1 if questao.valor == True else 0
        
        for materia in materias:

            questoes = materia.questao_set.all()

            acertos = questoes.filter(valor=True).count()
            quantidade = questoes.count()
            
            notaObtida = questoes.filter(valor=True).aggregate(
                total=models.Sum(1 * models.F('peso'))
            )['total'] or 0

            totais[materia.nome] = {
                'notaObtida': notaObtida,
                'acertos': acertos,
                'total': quantidade,
            }

        if total_questoes == 0:
            self.total_percentual = 0 
            self.totais = 0
            self.total_acertos = 0
            self.total_questoes = 0
            self.notaFinal = 0
            self.notaFinalPossivel = 0
        else: 
            total_percentual = round(total_acertos * 100 / total_questoes)
            self.total_percentual = total_percentual 
            self.totais = totais
            self.total_acertos = total_acertos
            self.total_questoes = total_questoes
            self.notaFinal = notaFinal
            self.notaFinalPossivel = notaFinalPossivel

        return {
            'totais': totais,
            'totalAcertos': total_acertos,
            'totalQuestoes': total_questoes,
            'notaFinal': notaFinal,
            'notaTotal': notaFinalPossivel,
            'total_percentual': total_percentual,
        }
    
class Materia(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    prova_fk = models.ForeignKey(Prova, on_delete=models.CASCADE)
    ordem = models.IntegerField(null=True)
    
    def getPontuacao(self):
        questoes = self.questao_set.all()
        
        acertos = questoes.filter(valor=True).count()
        quantidade = questoes.count()
        notaTotal =  questoes.aggregate(
            total=models.Sum(1 * models.F('peso'))
        )['total']
        notaObtida = questoes.filter(valor=True).aggregate(
                    total=models.Sum(1 * models.F('peso'))
                )['total'] or 0
        
        return {
            'notaTotal': notaTotal,
            'notaObtida': notaObtida,
            'acertos': acertos,
            'quantidade': quantidade,
            'percentual': round(acertos * 100 / quantidade) if quantidade else 0
        }
    
    class Meta: 
        db_table = 'materia'

class Questao(models.Model):
    OPCOES_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    numero = models.CharField(max_length=2)
    valor = models.BooleanField()
    materia_fk = models.ForeignKey(Materia, on_delete=models.CASCADE)
    resposta_correta = models.CharField(max_length=1, choices=OPCOES_CHOICES, null=True)
    resposta_inserida = models.CharField(max_length=1, choices=OPCOES_CHOICES, null=True)
    peso = models.FloatField(null=False, default=1)
    anulada = models.BooleanField(null=False, default=False)
    
    class Meta:
        db_table = 'questao'