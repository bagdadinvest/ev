"""
Create or customize your page models here.
"""

from coderedcms.forms import CoderedFormField
from coderedcms.models import CoderedArticleIndexPage
from coderedcms.models import CoderedArticlePage
from coderedcms.models import CoderedEmail
from coderedcms.models import CoderedEventIndexPage
from coderedcms.models import CoderedEventOccurrence
from coderedcms.models import CoderedEventPage
from coderedcms.models import CoderedFormPage
from coderedcms.models import CoderedLocationIndexPage
from coderedcms.models import CoderedLocationPage
from coderedcms.models import CoderedWebPage
from modelcluster.fields import ParentalKey


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = "Article"
        ordering = ["-first_published_at"]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["website.ArticleIndexPage"]

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Article Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.ArticlePage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.ArticlePage"]

    template = "coderedcms/pages/article_index_page.html"


class EventPage(CoderedEventPage):
    class Meta:
        verbose_name = "Event Page"

    parent_page_types = ["website.EventIndexPage"]
    template = "coderedcms/pages/event_page.html"


class EventIndexPage(CoderedEventIndexPage):
    """
    Shows a list of event sub-pages.
    """

    class Meta:
        verbose_name = "Events Landing Page"

    index_query_pagemodel = "website.EventPage"

    # Only allow EventPages beneath this page.
    subpage_types = ["website.EventPage"]

    template = "coderedcms/pages/event_index_page.html"


class EventOccurrence(CoderedEventOccurrence):
    event = ParentalKey(EventPage, related_name="occurrences")


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Form"

    template = "coderedcms/pages/form_page.html"


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("FormPage", related_name="form_fields")


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("FormPage", related_name="confirmation_emails")


class LocationPage(CoderedLocationPage):
    """
    A page that holds a location.  This could be a store, a restaurant, etc.
    """

    class Meta:
        verbose_name = "Location Page"

    template = "coderedcms/pages/location_page.html"

    # Only allow LocationIndexPages above this page.
    parent_page_types = ["website.LocationIndexPage"]


class LocationIndexPage(CoderedLocationIndexPage):
    """
    A page that holds a list of locations and displays them with a Google Map.
    This does require a Google Maps API Key in Settings > CRX Settings
    """

    class Meta:
        verbose_name = "Location Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.LocationPage"

    # Only allow LocationPages beneath this page.
    subpage_types = ["website.LocationPage"]

    template = "coderedcms/pages/location_index_page.html"


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"


from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField
from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from django.db import models
from wagtail_localize.models import TranslatableMixin
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

@register_snippet
class AppDescription(TranslatableMixin, ClusterableModel):
    """
    Snippet model to store app names, descriptions, and mockup images.
    """
    name = models.CharField(
        max_length=255,
        verbose_name="App Name",
        help_text="The name of the app.",
    )
    description = RichTextField(
        verbose_name="App Description",
        help_text="Detailed description of the app.",
    )
    mockup_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Mockup Image",
        help_text="Optional image representing the app."
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        ImageChooserPanel("mockup_image"),
        InlinePanel("tech_stacks", label="Tech Stack"),  # Link to tech stack
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "App Description"
        verbose_name_plural = "App Descriptions"

class AppTechStack(models.Model):
    """
    Stores individual technologies for an app's tech stack.
    """
    app = ParentalKey(
        "AppDescription",
        on_delete=models.CASCADE,
        related_name="tech_stacks",
    )
    tech_name = models.CharField(
        max_length=100,
        verbose_name="Technology Name",
        help_text="Name of the technology (e.g., Django, React).",
    )
    tech_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Technology Logo",
        help_text="Optional logo for the technology."
    )
    tech_description = models.TextField(
        blank=True,
        verbose_name="Technology Description",
        help_text="Short description of the technology.",
    )

    panels = [
        FieldPanel("tech_name"),
        FieldPanel("tech_description"),
        ImageChooserPanel("tech_logo"),
    ]

    def __str__(self):
        return self.tech_name

    class Meta:
        verbose_name = "Tech Stack"
        verbose_name_plural = "Tech Stacks"
