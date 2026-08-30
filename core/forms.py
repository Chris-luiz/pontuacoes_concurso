from django import forms
from .models import Prova, Materia, Questao

class ProvaForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'input mb-4'}))  
    data = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'input mb-4'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
    )
    link_prova = forms.CharField(widget=forms.TextInput(attrs={'class': 'input mb-4'}))  
    link_gabarito = forms.CharField(widget=forms.TextInput(attrs={'class': 'input mb-4'}))  

    class Meta:
        model = Prova
        fields = '__all__'
        
class MateriaForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'input mb-4'}))
    
    class Meta:
        model = Materia
        fields = '__all__'
        exclude = ['prova_fk']
        
class QuestaoForm(forms.ModelForm):
    OPCOES_CHOICES = [
        ("", "Selecione uma opção"),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]
     
    numero = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'autofocus': True}))
    valor = forms.ChoiceField(widget=forms.RadioSelect, choices=[("True", "Acerto"), ("False", "Erro")], required=True)
    resposta_correta = forms.ChoiceField(widget=forms.Select() , choices=OPCOES_CHOICES,  required=False)
    resposta_inserida = forms.ChoiceField(widget=forms.Select() , choices=OPCOES_CHOICES,  required=False)
    
    class Meta:
        model = Questao
        fields = '__all__'
        exclude = ['materia_fk']
        
    def clean_valor(self):
        return self.cleaned_data['valor'] == 'True'

        
class QuestaoLoteForm(forms.ModelForm):
    valor = forms.ChoiceField(widget=forms.RadioSelect, choices=[("True", "Acerto"), ("False", "Erro")], required=True)
    de = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input'}), required=True)
    ate = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input'}), required=True)
    
    class Meta:
        model = Questao
        fields = '__all__'
        exclude = ['materia_fk', 'numero', 'resposta_correta', 'resposta_inserida']
        
    def clean_valor(self):
        return self.cleaned_data['valor'] == 'True'

