
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from web_vk import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('ask/', views.ask, name='ask'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('setting/', views.setting, name='setting'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('tag/<str:tag_name>/', views.tag_questions, name='tag_questions'),
    path('hot/', views.hot, name='hot'),
    #path('', include('web_vk.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns