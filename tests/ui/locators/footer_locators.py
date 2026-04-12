class FooterLocators:
    """Футер — на сайте нет тега <footer>, просто div-ы в конце страницы."""
    # ищем по тексту лицензии — он точно есть только в нижней части
    FOOTER = "text=Лицензия"
    # соцсети — 5 штук: телега, вк, макс, ютуб, тикток
    SOCIAL_LINKS = "a[href*='t.me'], a[href*='vk.com'], a[href*='youtube'], a[href*='tiktok'], a[href*='max.ru']"
    # документы — все лежат в /documents/
    DOCUMENTS_LINKS = "a[href*='/documents/']"
    # текст лицензии
    LICENSE_TEXT = "text=Лицензия"
