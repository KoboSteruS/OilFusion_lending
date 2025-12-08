"""
Провайдер переводов.
В текущей версии автоматический перевод отключён - используются статические переводы из БД.
"""

from dataclasses import dataclass
from typing import Optional

from app.i18n.const import DEFAULT_LANGUAGE


@dataclass(frozen=True)
class TranslationResult:
    """Результат перевода."""

    text: str
    detected_source: Optional[str]


class GoogleTranslationProvider:
    """
    Провайдер перевода (заглушка).
    
    Автоматический перевод отключён. Все переводы хранятся статически в БД
    и загружаются из мультиязычных JSON файлов при миграции.
    """

    def __init__(self) -> None:
        self._translator = None
        self.available = False
        # Не выводим предупреждение - это нормальное поведение

    def translate(
        self,
        text: str,
        target_language: str,
        source_language: str = DEFAULT_LANGUAGE,
    ) -> TranslationResult:
        """
        Перевод текста на целевой язык.

        Args:
            text: исходная строка.
            target_language: язык перевода.
            source_language: язык оригинала.

        Returns:
            TranslationResult: результат перевода.
        """
        if not text.strip():
            return TranslationResult(text=text, detected_source=source_language)

        if not self.available:
            return TranslationResult(text=text, detected_source=source_language)

        try:
            translation = self._translator.translate(
                text, src=source_language, dest=target_language
            )
            return TranslationResult(
                text=translation.text, detected_source=translation.src
            )
        except Exception as exc:  # noqa: BLE001
            logger.error(
                "Ошибка автоматического перевода: {error}. Фрагмент: {snippet}",
                error=exc,
                snippet=text[:80],
            )
            # В случае ошибки возвращаем оригинал, чтобы не ломать интерфейс.
            return TranslationResult(text=text, detected_source=source_language)
