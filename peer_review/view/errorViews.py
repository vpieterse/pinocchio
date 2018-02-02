from django.shortcuts import render


# HTTP Error 404
def page_not_found(request):
    context = {'navSelect': "accountDetails"}
    return render(request, 'peer_review/user404.html', context)
