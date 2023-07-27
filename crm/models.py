from django.db import models


class Pais(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    pais = models.ForeignKey(Pais, null=True, on_delete= models.CASCADE)
    canal =  models.CharField(max_length=200, null=True, choices=(
        ('superprof','superprof'),
        ('tusclases','tusclases'),
        ('Apprentus','Apprentus'),
        ('Redes Sociales','Redes Sociales'),
        ('Referido','Referido'),
        ('Web propia','Web propia'),
        ('Directorio local','Directorio local'),
    ))
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class TipoCambio(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tipo_cambio = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ('pais', 'date_created')

class Product(models.Model):
    name=models.CharField(max_length=150,null=True)
    pais = models.ForeignKey(Pais, null=True, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    phone = models.CharField(max_length=200, null=True)
    especialidad = models.CharField(max_length=200, null=True, choices=(
        ('Estadistica','Estadistica'),
        ('Matematica','Matematica'),
        ('Quimica','Quimica'),
        ('Biologia','Biologia'),
        ('Fisica','Fisica'),
        ('Contabilidad','Contabilidad'),
        ('Administracion','Administracion'),
        ('Finanzas','Finanzas'),
        ('Otros','Otros'),
    ))
    
    
    #discount = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    
class Pago(models.Model):
    profe = models.ForeignKey(Product, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    monto_local = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Nuevo campo para el monto en moneda local
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tipo_cambio = models.DecimalField(max_digits=10, decimal_places=4, null=True)

    def save(self, *args, **kwargs):
        # Obtener el último tipo de cambio para el país del profesor
        tipo_cambio = TipoCambio.objects.filter(pais=self.profe.pais).latest('date_created')
        self.tipo_cambio = tipo_cambio.tipo_cambio
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Pago de {self.monto} a {self.profe.name} en {self.fecha}'
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete= models.CASCADE)
    tipo_servicio =  models.CharField(max_length=200, null=True, choices=(
        ('Clases','Clases'),
        ('Tarea','Tarea'),
        ('Examen','Examen'),
        ('Tesis','tesis'),
        ('Proyecto','Proyecto'),
        ('Otros','Otros'),
    ))
    profe_asignado = models.ForeignKey(Product, null=True, on_delete= models.CASCADE)
    cost_local = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    cost =models.DecimalField(max_digits=10, decimal_places=4, null=True)
    cost_profe = models.DecimalField(max_digits=10, decimal_places=4, null=True,blank=True) 
    comision_profe=models.DecimalField(max_digits=10, decimal_places=4, null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    fecha_entrega= models.DateTimeField(null=True)
    hora_clase_inicial= models.TimeField(null=True, blank=True)
    hora_clase_final= models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=200, null=True, choices=(
        ('COBRADO','COBRADO'),
        ('PENDIENTE PAGO','PENDIENTE PAGO'),
        ('DEVOLUCION','DEVOLUCION'),
        ('CANCELADO','CANCELADO'),
    ))
    se_le_pago = models.BooleanField(default=False) 

    def save(self, *args, **kwargs):
        # Realizar el cálculo del campo cost_profe
        if self.cost_profe is None and self.comision_profe is not None:
            self.cost_profe = self.cost * self.comision_profe / 100

        super().save(*args, **kwargs)

