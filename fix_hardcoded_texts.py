"""
Скрипт для добавления всех недостающих переводов в БД.
"""

from app import create_app
from app.database import ContentRepository
from app.utils.logger import get_logger

logger = get_logger()


def add_missing_translations():
    """Добавление всех недостающих переводов."""
    app = create_app()
    
    with app.app_context():
        logger.info("Добавление недостающих переводов...")
        
        # About section - заголовок "unique characteristics"
        ContentRepository.set(
            section='about',
            key='features_title',
            value_ru='Уникальные особенности',
            value_lv='Unikālās īpašības',
            value_en='Unique characteristics'
        )
        
        # Bio-Well section
        ContentRepository.set(
            section='personalization',
            key='biowell_title',
            value_ru='Технология AuraCloud® 3D основана на Bio-Well системе',
            value_lv='AuraCloud® 3D tehnoloģija balstās uz Bio-Well sistēmu',
            value_en='AuraCloud® 3D technology is based on the Bio-Well system'
        )
        
        ContentRepository.set(
            section='personalization',
            key='biowell_description',
            value_ru='Мы используем передовую технологию Bio-Well для визуализации энергетического поля человека. Эта система позволяет увидеть изменения в вашей ауре и подобрать оптимальные продукты.',
            value_lv='Mēs izmantojam modernu Bio-Well tehnoloģiju cilvēka enerģētiskā lauka vizualizācijai. Šī sistēma ļauj redzēt izmaiņas jūsu aurā un izvēlēties optimālus produktus.',
            value_en='We use advanced Bio-Well technology to visualize the human energy field. This system allows you to see changes in your aura and select optimal products.'
        )
        
        ContentRepository.set(
            section='personalization',
            key='biowell_button',
            value_ru='Узнать больше о Bio-Well',
            value_lv='Uzzināt vairāk par Bio-Well',
            value_en='Learn more about Bio-Well'
        )
        
        ContentRepository.set(
            section='personalization',
            key='learn_more_button',
            value_ru='Узнать больше о технологиях',
            value_lv='Uzzināt vairāk par tehnoloģijām',
            value_en='Learn more about technologies'
        )
        
        ContentRepository.set(
            section='personalization',
            key='testing_button',
            value_ru='Пройти тестирование',
            value_lv='Veikt testēšanu',
            value_en='Take the test'
        )
        
        # Products - кнопка каталога
        ContentRepository.set(
            section='products',
            key='view_catalog',
            value_ru='Смотреть каталог',
            value_lv='Skatīt katalogu',
            value_en='View Catalog'
        )
        
        # Blog - кнопка читать далее
        ContentRepository.set(
            section='blog',
            key='read_more',
            value_ru='Читать далее',
            value_lv='Lasīt tālāk',
            value_en='Read more'
        )
        
        # Reviews - текст "На основе"
        ContentRepository.set(
            section='reviews',
            key='based_on',
            value_ru='На основе',
            value_lv='Pamatojoties uz',
            value_en='Based on'
        )
        
        ContentRepository.set(
            section='reviews',
            key='reviews_count',
            value_ru='отзывов',
            value_lv='atsauksmēm',
            value_en='reviews'
        )
        
        logger.info("✅ Все недостающие переводы добавлены!")


if __name__ == '__main__':
    add_missing_translations()

