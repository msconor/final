from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.utils import timezone


class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'


class FoodCategory(models.Model):
    category_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Food Category'
        verbose_name_plural = 'Food Categories'

    def __str__(self):
        return f'{self.category_name}'

    @property
    def count_food_by_category(self):
        return Food.objects.filter(category=self).count()


class Food(models.Model):
    food_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, default=100.00)
    calories = models.DecimalField(max_digits=7, decimal_places=2)
    fat = models.DecimalField(max_digits=7, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=7, decimal_places=2)
    protein = models.DecimalField(max_digits=7, decimal_places=2)
    fiber = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='food_category',default=False)

    def __str__(self):
        return f'{self.food_name} - category: {self.category}'


class Image(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='get_images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.image}'


class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_consumed = models.ForeignKey(Food, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Food Log'
        verbose_name_plural = 'Food Log'

    def __str__(self):
        return f'{self.user.username} - {self.food_consumed.food_name}'


class Weight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    height = models.DecimalField(max_digits=7, decimal_places=2)
    entry_date = models.DateField()

    class Meta:
        verbose_name = 'Weight'
        verbose_name_plural = 'Weight'

    def __str__(self):
        return f'{self.user.username} - {self.weight}kg & {self.height}cm on {self.entry_date}'
    
class Sleep(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=7, decimal_places=2)
    sleep_date = models.DateField()

    class Meta:
        verbose_name = 'Sleep'
        verbose_name_plural = 'Sleep'

    def __str__(self):
        return f'{self.user.username} - {self.hours}hrs on {self.sleep_date}'

class Water(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    water = models.DecimalField(max_digits=6, decimal_places=2)
    drink_date = models.DateField()
    drink_time = models.TimeField()
    class Meta:
        verbose_name = 'Water'
        verbose_name_plural = 'Water'

    def __str__(self):
        return f'{self.user.username} - {self.water} ml on -{self.drink_date}-{self.drink_time}'

class Workout(models.Model):
    workout_name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    muscle_group = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=200)
    instructions = models.CharField(max_length=2000)
    time = models.DecimalField(max_digits=7, decimal_places=2)
    calories_burn = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.workout_name}'


class Video(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='get_video')
    video = models.FileField(upload_to='videos/')

    def __str__(self):
        return f'{self.video}'


class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calories_burned = models.ForeignKey(Workout, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Workout Log'
        verbose_name_plural = 'Workout Log'

    def __str__(self):
        return f'{self.user.username} - {self.calories_burned.workout_name}'

class Medicine(models.Model):
    medicine_unit = (
    ('Tablet (mg)','Tablet'),
    ('Syrup (ml)','Syrup'),
    ('Drop', 'Drop'),
    ('Spray','Spray'),
    ('Injection','Injection'),
    
)
    time = (
    ('1 AM','1 AM'),('2 AM','2 AM'),('3 AM','3 AM'),('4 AM','4 AM'),('5 AM','5 AM'),('6 AM','6 AM'),('7 AM','7 AM'),('8 AM','8 AM'),('9 AM','9 AM'),('10 AM','10 AM'),('11 AM','11 AM'),('12 AM','12 AM'),('12 PM','12 PM'),
    ('1 PM','1 PM'),('2 PM','2 PM'),('3 PM','3 PM'),('4 PM','4 PM'),('5 PM','5 PM'),('6 PM','6 PM'),('7 PM','7 PM'),('8 PM','8 PM'),('9 PM','9 PM'),('10 PM','10 PM'),('11 PM','11 PM'),
)
    medicine_name = models.CharField(max_length=200)
    unit = models.CharField(max_length=200, choices=medicine_unit, default="")
    dosage = models.IntegerField(default=1)
    start_date = models.DateField(("Start Date"), default=date.today)
    end_date = models.DateField(("End Date"), default=date.today)
    time = models.CharField(("Dosage Time"),max_length=200, choices=time, default="")
    
    def __str__(self):
        return f'{self.medicine_name}'

class MedicineLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine_consumed = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    intake_time = models.TimeField()

    class Meta:
        verbose_name = 'Medicine Log'
        verbose_name_plural = 'Medicine Log'
    
    def __str__(self):
        return f'{self.user.username} - {self.medicine_consumed}  - {self.intake_time}'

class Steps(models.Model):
    cardio = (
        ('Slow Walking','Slow Walking'),
        ('Walking','Walking'),
        ('Jogging','Jogging'),
        ('Running','Running')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cardio_doing = models.CharField(max_length=200,choices=cardio,default='')
    calories_burned = models.DecimalField(max_digits=7, decimal_places=2)
    walk_distance = models.DecimalField(max_digits=7, decimal_places=2)
    walk_distance_k = models.DecimalField(max_digits=7, decimal_places=2)
    time_consumed = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
            verbose_name = 'Steps'
            verbose_name_plural = 'Steps'

    def __str__(self):
            return f'{self.user.username} - {self.calories_burned} calories burned for {self.cardio_doing} is {self.walk_distance}steps and {self.walk_distance_k} kms in {self.time_consumed} mins'


