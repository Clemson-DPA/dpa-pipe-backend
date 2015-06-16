# -----------------------------------------------------------------------------
# Module: dpa.products.models
# Author: Josh Tomlinson (jtomlin)
# -----------------------------------------------------------------------------
"""Defines all models for dpa products.
 
Classes
-------
 
 
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from django.contrib.auth.models import User
from django.db import models

# utility app to handle hierarchical models efficiently
from mptt.models import MPTTModel

from locations.models import Location
from ptasks.models import PTask, PTaskVersion

# -----------------------------------------------------------------------------
# Globals:
# -----------------------------------------------------------------------------

SPEC_SEPARATOR = '='

# -----------------------------------------------------------------------------
class ProductCategory(models.Model):

    # ------------------------------------------------------------------------
    # Fields
    # ------------------------------------------------------------------------
    name = models.CharField(
        max_length=32,
        primary_key=True,
        help_text='The name of this category.'
    )

    description = models.CharField(
        max_length=1024,
        help_text='A description of what this product category is used for.'
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
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

# -----------------------------------------------------------------------------
class Product(models.Model):

    # ------------------------------------------------------------------------
    # Fields:
    # ------------------------------------------------------------------------
    ptask = models.ForeignKey(
        PTask,
        db_index=True,
        help_text='The ptask that owns this product.',
        related_name='products',
    )

    name = models.CharField(
        max_length=256,
        db_index=True,
        help_text='The name of this product.'
    )

    category = models.ForeignKey(
        ProductCategory,
        db_index=True,
        help_text="The product's category.",

    )

    description = models.CharField(
        max_length=1024,
        help_text='A description of this product.'
    )

    spec = models.CharField(
        max_length=1024,
        help_text='Specification for this product.',
        blank=True,
        editable = False,
    )

    official_version_number = models.IntegerField(
        help_text="The official version number of this product",
        default=0,
    )

    creator = models.ForeignKey(
        User,
        help_text='The user who created this product.',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        help_text='Date the product was created.',
    )
    
    # ------------------------------------------------------------------------
    # Internal classes:
    # ------------------------------------------------------------------------
    class Meta:
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        index_together = [['ptask', 'name', 'category'],]
        unique_together = (('ptask', 'name', 'category'),)

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

        # populate the spec field
        self.spec = SPEC_SEPARATOR.join([
            self.ptask.spec,
            "products",
            self.name,
            self.category.name ,
        ])

        super(Product, self).save()

# -----------------------------------------------------------------------------
class ProductVersion(models.Model):

    # ------------------------------------------------------------------------
    # Fields:
    # ------------------------------------------------------------------------
    ptask_version = models.ForeignKey(
        PTaskVersion,
        db_index=True,
        help_text='The ptask version associated with his product version.',
    )

    product = models.ForeignKey(
        Product,
        db_index=True,
        help_text='The product this version is associated with.',
        related_name='versions',
    )

    release_note = models.CharField(
        max_length=1024,
        help_text='A note regarding this version of the product.'
    )

    number = models.IntegerField(
        help_text="The version number of this product version.",
        blank=True,
        null=True,
        editable=False,
    )

    spec = models.CharField(
        max_length=1024,
        help_text='Specification for this version.',
        blank=True,
        editable = False,
    )

    published = models.BooleanField(
        default=False,
        help_text='True if the version is published, False otherwise.',
    )

    deprecated = models.BooleanField(
        default=False,
        help_text='True if the version is deprecated, False otherwise.',
    )

    creator = models.ForeignKey(
        User,
        help_text='The user who created this version.',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        help_text='The date this product version was created.',
    )

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

        ptask_ver = self.ptask_version.number
    
        # populate the spec field
        self.spec = SPEC_SEPARATOR.join([
            self.product.spec,
            str(ptask_ver).zfill(4),
        ])

        # populate the number field
        self.number = ptask_ver
            
        super(ProductVersion, self).save(*args, **kwargs) 

    # ------------------------------------------------------------------------
    # Internal classes:
    # ------------------------------------------------------------------------
    class Meta:
        managed = True
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'
        unique_together = (('product', 'ptask_version'),)

# -----------------------------------------------------------------------------
class ProductRepresentation(models.Model):

    # ------------------------------------------------------------------------
    # Fields:
    # ------------------------------------------------------------------------
    product_version = models.ForeignKey(
        ProductVersion,
        db_index=True,
        help_text='The product version this representation is associated with.',
        related_name='representations',
    )

    resolution = models.CharField(
        max_length=32,
        help_text='Resolution for this representation.',
        default="none"
    )

    representation_type = models.CharField(
        max_length=32,
        help_text='Type for this representation.',
    )

    frame_range = models.CharField(
        max_length=1024,
        help_text='Frame range for this representation.',
        blank=True,
        null=True,
    )

    spec = models.CharField(
        max_length=1024,
        help_text='Specification for this representation.',
        blank=True,
        editable = False,
    )

    creation_location = models.ForeignKey(
        Location,
        blank=True,
        help_text='The creation locations of the representation.',
    )

    creator = models.ForeignKey(
        User,
        help_text='The user who created this representation.',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        help_text='The date this representation was created.',
    )

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
            self.product_version.spec,
            self.representation_type,
            self.resolution,
        ])
            
        super(ProductRepresentation, self).save(*args, **kwargs) 

    # ------------------------------------------------------------------------
    # Internal classes:
    # ------------------------------------------------------------------------
    class Meta:
        managed = True
        verbose_name = 'Representation'
        verbose_name_plural = 'Respresentations'
        unique_together = (
            (
                'product_version', 
                'resolution', 
                'representation_type'
            ),
        )

# -----------------------------------------------------------------------------
class ProductGrouping(models.Model):

    parent_product_version = models.ForeignKey(
        ProductVersion,
        help_text="The parent product version in this relationship.",
        related_name='parent_groupings',
    )

    child_product_version = models.ForeignKey(
        ProductVersion,
        help_text="The child product version in this relationship.",
        related_name='child_groupings',
    )

    spec = models.CharField(
        max_length=1024,
        help_text='Specification for this representation status.',
        blank=True,
        editable = False,
    )

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
    
        self.spec = self.parent_product_version.spec + ',' + \
            self.child_product_version.spec
            
        super(ProductGrouping, self).save(*args, **kwargs) 

    # ------------------------------------------------------------------------
    # Internal classes:
    # ------------------------------------------------------------------------
    class Meta:
        managed = True
        verbose_name = 'Grouping'
        verbose_name_plural = 'Groupings'

# -----------------------------------------------------------------------------
class ProductRepresentationStatus(models.Model):

    # status choices enum
    ONLINE = 0
    DELETED = 1
    NEARLINE = 2
    TO_BE_DELETED = 3

    # XXX create a separate table for these
    # XXX maybe include an RGB for each ?
    STATUS_CHOICES = (
        (ONLINE, 'Online'),
        (DELETED, 'Deleted'),
        (NEARLINE, 'Nearline'),
        (TO_BE_DELETED, 'To be deleted'),
    )

    product_representation = models.ForeignKey(
        ProductRepresentation,
        help_text="The product representation in a given location.",
    )

    location = models.ForeignKey(
        Location,
        blank=True,
        help_text='The location of the representation.',
    )

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=ONLINE,
        help_text='The status of a representation in a specific location.'
    )
    
    spec = models.CharField(
        max_length=1024,
        help_text='Specification for this representation status.',
        blank=True,
        editable = False,
    )

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
    
        self.spec = self.product_representation.spec + ',' + \
            self.location.code
            
        super(ProductRepresentationStatus, self).save(*args, **kwargs) 

    # ------------------------------------------------------------------------
    # Internal classes:
    # ------------------------------------------------------------------------
    class Meta:
        managed = True
        verbose_name = 'Representation Status'
        verbose_name_plural = 'Representation Statuses'
        unique_together = (('product_representation', 'location'),)

# -----------------------------------------------------------------------------
class ProductSubscription(models.Model):
    
    product_version = models.ForeignKey(
        ProductVersion,
        db_index=True,
        help_text='The product version being subscribed to.',
        related_name='subscriptions',
    )

    ptask_version = models.ForeignKey(
        PTaskVersion,
        db_index=True,
        help_text='The ptask version associated with his product version.',
        related_name='subscriptions',
    )

    locked = models.BooleanField(
        default=False,
        help_text='True if the subscription is locked, False otherwise.',
    )

    spec = models.CharField(
        max_length=1024,
        help_text='Specification for this subscription.',
        blank=True,
        editable = False,
    )

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
    
        self.spec = self.ptask_version.spec + ',' + \
            self.product_version.spec 
            
        super(ProductSubscription, self).save(*args, **kwargs) 

    # ------------------------------------------------------------------------
    # Internal classes:
    # ------------------------------------------------------------------------
    class Meta:
        managed = True
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        unique_together = (('product_version', 'ptask_version'),)

