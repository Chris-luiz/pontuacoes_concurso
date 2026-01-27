from django.db import models

class Prova(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    data = models.DateField()
    
    QUESTOES = {
        'Lingua Portuguesa': {
            'Q1': False,
            'Q2': False,
            'Q3': True,
            'Q4': True,
            'Q5': False,
            'Q6': False,
            'Q7': False,
            'Q8': True,
            'Q9': False,
            'Q10': True,
        },

        'Raciocínio Lógico': {
            'Q11': True,
            'Q12': False,
            'Q13': False,
            'Q14': False,
            'Q15': False,
        },

        'Administração Financeira Orçamentária': {
            'Q16': False,
            'Q17': True,
            'Q18': False,
            'Q19': False,
            'Q20': True,
            'Q21': False,
            'Q22': False,
            'Q23': False,
            'Q24': False,
            'Q25': False,
        },

        'Controle Interno e Externo': {
            'Q26': True,
            'Q27': True,
            'Q28': False,
            'Q29': False,
            'Q30': True,
            'Q31': True,
            'Q32': False,
            'Q33': False,
            'Q34': True,
            'Q35': True,
        },

        'Direto Administrativo': {
            'Q36': False,
            'Q37': False,
            'Q38': False,
            'Q39': False,
            'Q40': False,
            'Q41': False,
            'Q42': True,
            'Q43': True,
            'Q44': False,
            'Q45': False,
        },

        'Legislação Municipal': {
            'Q46': True,
            'Q47': True,
            'Q48': True,
            'Q49': False,
            'Q50': True,
        },

        'Conhecimento Específico': {
            'Q51': True,
            'Q52': True,
            'Q53': True,
            'Q54': True,
            'Q55': False,
            'Q56': True,
            'Q57': False,
            'Q58': True,
            'Q59': False,
            'Q60': False,
            'Q61': True,
            'Q62': True,
            'Q63': False,
            'Q64': True,
            'Q65': True,
            'Q66': True,
            'Q67': True,
            'Q68': True,
            'Q69': True,
            'Q70': False,
        },
    }
    
    class Meta:
        db_table = 'prova'
    
    @property
    def obterQuestoes(self):
        return self.QUESTOES
    
    def obterTotais(self):
        total = {}
        
        for key, questoes in self.QUESTOES.items():
            total[key] = list(questoes.values()).count(True)

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