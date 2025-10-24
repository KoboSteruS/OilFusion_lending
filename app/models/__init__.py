"""
Модели данных для OilFusion Landing.
"""

from app.models.base import BaseContentModel
from app.models.content import AboutContent, PersonalizationContent, BlogArticle, BlogContent
from app.models.images import SectionBackgrounds
from app.models.products import ProductsContent
from app.models.services import ServicesContent
from app.models.contacts import ContactsContent
from app.models.hero import HeroContent
from app.models.sections_visibility import SectionsVisibility
from app.models.auracloud_slider import AuraCloudSlider

__all__ = ['BaseContentModel', 'AboutContent', 'PersonalizationContent', 'BlogArticle', 'BlogContent', 'SectionBackgrounds', 'ProductsContent', 'ServicesContent', 'ContactsContent', 'HeroContent', 'SectionsVisibility', 'AuraCloudSlider']

