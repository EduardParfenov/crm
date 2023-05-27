from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Tasks 

# Это определение формы для регистрации нового пользователя.
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User # Указывает, что модель, с которой мы связываем форму - это модель пользователей Django.
        fields = ['username', 'password1', 'password1']
        
# С помощью этой строки мы указываем, какие поля из модели User мы хотим использовать в форме.
 


class UpdateTaskForm(forms.ModelForm):
    # Создание поля для выбора пользователей, которым назначена задача
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # Запрос на выбор всех пользователей
        widget=forms.CheckboxSelectMultiple,  # Виджет для отображения выбора в виде чекбоксов
        required=False  # Поле не является обязательным для заполнения
    )

    class Meta:
        model = Tasks  # Модель Tasks, на основе которой создаётся форма
        fields = ('Standard', 'name', 'description', 'assigned_to')  # Поля модели, которые должны отображаться в форме

    def __init__(self, *args, **kwargs):
        super(UpdateTaskForm, self).__init__(*args, **kwargs)

        # Начальное значение поля "assigned_to" - пользователи, назначенные на эту задачу
        self.fields['assigned_to'].initial = self.instance.assigned_to.all()

    def save(self, commit=True):
        task = super(UpdateTaskForm, self).save(commit=False)

        if commit:
            task.save()

            task.assigned_to.clear()  # Удаление всех текущих пользователей, назначенных на задачу
            for user in self.cleaned_data['assigned_to']:  # Обход всех выбранных пользователей
                task.assigned_to.add(user)  # Добавление каждого выбранного пользователя к задаче
        #возвращаем задачи
        return task



class TaskFormAdd(forms.ModelForm):
    # Создаем поле формы assigned_to, в котором будем отображать все доступные для выбора пользователи
    assigned_to = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple())

    # Указываем, что моделью формы будет Tasks, а поля, которые должны быть в форме - Standard, name, description, assigned_to и file
    class Meta:
        #обращаемся к таблице Tasks и берем нужные нам поля
        model = Tasks
        fields = ['Standard', 'name', 'description', 'assigned_to', 'file']

        # Для поля description создаем виджет Textarea с указанием количества строк = 3
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),

            # Для поля file создаем виджет ClearableFileInput, который позволяет выбрать несколько файлов
            'file': forms.ClearableFileInput(attrs={'multiple': True})
        }
