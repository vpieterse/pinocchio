from django.contrib import admin

from .models import QuestionType, QuestionGrouping, Question, Header, Choice, User, UserDetail, Questionnaire, RoundDetail, TeamDetail

admin.site.register(QuestionType)
admin.site.register(QuestionGrouping)
admin.site.register(Question)
admin.site.register(Header)
admin.site.register(Choice)
admin.site.register(User)
admin.site.register(UserDetail)
admin.site.register(Questionnaire)
admin.site.register(RoundDetail)
admin.site.register(TeamDetail)