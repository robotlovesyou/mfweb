from django.core.cache import cache
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


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

    def all_future_gigs(self):
        """
        return a queryset selecting all future gigs
        """
        return self.filter(
            deleted=False,
            date__gt=timezone.now()).order_by('date')


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

    def delete(self):
        self.deleted = True
        self.save()


@receiver(pre_save, sender=Gig)
def clear_cache_on_gig_save(sender, **kwargs):
    """
    Clear the entire cache on model save. (Pretty blunt but updates are rare)
    """
    cache.clear()
