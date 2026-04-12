class MainPageLocators:
    """Главная страница — баннер, категории, отзывы."""
    # баннер — промо-блок в начале страницы (сезонные акции, летние курсы и т.д.)
    # обычно это ссылка с большой картинкой (.webp) в начале контента
    HERO_BANNER = "a[href*='summer_course']:has(img), .tile__tileb.active, a:has(img[src*='bonus'])"
    # возрастные категории — ровно 4 карточки в контенте (не в шапке)
    # отличаются от навигационных тем, что содержат текст "Выбрать"
    AGE_CATEGORY_CARDS = (
        "a[href*='/doshkolniki']:has-text('Выбрать'),"
        "a[href*='/nachalnaya-shkola']:has-text('Выбрать'),"
        "a[href*='/srednyaya-shkola']:has-text('Выбрать'),"
        "a[href*='/starshaya-shkola']:has-text('Выбрать')"
    )
    # секция возрастных категорий — первая карточка, к ней скроллим
    AGE_CATEGORY_SECTION = "a[href*='/doshkolniki']:has-text('Выбрать')"
    # направления — карточки предметов с иконками (математика, русский и т.д.)
    DIRECTION_BLOCKS = "a:has(img[src*='fon_'])"
    # секция отзывов — ищем по заголовку "гордимся"
    REVIEWS_SECTION = "text=Результаты, которыми мы гордимся"
    # отдельные отзывы — у каждого есть аватар *_krug.webp и ссылка "Читать весь отзыв"
    REVIEW_ITEMS = "img[src*='_krug.webp']"
    # текст отзыва — ссылка "Читать весь отзыв" рядом с аватаром
    REVIEW_TEXT_LINKS = "a:has-text('Читать весь отзыв')"
    # CTA-кнопки — оранжевые призывы к действию по всей странице
    CTA_BUTTONS = ".btn-warning"
    # футер — текст лицензии в самом низу
    FOOTER_AREA = "text=Лицензия"
    # контент страницы целиком — body
    PAGE_BODY = "body"
