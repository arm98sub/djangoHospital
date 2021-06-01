from django.db import models


class Articulo(models.Model):

    clave = models.CharField("Clave", max_length=30)
    nombre = models.CharField("Artícuclo", max_length=150)
    descripcion = models.CharField("Descripción", max_length=300, blank=True, null=True)
    imagen = models.ImageField("Imagen", upload_to="articulos")
    precio = models.DecimalField("Precio", max_digits=8, decimal_places=2)
    stock = models.IntegerField("Unidades")
    categoria = models.ForeignKey("articulos.Categoria", verbose_name="Categoría", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField("Categoria", max_length=150)

    def __str__(self):
        return self.nombre


class Venta(models.Model):
	fecha = models.DateField(auto_now_add=True)
	detalle_venta = models.ForeignKey('articulos.DetalleVenta',verbose_name='DetalleVenta',on_delete=models.CASCADE, null=True)

	def __str__(self):
		return str(self.fecha)

class DetalleVenta(models.Model):
	cantidad = models.IntegerField('Articulos vendidos', null=True)
	total = models.DecimalField('Total Venta', max_digits=10, decimal_places=2, null=True)