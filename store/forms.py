from django import forms
from .models import Contact



class ContactForm(forms.ModelForm):

    class Meta:
        model =Contact
        fields = ['name','email']

        widgets = {
            'name': forms.TextInput(),#attrs={'class': 'form-control'}
            'email': forms.EmailInput()
        }
    """
    name = forms.CharField(
        label='Nom',
        max_length=30,
        widget=forms.TextInput(attrs={}),
        required=True 
    )


    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={}),
        required=True)
    """