"""
Адаптеры для перевода моделей контента.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, List

from app.i18n.const import DEFAULT_LANGUAGE
from app.i18n.manager import translation_manager


def translate_hero(data: Dict, locale: str) -> Dict:
    hero = deepcopy(data)
    hero["slogan"] = translation_manager.get_text("hero.slogan", hero.get("slogan", ""), locale)
    hero["subtitle"] = translation_manager.get_text("hero.subtitle", hero.get("subtitle", ""), locale)
    hero["cta_primary"] = translation_manager.get_text("hero.cta_primary", hero.get("cta_primary", ""), locale)
    hero["cta_secondary"] = translation_manager.get_text("hero.cta_secondary", hero.get("cta_secondary", ""), locale)
    hero["scroll_text"] = translation_manager.get_text("hero.scroll_text", hero.get("scroll_text", ""), locale)
    return hero


def translate_about(data: Dict, locale: str) -> Dict:
    about = deepcopy(data)
    about["title"] = translation_manager.get_text("about.title", about.get("title", ""), locale)
    about["description"] = translation_manager.get_text("about.description", about.get("description", ""), locale)
    about["philosophy"] = translation_manager.get_text("about.philosophy", about.get("philosophy", ""), locale)

    features: List[Dict] = about.get("features", [])
    for index, feature in enumerate(features):
        feature_key = f"about.features.{index}"
        feature["title"] = translation_manager.get_text(
            f"{feature_key}.title", feature.get("title", ""), locale
        )
        feature["description"] = translation_manager.get_text(
            f"{feature_key}.description", feature.get("description", ""), locale
        )
    return about


def translate_products(data: Dict, locale: str) -> Dict:
    products = deepcopy(data)
    items: List[Dict] = products.get("products_list", [])
    for index, item in enumerate(items):
        item_key = f"products.items.{index}"
        item["name"] = translation_manager.get_text(f"{item_key}.name", item.get("name", ""), locale)
        item["category"] = translation_manager.get_text(
            f"{item_key}.category", item.get("category", ""), locale
        )
        item["description"] = translation_manager.get_text(
            f"{item_key}.description", item.get("description", ""), locale
        )
    products["title"] = translation_manager.get_text("products.title", products.get("title", ""), locale)
    return products


def translate_services(data: Dict, locale: str) -> Dict:
    services = deepcopy(data)
    services["title"] = translation_manager.get_text("services.title", services.get("title", ""), locale)
    entries: List[Dict] = services.get("services_list", [])
    for index, entry in enumerate(entries):
        entry_key = f"services.items.{index}"
        entry["name"] = translation_manager.get_text(f"{entry_key}.name", entry.get("name", ""), locale)
        entry["description"] = translation_manager.get_text(
            f"{entry_key}.description", entry.get("description", ""), locale
        )
        features = entry.get("features", [])
        for feature_index, value in enumerate(features):
            features[feature_index] = translation_manager.get_text(
                f"{entry_key}.features.{feature_index}", value, locale
            )
    return services


def translate_personalization(data: Dict, locale: str) -> Dict:
    personalization = deepcopy(data)
    personalization["title"] = translation_manager.get_text(
        "personalization.title", personalization.get("title", ""), locale
    )
    personalization["subtitle"] = translation_manager.get_text(
        "personalization.subtitle", personalization.get("subtitle", ""), locale
    )
    personalization["info_text"] = translation_manager.get_text(
        "personalization.info_text", personalization.get("info_text", ""), locale
    )
    personalization["info_description"] = translation_manager.get_text(
        "personalization.info_description", personalization.get("info_description", ""), locale
    )

    dna = personalization.get("dna_testing", {})
    dna["title"] = translation_manager.get_text("personalization.dna.title", dna.get("title", ""), locale)
    dna["description"] = translation_manager.get_text(
        "personalization.dna.description", dna.get("description", ""), locale
    )
    dna_features = dna.get("features", [])
    for index, feature in enumerate(dna_features):
        dna_features[index] = translation_manager.get_text(
            f"personalization.dna.features.{index}", feature, locale
        )

    auracloud = personalization.get("auracloud", {})
    auracloud["title"] = translation_manager.get_text(
        "personalization.auracloud.title", auracloud.get("title", ""), locale
    )
    auracloud["description"] = translation_manager.get_text(
        "personalization.auracloud.description", auracloud.get("description", ""), locale
    )
    auracloud_features = auracloud.get("features", [])
    for index, feature in enumerate(auracloud_features):
        auracloud_features[index] = translation_manager.get_text(
            f"personalization.auracloud.features.{index}", feature, locale
        )
    return personalization


def translate_auracloud_slider(data: Dict, locale: str) -> Dict:
    slider = deepcopy(data)
    slider["title"] = translation_manager.get_text("auracloud_slider.title", slider.get("title", ""), locale)
    slider["subtitle"] = translation_manager.get_text(
        "auracloud_slider.subtitle", slider.get("subtitle", ""), locale
    )
    slider["before_label"] = translation_manager.get_text(
        "auracloud_slider.before_label", slider.get("before_label", ""), locale
    )
    slider["after_label"] = translation_manager.get_text(
        "auracloud_slider.after_label", slider.get("after_label", ""), locale
    )
    slider["description"] = translation_manager.get_text(
        "auracloud_slider.description", slider.get("description", ""), locale
    )
    return slider


def translate_blog(data: Dict, locale: str) -> Dict:
    blog = deepcopy(data)
    blog["title"] = translation_manager.get_text("blog.title", blog.get("title", ""), locale)
    blog["subtitle"] = translation_manager.get_text("blog.subtitle", blog.get("subtitle", ""), locale)
    articles = blog.get("articles_list", [])
    for index, article in enumerate(articles):
        article_key = f"blog.articles.{index}"
        article["title"] = translation_manager.get_text(
            f"{article_key}.title", article.get("title", ""), locale
        )
        article["excerpt"] = translation_manager.get_text(
            f"{article_key}.excerpt", article.get("excerpt", ""), locale
        )
    return blog


def translate_contacts(data: Dict, locale: str) -> Dict:
    contacts = deepcopy(data)
    contacts["title"] = translation_manager.get_text("contacts.title", contacts.get("title", ""), locale)
    contacts["address"] = translation_manager.get_text("contacts.address", contacts.get("address", ""), locale)
    contacts["form_title"] = translation_manager.get_text(
        "contacts.form.title", contacts.get("form_title", ""), locale
    )
    contacts["form_subtitle"] = translation_manager.get_text(
        "contacts.form.subtitle", contacts.get("form_subtitle", ""), locale
    )
    contacts["form_button_text"] = translation_manager.get_text(
        "contacts.form.button", contacts.get("form_button_text", ""), locale
    )
    contacts["form_success_message"] = translation_manager.get_text(
        "contacts.form.success", contacts.get("form_success_message", ""), locale
    )
    return contacts


def translate_reviews(data: Dict, locale: str) -> Dict:
    reviews = deepcopy(data)
    reviews["title"] = translation_manager.get_text("reviews.title", reviews.get("title", ""), locale)
    entries = reviews.get("reviews_list", [])
    for index, review in enumerate(entries):
        review_key = f"reviews.items.{index}"
        review["author"] = translation_manager.get_text(
            f"{review_key}.author", review.get("author", ""), locale
        )
        review["text"] = translation_manager.get_text(f"{review_key}.text", review.get("text", ""), locale)
    return reviews


def translate_section_title(title: str, locale: str, key: str) -> str:
    """
    Хелпер для перевода произвольных заголовков секций.
    """
    if locale == DEFAULT_LANGUAGE:
        return title
    return translation_manager.get_text(key, title, locale)

