from django.contrib import admin
from adapter import admin_adapter
from composer import register_list_exercise_compisite
from django.contrib import messages
from .models import ListExerciseModel


class ListExerciseAdmin(admin.ModelAdmin):

    def save_model(self, request: any, obj: any, form: any, change: any):

        response = admin_adapter(request, register_list_exercise_compisite())

        if response.status_code < 300:
            return super().save_model(request, obj, form, change)
        else:
            messages.error(request, f"Erro ao registrar Exercicios: {response.body}")


admin.site.register(ListExerciseModel, ListExerciseAdmin)