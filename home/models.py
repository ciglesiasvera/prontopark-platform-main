from django.db import models
from django.utils.translation import gettext_lazy as _

class HomePageContent(models.Model):
    """
    Model to manage dynamic content for the home page
    """
    title = models.CharField(
        max_length=200, 
        verbose_name=_('Page Title')
    )
    subtitle = models.CharField(
        max_length=300, 
        verbose_name=_('Page Subtitle'), 
        blank=True, 
        null=True
    )
    description = models.TextField(
        verbose_name=_('Page Description'), 
        blank=True
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name=_('Active Status')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('Creation Date')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Last Update')
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Home Page Content')
        verbose_name_plural = _('Home Page Contents')
        ordering = ['-created_at']
