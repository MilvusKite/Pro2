from django import forms
from plots.models import Plot

class plotForm(forms.Form):
    which_Level_To_Plot = forms.ChoiceField(choices = (
        ('L1', 'PN'),
        ('L3', 'Chaperome'),
    ),required = True, label = 'Which Level to Plot')
    plot_Title = forms.ModelChoiceField(queryset=Plot.objects.all(),label = 'What to Plot')