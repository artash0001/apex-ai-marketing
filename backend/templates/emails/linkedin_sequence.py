"""
Apex AI Marketing - LinkedIn DM Sequence Templates

3-message LinkedIn outreach sequence. Shorter, more conversational
tone suited to the LinkedIn platform.

Placeholders:
  {name} - Prospect first name
  {company} - Company name
  {specific_finding} - Personalized observation
  {mutual_connection} - Shared connection or group (optional)
  {industry} - Prospect's industry
"""

LINKEDIN_SEQUENCE_EN = {
    1: {
        "name": "Connection Request + Value Hook",
        "day": 1,
        "note_with_request": True,
        "message": (
            "Hi {name}, I came across {company} while researching "
            "{industry} companies in the region. Noticed {specific_finding} "
            "-- would love to connect and share a quick observation that "
            "might be useful for your growth."
        ),
    },
    2: {
        "name": "The Insight DM",
        "day": 3,
        "note_with_request": False,
        "message": (
            "Thanks for connecting, {name}! As promised, here is the "
            "observation:\n\n"
            "{specific_finding}\n\n"
            "We see this pattern a lot with {industry} companies. "
            "The businesses that treat marketing as infrastructure "
            "rather than campaigns tend to see 3-5x better results "
            "at similar spend.\n\n"
            "We offer a free growth infrastructure audit that maps out "
            "exactly where the gaps are. Takes 48h, and you keep the "
            "full report. Interested?"
        ),
    },
    3: {
        "name": "Soft Close",
        "day": 7,
        "note_with_request": False,
        "message": (
            "Hi {name}, just circling back on that growth audit offer "
            "for {company}. Totally understand if the timing is off.\n\n"
            "If it helps, here is our calendar link -- zero pressure, "
            "and you will walk away with actionable insights either way:\n"
            "https://calendly.com/apex-ai-marketing\n\n"
            "Either way, happy to stay connected and share insights "
            "on {industry} growth when relevant."
        ),
    },
}

LINKEDIN_SEQUENCE_RU = {
    1: {
        "name": "Запрос на подключение",
        "day": 1,
        "note_with_request": True,
        "message": (
            "Здравствуйте, {name}! Нашёл {company}, изучая "
            "компании из сферы {industry} в регионе. Заметил "
            "{specific_finding} -- хотел бы связаться и поделиться "
            "наблюдением, которое может быть полезно для роста."
        ),
    },
    2: {
        "name": "Инсайт",
        "day": 3,
        "note_with_request": False,
        "message": (
            "Спасибо за контакт, {name}! Как обещал, вот наблюдение:\n\n"
            "{specific_finding}\n\n"
            "Мы часто видим эту картину у компаний в {industry}. "
            "Бизнесы, которые выстраивают маркетинг как инфраструктуру, "
            "а не набор кампаний, обычно получают в 3-5 раз "
            "лучший результат при тех же затратах.\n\n"
            "Мы проводим бесплатный аудит маркетинговой инфраструктуры, "
            "который точно показывает, где пробелы. Занимает 48 часов, "
            "полный отчёт остаётся у вас. Интересно?"
        ),
    },
    3: {
        "name": "Мягкое закрытие",
        "day": 7,
        "note_with_request": False,
        "message": (
            "{name}, возвращаюсь к предложению по аудиту для {company}. "
            "Полностью понимаю, если сейчас не время.\n\n"
            "Вот ссылка на календарь -- без давления, и вы в любом "
            "случае получите полезные инсайты:\n"
            "https://calendly.com/apex-ai-marketing\n\n"
            "В любом случае рад оставаться на связи и делиться "
            "наблюдениями о росте в {industry}."
        ),
    },
}


def get_linkedin_sequence(language: str = "en") -> dict:
    """Return the LinkedIn sequence for the given language."""
    if language == "ru":
        return LINKEDIN_SEQUENCE_RU
    return LINKEDIN_SEQUENCE_EN


def render_linkedin_message(
    step: int,
    language: str = "en",
    **kwargs,
) -> str:
    """Render a LinkedIn message with the given context variables.

    Args:
        step: Sequence step (1, 2, or 3).
        language: Language code ('en' or 'ru').
        **kwargs: Template variables (name, company, specific_finding, etc.)

    Returns:
        Rendered message string.
    """
    sequence = get_linkedin_sequence(language)
    template = sequence.get(step)
    if not template:
        raise ValueError(f"No LinkedIn template for step {step} in {language}")

    return template["message"].format(**kwargs)
