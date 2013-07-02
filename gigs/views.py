# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from gigs.models import Gig
from gigs.forms import GigForm


@login_required
def admin(request):
    return HttpResponse("Welcome to the admin page")


class GigCreateView(CreateView):
    """
    Admin View to create gigs
    """
    model = Gig
    form_class = GigForm
    success_url = reverse_lazy('gigs:admin')

    def form_valid(self, form):
        """
        Set a success flash and then forward the form
        """
        messages.success(self.request, 'Gig Created')
        return super(CreateView, self).form_valid(form)
