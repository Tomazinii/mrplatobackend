# from django.contrib import admin

# # Register your models here.
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import PhotoUser, UserAccount,RegisterStudents

# # admin.site.register(UserAccount)
# admin.site.register(RegisterStudents)
# admin.site.register(PhotoUser)


# class UserAdmin(BaseUserAdmin):
#     list_display = ("username", "email","matriculation","score_user")
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("username","email", "password1", "password2"),
#             },
#         ),
#     )

#     fieldsets = (
#         (None, {'fields': ('username', 'email','password')}),
#         ('Permissions', {'fields': ('score_user',)}),


#     )
    
    

#     list_filter = ("matriculation", "score_user", "email")
#     search_fields = ("username", "first_name", "last_name", "email")
#     ordering = ("username",)
#     filter_horizontal = (
#         "groups",
#         "user_permissions",
#     )
# # Re-register UserAdmin
# admin.site.register(UserAccount, UserAdmin)


# from rest_framework_simplejwt import token_blacklist

# class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

#     def has_delete_permission(self, *args, **kwargs):
#         return True # or whatever logic you want

# admin.site.unregister(token_blacklist.models.OutstandingToken)
# admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)

# from .models import Score
# admin.site.register(Score)