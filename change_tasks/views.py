from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from change_tasks.models import News, Tasks, Contact
from django.contrib.auth.models import User
from change_tasks.forms import UpdateTaskForm, UserCreationForm, TaskFormAdd
from django.contrib import messages


# главная страница
def home(request):
    # Получаем все новости и сортируем их по дате в обратном порядке
    news = News.objects.order_by("-data")
 
    # Формируем контекст для шаблона
    context = {
        "news": news,  # передаем список новостей в контекст
    }

    # Рендерим шаблон и передаем ему контекст
    return render(request, "home.html", context)


# регистрация
def register(request):
    # Проверяем метод запроса (POST - создание нового пользователя)
    if request.method == 'POST':
        # Создаем объект формы UserCreationForm и передаем данные из запроса
        form = UserCreationForm(request.POST)
        # Проверяем форму на валидность
        if form.is_valid():
            # Сохраняем данные формы и создаем новый объект пользователя
            form.save()
            # Получаем имя пользователя
            username = form.cleaned_data.get('username')
            # Выводим сообщение об успешной регистрации и перенаправляем на главную страницу
            messages.success(request, f'Аккаунт создан для юзера {username}!')
            return redirect('home')
    else:
        # Если метод GET, то создаем пустую форму
        form = UserCreationForm()
    # Сохраняем форму в контексте и рендерим шаблон регистрации
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


# список пользователей
def list_users(request):
    # Получаем всех пользователей из базы данных
    users = User.objects.all()
    # Создаем словарь с контекстом для передачи в шаблон
    context = {
        "users": users
    }
    # Рендерим шаблон с контекстом
    return render(request, 'list_users.html', context)


# задачи пользователя
# проверяем авторизованы ли мы с помощью декоратора login_required, если да, то заходим на страницу пользователя
@login_required
def user_page(request):
    # Получаем текущего пользователя
    user = request.user
    # Фильтруем задачи, которые назначены на текущего пользователя
    tasks = Tasks.objects.filter(assigned_to=user)
    # Формируем словарь контекста
    context = {
        "tasks": tasks
    }
    # возвращаем ответ с отрисованным шаблоном и переданным контекстом
    return render(request, 'user_page.html', context)

# делегировать задачу
# проверяем авторизованы ли мы с помощью декоратора login_required, если да, то заходим на страницу изменения задачи
@login_required
def UpdateView(request, task_id):
    # получает объект задания (Tasks) по его уникальному идентификатору (task_id), или возвращает страницу 404 ошибки, если такой объект не существует.
    task = get_object_or_404(Tasks, pk=task_id)
    # проверяет, был ли отправлен POST-запрос пользователем.
    if request.method == 'POST':
        # создает экземпляр формы UpdateTaskForm с данными, которые были отправлены пользователем, и существующим экземпляром задания в качестве instance.
        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid(): # проверяет не было ли пропущено обязательное поле
            task = form.save() # сохраняем форму
            messages.success(request, 'Передача задания прошла успешно!') # добавляет сообщение об успешном обновлении задания в очередь сообщений пользователя.
            # return redirect('task_edit', task_id=task.id) # перенаправляет пользователя на страницу редактирования задания с обновленными данными.
            return redirect('user_page')
    else:
        form = UpdateTaskForm(instance=task)

    context = {
        'form': form,
        'task': task,
    }
    return render(request, 'task_edit.html', context) # возвращает шаблон task_edit.html с переданным контекстом данных.


# создание задачи
# проверяем авторизованы ли мы с помощью декоратора login_required, если да, то заходим на страницу создания задачи
@login_required
def create_task(request):
    if request.method == 'POST': #если метод запроса POST, значит форма отправлена, нужно сохранить задачу в БД
        form = TaskFormAdd(request.POST, request.FILES) # создаем экземпляр формы и заполняем ее данными из запроса
        if form.is_valid(): # проверяем, валидна ли форма
            task = form.save(commit=False) # создаем объект задачи, но не сохраняем его в БД, используя commit=False
            task.save()  # сохраняем объект `Tasks` в базе данных

            assigned_users = form.cleaned_data.get('assigned_to')
            task.created_by.set([request.user])  # добавляем создателя задачи

            # добавляем назначенных пользователей
            for assigned_user in assigned_users:
                task.assigned_to.add(assigned_user)
             # выводим сообщение об успешном создании задачи
            messages.success(request, 'Задача успешно создана!')
            return redirect('home')
    else:
        form = TaskFormAdd()

    return render(request, 'task_add.html', {'form': form})


# страница контактов, где мы можем отправить сообщению админу и получить ответ
def contact(request):
    if request.method == 'POST':# Проверяем, если запрос был отправлен методом POST
        contact = Contact(contact_info=request.user)  # Создаем экземпляр модели Contact, связанный с текущим пользователем
        name = request.POST.get('name') # Получаем данные из формы
        email = request.POST.get('email')# Получаем данные из формы
        phone = request.POST.get('phone')# Получаем данные из формы
        subject = request.POST.get('subject')# Получаем данные из формы
        contact_info = request.user # Получаем данные из формы
        contact.name = name # Получаем данные из формы
        contact.email = email # Получаем данные из формы
        contact.phone = phone # Получаем данные из формы
        contact.subject = subject # Получаем данные из формы

        contact.save()# Сохраняем объект `Contact` в базе данных
        messages.success(
            request, f"Добавилась новая заявка! от пользователя  {contact_info}") # Отображаем сообщение об успешном сохранении заявки
 
        contact.save()  # Снова сохраняем объект `Contact` в базе данных
        return redirect('/', f"Добавилась новая заявка! ")  # Перенаправляем пользователя на домашнюю страницу
    return render(request, 'contact.html') # Если запрос был отправлен методом GET, отображаем страницу с формой


# проверяем авторизованы ли мы с помощью декоратора login_required, если да, то заходим на страницу заявок
@login_required
def contacts(request):

    zayzvka = Contact.objects.all().filter(contact_info=request.user) #выбираем все объекты модели Contact, которые относятся к текущему пользователю.

    return render(request, 
                  'user_contacts.html',
                  {'zayzvka': zayzvka})


# удаление заявки
def delete_contact(request, pk=None): #Функция delete_contact принимает запрос request и необязательный параметр pk, который является идентификатором объекта Contact, который нужно удалить
    Contact.objects.get(id=pk).delete() #получает объект Contact с помощью метода get() и передает значение параметра pk. Затем вызывается метод delete() для удаления объекта из базы данных.
    messages.success(
        request, f'Заявка успешно удалена пользователем!{request.user.username} !')
    return redirect('contacts') 

# Отображение детальной информации по задаче с id = task_id
def card_detail(request, task_id):
    
    task = get_object_or_404(Tasks, pk=task_id) # Получаем объект задачи из базы данных по её id
    # Отображаем страницу с подробной информацией о задаче
    return render(request, "card_detail.html", {"task": task})


def hide_task(request, pk=None):
    # Получаем объект задачи или возвращаем 404 ошибку, если такой задачи нет
    task = get_object_or_404(Tasks, id=pk)

    # Если метод запроса POST, то изменяем статус скрытости задачи и сохраняем ее
    if request.method == 'POST':
        task.is_hidden = not task.is_hidden
        task.save()
        # Перенаправляем пользователя на главную страницу
        # return redirect('home')
        return redirect('user_page')

