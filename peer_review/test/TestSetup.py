from datetime import datetime, timezone, timedelta
from peer_review.models import Questionnaire, RoundDetail, User, Question, FreeformItem, Choice, QuestionOrder, Response, \
    QuestionType, QuestionGrouping
import time


class TestSetup:
    def __init__(self):
        self.questionnaire = Questionnaire.objects.create(intro='Hello, this is a question',
                                                          label='This is a very unique label')

        start_date = datetime.now(timezone(timedelta(hours=2)))
        end_date = datetime.now(timezone(timedelta(hours=2)))

        self.round = RoundDetail.objects.create(name='test round', questionnaire=self.questionnaire,
                                                startingDate=start_date,
                                                endingDate=end_date,
                                                description='Hey there, we have a round')

        self.user = User.objects.create_user('bob@bob.com', 'bob', 'bob', 'simons', user_id=12345)
        self.user2 = User.objects.create_user('joe@gmail.com', 'joe', 'Smith', '12345', user_id=6789)

        self.question1 = Question.objects.create(questionText="Hey I'm a question number 1",
                                                 questionLabel="I'm the label",
                                                 pubDate=datetime.now(timezone(timedelta(hours=2))),
                                                 questionType=QuestionType.objects.create(name="Freeform"))
        FreeformItem.objects.create(question=self.question1, freeformType="Paragraph")

        self.question2 = Question.objects.create(questionText="Different question here",
                                                 questionLabel="I'm the label for the question",
                                                 pubDate=datetime.now(timezone(timedelta(hours=2))),
                                                 questionType=QuestionType.objects.create(name="Choice"))
        Choice.objects.create(question=self.question2, choiceText="choice 1", num="0")
        Choice.objects.create(question=self.question2, choiceText="choice 2", num="1")
        Choice.objects.create(question=self.question2, choiceText="choice 3", num="2")
        Choice.objects.create(question=self.question2, choiceText="choice 4", num="3")

        self.question3 = Question.objects.create(questionText="Hey I'm also a question",
                                                 questionLabel="I'm a label for this question",
                                                 pubDate=datetime.now(timezone(timedelta(hours=2))),
                                                 questionType=QuestionType.objects.create(name="Choice"))
        Choice.objects.create(question=self.question3, choiceText="Apples", num="0")
        Choice.objects.create(question=self.question3, choiceText="Oranges", num="1")
        Choice.objects.create(question=self.question3, choiceText="Kiwis", num="2")
        Choice.objects.create(question=self.question3, choiceText="Bananas", num="3")

        self.questionnaire = Questionnaire.objects.create(intro='Hello, this is a questionnaire',
                                                          label='This is the description')

        QuestionOrder.objects.create(questionnaire=self.questionnaire,
                                     question=self.question1,
                                     order=0)
        QuestionOrder.objects.create(questionnaire=self.questionnaire,
                                     question=self.question2,
                                     order=1)
        QuestionOrder.objects.create(questionnaire=self.questionnaire,
                                     question=self.question3,
                                     order=2)
        batch_num = 0
        Response.objects.create(question=self.question1,
                                roundDetail=self.round,
                                user=self.user,
                                subjectUser=self.user2,
                                label=None,
                                answer="We have an answer",
                                batch_id=str(int(time.time()*1000)) + str(batch_num))
        batch_num += 1
        Response.objects.create(question=self.question1,
                                roundDetail=self.round,
                                user=self.user,
                                subjectUser=self.user2,
                                label=None,
                                answer="We have a different answer",
                                batch_id=str(int(time.time()*1000)) + str(batch_num))
        batch_num += 1
        Response.objects.create(question=self.question2,
                                roundDetail=self.round,
                                user=self.user,
                                subjectUser=self.user2,
                                label=None,
                                answer="choice 1",
                                batch_id=str(int(time.time()*1000)) + str(batch_num))
        batch_num += 1
        Response.objects.create(question=self.question2,
                                roundDetail=self.round,
                                user=self.user,
                                subjectUser=self.user2,
                                label=None,
                                answer="choice 2",
                                batch_id=str(int(time.time()*1000)) + str(batch_num))
        batch_num += 1
        Response.objects.create(question=self.question3,
                                roundDetail=self.round,
                                user=self.user,
                                subjectUser=self.user2,
                                label=None,
                                answer="Apples",
                                batch_id=str(int(time.time()*1000)) + str(batch_num))
        batch_num += 1
        Response.objects.create(question=self.question3,
                                roundDetail=self.round,
                                user=self.user,
                                subjectUser=self.user2,
                                label=None,
                                answer="Bananas",
                                batch_id=str(int(time.time()*1000)) + str(batch_num))
        batch_num += 1

        User.objects.create_superuser('admin', 'admin', user_id=str(1111))