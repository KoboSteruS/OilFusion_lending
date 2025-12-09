"""
Заполнение базы данных контентом на трёх языках (RU/LV/EN).
Запустите этот скрипт для добавления начального контента.
"""

from app import create_app
from app.database import ContentRepository
from app.utils.logger import get_logger

logger = get_logger()


def seed_content():
    """Заполнение БД контентом на трёх языках."""
    app = create_app()
    
    with app.app_context():
        logger.info("Начинаем заполнение контента на трёх языках")
        
        # ===== HERO СЕКЦИЯ =====
        logger.info("Заполнение Hero секции...")
        
        ContentRepository.set(
            section='hero',
            key='slogan',
            value_ru='Balance in every drop',
            value_lv='Līdzsvars katrā pilienā',
            value_en='Balance in every drop'
        )
        
        ContentRepository.set(
            section='hero',
            key='subtitle',
            value_ru='Персонализированные масла на основе технологий AuraCloud® 3D и ДНК-тестирования',
            value_lv='Personalizētas eļļas, pamatojoties uz AuraCloud® 3D un DNS testēšanas tehnoloģijām',
            value_en='Personalized oils based on AuraCloud® 3D and DNA testing technologies'
        )
        
        ContentRepository.set(
            section='hero',
            key='cta_primary',
            value_ru='Подобрать масло',
            value_lv='Izvēlēties eļļu',
            value_en='Select Oil'
        )
        
        ContentRepository.set(
            section='hero',
            key='cta_secondary',
            value_ru='Записаться',
            value_lv='Pierakstīties',
            value_en='Book Appointment'
        )
        
        ContentRepository.set(
            section='hero',
            key='scroll_text',
            value_ru='Прокрутите вниз',
            value_lv='Ritiniet uz leju',
            value_en='Scroll down'
        )
        
        # ===== О НАС =====
        logger.info("Заполнение О нас...")
        
        ContentRepository.set(
            section='about',
            key='title',
            value_ru='О компании OilFusion',
            value_lv='Par OilFusion uzņēmumu',
            value_en='About OilFusion'
        )
        
        ContentRepository.set(
            section='about',
            key='description',
            value_ru='Мы создаем персонализированные масляные композиции, учитывая уникальные особенности каждого человека',
            value_lv='Mēs izveidojam personalizētas eļļas kompozīcijas, ņemot vērā katra cilvēka unikālās īpašības',
            value_en='We create personalized oil blends tailored to each person\'s unique characteristics'
        )
        
        ContentRepository.set(
            section='about',
            key='philosophy',
            value_ru='Наша философия основана на научном подходе к здоровью и красоте',
            value_lv='Mūsu filozofija balstās uz zinātnisku pieeju veselībai un skaistumam',
            value_en='Our philosophy is based on a scientific approach to health and beauty'
        )
        
        ContentRepository.set(
            section='about',
            key='learn_more_button',
            value_ru='Узнать больше о технологиях',
            value_lv='Uzziniet vairāk par tehnoloģijām',
            value_en='Learn more about technologies'
        )
        
        # Features для About секции в виде JSON с мультиязычностью
        import json
        about_features = [
            {
                'icon': 'aura',
                'title': {'ru': 'AuraCloud® 3D', 'lv': 'AuraCloud® 3D', 'en': 'AuraCloud® 3D'},
                'description': {
                    'ru': 'Передовая технология визуализации энергетической ауры для точного подбора продуктов',
                    'lv': 'Progresīva enerģētiskās auras vizualizācijas tehnoloģija precīzai produktu izvēlei',
                    'en': 'Advanced energy aura visualization technology for precise product selection'
                }
            },
            {
                'icon': 'dna',
                'title': {'ru': 'ДНК-тестирование', 'lv': 'DNS testēšana', 'en': 'DNA Testing'},
                'description': {
                    'ru': 'Индивидуальный подбор масел на основе вашего генетического профиля',
                    'lv': 'Individuāla eļļu izvēle, pamatojoties uz jūsu ģenētisko profilu',
                    'en': 'Individual oil selection based on your genetic profile'
                }
            }
        ]
        
        ContentRepository.set(
            section='about',
            key='features',
            value_ru=json.dumps(about_features, ensure_ascii=False),
            value_lv=json.dumps(about_features, ensure_ascii=False),
            value_en=json.dumps(about_features, ensure_ascii=False),
            data_type='json'
        )
        
        # ===== ПРОДУКЦИЯ =====
        logger.info("Заполнение Продукции...")
        
        ContentRepository.set(
            section='products',
            key='title',
            value_ru='Наша продукция',
            value_lv='Mūsu produkcija',
            value_en='Our Products'
        )
        
        ContentRepository.set(
            section='products',
            key='subtitle',
            value_ru='Персонализированные масла для вашего здоровья и гармонии',
            value_lv='Personalizētas eļļas jūsu veselībai un harmonijai',
            value_en='Personalized oils for your health and harmony'
        )
        
        ContentRepository.set(
            section='products',
            key='catalog_button',
            value_ru='Смотреть каталог',
            value_lv='Skatīt katalogu',
            value_en='View Catalog'
        )
        
        ContentRepository.set(
            section='products',
            key='details_button',
            value_ru='Подробнее',
            value_lv='Sīkāk',
            value_en='Learn More'
        )
        
        # Продукты в виде JSON
        import json
        products_list = [
            {
                'id': 1,
                'name_ru': 'Персонализированное масло',
                'name_lv': 'Personalizēta eļļa',
                'name_en': 'Personalized Oil',
                'description_ru': 'Уникальная формула, подобранная на основе вашего ДНК-профиля',
                'description_lv': 'Unikāla formula, izvēlēta, pamatojoties uz jūsu DNS profilu',
                'description_en': 'Unique formula selected based on your DNA profile',
                'price': 'от 3 500 ₽',
                'price_lv': 'no 3 500 ₽',
                'price_en': 'from 3 500 ₽',
                'image': '/static/img/leaf-icon.png',
                'featured': True
            },
            {
                'id': 2,
                'name_ru': 'Масло для ауры',
                'name_lv': 'Auras eļļa',
                'name_en': 'Aura Oil',
                'description_ru': 'Специальная смесь для гармонизации энергетического поля',
                'description_lv': 'Īpaša maisījums enerģētiskā lauka harmonizācijai',
                'description_en': 'Special blend for harmonizing your energy field',
                'price': 'от 4 200 ₽',
                'price_lv': 'no 4 200 ₽',
                'price_en': 'from 4 200 ₽',
                'image': '/static/img/star-icon.png',
                'featured': True
            },
            {
                'id': 3,
                'name_ru': 'Комплексная программа',
                'name_lv': 'Kompleksa programma',
                'name_en': 'Comprehensive Program',
                'description_ru': 'Полный набор продуктов с индивидуальным сопровождением',
                'description_lv': 'Pilns produktu komplekts ar individuālu atbalstu',
                'description_en': 'Complete product set with individual support',
                'price': 'от 12 000 ₽',
                'price_lv': 'no 12 000 ₽',
                'price_en': 'from 12 000 ₽',
                'image': '/static/img/microscope-icon.png',
                'featured': True
            }
        ]
        
        ContentRepository.set(
            section='products',
            key='products',
            value_ru=json.dumps(products_list, ensure_ascii=False),
            value_lv=json.dumps(products_list, ensure_ascii=False),
            value_en=json.dumps(products_list, ensure_ascii=False),
            data_type='json'
        )
        
        # ===== УСЛУГИ =====
        logger.info("Заполнение Услуг...")
        
        ContentRepository.set(
            section='services',
            key='title',
            value_ru='Наши услуги',
            value_lv='Mūsu pakalpojumi',
            value_en='Our Services'
        )
        
        ContentRepository.set(
            section='services',
            key='subtitle',
            value_ru='Комплексный подход к вашему здоровью',
            value_lv='Visaptveroša pieeja jūsu veselībai',
            value_en='Comprehensive approach to your health'
        )
        
        ContentRepository.set(
            section='services',
            key='dna_testing_title',
            value_ru='ДНК-тестирование',
            value_lv='DNS testēšana',
            value_en='DNA Testing'
        )
        
        ContentRepository.set(
            section='services',
            key='dna_testing_desc',
            value_ru='Анализ генетических особенностей для подбора идеального состава масел',
            value_lv='Ģenētisko īpašību analīze, lai izvēlētos ideālo eļļas sastāvu',
            value_en='Genetic analysis to select the perfect oil composition'
        )
        
        ContentRepository.set(
            section='services',
            key='auracloud_title',
            value_ru='Сканирование AuraCloud® 3D',
            value_lv='AuraCloud® 3D skenēšana',
            value_en='AuraCloud® 3D Scanning'
        )
        
        ContentRepository.set(
            section='services',
            key='auracloud_desc',
            value_ru='Энергетическая диагностика состояния организма',
            value_lv='Organisma stāvokļa enerģētiskā diagnostika',
            value_en='Energy diagnostics of body condition'
        )
        
        ContentRepository.set(
            section='services',
            key='consultation_title',
            value_ru='Консультация специалиста',
            value_lv='Speciālista konsultācija',
            value_en='Expert Consultation'
        )
        
        ContentRepository.set(
            section='services',
            key='consultation_desc',
            value_ru='Индивидуальный подбор масел с учетом всех факторов',
            value_lv='Individuāla eļļu izvēle, ņemot vērā visus faktorus',
            value_en='Individual oil selection considering all factors'
        )
        
        # Services list в формате JSON с мультиязычностью
        services_list = [
            {
                'icon': '/static/img/dna-icon.svg',
                'name': {'ru': 'ДНК-тестирование', 'lv': 'DNS testēšana', 'en': 'DNA Testing'},
                'description': {
                    'ru': 'Полный генетический анализ для индивидуального подбора масел',
                    'lv': 'Pilna ģenētiskā analīze individuālai eļļu izvēlei',
                    'en': 'Complete genetic analysis for individual oil selection'
                },
                'features': {
                    'ru': ['Забор биоматериала', 'Лабораторный анализ', 'Подробный отчёт', 'Консультация специалиста'],
                    'lv': ['Biomateriāla ņemšana', 'Laboratoriskā analīze', 'Detalizēts pārskats', 'Speciālista konsultācija'],
                    'en': ['Sample collection', 'Laboratory analysis', 'Detailed report', 'Expert consultation']
                },
                'price': {'ru': 'от 8 500 ₽', 'lv': 'no 8 500 ₽', 'en': 'from 8 500 ₽'}
            },
            {
                'icon': '/static/img/aura-icon.svg',
                'name': {'ru': 'Сканирование AuraCloud® 3D', 'lv': 'AuraCloud® 3D skenēšana', 'en': 'AuraCloud® 3D Scanning'},
                'description': {
                    'ru': 'Визуализация и анализ вашей энергетической ауры',
                    'lv': 'Jūsu enerģētiskās auras vizualizācija un analīze',
                    'en': 'Visualization and analysis of your energy aura'
                },
                'features': {
                    'ru': ['3D сканирование ауры', 'Детальная визуализация', 'Анализ энергетики', 'Рекомендации по коррекции'],
                    'lv': ['3D auras skenēšana', 'Detalizēta vizualizācija', 'Enerģētikas analīze', 'Korekcijas rekomendācijas'],
                    'en': ['3D aura scanning', 'Detailed visualization', 'Energy analysis', 'Correction recommendations']
                },
                'price': {'ru': 'от 5 000 ₽', 'lv': 'no 5 000 ₽', 'en': 'from 5 000 ₽'}
            },
            {
                'icon': '/static/img/consult-icon.svg',
                'name': {'ru': 'Персональная консультация', 'lv': 'Personīgā konsultācija', 'en': 'Personal Consultation'},
                'description': {
                    'ru': 'Индивидуальный подбор продуктов и программы применения',
                    'lv': 'Individuāla produktu un lietošanas programmas izvēle',
                    'en': 'Individual product and application program selection'
                },
                'features': {
                    'ru': ['Диагностика состояния', 'Подбор программы', 'Рекомендации по применению', 'Сопровождение 30 дней'],
                    'lv': ['Stāvokļa diagnostika', 'Programmas izvēle', 'Lietošanas rekomendācijas', 'Atbalsts 30 dienas'],
                    'en': ['Condition diagnostics', 'Program selection', 'Application recommendations', '30 day support']
                },
                'price': {'ru': 'от 3 000 ₽', 'lv': 'no 3 000 ₽', 'en': 'from 3 000 ₽'}
            }
        ]
        
        ContentRepository.set(
            section='services',
            key='services_list',
            value_ru=json.dumps(services_list, ensure_ascii=False),
            value_lv=json.dumps(services_list, ensure_ascii=False),
            value_en=json.dumps(services_list, ensure_ascii=False),
            data_type='json'
        )
        
        # ===== ПЕРСОНАЛИЗАЦИЯ =====
        logger.info("Заполнение Персонализации...")
        
        ContentRepository.set(
            section='personalization',
            key='title',
            value_ru='Персонализация',
            value_lv='Personalizācija',
            value_en='Personalization'
        )
        
        ContentRepository.set(
            section='personalization',
            key='subtitle',
            value_ru='Технологии для вашего здоровья',
            value_lv='Tehnoloģijas jūsu veselībai',
            value_en='Technologies for your health'
        )
        
        ContentRepository.set(
            section='personalization',
            key='dna_testing',
            value_ru='ДНК-тестирование позволяет определить генетические особенности и подобрать идеальный состав',
            value_lv='DNS testēšana ļauj noteikt ģenētiskās īpašības un izvēlēties ideālo sastāvu',
            value_en='DNA testing determines genetic features and selects the perfect composition'
        )
        
        ContentRepository.set(
            section='personalization',
            key='auracloud',
            value_ru='AuraCloud® 3D сканирование показывает текущее состояние организма',
            value_lv='AuraCloud® 3D skenēšana parāda organisma pašreizējo stāvokli',
            value_en='AuraCloud® 3D scanning shows current body condition'
        )
        
        ContentRepository.set(
            section='personalization',
            key='dna_testing_title',
            value_ru='ДНК-тестирование',
            value_lv='DNS testēšana',
            value_en='DNA Testing'
        )
        
        ContentRepository.set(
            section='personalization',
            key='auracloud_title',
            value_ru='AuraCloud® 3D',
            value_lv='AuraCloud® 3D',
            value_en='AuraCloud® 3D'
        )
        
        ContentRepository.set(
            section='personalization',
            key='testing_button',
            value_ru='Пройти тестирование',
            value_lv='Iziet testēšanu',
            value_en='Get Tested'
        )
        
        ContentRepository.set(
            section='personalization',
            key='scanning_button',
            value_ru='Пройти сканирование',
            value_lv='Iziet skenēšanu',
            value_en='Get Scanned'
        )
        
        ContentRepository.set(
            section='personalization',
            key='info_text',
            value_ru='Технология AuraCloud® 3D основана на Bio-Well системе',
            value_lv='AuraCloud® 3D tehnoloģija ir balstīta uz Bio-Well sistēmu',
            value_en='AuraCloud® 3D technology is based on the Bio-Well system'
        )
        
        ContentRepository.set(
            section='personalization',
            key='info_description',
            value_ru='Мы используем передовую технологию Bio-Well для визуализации энергетического поля человека. Эта система позволяет увидеть изменения в вашей ауре и подобрать оптимальные продукты.',
            value_lv='Mēs izmantojam progresīvo Bio-Well tehnoloģiju cilvēka enerģētiskā lauka vizualizācijai. Šī sistēma ļauj redzēt izmaiņas jūsu aurā un izvēlēties optimālos produktus.',
            value_en='We use advanced Bio-Well technology to visualize the human energy field. This system allows you to see changes in your aura and select optimal products.'
        )
        
        ContentRepository.set(
            section='personalization',
            key='biowell_button',
            value_ru='Узнать больше о Bio-Well',
            value_lv='Uzziniet vairāk par Bio-Well',
            value_en='Learn more about Bio-Well'
        )
        
        ContentRepository.set(
            section='personalization',
            key='bio_well_url',
            value_ru='https://bio-well.com',
            value_lv='https://bio-well.com',
            value_en='https://bio-well.com'
        )
        
        # ===== БЛОГ =====
        logger.info("Заполнение Блога...")
        
        ContentRepository.set(
            section='blog',
            key='title',
            value_ru='Блог',
            value_lv='Blogs',
            value_en='Blog'
        )
        
        ContentRepository.set(
            section='blog',
            key='subtitle',
            value_ru='Полезная информация о здоровье и персонализации',
            value_lv='Noderīga informācija par veselību un personalizāciju',
            value_en='Useful information about health and personalization'
        )
        
        ContentRepository.set(
            section='blog',
            key='read_more',
            value_ru='Читать далее',
            value_lv='Lasīt vairāk',
            value_en='Read more'
        )
        
        ContentRepository.set(
            section='blog',
            key='min_read',
            value_ru='мин чтения',
            value_lv='min lasīšanas',
            value_en='min read'
        )
        
        ContentRepository.set(
            section='blog',
            key='all_articles',
            value_ru='Читать все статьи',
            value_lv='Lasīt visus rakstus',
            value_en='Read all articles'
        )
        
        # ===== КОНТАКТЫ =====
        logger.info("Заполнение Контактов...")
        
        ContentRepository.set(
            section='contacts',
            key='title',
            value_ru='Контакты',
            value_lv='Kontakti',
            value_en='Contacts'
        )
        
        ContentRepository.set(
            section='contacts',
            key='subtitle',
            value_ru='Свяжитесь с нами',
            value_lv='Sazinieties ar mums',
            value_en='Contact Us'
        )
        
        ContentRepository.set(
            section='contacts',
            key='form_title',
            value_ru='Записаться на консультацию',
            value_lv='Pierakstīties konsultācijai',
            value_en='Book a Consultation'
        )
        
        ContentRepository.set(
            section='contacts',
            key='name_placeholder',
            value_ru='Ваше имя',
            value_lv='Jūsu vārds',
            value_en='Your Name'
        )
        
        ContentRepository.set(
            section='contacts',
            key='email_placeholder',
            value_ru='Email',
            value_lv='E-pasts',
            value_en='Email'
        )
        
        ContentRepository.set(
            section='contacts',
            key='phone_placeholder',
            value_ru='Телефон',
            value_lv='Tālrunis',
            value_en='Phone'
        )
        
        ContentRepository.set(
            section='contacts',
            key='message_placeholder',
            value_ru='Ваше сообщение',
            value_lv='Jūsu ziņojums',
            value_en='Your Message'
        )
        
        ContentRepository.set(
            section='contacts',
            key='submit_button',
            value_ru='Отправить',
            value_lv='Nosūtīt',
            value_en='Send'
        )
        
        ContentRepository.set(
            section='contacts',
            key='address_title',
            value_ru='Адрес',
            value_lv='Adrese',
            value_en='Address'
        )
        
        ContentRepository.set(
            section='contacts',
            key='phone_title',
            value_ru='Телефон',
            value_lv='Tālrunis',
            value_en='Phone'
        )
        
        ContentRepository.set(
            section='contacts',
            key='email_title',
            value_ru='Email',
            value_lv='E-pasts',
            value_en='Email'
        )
        
        # ===== AURACLOUD SLIDER =====
        logger.info("Заполнение AuraCloud слайдера...")
        
        ContentRepository.set(
            section='auracloud_slider',
            key='title',
            value_ru='Технология AuraCloud® 3D',
            value_lv='AuraCloud® 3D tehnoloģija',
            value_en='AuraCloud® 3D Technology'
        )
        
        ContentRepository.set(
            section='auracloud_slider',
            key='subtitle',
            value_ru='Увидьте разницу до и после',
            value_lv='Redziet atšķirību pirms un pēc',
            value_en='See the difference before and after'
        )
        
        ContentRepository.set(
            section='auracloud_slider',
            key='before_label',
            value_ru='До',
            value_lv='Pirms',
            value_en='Before'
        )
        
        ContentRepository.set(
            section='auracloud_slider',
            key='after_label',
            value_ru='После',
            value_lv='Pēc',
            value_en='After'
        )
        
        ContentRepository.set(
            section='auracloud_slider',
            key='description',
            value_ru='AuraCloud® 3D показывает изменения энергетического поля',
            value_lv='AuraCloud® 3D parāda enerģētiskā lauka izmaiņas',
            value_en='AuraCloud® 3D shows energy field changes'
        )
        
        # ===== ОТЗЫВЫ =====
        logger.info("Заполнение Отзывов...")
        
        ContentRepository.set(
            section='reviews',
            key='title',
            value_ru='Отзывы наших клиентов',
            value_lv='Mūsu klientu atsauksmes',
            value_en='Customer Reviews'
        )
        
        ContentRepository.set(
            section='reviews',
            key='subtitle',
            value_ru='Что говорят о нас',
            value_lv='Ko saka par mums',
            value_en='What they say about us'
        )
        
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
        
        # ===== FOOTER =====
        logger.info("Заполнение Footer...")
        
        ContentRepository.set(
            section='footer',
            key='copyright',
            value_ru='© OilFusion 2024. Все права защищены.',
            value_lv='© OilFusion 2024. Visas tiesības aizsargātas.',
            value_en='© OilFusion 2024. All rights reserved.'
        )
        
        logger.info("✅ Контент успешно заполнен для всех секций на трёх языках!")
        logger.info("Теперь можно переключать языки на сайте и редактировать в админке")


if __name__ == '__main__':
    seed_content()

