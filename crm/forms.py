from .models import *
from django import forms
from django.forms import ModelForm
from django.db.models import Max
import calendar
from datetime import date

class ContactForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets={
                   "name":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "pais":forms.Select(attrs={'class': "form-control form-control-sm"}),
                   "canal":forms.Select(attrs={'class': "form-control form-control-sm"}),
                   "phone":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "email":forms.TextInput(attrs={'class': "form-control form-control-sm",'required': False}),
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

        
class ReporteIngresosForm(forms.Form):
    # Obtener el año actual
    current_year = date.today().year

    # Obtener los últimos registros de profesores
    profesores = Product.objects.annotate(last_date=Max('order__date_created')).order_by('-last_date')

    profesores_choices = [(None, 'Todos los profesores')] + [(profesor.id, f"{profesor.name} - Último registro: {profesor.last_date}") for profesor in profesores]

    # Opción de filtrado por profesor
    profesor = forms.ChoiceField(choices=profesores_choices, label="Profesor", required=False)

    # Opción de filtrado por mes
    mes = forms.ChoiceField(choices=[(str(i), calendar.month_name[i]) for i in range(1, 13)], label="Mes", required=False)

    # Opción de filtrado por año con valor predeterminado establecido al año actual
    year = forms.ChoiceField(choices=[(str(i), i) for i in range(current_year - 10, current_year + 1)], label="Año", required=False, initial=current_year)

    # Opción de filtrado por fecha personalizada
    fecha_personalizada = forms.BooleanField(label="Fecha personalizada", required=False)

    # Campos de rango de fechas para la opción de fecha personalizada
    fecha_inicial = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}), label="Fecha inicial", required=False)
    fecha_final = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}), label="Fecha final", required=False)

class TipoCambioForm(forms.ModelForm):
    class Meta:
        model = TipoCambio
        fields = ['pais', 'tipo_cambio']