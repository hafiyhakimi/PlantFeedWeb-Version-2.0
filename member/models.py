from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class PersonManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
class Person(AbstractBaseUser, PermissionsMixin):
    Email = models.CharField(max_length=150, unique=True)
    Pass = models.CharField(max_length=150, default='')
    Username = models.CharField(max_length=150)
    Name = models.CharField(max_length=150)
    DateOfBirth = models.CharField(max_length=150)
    Age = models.IntegerField ()
    District = models.CharField(max_length=150)
    State = models.CharField(max_length=150)
    Occupation = models.CharField(max_length=150)
    About = models.CharField(max_length=150)
    Gender = models.CharField(max_length=1)
    MaritalStatus = models.CharField(max_length=150)
    UserLevel = models.CharField(max_length=10)
    
    objects = PersonManager()
    
    USERNAME_FIELD = 'Email'

    def upload_photo(self, filename):
        path = 'images/{}'.format(filename)
        return path

    Photo = models.ImageField(upload_to='images/', null=True, blank=True)

    class Meta:
        db_table = 'login_person'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.pk = None
    
    def user_form(sender, instance, created, **kwargs):
        if created:
            Person.objects.create(user=instance)
            instance.Person.save()
            
# class Person(models.Model):
#     Email = models.CharField(max_length=150, unique=True)
#     Password = models.CharField(max_length=150)
#     Username = models.CharField(max_length=150)
#     Name = models.CharField(max_length=150)
#     DateOfBirth = models.CharField(max_length=150)
#     Age = models.IntegerField ()
#     District = models.CharField(max_length=150)
#     State = models.CharField(max_length=150)
#     Occupation = models.CharField(max_length=150)
#     About = models.CharField(max_length=150)
#     Gender = models.CharField(max_length=1)
#     MaritalStatus = models.CharField(max_length=150)
#     UserLevel = models.CharField(max_length=10)

#     def upload_photo(self, filename):
#         path = 'images/{}'.format(filename)
#         return path

#     Photo = models.ImageField(upload_to='images/', null=True, blank=True)

#     class Meta:
#         db_table = 'login_person'
        
#     def save(self):
#         super().save()
#         self.pk=None
    
#     def user_form(sender, instance, created, **kwargs):
#         if created:
#             Person.objects.create(user=instance)
#             instance.Person.save()

class MemberRequest(models.Model):

    class Meta:
        db_table = 'MemberRequest'
        # unique_together = [['to_user', 'from_user']]
    
    timestamp = models.DateTimeField(auto_now_add=True)
    to_user = models.ForeignKey(Person, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(Person, related_name='from_user', on_delete=models.CASCADE)
	

    def save(self):
        super().save()
        #super().save(using='farming')

    #def deleteRecordFarming(self):
    #    super().delete(using='farming')
        
    def deleteRecordIgrow(self):
        super().delete()

    class Meta:
        unique_together = [['to_user', 'from_user']]

class Room(models.Model):
    
    member1 = models.ForeignKey(Person, related_name='member1', on_delete=models.SET_NULL, null=True)
    member2 = models.ForeignKey(Person, related_name='member2', on_delete=models.SET_NULL, null=True)

    def save(self):
        super().save()
        #super().save(using='farming')
        return self.id
    

class Memberlist(models.Model):

    from_person = models.ForeignKey(Person, related_name='from_person', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person, related_name='to_person', on_delete=models.CASCADE)
    chatRoom = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    def save(self):
        super().save()
        #super().save(using='farming')

    #def deleteRecordFarming(self):
    #    super().delete(using='farming')
        
    def deleteRecordIgrow(self):
        super().delete()

    class Meta:
        
        unique_together = [['from_person', 'to_person']]



class Message(models.Model):
    value = models.TextField()
    date = models.DateTimeField(default=datetime.now, blank=True)
    sender = room = models.CharField(max_length=255)
    # sender = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    def save(self):
        super().save()
        #super().save(using='farming')
    


class SensorData(models.Model):
    class Meta:
        db_table = 'SensorData'    
    Detail = models.CharField(max_length=255)
    Name = models.CharField(max_length=150)

class Plants(models.Model):
    class Meta:
        db_table = 'Plants'
    Pictures = models.ImageField(upload_to='uploads/')
    Species = models.CharField(max_length=150)
    Types = models.CharField(max_length=150)


class Users(models.Model):
    username = models.CharField(max_length=10, unique=True) #AI190201
    password = models.CharField(max_length=30) #ninja saga
    name = models.CharField(max_length=100) #FAIZ BIN AB. HAMID
    age = models.IntegerField() #22
    ranking = models.FloatField() #2.5

    def upload_photo(self, filename):
        path = 'LOGIN/photo/{}'.format(filename)
        return path

    photo = models.ImageField(upload_to=upload_photo, null=True, blank=True)

    def upload_file(self, filename):
        path = 'LOGIN/file/{}'.format(filename)
        return path

    resume = models.ImageField(upload_to=upload_file, null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.password}"


class SoilTag(models.Model):
    
    class Meta:
        db_table = 'SoilTag'  

    SoilTagName = models.CharField(max_length=50, unique=True)

    def save(self):
        super().save()
        super().save(using='farming')

    def deleteRecordFarming(self):
        super().delete(using='farming')
        
    def deleteRecordIgrow(self):
        super().delete()


class PlantTag(models.Model):
    
    class Meta:
        db_table = 'PlantTag'  

    PlantTagName = models.CharField(max_length=50, unique=True)

    def save(self):
        super().save()
        super().save(using='farming')

    def deleteRecordFarming(self):
        super().delete(using='farming')
        
    def deleteRecordIgrow(self):
        super().delete()



    
