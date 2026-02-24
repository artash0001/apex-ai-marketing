"""
Apex AI Marketing - Russian Telegram Community Post Templates

Weekly insight posts for Russian-speaking Telegram business communities
in Dubai (e.g., "Бизнес в Дубае", "Маркетинг ОАЭ", etc.).

These are value-first posts designed to establish expertise and
generate inbound interest. Not direct sales pitches.

Placeholders:
  {topic} - Specific topic being covered
  {stat} - Relevant statistic or data point
  {insight} - The key insight or takeaway
  {cta_link} - Call-to-action link (Calendly or article)
  {week_number} - Week number for series continuity
"""

TELEGRAM_WEEKLY_INSIGHTS_RU = {
    "digital_infrastructure": {
        "name": "Цифровая инфраструктура",
        "post": (
            "Маркетинг в Дубае: инсайт недели #{week_number}\n\n"
            "{topic}\n\n"
            "Проанализировали {stat} компаний в ОАЭ и вот что обнаружили:\n\n"
            "{insight}\n\n"
            "Почему это важно: большинство бизнесов в Дубае запускают "
            "маркетинг как набор отдельных активностей -- пост в Instagram, "
            "объявление в Google, статья на сайте. Каждая живёт своей жизнью.\n\n"
            "Компании, которые выстраивают это как единую инфраструктуру, "
            "получают кумулятивный эффект: каждый элемент усиливает остальные.\n\n"
            "Практический вывод: начните с аудита того, что у вас уже есть. "
            "Часто 80% нужных элементов на месте, просто не связаны между собой.\n\n"
            "Если хотите получить бесплатный аудит маркетинговой "
            "инфраструктуры вашей компании -- пишите в ЛС или "
            "записывайтесь: {cta_link}\n\n"
            "#маркетинг #дубай #бизнес #рост"
        ),
    },
    "ai_marketing": {
        "name": "AI в маркетинге",
        "post": (
            "AI в маркетинге: что реально работает #{week_number}\n\n"
            "{topic}\n\n"
            "Много хайпа, мало конкретики. Делюсь тем, что видим на практике:\n\n"
            "{insight}\n\n"
            "Ключевой момент: AI в маркетинге -- это не про замену людей. "
            "Это про построение системы, которая учится и улучшается "
            "каждую неделю автоматически.\n\n"
            "Три вещи, которые AI уже делает лучше человека:\n"
            "1. Анализ данных и выявление паттернов\n"
            "2. A/B тестирование и оптимизация в реальном времени\n"
            "3. Персонализация контента под сегменты аудитории\n\n"
            "Три вещи, где AI пока нужен человек:\n"
            "1. Стратегия и позиционирование\n"
            "2. Креативные прорывы\n"
            "3. Построение отношений\n\n"
            "Золотая середина -- AI-инфраструктура с человеческим "
            "стратегическим управлением.\n\n"
            "Вопросы по AI в маркетинге? Пишите, разберём ваш случай: {cta_link}\n\n"
            "#AI #маркетинг #технологии #дубай"
        ),
    },
    "growth_cases": {
        "name": "Кейсы роста",
        "post": (
            "Как это работает: разбор подхода #{week_number}\n\n"
            "{topic}\n\n"
            "Типичная ситуация: {stat}\n\n"
            "{insight}\n\n"
            "Что обычно меняем в первую очередь:\n\n"
            "1. Аудит всей воронки от первого касания до сделки\n"
            "2. Находим 3-5 точек, где теряется больше всего клиентов\n"
            "3. Выстраиваем систему, а не отдельные кампании\n"
            "4. Подключаем AI для непрерывной оптимизации\n"
            "5. Еженедельно замеряем и корректируем\n\n"
            "Результат через 90 дней: предсказуемый поток заявок "
            "вместо хаотичных всплесков.\n\n"
            "Хотите разобрать вашу ситуацию? Бесплатный аудит "
            "маркетинговой инфраструктуры: {cta_link}\n\n"
            "#маркетинг #рост #дубай #бизнесдубай"
        ),
    },
    "local_seo": {
        "name": "Локальное SEO в ОАЭ",
        "post": (
            "Локальный маркетинг в ОАЭ: факт недели #{week_number}\n\n"
            "{topic}\n\n"
            "{stat}\n\n"
            "{insight}\n\n"
            "Что проверить прямо сейчас:\n\n"
            "- Google Business Profile: заполнен на 100%?\n"
            "- Отзывы: отвечаете на все, включая негативные?\n"
            "- Сайт: есть страницы под каждый район/эмират?\n"
            "- Справочники: Apple Maps, Bing Places, 2GIS?\n"
            "- Структурированные данные: LocalBusiness schema на сайте?\n\n"
            "Каждый из этих пунктов -- это канал, через который "
            "клиенты ищут вас прямо сейчас. Если какой-то не настроен, "
            "клиенты уходят к конкурентам.\n\n"
            "Хотите узнать, как выглядит ваша локальная видимость? "
            "Бесплатная проверка: {cta_link}\n\n"
            "#SEO #локальныймаркетинг #дубай #ОАЭ"
        ),
    },
}


def get_telegram_post(
    post_type: str,
    week_number: int = 1,
    topic: str = "",
    stat: str = "",
    insight: str = "",
    cta_link: str = "https://calendly.com/apex-ai-marketing",
) -> str:
    """Render a Telegram community post.

    Args:
        post_type: Template key from TELEGRAM_WEEKLY_INSIGHTS_RU.
        week_number: Week number for series continuity.
        topic: Specific topic being covered.
        stat: Relevant statistic or data point.
        insight: The key insight or takeaway.
        cta_link: Call-to-action link.

    Returns:
        Rendered post text.
    """
    template = TELEGRAM_WEEKLY_INSIGHTS_RU.get(post_type)
    if not template:
        raise ValueError(f"Unknown post type: {post_type}")

    return template["post"].format(
        week_number=week_number,
        topic=topic,
        stat=stat,
        insight=insight,
        cta_link=cta_link,
    )


# Rotation schedule for weekly posts
WEEKLY_ROTATION = [
    "digital_infrastructure",
    "ai_marketing",
    "growth_cases",
    "local_seo",
]


def get_post_type_for_week(week_number: int) -> str:
    """Return the post type for a given week based on rotation."""
    return WEEKLY_ROTATION[(week_number - 1) % len(WEEKLY_ROTATION)]
