from .models import *
from django import forms
from django.forms import ModelForm


class ContactForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets={
                   "name":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "pais":forms.Select(attrs={'class': "form-control form-control-sm"}),
                   "canal":forms.Select(attrs={'class': "form-control form-control-sm"}),
                   "phone":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "email":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                }  

class Form(forms.ModelForm):
    se_le_pago = forms.BooleanField(label="Pagado al profe", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.all().order_by('-date_created')
    class Meta:
        model = Order
        fields = '__all__'
        widgets={                   
                   "customer":forms.Select(attrs={'class': "form-control form-control-sm"}),
                   "tipo_servicio":forms.Select(attrs={'class': "form-control form-control-sm"}),
                   "cost_local": forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
                   "cost": forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
                   "profe_asignado":forms.Select(attrs={'class': "form-control form-control-sm"}),
                   "cost_profe": forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
                   "comision_profe": forms.NumberInput(attrs={'class': 'form-control form-control-sm','required': False}),
                   "fecha_entrega":forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
                   "hora_clase_inicial": forms.TimeInput(attrs={'class': 'form-control form-control-sm', 'type': 'time'}),
                   "hora_clase_final": forms.TimeInput(attrs={'class': 'form-control form-control-sm', 'type': 'time'}),
                   "status": forms.Select(attrs={'class': "form-control form-control-sm"}),

                } 
        labels={
                     "fecha_entrega": "Fecha de entrega",
                     "customer":"Cliente",
                     "cost_local": "Precio Moneda local",
                     "cost":"Precio en USD",
                     "cost_profe":"Monto de ganancia al Profe USD",
                     "comision_profe": "(%) de ganancia al profe (si Monto anterior es vacio, del 1 al 100)",
                } 
       


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets={
                   "name":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "pais":forms.Select(attrs={'class': "form-control form-control-sm"}),
                   "especialidad":forms.Select(attrs={'class': "form-control form-control-sm"}),
                } 

        
        