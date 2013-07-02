from django.forms.widgets import DateInput


class MFWebDateInput(DateInput):
    """
    HTML5 Date input
    """
    input_type = 'date'
