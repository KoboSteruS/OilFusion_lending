"""
Менеджер переводов контента.
"""

from __future__ import annotations

import json
import threading
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from loguru import logger

from app.config.settings import Config
from app.i18n.const import DEFAULT_LANGUAGE, LANGUAGE_LABELS, SUPPORTED_LANGUAGES
from app.i18n.translator import GoogleTranslationProvider, TranslationResult


@dataclass
class TranslationRecord:
    """Структура записи перевода для отображения в админке."""

    key: str
    original: str
    translations: Dict[str, Dict[str, Optional[str]]]


class TranslationManager:
    """
    Менеджер хранит переводы в JSON и обеспечивает автоперевод.
    """

    def __init__(
        self,
        storage_path: Optional[Path] = None,
        supported_languages: Iterable[str] = SUPPORTED_LANGUAGES,
        default_language: str = DEFAULT_LANGUAGE,
    ) -> None:
        self._storage_path = storage_path or Config.BASE_DIR / "data" / "translations.json"
        self._supported_languages = tuple(supported_languages)
        self._default_language = default_language
        self._provider = GoogleTranslationProvider()
        self._auto_enabled = Config.AUTO_TRANSLATION_ENABLED and self._provider.available
        self._lock = threading.Lock()
        self._data: Dict[str, Dict] = self._load()

    # -------------------- public API --------------------

    def get_text(self, key: str, original: str, locale: str) -> str:
        """
        Возвращает текст на нужном языке, при необходимости выполняя автоперевод.
        """
        if locale not in self._supported_languages:
            logger.warning("Запрошен неподдерживаемый язык: {}", locale)
            locale = self._default_language

        # Для дефолтного языка всегда возвращаем оригинал
        if locale == self._default_language:
            self.ensure_entry(key, original)
            return original

        # Сначала проверяем, есть ли сохранённый перевод (manual или auto)
        with self._lock:
            entry = self.ensure_entry(key, original)
            stored_translation = entry["translations"].get(locale)
            if stored_translation and stored_translation.get("value"):
                return stored_translation["value"]

        # Если автоперевод выключен, возвращаем оригинал
        if not self._auto_enabled:
            return original

        # Выполняем автоперевод вне блока lock
        result = self._provider.translate(
            original, target_language=locale, source_language=self._default_language
        )

        with self._lock:
            entry = self.ensure_entry(key, original)
            entry["translations"][locale] = self._build_translation_payload(result.text, source="auto")
            self._save()
            return result.text

    def set_manual_translation(self, key: str, locale: str, value: str) -> None:
        """
        Сохраняет ручной перевод.
        """
        if locale == self._default_language:
            logger.warning("Игнорируем попытку перезаписать язык по умолчанию: {}", key)
            return

        with self._lock:
            entry = self.ensure_entry(key, entry_original := self._data.get(key, {}).get("meta", {}).get("original", ""))
            if not value.strip():
                entry["translations"].pop(locale, None)
                logger.info("Удалён перевод {} для ключа {}", locale, key)
            else:
                entry["translations"][locale] = self._build_translation_payload(value, source="manual")
                logger.info("Сохранён ручной перевод {} для ключа {}", locale, key)
            self._save()

    def auto_translate(self, key: str, locale: str) -> Optional[str]:
        """
        Принудительно выполняет автоперевод и сохраняет его.
        """
        entry = self.ensure_entry(key, self.get_original(key))
        original = entry["meta"]["original"]
        if locale == self._default_language or not self._auto_enabled:
            return original

        result: TranslationResult = self._provider.translate(
            original,
            target_language=locale,
            source_language=self._default_language,
        )
        with self._lock:
            entry = self.ensure_entry(key, original)
            entry["translations"][locale] = self._build_translation_payload(result.text, source="auto")
            self._save()
            return result.text

    def list_records(self) -> List[TranslationRecord]:
        """
        Возвращает список записей для административного интерфейса.
        """
        records: List[TranslationRecord] = []
        with self._lock:
            for key, entry in sorted(self._data.items()):
                translations = {
                    lang: {
                        "value": entry["translations"].get(lang, {}).get("value"),
                        "source": entry["translations"].get(lang, {}).get("source"),
                        "updated_at": entry["translations"].get(lang, {}).get("updated_at"),
                        "label": LANGUAGE_LABELS.get(lang, lang.upper()),
                    }
                    for lang in self._supported_languages
                    if lang != self._default_language
                }
                records.append(
                    TranslationRecord(
                        key=key,
                        original=entry["meta"].get("original", ""),
                        translations=translations,
                    )
                )
        return records

    def ensure_entry(self, key: str, original: str) -> Dict:
        """
        Обновляет/создаёт запись перевода и возвращает её.
        """
        original = original or ""
        with self._lock:
            entry = self._data.setdefault(
                key,
                {
                    "meta": {
                        "original": original,
                        "original_hash": self._hash(original),
                        "created_at": self._timestamp(),
                        "updated_at": self._timestamp(),
                    },
                    "translations": {},
                },
            )

            # Обновляем оригинал, если он изменился.
            if self._hash(original) != entry["meta"].get("original_hash"):
                entry["meta"]["original"] = original
                entry["meta"]["original_hash"] = self._hash(original)
                entry["meta"]["updated_at"] = self._timestamp()
                logger.info("Обновлён оригинал текста для ключа {}", key)
                # Перезапускаем автоперевод для auto-записей
                auto_languages = [
                    lang for lang, payload in entry["translations"].items() if payload.get("source") == "auto"
                ]
                for lang in auto_languages:
                    self._lock.release()
                    try:
                        self.auto_translate(key, lang)
                    finally:
                        self._lock.acquire()
        return self._data[key]

    def get_original(self, key: str) -> str:
        """
        Возвращает оригинальный текст для ключа.
        """
        with self._lock:
            return self._data.get(key, {}).get("meta", {}).get("original", "")

    # -------------------- внутренние методы --------------------

    def _load(self) -> Dict[str, Dict]:
        if not self._storage_path.exists():
            return {}
        try:
            with self._storage_path.open("r", encoding="utf-8") as fp:
                return json.load(fp)
        except json.JSONDecodeError as exc:
            logger.error("Ошибка чтения файла переводов: {}", exc)
            return {}

    def _save(self) -> None:
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        with self._storage_path.open("w", encoding="utf-8") as fp:
            json.dump(self._data, fp, ensure_ascii=False, indent=2)

    @staticmethod
    def _hash(value: str) -> str:
        return sha256(value.encode("utf-8")).hexdigest()

    @staticmethod
    def _timestamp() -> str:
        return datetime.utcnow().isoformat()

    @staticmethod
    def _build_translation_payload(value: str, source: str) -> Dict[str, str]:
        return {
            "value": value,
            "source": source,
            "updated_at": TranslationManager._timestamp(),
        }


# Глобальный инстанс менеджера для повторного использования.
translation_manager = TranslationManager()

