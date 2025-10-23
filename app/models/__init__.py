"""
Модели данных для OilFusion Landing.
"""

from app.models.content import AboutContent, PersonalizationContent, BlogArticle, BlogContent
from app.models.images import SectionBackgrounds
from app.models.products import ProductsContent
from app.models.services import ServicesContent
from app.models.contacts import ContactsContent
from app.models.hero import HeroContent
from app.models.sections_visibility import SectionsVisibility

__all__ = ['AboutContent', 'PersonalizationContent', 'BlogArticle', 'BlogContent', 'SectionBackgrounds', 'ProductsContent', 'ServicesContent', 'ContactsContent', 'HeroContent', 'SectionsVisibility']

