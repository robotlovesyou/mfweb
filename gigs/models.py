from django.db import models


class Gig(models.Model):
    """
    Model to represent a live appearance
    """
    # Title/Location/Venue field. Single field for flexibility.
    title = models.CharField(max_length=200)
    # Date of live appearance
    date = models.DateField()
    # URL for venue/gig - optional
    url = models.URLField(blank=True)
    # Deleted?
    deleted = models.BooleanField(default=False)
