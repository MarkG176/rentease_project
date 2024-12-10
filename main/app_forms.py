from django import forms
from main.models import Tenants,Incidents

GENDER_CHOICES = {"Male": "Male", "Female": "Female"}
class TenantForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = Tenants
        fields = ['name', 'email', 'phone', 'adm_no']

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incidents
        fields = ['tenant_name', 'lot_no', 'description', 'is_utility', 'is_social']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

