from django import forms
from django.forms import fields
from .models import Cliente,Servicio
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import PrependedText

class ClienteForm(forms.ModelForm):
    
    class Meta:
        model = Servicio
        fields= '__all__'
        labels = ''
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].label=''
            self.fields[str(field)].widget.attrs.update({"placeholder":str(field)})
            
        """self.helper = FormHelper()
        self.helper.layout = Layout(
                Fieldset(
                "name","price"
            ),
                PrependedText('name', '@', placeholder="username")
          
        )
        """
