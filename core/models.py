from django.db import models

class Prova(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    data = models.DateField()
    
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
        total = {}
        for key, questao in self.obterQuestoes.items():
            total[key] = questao.filter(valor=True).count()

        total['total'] = sum(total.values())
        return total
    
    
class Materia(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    prova_fk = models.ForeignKey(Prova, on_delete=models.CASCADE)
    
    class Meta: 
        db_table = 'materia'

class Questao(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    numero = models.CharField(max_length=2)
    valor = models.BooleanField()
    materia_fk = models.ForeignKey(Materia, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'questao'