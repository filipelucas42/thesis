from django.db import models
from django.utils.timezone import now
from wagtail.core.models import Page as WagtailPage, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.fields import StreamField
from wagtail.core import blocks


# Create your models here.
class New(models.Model):
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=False)
    description = models.TextField(blank=True)
    date = models.DateField(default=now)
    image = models.TextField(blank=True)


class Directory(models.Model):
    identifier = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class Publication(models.Model):
    title = models.CharField(max_length=255)
    file = models.TextField(blank=True)
    image = models.TextField(blank=True)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)


class FormationOffer(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    start_date = models.DateField(default=now)
    end_date = models.DateField()


class FormationSubmission(models.Model):
    name = models.TextField(blank=True)
    email = models.TextField(blank=True)
    text = models.TextField(blank=True)
    date = models.DateField(default=now)


class Country(models.Model):
    label = models.CharField(max_length=255, blank=False)
    code = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.label


class DataPoint(models.Model):
    MOBILE = "mobile"
    INTERNET = "internet"

    GRAPH_CHOICES = (
        (MOBILE, "mobile penetration rate"),
        (INTERNET, "internet access rate"),
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    year = models.IntegerField()
    value = models.IntegerField()
    graph = models.CharField(max_length=255, blank=False, choices=GRAPH_CHOICES, default=MOBILE)

    class Meta:
        unique_together = ('country', 'year', 'graph')


class Page(WagtailPage):
    template = "arctel/wagtail.html"
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('list', blocks.ListBlock(blocks.CharBlock(label="Item"))),
        ('image', ImageChooserBlock()),
    ], blank=True)
    content_panels = WagtailPage.content_panels + [
        FieldPanel('body', classname="full"),
    ]
