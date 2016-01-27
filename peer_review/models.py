from datetime import datetime

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
    topWord = models.CharField(max_length=25)
    bottomWord = models.CharField(max_length=25)
    optional = models.BooleanField(default=False)

class Label(models.Model):
    question = models.ForeignKey(Question)
    labelText = models.CharField(max_length=200)

    def __str__(self):
        return self.labelText

class User(models.Model):
    title = models.CharField(max_length=4)
    initials = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    cell = models.CharField(max_length=10)
    email = models.CharField(max_length=60)
    userId = models.CharField(max_length=8, unique=True)
    OTP = models.BooleanField(default=True)
    status = models.CharField(max_length=1)

    def __str__(self):
        return self.userId + " - " + self.surname + " " + self.initials


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
    name = models.CharField(max_length = 15, unique=True)
    questionnaire = models.ForeignKey(Questionnaire, null =True)
    startingDate = models.DateTimeField('starting date')
    endingDate = models.DateTimeField('ending date')
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.description


class TeamDetail(models.Model):
    user = models.ForeignKey(User, null=False)
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
        return self.roundDetail.description + " " + self.teamName + " (" + self.user.surname + ", " + self.user.initials + ")"

class Response(models.Model):
    question = models.ForeignKey(Question)                                      #The question
    roundDetail = models.ForeignKey(RoundDetail)                                #The round
    user = models.ForeignKey(User, null=False, related_name="user")             #The answererer
    otherUser = models.ForeignKey(User, null=False, related_name="otherUser")   #The person the question is about.
    label = models.ForeignKey(Label)                                            #The label the question is about.
    answer = models.CharField(max_length=300)                                   #Answer to the question

    def __str__(self):
        return self.pk + ' ' + self.user.userId + ' ' + self.otherUser.userId + ' ' + self.label + ' ' + self.answer + ' ' + self.question.pk


