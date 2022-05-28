from django.shortcuts import render
# Мои импорты
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from .models import Customer  # models.py
from Inbox.forms import Customerform, EmailForm  # forms.py
from django.contrib import messages  # возвращает сообщение
from django.http import HttpResponseRedirect  # редиректит страницы
from django.core.paginator import Paginator  # пагинация
from django.db.models import Q  # глобальныай поиск
from datetime import datetime  # получение даты
from django.core.mail import EmailMessage  # отправка email
from django.contrib.auth import logout  # autologout


# ====================== FRONTEND =======================/
# Домашняя страница
def home(request):
    return render(request, 'home.html')


# Функция отправки сообщениий
def send_message(request):
    if request.method == 'POST':
        form = Customerform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Сообщение отправлено успешно")
        return HttpResponseRedirect('/')
    else:
        form = Customerform()
    return render(request, 'home.html', {'form': form})


# ====================== BACKEND  ===========================/
# Страница Inbox
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def inbox(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_customer_list = Customer.objects.filter(
            Q(name__icontains=q) | Q(phone__icontains=q) |
            Q(email__icontains=q) | Q(subject__icontains=q) |
            Q(status__icontains=q) | Q(message__icontains=q)
        ).order_by('-created_at')
    else:
        all_customer_list = Customer.objects.all().order_by('-created_at')

    paginator = Paginator(all_customer_list, 10)
    page = request.GET.get('page')
    all_customer = paginator.get_page(page)

    # ====================== Счетчик сообщениий  ====================/

    # Общие
    total = Customer.objects.all().count()

    # Прочитанные
    read = Customer.objects.filter(status='Прочитанные')

    # Непрочитанные
    pending = Customer.objects.filter(status='Ожидаемые')

    # Сегодняшние
    base = datetime.now().date()
    today = Customer.objects.filter(created_at__gt=base)

    return render(request, 'inbox.html', {"customers": all_customer,
                                          "total": total, "read": read, "pending": pending, "today": today})


# Страница Inbox
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_message(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.delete()
    messages.success(request, "Сообщение удалено успешно")
    return HttpResponseRedirect('/inbox')


# Личное сообщение
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if customer != None:
        return render(request, 'customer.html', {"customer": customer})


# Отметка прочитано
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mark_message(request):
    if request.method == 'POST':
        customer = Customer.objects.get(id=request.POST.get('id'))
        if customer != None:
            customer.status = request.POST.get('status')
            customer.save()
            messages.success(request, "Сообщение отмечено как ПРОЧИТАННО")
            return HttpResponseRedirect('/inbox')


# Ответ на сообщение
def email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)

        company = "Reply Axtraoil"

        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            email = form.cleaned_data["email"]
            cc = form.cleaned_data["cc"]
            files = request.FILES.getlist("attach")
            mail = EmailMessage(subject, message, company, [email], [cc])
            for f in files:
                mail.attach(f.name, f.read(), f.content_type)
            mail.send()

            messages.success(request, "Сообщение доставлено успешно")
            return HttpResponseRedirect('inbox')
    else:
        form = EmailForm(request.FILES)
        return render(request, {'form': form})


# AutoLogout
def AutoLogoutUser(request):
    logout(request)
    request.user=None
    messages.info(request, ".") # Вставил точку т.к аргумент не может быть пустым
    return HttpResponseRedirect('/')
