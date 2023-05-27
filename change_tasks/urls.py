from django.urls import path
from change_tasks import views

urlpatterns = [
    # path("",views.home,name="home"),
    # path("list_users/",views.list_users,name="list_users"),
    # path("profile/",views.user_page,name="user_page"),
    
    # # path('task/<int:pk>/edit/', views.UpdateView, name='task_edit'),
    # path('task/<int:task_id>/edit/', views.UpdateView, name='task_edit'),
    # path("create_task/",views.create_task,name="create_task"),
    # path("contact/",views.contact,name="contact"),

    # path('contacts/', views.contacts, name='contacts'),
    # path('contacts/<int:pk>',
    #      views.delete_contact, name="delete-contact"),

    #  # path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    # path("card_detail/<int:task_id>",
    #      views.card_detail, name="card_detail"),


    #  path('profile/<int:pk>',
    #      views.hide_task, name="hide_task"),

            path('', views.home, name="home"), # Главная страница приложения
            path('list_users/', views.list_users, name="list_users"), # Страница, на которой отображаются все зарегистрированные пользователи
            path('profile/', views.user_page, name="user_page"), # Страница профиля пользователя, где пользователь может просмотреть назначенные ему задачи
            path('task/<int:task_id>/edit/', views.UpdateView, name="task_edit"), # Страница для редактирования существующей задачи
            path('create_task/', views.create_task, name="create_task"), # Страница для создания новой задачи
            path('contact/', views.contact, name="contact"), # Страница для отправки сообщения админу
            path('contacts/', views.contacts, name="contacts"), # Страница со списком заявок, отправленных пользователем
            path('contacts/<int:pk>', views.delete_contact, name="delete-contact"), # Удаление заявки по её ID
            path('card_detail/<int:task_id>', views.card_detail, name="card_detail"), # Страница с подробной информацией о задаче
            path('profile/<int:pk>', views.hide_task, name="hide_task"), # Скрытие/отображение задачи по её ID
]
