# -----------------------------------------------------------------------------
# Module: dpa.locations.models
# Author: Josh Tomlinson (jtomlin)
# -----------------------------------------------------------------------------
"""Defines all models for dpa filesystem locations."""

# -----------------------------------------------------------------------------
# Imports:
# -----------------------------------------------------------------------------
 
from django.db import models

# -----------------------------------------------------------------------------
# Public Classes: 
# -----------------------------------------------------------------------------
class Location(models.Model):
    """Identifies a location where the dpa pipeline is running.
    
    Locations are outlined by filesystem boundaries.   
    
    """

    # ------------------------------------------------------------------------
    # Fields:
    # ------------------------------------------------------------------------
    code = models.CharField(
        max_length=32,
        primary_key=True,
        help_text="A unique code name for this location.",
    )

    name = models.CharField(
        max_length=32,
        help_text="A short descriptive name for this location.",
    )    

    description = models.CharField(
        max_length=256,
        help_text="A longer description of this location.",
    )

    timezone = models.CharField(
        max_length=32,
        help_text="The timezone of this location."
    )    

    latitude = models.FloatField(
        help_text="The latitude of the location."
    )

    longitude = models.FloatField(
        help_text="The longitutde of the location."
    )

    active = models.BooleanField(
        default=True,
        help_text="True if the location is active, False otherwise.",
    )

    host = models.CharField(
        blank=True,
        max_length=256,
        help_text="Host name for this location.",
    )    

    filesystem_root = models.CharField(
        max_length=1024,
        help_text="Root path to this locations ptask hierarchy.",
    )    

    # ------------------------------------------------------------------------
    # Special Methods:
    # ------------------------------------------------------------------------
    def __unicode__(self):
        return unicode(self.name)

    # ------------------------------------------------------------------------
    class Meta:
        managed = True

