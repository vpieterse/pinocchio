from django.shortcuts import render

from peer_review.models import RoundDetail, Questionnaire


def maintain_round(request):
    context = {'roundDetail': RoundDetail.objects.all(),
               'questionnaires': Questionnaire.objects.all()}
    return render(request, 'peer_review/maintainRound.html', context)