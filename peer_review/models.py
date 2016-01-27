from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.management import call_command
from django.db import models
from django.utils import timezone


class Document(models.Model):
    docfile = models.FileField(upload_to='documents')


class QuestionType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class QuestionGrouping(models.Model):
    grouping = models.CharField(max_length=10)

    def __str__(self):
        return self.grouping


class Question(models.Model):
    questionText = models.CharField(max_length=1000)
    questionLabel = models.CharField(max_length=300, unique=True)
    pubDate = models.DateTimeField('date published')
    questionType = models.ForeignKey(QuestionType)
    questionGrouping = models.ForeignKey(QuestionGrouping)

    def __str__(self):
        return self.questionText

    def was_published_recently(self):
        return self.pubDate >= timezone.now() - datetime.timedelta(days=1)

    @staticmethod
    def make_dump():
        output = open("dump", 'w')  # Point stdout at a file for dumping data to.
        call_command('dumpdata', 'Question', format='json', indent=4, stdout=output)
        output.close()


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choiceText = models.CharField(max_length=200)
    num = models.IntegerField(default=1)

    def __str__(self):
        return self.choiceText


class FreeformItem(models.Model):
    question = models.ForeignKey(Question)
    value = models.CharField(max_length=200)
    freeformType = models.CharField(max_length=10)

    def __str__(self):
        return self.value


class Rank(models.Model):
    question = models.ForeignKey(Question)
    firstWord = models.CharField(max_length=200)
    secondWord = models.CharField(max_length=200)

    def __str__(self):
        return self.firstWord + " - " + self.secondWord


class Rate(models.Model):
    question = models.ForeignKey(Question)
    numberOfOptions = models.IntegerField(default=5)
    optional = models.BooleanField(default=False)
    num = models.IntegerField(default=0)


class Label(models.Model):
    question = models.ForeignKey(Question)
    labelText = models.CharField(max_length=200)

    def __str__(self):
        return self.labelText


class UserDetail(models.Model):
    title = models.CharField(max_length=4)
    initials = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    cell = models.CharField(max_length=10)
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return self.surname + " " + self.initials


class User(AbstractBaseUser, PermissionsMixin):
    userId = models.CharField(max_length=8, unique=True)
    password = models.CharField(max_length=100)
    OTP = models.BooleanField(default=True)
    status = models.CharField(max_length=1)
    userDetail = models.OneToOneField(
            UserDetail,
            on_delete=models.CASCADE
    )

    USERNAME_FIELD = 'userDetail.email'
    # TODO Add more required fields maybe
    #REQUIRED_FIELDS = ['status']

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, help_text=_(
        'Designates whether this user should be treated as '
        'active. Unselect this instead of deleting accounts.'))

    objects = UserManager()

    # TODO Perhaps change this
    def get_full_name(self):
        """Return the email."""
        return self.userDetail.email

    def get_short_name(self):
        """Return the email."""
        return self.userDetail.email

    def __str__(self):
        return self.userDetail.email + " - " + self.userDetail.surname + " " + self.userDetail.initials

class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class Questionnaire(models.Model):
    intro = models.CharField(max_length=1000)
    label = models.CharField(max_length=300, unique=True)
    questionOrders = models.ManyToManyField(Question, through='QuestionOrder')

    def __str__(self):
        return self.label

class QuestionOrder(models.Model):
    questionnaire = models.ForeignKey(Questionnaire)
    question = models.ForeignKey(Question)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.question.questionLabel

class RoundDetail(models.Model):
    name = models.CharField(max_length = 15)
    questionnaire = models.ForeignKey(Questionnaire, null =True)
    startingDate = models.DateTimeField('starting date')
    endingDate = models.DateTimeField('ending date')
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.description


class TeamDetail(models.Model):
    userDetail = models.ForeignKey(UserDetail, null=True)
    roundDetail = models.ForeignKey(RoundDetail)
    teamName = models.CharField(max_length=200, default="emptyTeam")
    NOT_ATTEMPTED = "NA"
    IN_PROGRESS = "IP"
    COMPLETED = "C"
    STATUS_CHOICES = (
        (NOT_ATTEMPTED, "Not attempted"),
        (IN_PROGRESS, "In progress"),
        (COMPLETED, "Completed")
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_ATTEMPTED)

    def __str__(self):
        return self.roundDetail.description + " " + self.teamName + " (" + self.userDetail.surname + ", " + self.userDetail.initials + ")"
