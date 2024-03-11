from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response

# Kiritilgan miqdordagi mahsulotni ishlab chiqarish uchun qancha miqdordagi 
# material kerakligini hisoblaydigan 'product_materials' nomli funksiya tuzamiz.

def products_materials(product_id, quantity):
    products = Product_Materials.objects.filter(product_id=product_id)
    result = {}
    for item in products:
        result[item.material_id.id] = item.material_qty * quantity
    return result

# Malumotlar bazasidagi ma'lumotlarni list ko'rinishiga o'tkazib beradigan 'db_to_list' nomli funksiya tuzamiz.

def db_to_list():
    db_list = []
    database_obj = Warehouse.objects.all()
    for obj in database_obj:
        db_list.append([obj.id, obj.material_id.id, obj.remainder, obj.price])
    return db_list

# Omborxonaga kelgan barcha materiallarning idsini qaytaradigan 'db_material_list' nomli funksiya tuzamiz.

def db_material_list():
    material_list = []
    database_obj = Warehouse.objects.all()
    for obj in database_obj:
        material_list.append(obj.material_id.id)
    return material_list

class HisobotView(APIView):
    def post(self, request):
        natija = []
        db_list = db_to_list()
        for product in request.data:
            product_materials = []
            natija.append(
                {
                    'product_name' : product,
                    'product_quantity' : request.data[product],
                    'product_materials' : product_materials
                }
            )
            product_id = Product.objects.get(name=product).id
            mtlist = products_materials(product_id, request.data[product])
            for key in mtlist:
                for item in db_list:
                    if item[1] == key and item[2] > 0:
                        if item[2] >= mtlist[key]:
                            item[2] = item[2] - mtlist[key]       
                            product_materials.append(
                                {
                                    'warehouse_id': item[0],
                                    'material_name' : Material.objects.get(id=key).name,
                                    'qty': mtlist[key],
                                    'price' : item[3]
                                }
                            )
                            mtlist[key] = 0
                        else:
                            mtlist[key] = mtlist[key] - item[2]
                            
                            product_materials.append(
                                {
                                    'warehouse_id': item[0],
                                    'material_name' : Material.objects.get(id=key).name,
                                    'qty': item[2],
                                    'price' : item[3]
                                }
                            )
                            item[2] = 0
                
                    if mtlist[key] == 0:
                        break
            for key in mtlist:
                if  mtlist[key] > 0:
                        product_materials.append(
                                {
                                    'warehouse_id': None,
                                    'material_name' : Material.objects.get(id=key).name,
                                    'qty': mtlist[key],
                                    'price' : None
                                }
                            )   
            if not key in db_material_list():
                product_materials.append(
                                {
                                    'warehouse_id': None,
                                    'material_name' : Material.objects.get(id=key).name,
                                    'qty': mtlist[key],
                                    'price' : None,
                                    'message':'Bunday material omborda mavjud emas.'
                                }
                            )   
        return Response({"status" : True, 'result' : natija})
    



    