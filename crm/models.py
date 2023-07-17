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
        ('Redes Sociales','Redes Sociales'),
        ('Referido','Referido'),
        ('Web propia','Web propia'),
        ('Directorio local','Directorio local'),
    ))
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    


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
    cost_local = models.FloatField(null=True)
    cost = models.FloatField(null=True)
    cost_profe = models.FloatField(null=True)
    comision_profe=models.FloatField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    fecha_entrega= models.DateTimeField(null=True)
    hora_clase_inicial= models.TimeField(null=True, blank=True)
    hora_clase_final= models.TimeField(null=True, blank=True)
    se_le_pago = models.BooleanField(default=False) 
    status = models.CharField(max_length=200, null=True, choices=(
        ('PAGADO','PAGADO'),
        ('PENDIENTE PAGO','PENDIENTE PAGO'),
        ('DEVOLUCION','DEVOLUCION'),
        ('CANCELADO','CANCELADO'),
    ))
    
    def save(self, *args, **kwargs):
        # Realizar el cálculo del campo cost_profe
        if self.cost_profe is None and self.comision_profe is not None:
            self.cost_profe = self.cost * self.comision_profe / 100

        super().save(*args, **kwargs)
