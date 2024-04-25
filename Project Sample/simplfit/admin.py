from django.contrib import admin

from .models import User, Food, FoodCategory, FoodLog, Image, Weight, Sleep, Water, Workout, WorkoutLog, Video, Medicine, MedicineLog, Steps

admin.site.register(User)
admin.site.register(Food)
admin.site.register(FoodCategory)
admin.site.register(FoodLog)
admin.site.register(Image)
admin.site.register(Weight)
admin.site.register(Sleep)
admin.site.register(Medicine)
admin.site.register(MedicineLog)
admin.site.register(Water)
admin.site.register(Workout)
admin.site.register(WorkoutLog)
admin.site.register(Video)
admin.site.register(Steps)
