from django import forms

class ConcessionForm(forms.Form):
    code = forms.IntegerField(label='Kod ulgi:')
    discount = forms.IntegerField(label='Wysokość ulgi:', max_value=100, min_value=0)
    name = forms.CharField(label='Nazwa:', max_length=30)

class CardTypeForm(forms.Form):
    name = forms.CharField(label='Nazwa nośnika:', max_length=40)

class DeleteCardTypeForm(forms.Form):
    id = forms.IntegerField(label='ID typu nośnika:')

class DeleteConcessionForm(forms.Form):
    id = forms.IntegerField(label='ID typu ulgi:')