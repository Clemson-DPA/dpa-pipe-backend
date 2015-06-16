# -----------------------------------------------------------------------------
# Module: dpa.ptasks.models
# Author: Josh Tomlinson (jtomlin)
# -----------------------------------------------------------------------------
"""Defines all models for dpa ptasks.
 
Classes
-------
 
PTask
    Project tasks
PTaskAssignment
    User assignments to ptasks
PTaskType
    Predefined types for ptasks
PTaskVersion
    Versions of a PTask
 
"""

# ----------------------------------------------------------------------------
# Imports:
# ----------------------------------------------------------------------------

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

# utility app to handle hierarchical models efficiently
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from locations.models import Location

# ----------------------------------------------------------------------------
# Globals
# ----------------------------------------------------------------------------

SPEC_SEPARATOR = '='

# ----------------------------------------------------------------------------
# Public Classes:
# ----------------------------------------------------------------------------
class PTaskType(models.Model):

    # ------------------------------------------------------------------------
    # Fields:
    # ------------------------------------------------------------------------
    name = models.CharField(
        max_length=32,
        primary_key=True,
        help_text='The name of this ptask type.'
    )

    description = models.CharField(
        max_length=1024,
        help_text='A description of what this ptask type is used for.'
    )

    level_hint =  models.IntegerField(
        default=1,
        help_text='An integer indicating the level of a ptask'
    )

    # ------------------------------------------------------------------------
    # Special methods:
    # ------------------------------------------------------------------------
    def __unicode__(self):
        return unicode(self.name)

    # ------------------------------------------------------------------------
    # Internal classes:
    # ------------------------------------------------------------------------
    class Meta:
        managed = True
        verbose_name = 'Type'
        verbose_name_plural = 'Types'

# ----------------------------------------------------------------------------
class PTask(MPTTModel):

    # status choices enum
    READY_TO_BEGIN = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    ON_HOLD = 3

    # ------------------------------------------------------------------------
    # Fields:
    # ------------------------------------------------------------------------
    # XXX create a separate table for these
    # XXX maybe include an RGB for each ?
    STATUS_CHOICES = (
        (READY_TO_BEGIN, 'Ready To Begin'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (ON_HOLD, 'On Hold')
    )

    parent = TreeForeignKey(
        'self',
        db_index=True,
        help_text='The parent ptask of this ptask.',
        blank=True,
        null=True,
        related_name='children',
    )

    name = models.CharField(
        max_length=128,
        db_index=True,
        help_text='The name of this ptask.',
    )

    ptask_type = models.ForeignKey(
        PTaskType,
        help_text='The type of this ptask.',
    )

    description = models.CharField(
        max_length=1024,
        help_text='A description of this ptask.',
    )

    creator = models.ForeignKey(
        User,
        help_text='The creator of this ptask.',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        help_text='The date this ptask was created.',
    )

    start_date = models.DateField(
        help_text='The date work is to be started on this ptask.',
    )

    due_date = models.DateField(
        help_text='The date work is to be completed on this ptask.',
    )

    priority = models.IntegerField(
        default=50,
        help_text='PTask priority. Lower number means higher priority.',
    )

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=READY_TO_BEGIN,
        help_text='The status of work being done on this ptask.',
    )

    active = models.BooleanField(
        default=True,
        help_text='True if ptask is active, False otherwise.',
    )

    spec = models.CharField(
        max_length=1024,
        help_text='Specification for this ptask.',
        blank=True,
        editable=False,
    )

    # ------------------------------------------------------------------------
    # Internal classes:
    # ------------------------------------------------------------------------
    class Meta:
        managed = True
        verbose_name = 'PTask'
        verbose_name_plural = 'PTasks'
        index_together = [['parent', 'name'],]
        unique_together = (('parent', 'name'),)

    # ------------------------------------------------------------------------
    # Special methods:
    # ------------------------------------------------------------------------
    def __unicode__(self):
        return unicode(self.spec)

    # ------------------------------------------------------------------------
    # Public methods:
    # ------------------------------------------------------------------------
    def save(self, *args, **kwargs):
        """Make sure the spec is set properly."""

        force_update = kwargs.pop('force_update', False)

        if not force_update and self.parent is None:
            # postgres doesn't use a unique value for NULL. so need to make
            # sure there isn't a top-level ptask with this name.
            top_level_ptasks = PTask.objects.filter(parent=None)
            if self.name in [t.name for t in top_level_ptasks]:
                raise ValidationError(
                    "{t} already exists with the name: '{n}'".format(
                        t=self.ptask_type, n=self.name)
                )

        # populate the spec field
        if self.parent and self.parent.spec:
            self.spec = SPEC_SEPARATOR.join([
                self.parent.spec,
                self.name,
            ])
        else:
            self.spec = self.name 

        super(PTask, self).save()

# ----------------------------------------------------------------------------
class PTaskAssignment(models.Model):

    # ------------------------------------------------------------------------
    # Fields
    # ------------------------------------------------------------------------
    ptask = models.ForeignKey(
        PTask,
        help_text='The ptask to assign a user to.',
        related_name="assignments",
    )

    user = models.ForeignKey(
        User,
        help_text='The user to assign to the ptask.',
    )

    start_date = models.DateField(
        blank=True,
        null=True,
        help_text='The start date for this user on this ptask.',
    )

    end_date = models.DateField(
        blank=True,
        null=True,
        help_text='The end date for this user on this ptask.',
    )

    active = models.BooleanField(
        default=True,
        help_text='True if ptask is active, False otherwise.',
    )

    spec = models.CharField(
        max_length=1024,
        help_text='Specification for this ptask assignment.',
        blank=True,
        editable=False,
    )

    # ------------------------------------------------------------------------
    # Internal classes:
    # ------------------------------------------------------------------------
    class Meta:
        managed = True
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
        unique_together = (('ptask', 'user'),)

    # ------------------------------------------------------------------------
    # Special methods:
    # ------------------------------------------------------------------------
    def __unicode__(self):
        return unicode(self.ptask.name + ':' + self.user.username)

    # ------------------------------------------------------------------------
    # Public methods:
    # ------------------------------------------------------------------------
    def save(self, *args, **kwargs):
        """Make sure the spec is set properly."""

        self.spec = self.ptask.spec + ',' + self.user.username

        super(PTaskAssignment, self).save(*args, **kwargs) 

# ----------------------------------------------------------------------------
class PTaskVersion(MPTTModel):

    # ------------------------------------------------------------------------
    # Fields
    # ------------------------------------------------------------------------
    ptask = models.ForeignKey(
        PTask,
        help_text='The ptask this version is associated with.',
        related_name='versions',
    )

    creator = models.ForeignKey(
        User,
        help_text='The user who created this version.',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        help_text='The date this ptask version was created.',
    )

    description = models.CharField(
        max_length=1024,
        help_text='A description of this ptask version.',
    )

    parent = TreeForeignKey(
        'self',
        db_index=True,
        help_text='The parent version of this version.',
        blank=True,
        null=True,
        related_name='children',
    )
    
    number = models.IntegerField(
        blank=False,
        help_text='The actual version number of this ptask version.',
    )

    spec = models.CharField(
        max_length=1024,
        help_text='Specification for this ptask.',
        blank=True,
        editable=False,
    )

    location = models.ForeignKey(
        Location,
        blank=True,
        help_text='The location that owns this version.',
    )

    # XXX active boolean

    # ------------------------------------------------------------------------
    # Special methods:
    # ------------------------------------------------------------------------
    def __unicode__(self):
        return unicode(self.spec)

    # ------------------------------------------------------------------------
    # Public methods:
    # ------------------------------------------------------------------------
    def save(self, *args, **kwargs):
        """Make sure the spec is set properly."""
    
        self.spec = SPEC_SEPARATOR.join([
            self.ptask.spec,
        ])
        self.spec += "@{0:04d}".format(self.number)
            
        super(PTaskVersion, self).save(*args, **kwargs) 

    # ------------------------------------------------------------------------
    # Internal classes:
    # ------------------------------------------------------------------------
    class Meta:
        managed = True
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'
        unique_together = (('ptask', 'number'),)

