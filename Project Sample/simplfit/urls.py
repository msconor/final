from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('',views.home,name="home"),
    path('home.html',views.home,name="home"),
    path('french-home.html',views.french_home,name="french_home"),
    path('login.html',views.login_view,name="login"),
    path('register.html',views.register,name="register"),

    path('waterlog/water',views.water_log_view,name="water_log"),
    path('waterlog/delete/<int:water_id>', views.water_log_delete, name='water_log_delete'),
    path('waterlog/water_goal.html',views.water_goal,name="water_goal"),
    path('waterlog/delete', views.water_log_delete_all, name='water_log_delete_all'),

    path('nutri.html',views.nutri,name="nutri"),
    path('nutri_img.html',views.nutri_img,name="nutri_img"),
    path('exercise.html',views.exercise,name="exercise"),
    path('menstrual_cycle.html',views.menstrual,name="menstrual_cycle"),

    path('sleeplog/sleep',views.sleep_log_view,name="sleep_log"),
    path('sleeplog/delete/<int:sleep_id>', views.sleep_log_delete, name='sleep_log_delete'),
    path('sleeplog/sleep_goal.html',views.sleep_goal,name="sleep_goal"),
    path('sleeplog/delete', views.sleep_log_delete_all, name='sleep_log_delete_all'),

    path('steplog/step',views.step_log_view,name="step_log"),
    path('steplog/step_goal.html',views.step_goal,name="step_goal"),
    path('steplog/delete/<int:step_id>', views.step_log_delete, name='step_log_delete'),
    path('steplog/delete', views.step_log_delete_all, name='step_log_delete_all'),

    path('foodrecipes.html',views.food_recipes,name="foodrecipes"),
    path('weather.html',views.weather,name="weather"),
    path('blog.html', views.blog, name="blog"),
    path('blog-details-1.html', views.blog_details_1, name="blog-details"),
    path('blog-details-2.html', views.blog_details_2, name="blog-details"),
    path('blog-details-3.html', views.blog_details_3, name="blog-details"),

    path('index', views.index, name='index'),
    path('index_workout', views.index_workout, name='index_workout'),
    path('logout', views.logout_view, name='logout'),
    path('profile/weight', views.weight_log_view, name='weight_log'),
    path('profile/weight/delete/<int:weight_id>', views.weight_log_delete, name='weight_log_delete'),
    path('profile/weight/delete', views.weight_log_delete_all, name='weight_log_delete_all'),

    path('food/list', views.food_list_view, name='food_list'),
    path('food/add', views.food_add_view, name='food_add'),
    path('foodlog', views.food_log_view, name='food_log'),
    path('food_goal.html', views.food_goal, name='food_goal'),
    path('food/foodlog/delete/<int:food_id>', views.food_log_delete, name='food_log_delete'),
    path('food/foodlog/delete', views.food_log_delete_all, name='food_log_delete_all'),
    path('food/<str:food_id>', views.food_details_view, name='food_details'),

    path('categories', views.categories_view, name='categories_view'),
    path('categories/<str:category_name>', views.category_details_view, name='category_details_view'),

    path('workout/list', views.workout_list_view, name='workout_list'),
    path('workout/add', views.workout_add_view, name='workout_add'),
    path('workoutlog', views.workout_log_view, name='workout_log'),
    path('workout/workoutlog/delete/<int:workout_id>', views.workout_log_delete, name='workout_log_delete'),
    path('workout/workout/delete', views.workout_log_delete_all, name='workout_log_delete_all'),
    path('workout/<str:workout_id>', views.workout_details_view, name='workout_details'),

     path('medicine/add', views.medicine_add_view, name='medicine_add'),
     path('medicinelog', views.medicine_log_view, name='medicine_log'),
     path('medicine/medicinelog/delete/<int:medicine_id>', views.medicine_log_delete, name='medicine_log_delete'),
     path('medicine/medicinelog/delete', views.medicine_log_delete_all, name='medicine_log_delete_all'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

    
