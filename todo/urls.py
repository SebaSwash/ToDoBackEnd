"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin

# ========== Importación de vistas ==========
from users import views as user_views
from tasks import views as tasks_views
from subjects import views as subjects_views

urlpatterns = [
    path('session/', user_views.post_session_authentication),
    path('users/<int:user_id>', user_views.get_user_data),
    path('users/<int:user_id>/tasks/', tasks_views.multiple_tasks_router),
    path('users/<int:user_id>/tasks/<int:task_id>/', tasks_views.single_tasks_router),
    path('users/<int:user_id>/subjects/', subjects_views.multiple_subjects_router),
    path('admin/', admin.site.urls),
]
