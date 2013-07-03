from datetime import date
from django.forms.widgets import DateInput


class MFWebDateInput(DateInput):
    """
    HTML5 Date input
    """
    input_type = 'date'

    def _format_value(self, value):
        """
        Format the date to an RFC3339 full-date
        """
        if(type(value) == date):
            return value.strftime('%Y-%m-%d')
        else:
            return super(DateInput, self)._format_value(value)
