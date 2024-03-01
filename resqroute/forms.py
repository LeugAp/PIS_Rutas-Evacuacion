from django import forms
from .models import Staff, Brigade, FunctionsBrigade, Map, Node, Connection
from PIL import Image

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['dni', 'name', 'last_name', 'email', 'phone_number', 'staff_type', 'faculty']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'staff_type': forms.Select(attrs={'class': 'form-select','id': 'id_staff_type'}),
            'faculty': forms.Select(attrs={'class': 'form-select', 'id': 'id_faculty'}),
        }

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)


    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni.isdigit():
            raise forms.ValidationError("Debe contener solo números.")
        if len(dni) != 10:
            raise forms.ValidationError("Debe tener 10 caracteres.")
        
        if Staff.objects.filter(dni=dni).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya está registrado.")
        
        return dni

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@unl.edu.ec'):
            raise forms.ValidationError("Debe ser de dominio 'unl.edu.ec'.")
        
        if Staff.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya está registrado.")
        
        return email
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@unl.edu.ec'):
            raise forms.ValidationError("Debe ser de dominio 'unl.edu.ec'.")
        
        if Staff.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya está registrado.")
        
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError("Debe contener solo números.")
        if len(phone_number) != 9:
            raise forms.ValidationError("Debe tener 9 caracteres.")
        
        if Staff.objects.filter(phone_number=phone_number).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya está registrado.")
        
        return phone_number

class FormBrigade(forms.ModelForm):

    class Meta:
        model = Brigade
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'id': 'name'})

class FormFunctionsBrigade(forms.ModelForm):

    class Meta:
        model = FunctionsBrigade
        fields = ('brigade', 'function')

    def __init__(self, *args, initial_brigade=None,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brigade'].widget.attrs.update({'class': 'form-control visually-hidden', 'id': 'brigade'})
        self.fields['function'].widget.attrs.update({'class': 'form-control', 'id': 'function', 'placeholder': 'Función de la brigada'})

        if initial_brigade:
            self.fields['brigade'].initial = initial_brigade

class MapForm(forms.ModelForm):
    class Meta:
        model = Map
        fields = ['name', 'img']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'img': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Map.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya está registrado.")
        return name

    def clean_img(self):
        img = self.cleaned_data.get('img')
        if img:
            if not img.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise forms.ValidationError("El archivo debe ser una imagen (PNG, JPG, JPEG, GIF).")
        return img

class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ['name', 'latitude', 'longitude', 'is_safe']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.TextInput(attrs={'class': 'form-control'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control'}),
            'is_safe': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Node.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya está registrado.")
        return name

    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        if not isinstance(latitude, float):
            raise forms.ValidationError("Debe ser un número.")
        return latitude

    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')
        if not isinstance(longitude, float):
            raise forms.ValidationError("Debe ser un número.")
        return longitude
    
    def clean_is_safe(self):
        is_safe = self.cleaned_data.get('is_safe')
        if is_safe not in ['s', 'n']:
            raise forms.ValidationError("Solo debe elegir entre 's' o 'n'")
        return is_safe

class FormConnection(forms.ModelForm):
    
    class Meta:
        model = Connection
        fields = ('source', 'destination', 'weight')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].widget.attrs.update({'class': 'form-control', 'id': 'source'})
        self.fields['destination'].widget.attrs.update({'class': 'form-control', 'id': 'destination'})
        self.fields['weight'].widget.attrs.update({'class': 'form-control visually-hidden', 'id': 'weight', 'value': 1})