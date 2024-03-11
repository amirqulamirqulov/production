from django.db import models



class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Material(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product_Materials(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    material_qty = models.FloatField()


class Warehouse(models.Model):
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    remainder = models.IntegerField()
    price = models.IntegerField()

    def __str__(self) -> str:
        return self.material_id.name




