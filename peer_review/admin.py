from django.contrib import admin

from .models import QuestionType, QuestionGrouping, Question, Choice, Rank, Rate, User, Questionnaire, \
    RoundDetail, TeamDetail, Label, QuestionOrder, FreeformItem

admin.site.register(QuestionType)
admin.site.register(QuestionGrouping)
admin.site.register(QuestionOrder)
admin.site.register(Question)
admin.site.register(Rank)
admin.site.register(Rate)
admin.site.register(Choice)
admin.site.register(User)
admin.site.register(Questionnaire)
admin.site.register(RoundDetail)
admin.site.register(TeamDetail)
admin.site.register(Label)
admin.site.register(FreeformItem)