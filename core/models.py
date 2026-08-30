from django.db import models

class Prova(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    data = models.DateField()
    link_prova = models.CharField(max_length=255, null=True)
    link_gabarito = models.CharField(max_length=255, null=True)
    
    class Meta:
        db_table = 'prova'
    
    @property
    def obterQuestoes(self):
        materias = Materia.objects.filter(prova_fk=self.id).prefetch_related('questao_set')
        
        materias_itens = {}
        
        for materia in materias:
            materias_itens[materia.nome] = materia.questao_set.all()
            
        return materias_itens
    
    def obterTotais(self):
        materias = Materia.objects.filter(prova_fk=self.id).prefetch_related('questao_set')
        totais = {}

        total_acertos = 0
        total_questoes = 0

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