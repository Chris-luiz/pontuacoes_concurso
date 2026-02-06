from django import forms
from .models import Prova, Materia, Questao

class ProvaForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'input mb-4'}))
        
    data = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'input mb-4'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
    )
        
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
    numero = forms.CharField(widget=forms.TextInput(attrs={'class': 'input mb-4'}))
    valor = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox mb-4'}), required=False)
    
    class Meta:
        model = Questao
        fields = '__all__'
        exclude = ['materia_fk']