from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import EmailValidator

# Create your models here.

#majors for engineering for now
#Architecture
#Bioengineering
#Chemical Engineering
#Civil Engineering
#Computer Engineering
#Electrical Engineering
#Materials Engineering
#Mechanical Engineering
#Mining Engineering
#Software Engineering
class Major(models.Model):
    MAJORS = (  # enum of options of majors
        ('architecture', 'Architecture'),
        ('bioengineering', 'Bioengineering'),
        ('chemical_engineering', 'Chemical Engineering'),
        ('civil_engineering', 'Civil Engineering'),
        ('computer_engineering', 'Computer Engineering'),
        ('electrical_engineering', 'Electrical Engineering'),
        ('materials_engineering', 'Materials Engineering'),
        ('mechanical_engineering', 'Mechanical Engineering'),
        ('mining_engineering', 'Mining Engineering'),
        ('software_engineering', 'Software Engineering')
    )
    FACULTIES = (
        ('engineering', 'Engineering'),
        ('science', 'Science'),
        ('arts', 'Arts'),
        ('education', 'Education'),
    )
    name = models.CharField(max_length=70, choices=MAJORS, default='architecture', primary_key=True) ##ensures only one of each major
    faculty = models.CharField(max_length=70, choices=FACULTIES, default='engineering')
    def __str__(self):
        return ("%s" % (self.name))

class Course(models.Model): ##A course belongs to many majors. Many courses belong to the same major. Therefore many to many
    COURSES = (  # enum of options of courses
        ('comp_250', 'COMP 250'),
        ('ecse_428', 'ECSE 428'),
        ('ecse_322', 'ECSE 322'),
        ('ecse_330', 'ECSE 330'),
        ('math_363', 'MATH 363')
    )
    name = models.CharField(max_length=70, choices=COURSES, primary_key=True)
    majors = models.ManyToManyField(Major)

    def __str__(self):
        return (self.name)

class FBUser(models.Model):

    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    user_id = models.SlugField(default='', max_length=16, validators=[MinLengthValidator(16)]) #contains only letters, numbers, underscores, or hyphens, usually used in URLs
    user_type = models.CharField(max_length=70, null=True)
    mcgill_email = models.EmailField(default='', max_length=254, validators=[EmailValidator(message="Please enter a valid McGill email address.", whitelist="mcgill.ca")])
    authentication_status = models.CharField(default='authentication_no', max_length=20)
    code = models.SlugField(default='', max_length=20)
    timezone = models.IntegerField()

    major = models.ForeignKey(Major, on_delete=models.CASCADE, null=True);
    courses = models.ManyToManyField(Course) ##no special tricks, we allow FBUser to take courses outside of their major (for simplicity and this also happens to be the case)

    def __str__(self):
        return ("%s %s" % (self.first_name , self.last_name))

    def set_user_type(self, user_type):
        self.user_type = user_type
        self.save()

class StudentSociety(models.Model):
    fbuser = models.ForeignKey(FBUser, on_delete=models.CASCADE)
    def __str__(self):
        return ("%s" % (self.fbuser.first_name))

class Admin(models.Model):
    fbuser = models.ForeignKey(FBUser, on_delete=models.CASCADE)
    def __str__(self):
        return ("%s" % (self.fbuser.first_name))

class Conversation(models.Model):
    fbuser = models.ForeignKey(FBUser, on_delete=models.CASCADE)
    question = models.PositiveIntegerField()

    def __str__(self):
        return ("%s %s" % (self.fbuser.first_name , self.question))

    def set_conversation_question(self, question):
        self.question = question
        self.save()

class EventType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    def __str__(self):
        return ("%s" % (self.name))

class Event(models.Model):
    id = models.SlugField(max_length=25, primary_key=True)
    name = models.CharField(max_length=70, null=True)
    category = models.CharField(max_length=100, null=True)
    link = models.CharField(max_length=300, null=True)
    creator = models.ForeignKey(StudentSociety, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    event_time = models.DateTimeField(null=True)

    types = models.ManyToManyField(EventType)

    def __str__(self):
        return ("%s" % (self.name))
