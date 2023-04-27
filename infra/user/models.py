from django.db import models

from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        extra_fields.setdefault('is_staff', True)
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
          extra_fields.setdefault('is_staff', True)
          extra_fields.setdefault('is_superuser', True)
          if extra_fields.get('is_staff') is not True:
              raise ValueError('SuperUser must have is_staff=True')
          if extra_fields.get('is_superuser') is not True:
              raise ValueError('Superuser must have is_superuser=True.') 
          return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    nickname = models.CharField(max_length=50)
    matriculation = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    online = models.BooleanField(default=False)
    score_user = models.FloatField(default=0)
    turma = models.ForeignKey("turma.Class", on_delete=models.CASCADE, null=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
    
    def __str__(self):
        return self.email



class Score(models.Model):
    type = models.CharField(max_length=50)
    question_id = models.IntegerField()
    user_score = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    acert = models.BooleanField(default=False)
    tried = models.BooleanField(default=False)
    data = models.JSONField(null=True,blank=True)


    def __str__(self) -> str:
        return f"{self.type} - {self.question_id}"


class RegisterStudents(models.Model):
    turma = models.ForeignKey("turma.Class", on_delete=models.CASCADE)
    archive = models.FileField(upload_to=None, max_length=255)

    def __str__(self):
        return f"{self.turma}"


class PhotoUser(models.Model):
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    photo = models.FileField(upload_to="user", blank=True, default="user/userimage.png")
