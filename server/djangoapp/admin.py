from django.contrib import admin
from .models import CarMake,CarModel

#register inlines
class CarMakeInlines(admin.StackedInline):
    model = CarMake
    extra=5

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

#register models
class CarMakeAdmin(admin.ModelAdmin):
     list_display=['name','description']

class CarModelAdmin(admin.ModelAdmin):
    list_display=['name']



admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)

# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
