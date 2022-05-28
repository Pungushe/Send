from django.contrib import admin
from django.urls import path, include

from Inbox import views
from config import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # =========== Frontend ===============/
    # Домашняя страница
    path('', views.home, name='home'),
    # Login/Logout
    path('login/', include('django.contrib.auth.urls')),
    # сообщение
    path('send_message', views.send_message, name='send_message'),

    # =========== Backend ===============/
    # Inbox
    path('inbox/', views.inbox, name='inbox'),
    # Удаление сообщений
    path('delete_message/<str:customer_id>', views.delete_message, name='delete_message'),
    # Личное с сообщение
    path('customer/<str:customer_id>', views.customer, name='customer'),
    # Отметка прочитано
    path('mark_message', views.mark_message, name='mark_message'),
    # Ответ на сообщение
    path('email', views.email, name='email'),
    # auto logout
    path('autologout/', views.AutoLogoutUser, name='autologout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
