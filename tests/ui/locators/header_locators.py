class HeaderLocators:
    """Шапка сайта — меню, логотип, кнопки."""
    # логотип — картинка logo.svg, по клику ведёт на главную
    # пробуем найти <a> с картинкой, если нет — саму картинку
    LOGO = "a:has(img[src*='logo.svg']), img[src*='logo.svg']"
    NAV_ALL_COURSES = "a[href*='filter_courses']"
    NAV_SUMMER_COURSES = "a[href*='summer_course']"
    NAV_BLOG = "a[href*='blog']"
    NAV_ENROLLMENT_BUTTON = "text=Подобрать занятия"
    NAV_LOGIN_BUTTON = "a[href*='lk-dev.tochka-school.ru']"
    # хедер целиком — нужен чтобы проверить видимость после скролла
    HEADER = "header, nav, [class*='header'], [class*='Header']"
