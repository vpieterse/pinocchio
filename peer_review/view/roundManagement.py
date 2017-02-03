from django.shortcuts import render
from peer_review.decorators.adminRequired import admin_required

from peer_review.models import RoundDetail, Questionnaire


@admin_required
def maintain_round(request):
    context = {'roundDetail': RoundDetail.objects.all(),
               'questionnaires': Questionnaire.objects.all()}
    return render(request, 'peer_review/maintainRound.html', context)