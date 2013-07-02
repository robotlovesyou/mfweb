from django.forms import ModelForm

from gigs.models import Gig


class GigForm(ModelForm):
    """
    Form for the Gig model
    """
    class Meta:
        model = Gig
