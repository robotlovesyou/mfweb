# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def admin(request):
    return HttpResponse("Welcome to the admin page")
