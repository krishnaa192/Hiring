from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
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
        return self.create_user(email, password, **extra_fields)
    

    
# Create your models here.
class Profile(AbstractBaseUser,PermissionsMixin):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100,unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)



    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    def __str__(self):
        return self.name




class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Candidate(models.Model):
    id=models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE ,null=True)
    phone = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    current_ctc = models.CharField(max_length=100 ,default=None)
    expected_ctc = models.CharField(max_length=100)
    graduated_from = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    skills = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resume',null=True)
   # Many-to-many relationship with Skill model


    def __str__(self):
        return self.profile.name
    
class Recruiter(models.Model):
    comany_id=models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    logo=models.ImageField(upload_to='logo')
    about_company = models.TextField()
    company_address = models.CharField(max_length=100)
    company_website = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name
    
class Job(models.Model):
    id=models.AutoField(primary_key=True)
    job_types=[
        ('Full Time','Full Time'),
        ('Part Time','Part Time'),
        ('Internship','Internship'),
    ]
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.CharField(max_length=22)
    posted_on = models.DateTimeField(auto_now_add=True)
    experience = models.CharField(max_length=100)
    job_type=models.CharField(choices=job_types,max_length=100)
    


    def __str__(self):
        return self.title
    
    
class Apply(models.Model):
    id=models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='profile',null=True)
    candidate_detail = models.ForeignKey(Candidate, on_delete=models.CASCADE,null=True)
    recruiter_detail = models.ForeignKey(Recruiter, on_delete=models.CASCADE,null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    about = models.TextField(help_text="Why should we hire you")
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profile.name+" applied for "+self.recruiter_detail.company_name+" "+"for the post"+" "+self.job.title

