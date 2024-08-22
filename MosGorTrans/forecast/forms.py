from .models import homes
from django.forms import ModelForm, TextInput

class homeForm(ModelForm):
    class Meta:
        model = homes
        fields = ["apart", "flats", "office"]
        widgets = { 
            "apart":TextInput(attrs={  
                "class":"form-control",
                "placeholder":"м²",
                "type":"number",
                "text-align":"center",

            }),
            "flats":TextInput(attrs={  
                "class":"form-control",
                "placeholder":"м²",
                "type":"number",
                "text-align":"center",
            }),
            "office":TextInput(attrs={
                "class":"form-control",
                "placeholder":"м²",
                "type":"number",
                "text-align":"center",

            }),
        }
