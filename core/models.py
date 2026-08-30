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

    def obterTotais(self, provaId=None, materiaNome=None, totalOnly=False):
        
        id = self.id if provaId is None else provaId
        
        materias = Materia.objects.filter(prova_fk=id).prefetch_related('questao_set')

        totais = {}

        total_acertos = 0
        total_questoes = 0
        
        if materiaNome:
            pass

        for materia in materias:

            questoes = materia.questao_set.all()

            acertos = questoes.filter(valor=True).count()
            quantidade = questoes.count()

            totais[materia.nome] = {
                'acertos': acertos,
                'total': quantidade,
            }

            total_acertos += acertos
            total_questoes += quantidade

        totais['total'] = {
            'acertos': total_acertos,
            'total': total_questoes,
        }
        
        self.total_percentual = round(total_acertos * 100 / total_questoes)
        self.totais = totais

        return totais
    
class Materia(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    prova_fk = models.ForeignKey(Prova, on_delete=models.CASCADE)
    
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
    
    class Meta:
        db_table = 'questao'