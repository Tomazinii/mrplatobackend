# from django.dispatch import receiver
# from django.db.models.signals import post_save
# import json
# import re
# from rest_framework.response import Response
# from django.http import HttpResponseNotModified
# from infra.user.models import RegisterStudents,UserAccount,PhotoUser
# from django.core.mail import send_mail
# from django.conf import settings

# from .list_email import create_list_email



# @receiver(post_save, sender=UserAccount)
# def my_call_photo(sender,instance,created,**kwargs):
#     if created:
#         PhotoUser.objects.create(user=instance)
                


# @receiver(post_save, sender=RegisterStudents)
# def my_call(sender,instance,created,**kwargs):
    
#     if created and create_list_email() != None:
        
#         archive = instance.archive.open()
#         data = json.load(archive)


#         for z in data["dict"]:
#             try:
#                 txt = str(z["name"])
#                 nickname = txt.split()[0]
#                 user = UserAccount.objects.create_superuser(email=z["email"],username=z["name"],password=str(z["matricula"]),matriculation=z["matricula"],nickname=nickname)
#                 user.is_superuser = False
#                 user.save()
#             except:
#                 print("erro")
            
                

#         message = "Welcome to Mrplato Platform. The Password is your matriculation. Good studies!"
#         send_mail(subject="You have been successfully registered in mrplato", message = message, from_email=settings.EMAIL_HOST_USER,recipient_list=create_list_email())


        
