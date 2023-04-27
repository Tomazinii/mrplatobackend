import json
from django.contrib.auth.admin import UserAdmin
from infra.user.models import UserAccount
from django.contrib import admin
from adapter import admin_adapter
from infra.user.models import RegisterStudents
from composer import register_user_composer
from django.contrib import messages


class CustomUserAdmin(UserAdmin):

    list_display = ("username", "email","turma","score_user")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username","email", "password1", "password2","turma"),
            },
        ),
    )

    fieldsets = (
        (None, {'fields': ('username', 'email','password',"turma","is_staff","is_superuser","is_active")}),
        ('Permissions', {'fields': ('score_user',)}),


    )
    
    

    list_filter = ("turma", "score_user", "email")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

admin.site.register(UserAccount, CustomUserAdmin)


class CustomRegisterUsers(admin.ModelAdmin):
    
    def save_model(self, request: any, obj: any, form: any, change: any) -> None:
        
        response = admin_adapter(request, register_user_composer())

        if response.status_code < 300:
            return messages.SUCCESS
        else:
            messages.error(request, f"Erro ao registrar usuários: {response.body}")
    

admin.site.register(RegisterStudents,CustomRegisterUsers)


from rest_framework_simplejwt import token_blacklist

class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)
