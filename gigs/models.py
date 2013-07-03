from django.db import models


class GigManager(models.Manager):
    """
    Manager class for Gig model
    """
    def create_gig(self, title, date, url=''):
        """
        Convenience method to create and save a gig in a single step
        """
        gig = self.model(
            title=title,
            date=date,
            url=url
        )
        gig.save()
        return gig


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

    #Set the custom manager object
    objects = GigManager()
