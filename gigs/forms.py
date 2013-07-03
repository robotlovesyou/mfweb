from django.forms import ModelForm
from django.forms.widgets import TextInput

from gigs.models import Gig
from gigs.widgets import MFWebDateInput


class GigForm(ModelForm):
    """
    Form for the Gig model
    """
    class Meta:
        model = Gig
        fields = ('title', 'date', 'url')
        widgets = {
            'date': MFWebDateInput(),
            'title': TextInput(),
            'url': TextInput()
        }
