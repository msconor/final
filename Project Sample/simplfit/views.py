from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse

from .models import User, Food, FoodCategory, FoodLog, Image, Weight, Sleep, Water,Workout,WorkoutLog,Video, Medicine, MedicineLog,Steps
from .forms import FoodForm, ImageForm, WorkoutForm, VideoForm, MedicineForm

def home(request):
    return render(request,'home.html',{})

def french_home(request):
    return render(request,'french-home.html',{})

def nutri(request):
    import json
    import requests
    if request.method == 'POST':
        query = request.POST['query']
        api_url='https://api.api-ninjas.com/v1/nutrition?query='
        api_request= requests.get(api_url + query, headers = {'X-Api-Key':'Jbl5w1oQwNcNNKOnzZ2p/Q==AxfZUC8NCfTqgni2'})
        try:
            api = json.loads(api_request.content)
            print(api_request.content)
        except Exception as e:
            api = "oops! There was an error"
            print(e)
        return render(request, 'nutri.html',{'api':api})
    else:
        return render(request, 'nutri.html',{'query':'Enter a valid query'})

def nutri_img(request):
    import os
    import json
    import requests
    if request.method == 'POST':
        img = request.POST['query']
        api_user_token = '25742373693a91ab434755a9219ddb6bc9d87c78'
        headers = {'Authorization': 'Bearer ' + api_user_token}

        # Single/Several Dishes Detection
        url = 'https://api.logmeal.es/v2/image/segmentation/complete'
        resp = requests.post(url,files={'image':open(os.path.join("C:/Users/thula/Downloads", img), 'rb')},headers=headers)

        # Nutritional information
        url = 'https://api.logmeal.es/v2/recipe/nutritionalInfo'
        resp = requests.post(url,json={'imageId': resp.json()['imageId']}, headers=headers)
        
        try:
            api = json.loads(resp.content)
            print(resp.json()) # display nutritional info
        except Exception as e:
            api = "oops! There was an error"
            print(e)
        return render(request, 'nutri_img.html',{'api':api})
    else:
        return render(request, 'nutri_img.html',{'query':'Enter a valid query'})
    
def weather(request):
    import json
    import requests
    if request.method == 'POST':
        query = request.POST['query']
        api_url='https://api.api-ninjas.com/v1/weather?city='
        api_url1='https://api.api-ninjas.com/v1/airquality?city='
        api_request= requests.get(api_url + query, headers = {'X-Api-Key':'Jbl5w1oQwNcNNKOnzZ2p/Q==AxfZUC8NCfTqgni2'})
        api_request1= requests.get(api_url1 + query, headers = {'X-Api-Key':'Jbl5w1oQwNcNNKOnzZ2p/Q==AxfZUC8NCfTqgni2'})
        try:
            api = json.loads(api_request.content)
            api1 = json.loads(api_request1.content)
            print(api_request.content)
            print(api_request1.content)
            print(query)
        except Exception as e:
            api = "oops! There was an error"
            api1 = "oops! There was an error"
            print(e)
        return render(request, 'weather.html',{'api':api,'api1':api1,'query':query})
    else:
        return render(request, 'weather.html',{'query':'Enter a valid query'})

def index(request):
    return food_list_view(request)

def index_workout(request):
    return workout_list_view(request)

def food_recipes(request):
    return render(request,'foodrecipes.html',{})

def menstrual(request):
    return render(request,'menstrual_cycle.html',{})

def exercise(request):
    import json
    import requests
    if request.method == 'POST':
        query = request.POST['query']
        select = request.POST['select']
        api_url='https://api.api-ninjas.com/v1/exercises?'+select+'='
        api_request= requests.get(api_url + query, headers = {'X-Api-Key':'Jbl5w1oQwNcNNKOnzZ2p/Q==AxfZUC8NCfTqgni2'})
        try:
            api = json.loads(api_request.content)
            print(api_request.content)
        except Exception as e:
            api = "oops! There was an error"
            print(e)
        return render(request, 'exercise.html',{'api':api})
    else:
        return render(request, 'exercise.html',{'query':'Enter a valid query'})
    
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'register.html', {
                'message': 'Passwords must match.',
                'categories': FoodCategory.objects.all()
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                'message': 'Username already taken.',
                'categories': FoodCategory.objects.all()
            })
        login(request, user)
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'register.html', {
            'categories': FoodCategory.objects.all()
        })


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'login.html', {
                'message': 'Invalid username and/or password.',
                'categories': FoodCategory.objects.all()
            })
    else:
        return render(request, 'login.html',  {
            'categories': FoodCategory.objects.all()
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def food_list_view(request):
    '''
    It renders a page that displays all food items
    Food items are paginated: 4 per page
    '''
    foods = Food.objects.all()

    for food in foods:
        food.image = food.get_images.first()

    # Show 4 food items per page
    page = request.GET.get('page', 1)
    paginator = Paginator(foods, 3)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'pages': pages,
        'title': 'Food List'
    })


def food_details_view(request, food_id):
    '''
    It renders a page that displays the details of a selected food item
    '''
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    food = Food.objects.get(id=food_id)

    return render(request, 'food.html', {
        'categories': FoodCategory.objects.all(),
        'food': food,
        'images': food.get_images.all(),
    })
    

@login_required
def food_add_view(request):
    '''
    It allows the user to add a new food item
    '''
    ImageFormSet = forms.modelformset_factory(Image, form=ImageForm, extra=2)

    if request.method == 'POST':
        food_form = FoodForm(request.POST, request.FILES)
        image_form = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if food_form.is_valid() and image_form.is_valid():
            new_food = food_form.save(commit=False)
            new_food.save()

            for food_form in image_form.cleaned_data:
                if food_form:
                    image = food_form['image']

                    new_image = Image(food=new_food, image=image)
                    new_image.save()

            return render(request, 'food_add.html', {
                'categories': FoodCategory.objects.all(),
                'food_form': FoodForm(),
                'image_form': ImageFormSet(queryset=Image.objects.none()),
                'success': True
            })
        
        else:
            return render(request, 'food_add.html', {
                'categories': FoodCategory.objects.all(),
                'food_form': FoodForm(),
                'image_form': ImageFormSet(queryset=Image.objects.none()),
            })

    else:
        return render(request, 'food_add.html', {
            'categories': FoodCategory.objects.all(),
            'food_form': FoodForm(),
            'image_form': ImageFormSet(queryset=Image.objects.none()),
        })
    

@login_required
def food_log_view(request):

    foods = Food.objects.all()

    for food in foods:
        food.image = food.get_images.first()

    # Show 4 food items per page
    page = request.GET.get('page', 1)
    paginator = Paginator(foods, 3)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    
    if request.method == 'POST':
        foods = Food.objects.all()

        # get the food item selected by the user
        food = request.POST['food_consumed']
        food_consumed = Food.objects.get(food_name=food)

        # get the currently logged in user
        user = request.user
        
        # add selected food to the food log
        food_log = FoodLog(user=user, food_consumed=food_consumed)
        food_log.save()

    else: # GET method
        foods = Food.objects.all()
        
    # get the food log of the logged in user
    user_food_log = FoodLog.objects.filter(user=request.user)
    
    return render(request, 'food_log.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'pages': pages,
        'user_food_log': user_food_log
    })

def food_goal(request):
  
    if request.method == 'POST':
        return HttpResponse('<script type="text/javascript">window.close();</script>')
    
    return render(request, 'food_goal.html', {
        'categories': FoodCategory.objects.all()
    })

@login_required
def food_log_delete(request, food_id):
    '''
    It allows the user to delete food items from their food log
    '''
    # get the food log of the logged in user
    food_consumed = FoodLog.objects.filter(id=food_id)

    if request.method == 'POST':
        food_consumed.delete()
        return redirect('food_log')
    
    return render(request, 'food_log_delete.html', {
        'categories': FoodCategory.objects.all()
    })

@login_required
def food_log_delete_all(request):
    '''
    It allows the user to delete food items from their food log
    '''
    # get the food log of the logged in user
    food_consumed = FoodLog.objects.all()

    if request.method == 'POST':
        food_consumed.all().delete()
        return redirect('food_log')
    
    return render(request, 'food_log_delete_all.html', {
        'categories': FoodCategory.objects.all()
    })

@login_required
def water_log_view(request):
    if request.method == 'POST':

        # get the values from the form
        water= request.POST['water']
        drink_date = request.POST['date']
        drink_time = request.POST['time']

        # get the currently logged in user
        user = request.user

        # add the data to the weight log
        water_log = Water(user=user,water=water, drink_date=drink_date, drink_time=drink_time)
        water_log.save()

    # get the weight log of the logged in user
    user_water_log = Water.objects.filter(user=request.user)
    
    return render(request, 'water_track.html', {
        'categories': FoodCategory.objects.all(),
        'user_water_log': user_water_log
    })

def water_goal(request):
  
    if request.method == 'POST':
        return HttpResponse('<script type="text/javascript">window.close();</script>')
    
    return render(request, 'water_goal.html', {
        'categories': FoodCategory.objects.all()
    })

@login_required
def water_log_delete(request, water_id):
    '''
    It allows the user to delete food items from their food log
    '''
    # get the food log of the logged in user
    water_consumed = Water.objects.filter(id=water_id)

    if request.method == 'POST':
        water_consumed.delete()
        return redirect('water_log')
    
    return render(request, 'water_log_delete.html', {
        'categories': FoodCategory.objects.all()
    })

@login_required
def water_log_delete_all(request):
    '''
    It allows the user to delete food items from their food log
    '''
    # get the food log of the logged in user
    water_consumed = Water.objects.all()

    if request.method == 'POST':
        water_consumed.all().delete()
        return redirect('water_log')
    
    return render(request, 'water_log_delete_all.html', {
        'categories': FoodCategory.objects.all()
    })

@login_required
def sleep_log_view(request):
    if request.method == 'POST':

        # get the values from the form
        hours= request.POST['hours']
        sleep_date = request.POST['date']

        # get the currently logged in user
        user = request.user

        # add the data to the weight log
        sleep_log = Sleep(user=user,hours=hours, sleep_date=sleep_date)
        sleep_log.save()

    # get the weight log of the logged in user
    user_sleep_log = Sleep.objects.filter(user=request.user)
    
    return render(request, 'sleep_track.html', {
        'categories': FoodCategory.objects.all(),
        'user_sleep_log': user_sleep_log
    })

def sleep_goal(request):
  
    if request.method == 'POST':
        return HttpResponse('<script type="text/javascript">window.close();</script>')
    
    return render(request, 'sleep_goal.html', {
        'categories': FoodCategory.objects.all()
    })

@login_required
def sleep_log_delete(request, sleep_id):
    '''
    It allows the user to delete a weight record from their weight log
    '''
    # get the weight log of the logged in user
    sleep_recorded = Sleep.objects.filter(id=sleep_id) 

    if request.method == 'POST':
        sleep_recorded.delete()
        return redirect('sleep_log')
    
    return render(request, 'sleep_log_delete.html', {
        'categories': FoodCategory.objects.all()
    })

@login_required
def sleep_log_delete_all(request):
    '''
    It allows the user to delete food items from their food log
    '''
    # get the food log of the logged in user
    sleep_log = Sleep.objects.all()

    if request.method == 'POST':
        sleep_log.all().delete()
        return redirect('sleep_log')
    
    return render(request, 'sleep_log_delete_all.html', {
        'categories': FoodCategory.objects.all()
    })

@login_required
def weight_log_view(request):
    '''
    It allows the user to record their weight
    '''
    if request.method == 'POST':

        # get the values from the form
        weight = request.POST['weight']
        height = request.POST['height']
        entry_date = request.POST['date']

        # get the currently logged in user
        user = request.user

        # add the data to the weight log
        weight_log = Weight(user=user, weight=weight, entry_date=entry_date, height = height)
        weight_log.save()

    # get the weight log of the logged in user
    user_weight_log = Weight.objects.filter(user=request.user)
    
    return render(request, 'user_profile.html', {
        'categories': FoodCategory.objects.all(),
        'user_weight_log': user_weight_log
    })


@login_required
def weight_log_delete(request, weight_id):
    '''
    It allows the user to delete a weight record from their weight log
    '''
    # get the weight log of the logged in user
    weight_recorded = Weight.objects.filter(id=weight_id) 

    if request.method == 'POST':
        weight_recorded.delete()
        return redirect('weight_log')
    
    return render(request, 'weight_log_delete.html', {
        'categories': FoodCategory.objects.all()
    })

@login_required
def weight_log_delete_all(request):
    '''
    It allows the user to delete food items from their food log
    '''
    # get the food log of the logged in user
    weight_consumed = Weight.objects.all()

    if request.method == 'POST':
        weight_consumed.all().delete()
        return redirect('weight_log')
    
    return render(request, 'weight_log_delete_all.html', {
        'categories': FoodCategory.objects.all()
    })

def categories_view(request):
    '''
    It renders a list of all food categories
    '''
    return render(request, 'categories.html', {
        'categories': FoodCategory.objects.all()
    })


def category_details_view(request, category_name):
    '''
    Clicking on the name of any category takes the user to a page that 
    displays all of the foods in that category
    Food items are paginated: 4 per page
    '''
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    category = FoodCategory.objects.get(category_name=category_name)
    foods = Food.objects.filter(category=category)

    for food in foods:
        food.image = food.get_images.first()

    # Show 4 food items per page
    page = request.GET.get('page', 1)
    paginator = Paginator(foods, 4)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'food_category.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'foods_count': foods.count(),
        'pages': pages,
        'title': category.category_name
    })

def blog(request):
    return render(request,'blog.html',{})

def blog_details_1(request):
    return render(request,'blog-details-1.html',{})

def blog_details_2(request):
    return render(request,'blog-details-2.html',{})

def blog_details_3(request):
    return render(request,'blog-details-3.html',{})


def workout_list_view(request):
    '''
    It renders a page that displays all food items
    Food items are paginated: 4 per page
    '''
    workouts = Workout.objects.all()

    for workout in workouts:
        workout.video = workout.get_video.first()

    # Show 4 food items per page
    page = request.GET.get('page', 1)
    paginator = Paginator(workouts, 4)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'index_workout.html', {
        'categories': FoodCategory.objects.all(),
        'workouts': workouts,
        'pages': pages,
        'title': 'Workout List'
    })


def workout_details_view(request, workout_id):
    '''
    It renders a page that displays the details of a selected food item
    '''
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    workout = Workout.objects.get(id=workout_id)

    return render(request, 'workout.html', {
        'categories': FoodCategory.objects.all(),
        'workout': workout,
        'videos': workout.get_video.all(),
    })
    

@login_required
def workout_add_view(request):
    '''
    It allows the user to add a new food item
    '''
    VideoFormSet = forms.modelformset_factory(Video, form=VideoForm, extra=1)

    if request.method == 'POST':
        workout_form = WorkoutForm(request.POST, request.FILES)
        video_form =  VideoFormSet(request.POST, request.FILES, queryset=Video.objects.none())

        if workout_form.is_valid() and video_form.is_valid():
            new_workout = workout_form.save(commit=False)
            new_workout.save()

            for workout_form in video_form.cleaned_data:
                if workout_form:
                    video = workout_form['video']

                    new_video = Video(workout=new_workout, video=video)
                    new_video.save()

            return render(request, 'workout_add.html', {
                'categories': FoodCategory.objects.all(),
                'workout_form': WorkoutForm(),
                'video_form': VideoFormSet(queryset=Video.objects.none()),
                'success': True
            })
        
        else:
            return render(request, 'workout_add.html', {
                'categories': FoodCategory.objects.all(),
                'workout_form': WorkoutForm(),
                'video_form': VideoFormSet(queryset=Video.objects.none()),
            })

    else:
        return render(request, 'workout_add.html', {
            'categories': FoodCategory.objects.all(),
            'workout_form': WorkoutForm(),
            'video_form': VideoFormSet(queryset=Video.objects.none()),
        })
    

@login_required
def workout_log_view(request):
    '''
    It allows the user to select food items and 
    add them to their food log
    '''
    if request.method == 'POST':
        workouts = Workout.objects.all()

        # get the food item selected by the user
        workout = request.POST['calories_burned']
        calories_burned = Workout.objects.get(workout_name=workout)

        # get the currently logged in user
        user = request.user
        
        # add selected food to the food log
        workout_log = WorkoutLog(user=user, calories_burned=calories_burned)
        workout_log.save()

    else: # GET method
        workouts = Workout.objects.all()
        
    # get the food log of the logged in user
    user_workout_log = WorkoutLog.objects.filter(user=request.user)
    user_step_log = Steps.objects.filter(user=request.user)
    
    return render(request, 'workout_log.html', {
        'categories': FoodCategory.objects.all(),
        'workouts': workouts,
        'user_workout_log': user_workout_log,
        'user_step_log': user_step_log
    })


@login_required
def workout_log_delete(request, workout_id):
    '''
    It allows the user to delete food items from their food log
    '''
    # get the food log of the logged in user
    calories_burned = WorkoutLog.objects.filter(id=workout_id)

    if request.method == 'POST':
        calories_burned.delete()
        return redirect('workout_log')
    
    return render(request, 'workout_log_delete.html', {
        'categories': FoodCategory.objects.all()
    })

@login_required
def workout_log_delete_all(request):
    '''
    It allows the user to delete food items from their food log
    '''
    # get the food log of the logged in user
    workout_consumed = WorkoutLog.objects.all()

    if request.method == 'POST':
        workout_consumed.all().delete()
        return redirect('workout_log')
    
    return render(request, 'workout_log_delete_all.html', {
        'categories': FoodCategory.objects.all()
    })

@login_required
def medicine_add_view(request):
    '''
    It allows the user to add a new food item
    '''
    if request.method == 'POST':
        medicine_form = MedicineForm(request.POST)

        if medicine_form.is_valid():
            new_medicine = medicine_form.save(commit=False)
            new_medicine.save()

            return render(request, 'medicine_add.html', {
                'categories': FoodCategory.objects.all(),
                'medicine_form': MedicineForm(),
                'success': True
            })
        
        else:
            return render(request, 'medicine_add.html', {
                'categories': FoodCategory.objects.all(),
                'medicine_form': MedicineForm(),
            })

    else:
        return render(request, 'medicine_add.html', {
            'categories': FoodCategory.objects.all(),
            'medicine_form': MedicineForm(),
        })

@login_required
def medicine_log_view(request):
    '''
    It allows the user to select food items and 
    add them to their food log
    '''
    if request.method == 'POST':
        medicines = Medicine.objects.all()

        # get the values from the form
        intake_time = request.POST['intake_time']

        # get the currently logged in user
        user = request.user

        # get the food item selected by the user
        medicine = request.POST['medicine_consumed']
        medicine_consumed = Medicine.objects.get(medicine_name=medicine)

        # get the currently logged in user
        user = request.user
        
        # add selected food to the food log
        medicine_log = MedicineLog(user=user, medicine_consumed=medicine_consumed,intake_time=intake_time)
        medicine_log.save()

    else: # GET method
        medicines = Medicine.objects.all()
        
    # get the food log of the logged in user
    user_medicine_log = MedicineLog.objects.filter(user=request.user)
    
    return render(request, 'medicine_log.html', {
        'categories': FoodCategory.objects.all(),
        'medicines': medicines,
        'user_medicine_log': user_medicine_log
    })


@login_required
def medicine_log_delete(request, medicine_id):
    '''
    It allows the user to delete food items from their food log
    '''
    # get the food log of the logged in user
    medicine_consumed = MedicineLog.objects.filter(id=medicine_id)

    if request.method == 'POST':
        medicine_consumed.delete()
        return redirect('medicine_log')
    
    return render(request, 'medicine_log_delete.html', {
        'categories': FoodCategory.objects.all()
    })


@login_required
def medicine_log_delete_all(request):
    '''
    It allows the user to delete food items from their food log
    '''
    # get the food log of the logged in user
    medicine_consumed = Medicine.objects.all()

    if request.method == 'POST':
        medicine_consumed.all().delete()
        return redirect('medicine_log')
    
    return render(request, 'medicine_log_delete_all.html', {
        'categories': FoodCategory.objects.all()
    })

@login_required
def step_log_view(request):
    if request.method == 'POST':

        # get the values from the form
        calories_burned= request.POST['calories_burned']
        walk_distance = request.POST['walk_distance']
        walk_distance_k = request.POST['walk_distance_k']
        time_consumed = request.POST['time_consumed']
        cardio_doing = request.POST['cardio_doing']

        # get the currently logged in user
        user = request.user

        # add the data to the weight log
        step_log = Steps(user=user,calories_burned=calories_burned, walk_distance=walk_distance, time_consumed=time_consumed,walk_distance_k=walk_distance_k,cardio_doing=cardio_doing)
        step_log.save()

    # get the weight log of the logged in user
    user_step_log = Steps.objects.filter(user=request.user)
    
    return render(request, 'steps_track.html', {
        'categories': FoodCategory.objects.all(),
        'user_step_log': user_step_log
    })


@login_required
def step_log_delete(request, step_id):
    '''
    It allows the user to delete a weight record from their weight log
    '''
    # get the weight log of the logged in user
    step_recorded = Steps.objects.filter(id=step_id) 

    if request.method == 'POST':
        step_recorded.delete()
        return redirect('step_log')
    
    return render(request, 'step_log_delete.html', {
        'categories': FoodCategory.objects.all()
    })

@login_required
def step_log_delete_all(request):
    '''
    It allows the user to delete food items from their food log
    '''
    # get the food log of the logged in user
    step_log = Steps.objects.all()

    if request.method == 'POST':
        step_log.all().delete()
        return redirect('step_log')
    
    return render(request, 'step_log_delete_all.html', {
        'categories': FoodCategory.objects.all()
    })

def step_goal(request):
  
    if request.method == 'POST':
        return HttpResponse('<script type="text/javascript">window.close();</script>')
    
    return render(request, 'step_goal.html', {
        'categories': FoodCategory.objects.all()
    })
