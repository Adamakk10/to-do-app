from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('tasks', views.TaskViewSet)
router.register('tasks/detail', views.TaskDetailView)
app_name = 'tasks'


urlpatterns = [
    path('', include(router.urls))
    
]