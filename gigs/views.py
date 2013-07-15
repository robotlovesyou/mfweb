# Create your views here.
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic.base import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from gigs.models import Gig
from gigs.forms import GigForm


def csrf_render_to_response(request, template, context):
    """
    Include the csrf token in a render to response call
    """
    context.update(csrf(request))
    return render_to_response(template, context)


class HomePageView(ListView):
    context_object_name = 'gigs'
    queryset = Gig.objects.all_future_gigs()[:5]
    template_name = 'gigs/home.html'


class AllGigsView(ListView):
    context_object_name = 'gigs'
    queryset = Gig.objects.all_future_gigs()
    template_name = 'gigs/all.html'


class GigAdminListView(ListView):
    context_object_name = 'gigs'
    queryset = Gig.objects.all_future_gigs()
    template_name = 'gigs/admin_gig_list.html'


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


class GigUpdateView(UpdateView):
    """
    Admin View to edit gigs
    """
    model = Gig
    form_class = GigForm
    success_url = reverse_lazy('gigs:admin')


class GigDeleteView(View):
    """
    Admin View to delete gigs
    """
    template_name = 'gigs/gig_confirm_delete.html'
    success_url = reverse_lazy('gigs:admin')

    def dispatch(self, request, *args, **kwargs):
        self.gig = get_object_or_404(Gig, pk=kwargs['pk'])
        return super().dispatch(request, args, kwargs)

    def get(self, request, *args, **kwargs):
        return csrf_render_to_response(
            request,
            self.template_name,
            {'gig': self.gig}
        )

    def post(self, request, *args, **kwargs):
        self.gig.deleted = True
        self.gig.save()
        return redirect(reverse('gigs:admin'))

