from django.shortcuts import render, redirect
from .models import Customer, Product, Order, Pago,TipoCambio
from .filters import ProductFilter
from .forms import Form, ProductForm, ContactForm
from django.db.models import Count, Q, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal, ROUND_DOWN
from datetime import datetime, date
from twilio.rest import Client
from django.http import JsonResponse
from .config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER


def enviar_mensaje_whatsapp(request, phone, tipo_servicio, fecha_entrega, mensaje_personalizado=None):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    phone_number = TWILIO_PHONE_NUMBER
    client = Client(account_sid, auth_token)

    # Consultar el nombre del profesor a partir del teléfono
    try:
        profe = Product.objects.get(phone=phone)
        nombre_profesor = profe.name
    except Product.DoesNotExist:
        nombre_profesor = 'Profesor desconocido'

    if mensaje_personalizado:
        mensaje = mensaje_personalizado
    else:
        mensaje = f'Hola {nombre_profesor}, tienes un servicio de "{tipo_servicio}" programado para el {fecha_entrega}. Le recordamos entregar las tareas o iniciar clases a tiempo.'

    try:
        message = client.messages.create(
            from_='whatsapp:{phone_number}',
            body=mensaje,
            to=f'whatsapp:{phone}'
        )
        # El mensaje se envió correctamente
        response_data = {
            'success': True,
            'message': 'Mensaje enviado exitosamente.'
        }
    except Exception as e:
        # Ocurrió un error al enviar el mensaje
        response_data = {
            'success': False,
            'message': f'Error al enviar el mensaje: {str(e)}'
        }

    # Devolver una respuesta JSON
    return JsonResponse(response_data)

@login_required
def dashboard(request):

    # Obtener la fecha actual
    today = date.today()
    # Obtener la fecha actual (mes actual)
    Fecha_mes_actual = timezone.now()

    # Calcular el total de órdenes durante el mes actual
    total_orders_mes_actual = Order.objects.filter(date_created__year=today.year, date_created__month=today.month).count()

    # Calcular el total de ingresos durante el mes actual
    total_ingresos_mes_actual = Order.objects.filter(date_created__year=today.year, date_created__month=today.month).aggregate(Sum('cost'))['cost__sum'] or 0

    # Calcular el total de ingreso de "Tuprofeestadistica" (cost - cost_profe)
    total_ingresos_tuprofeestadistica = Order.objects.filter(date_created__year=today.year, date_created__month=today.month).aggregate(Sum('cost_profe'))['cost_profe__sum'] or 0

    # Calcular el total de órdenes por entregar hoy y en fechas posteriores
    total_orders_por_entregar = Order.objects.filter(fecha_entrega__gte=today).count()

    orders = Order.objects.all()
    orders_label = set()
    for o in orders:
        orders_label.add(o.profe_asignado)
    orders_group = list(Order.objects.values('profe_asignado').annotate(dcount=Count('profe_asignado')))
    og = []
    for o in orders_group:
        og.append(o["dcount"])
    total_orders = orders.count()
    recent_orders = orders.order_by('-fecha_entrega')[:10]
    context = {
        'orders': orders,
        'orders_label': orders_label,
        'products': products,
        'total_orders': total_orders,
        'total_orders_mes_actual': total_orders_mes_actual,
        'total_ingresos_mes_actual': total_ingresos_mes_actual,
        'total_ingresos_tuprofeestadistica': total_ingresos_tuprofeestadistica,
        'total_orders_por_entregar': total_orders_por_entregar,
        'recent_orders': recent_orders,
        'og': og,
        'Fecha_mes_actual':Fecha_mes_actual,
    }

    #context  = {'orders': orders, 'orders_label': orders_label, 'products': products,
    #'total_orders':total_orders, 'recent_orders':recent_orders,'og':og}
    return render(request,'crm/dashboard.html', context)

def enviar_mensaje_personalizado(request, phone, mensaje_personalizado):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    phone_number = TWILIO_PHONE_NUMBER
    client = Client(account_sid, auth_token)

    # Consultar el nombre del profesor a partir del teléfono
    try:
        profe = Product.objects.get(phone=phone)
        nombre_profesor = profe.name
    except Product.DoesNotExist:
        nombre_profesor = 'Profesor desconocido'

    mensaje = mensaje_personalizado

    try:
        message = client.messages.create(
            from_='whatsapp:{phone_number}',
            body=mensaje,
            to=f'whatsapp:{phone}'
        )
        # El mensaje se envió correctamente
        response_data = {
            'success': True,
            'message': 'Mensaje personalizado enviado exitosamente.'
        }
    except Exception as e:
        # Ocurrió un error al enviar el mensaje
        response_data = {
            'success': False,
            'message': f'Error al enviar el mensaje personalizado: {str(e)}'
        }

    # Devolver una respuesta JSON
    return JsonResponse(response_data)

@login_required
def products(request):
    products = Product.objects.all()
    pf = ProductFilter(request.GET, queryset=products)
    products = pf.qs
    return render(request,'crm/products.html',{'products':products,'pf':pf})

@login_required
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('/products')
    context = {'form': form}
    return render(request,'crm/form_page.html',context)

@login_required
def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products')
    context = {'form':form}
    return render(request,'crm/form_page.html', context)

@login_required
def orders(request):
    orders = Order.objects.order_by("-date_created")
    return render(request,'crm/orders.html',{'orders':orders})

@login_required
def contacts(request):
    req = request.GET.get('search',None)
    if req is not None:
        query = request.GET.get('search')
        customers = Customer.objects.filter(Q(name__icontains=query) | Q(email__icontains=query)
        | Q(phone__icontains=query))
    else:
        customers = Customer.objects.all()
    return render(request,'crm/contacts.html',{'customers':customers})

@login_required
def add_contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/contacts')
    context = {'form':form}
    return render(request,"crm/form_page.html",context)

@login_required
def update_contact(request, pk):
    contact = Customer.objects.get(id=pk)
    form = ContactForm(instance=contact)
    if request.method == 'POST':
        form = ContactForm(request.POST,instance=contact)
        if form.is_valid():
            form.save()
            return redirect('/contacts')
    context = {'form': form}
    return render(request,'crm/form_page.html',context)

@login_required
def delete_contact(request, pk):
    contact = Customer.objects.get(id=pk)
    contact.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def customer_orders(request, pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()
    total_orders = order.count()
    context = {'customer':customer,'order':order, 'total_orders':total_orders}
    return render(request,'crm/customer_orders.html', context)

@login_required
def create_order(request):
    form = Form()
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            form.save()

            # Obtener la información de la nueva orden
            tipo_servicio = form.cleaned_data['tipo_servicio']
            fecha_entrega = form.cleaned_data['fecha_entrega']
            profe_asignado = form.cleaned_data['profe_asignado']

            # Construir el mensaje personalizado
            mensaje_personalizado = f'Hola {profe_asignado.name}, se confirmó el servicio de "{tipo_servicio}" para el cliente {form.cleaned_data["customer"].name} el día {fecha_entrega}.'
            if tipo_servicio == 'clases' and form.cleaned_data['hora_clase_inicial']:
                mensaje_personalizado += f' La hora de inicio es {form.cleaned_data["hora_clase_inicial"].strftime("%H:%M")}.'

             # Llamar a la función enviar_mensaje_personalizado con los datos del formulario
            enviar_mensaje_personalizado(
                request,
                phone=profe_asignado.phone,
                mensaje_personalizado=mensaje_personalizado
            )

            return redirect('/orders')
    context = {'form': form}
    return render(request, 'crm/form_page.html', context)


@login_required
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = Form(instance=order)
    if request.method == 'POST':
        form = Form(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/orders')
    context = {'form': form}
    return render(request,'crm/form_page.html',context)
    
@login_required
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def nomina(request):
    # Obtener la fecha actual y la fecha de hace una semana (restar un día a la fecha actual)
    today = timezone.now() - timezone.timedelta(days=1)
    last_week = today - timezone.timedelta(days=6)

    # Obtener todas las órdenes con status "Cobrado", no pagadas y con fecha de entrega dentro del rango de la última semana
    orders = Order.objects.filter(se_le_pago=False, status='COBRADO', fecha_entrega__gte=last_week, fecha_entrega__lte=today)

    # Crear un diccionario para almacenar el total a cobrar por cada profesor
    total_por_profesor = {}

    ## Calcular el total a cobrar para cada profesor y el monto en moneda local
    for order in orders:
        profe_asignado = order.profe_asignado
        if profe_asignado not in total_por_profesor:
            total_por_profesor[profe_asignado] = {
                'total': Decimal('0'),
                'tipo_cambio': Decimal('0'),
                'monto_local': Decimal('0'),
            }
            
        total_por_profesor[profe_asignado]['total'] += order.cost_profe

        # Obtener el tipo de cambio para el país del profesor y la fecha actual
        tipo_cambio_obj = TipoCambio.objects.filter(pais=profe_asignado.pais).latest('date_created')
        #tipo_cambio_obj = TipoCambio.objects.filter(pais=profe_asignado.pais, date_created__lte=today).latest('date_created')
        tipo_cambio = tipo_cambio_obj.tipo_cambio
        total_por_profesor[profe_asignado]['tipo_cambio'] = tipo_cambio
        total_por_profesor[profe_asignado]['monto_local'] = total_por_profesor[profe_asignado]['total'] * tipo_cambio

        # Ajustar la representación de los valores para mostrar solo dos decimales si es necesario
        total_por_profesor[profe_asignado]['total'] = total_por_profesor[profe_asignado]['total'].quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        total_por_profesor[profe_asignado]['monto_local'] = total_por_profesor[profe_asignado]['monto_local'].quantize(Decimal('0.01'), rounding=ROUND_DOWN)

    orders_por_profesor = {}

    for profe in total_por_profesor.keys():
        orders_por_profesor[profe] = Order.objects.filter(profe_asignado=profe, fecha_entrega__range=(last_week, today))

    # Obtener el tipo de cambio actual para mostrarlo en el formulario
    tipo_cambio_actual = TipoCambio.objects.filter(date_created__lte=timezone.now()).latest('date_created')

    # Renderizar la plantilla con la información de la nómina
    context = {
        'total_por_profesor': total_por_profesor,
        'today': today,
        'last_week': last_week,
        'orders_por_profesor': orders_por_profesor,
        'tipo_cambio_actual': tipo_cambio_actual,
    }
    return render(request, 'crm/nomina.html', context)


@login_required
def pagar_nomina(request, profe_id, fecha_inicial, fecha_final):
    # Obtener el profesor y las órdenes no pagadas en el rango de fechas
    profe = Product.objects.get(id=profe_id)
    orders = Order.objects.filter(se_le_pago=False, status='COBRADO',profe_asignado=profe, fecha_entrega__range=(fecha_inicial, fecha_final))

    # Calcular el total a pagar
    total = sum(order.cost_profe for order in orders)

    # Obtener el tipo de cambio para el país del profesor y la fecha actual
    tipo_cambio_obj = TipoCambio.objects.filter(pais=profe.pais, date_created__lte=timezone.now()).latest('date_created')
    tipo_cambio = tipo_cambio_obj.tipo_cambio
    monto_local = round(total * tipo_cambio, 2)

    # Marcar todas las órdenes como pagadas
    for order in orders:
        order.se_le_pago = True
        order.save()

    # Registrar el pago en la nueva tabla
    pago = Pago.objects.create(profe=profe, monto=total, monto_local=monto_local, tipo_cambio=tipo_cambio)

     # Construir el mensaje personalizado
    mensaje_personalizado = f'Hola {profe.name}, se realizó un pago de {total:.2f}$ para las tareas/clases entre el {fecha_inicial} y el {fecha_final}. El monto en Bs a recibir es {monto_local:.2f}, (tipo de cambio: {tipo_cambio}). Gracias por tu trabajo.'

    # Llamar a la función enviar_mensaje_personalizado con los datos del mensaje
    enviar_mensaje_personalizado(request, phone=profe.phone, mensaje_personalizado=mensaje_personalizado)

    # Redirigir al usuario a la página de la nómina
    return redirect('nomina')





def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,"Username or Password is not correct.")
    return render(request, 'crm/signin.html',{})

def signout(request):
    logout(request)
    return redirect('signin')