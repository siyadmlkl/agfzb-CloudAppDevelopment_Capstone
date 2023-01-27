from .models import CarMake,CarModel


models = CarModel.objects.all().values()
print(models)