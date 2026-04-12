class CoursesLocators:
    """Каталог курсов — /filter_courses."""
    # карточки курсов — появляются динамически через JS как .tile__tileb.active
    # если нет активных тайлов, фолбэк на ссылки filter_courses/предмет/класс
    COURSE_CARD = ".tile__tileb.active, a[href*='filter_courses/'][href*='/']"
    # названия — текст внутри карточки, ищем через "Курс по"
    COURSE_TITLE = ".tile__tileb.active .tmore_b, a[href*='filter_courses/'][href*='/']"
    # общий контент страницы — body, чтобы проверять текст
    PAGE_BODY = "body"
    # подвал — нижняя часть страницы, до которой скроллим
    FOOTER = "footer"
