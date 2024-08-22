from .models import homes
from django.forms import ModelForm, TextInput

class homeForm(ModelForm):
    class Meta:
        model = homes
        fields = ["apart", "flats", "office"]
        widgets = { 
            "apart":TextInput(attrs={  
                "class":"form-control",
                "placeholder":"enter the name",
                "type":"number",
            }),
            "flats":TextInput(attrs={  
                "class":"form-control",
                "type":"number",
            }),
            "office":TextInput(attrs={
                "class":"form-control",
                "placeholder":"enter the description",
                "type":"number",
            }),
        }
