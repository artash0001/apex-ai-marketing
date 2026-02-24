"""
Apex AI Marketing - Agent 15: Russian Localizer

Model: Claude Sonnet
Engine: All engines (Russian market)
Language: ru

Creates and adapts all Russian-language content.
Does NOT translate — writes natively.
"""

from agents.base_agent import BaseAgent, AgentOutput
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class RussianLocalizer(BaseAgent):
    name = "Russian Localizer"
    role = (
        "Creates and adapts all Russian-language content. "
        "Does NOT translate — writes natively."
    )
    engine = "All engines (Russian market)"
    model = settings.DEFAULT_MODEL  # Claude Sonnet
    temperature = 0.7
    max_tokens = 6144
    language = "ru"

    system_prompt = (
        "Вы — русскоязычный маркетолог и копирайтер в Apex AI Marketing. "
        "Вы пишете контент для русскоязычных предпринимателей в Дубае и ОАЭ.\n\n"
        "Правила:\n"
        "- Пишите на родном русском, НЕ переводите с английского\n"
        "- Используйте форму 'Вы' в деловой переписке\n"
        "- Терминологию 'growth infrastructure' адаптируйте как 'инфраструктура роста' "
        "или 'система роста'\n"
        "- 'Engine' = 'движок' или 'система' (зависит от контекста)\n"
        "- Стиль: деловой, прямой, конкретный. Без воды и пустых обещаний.\n"
        "- Для Telegram: более неформальный тон, но всё равно профессиональный\n"
        "- Учитывайте специфику русского бизнес-сообщества в Дубае: referrals важнее "
        "рекламы, Telegram — основной канал, доверие строится через личные встречи и RBC\n"
        "- Никогда не фабрикуйте статистику и результаты клиентов\n\n"
        "Голос бренда Apex AI Marketing (на русском):\n"
        "- Инженерный подход, прямота, измеримость, анти-хайп\n"
        "- Сначала бизнес-результат, потом механизм\n"
        "- Используйте: 'система,' 'инфраструктура,' 'движок,' 'строить,' 'измерять'\n"
        "- НИКОГДА не используйте: 'революционный,' 'инновационный,' 'уникальный,' "
        "'не имеющий аналогов,' 'синергия,' 'комплексный подход'\n"
        "- НИКОГДА не выдумывайте статистику, клиентов, кейсы или результаты\n"
        "- При неуверенности: 'Мы пока не знаем — вот как мы это выясним'\n\n"
        "Терминология (EN → RU):\n"
        "- Growth Infrastructure → Инфраструктура роста\n"
        "- Engine → Движок / Система\n"
        "- Revenue Stack Foundation → Фундамент для доходов (CRM + автоматизация)\n"
        "- Local Visibility Engine → Система локальной видимости\n"
        "- Inbound Demand Engine → Система входящего потока\n"
        "- Outbound Engine → Система исходящего привлечения\n"
        "- Paid Acquisition Engine → Система платного привлечения\n"
        "- Lifecycle & Retention Engine → Система удержания и жизненного цикла\n"
        "- Growth Ops Retainer → Операционное управление ростом\n"
        "- Infrastructure Audit → Аудит инфраструктуры\n"
        "- Revenue Leak → Утечка дохода\n"
        "- Pipeline → Воронка / Пайплайн\n"
        "- KPI → KPI (не переводить)\n"
        "- CRM → CRM (не переводить)\n"
        "- ROI → ROI (не переводить)\n\n"
        "Специфика рынка Дубай/ОАЭ:\n"
        "- Русскоязычное сообщество: ~300 000 резидентов, 3 000+ компаний\n"
        "- Основные каналы: Telegram, WhatsApp, личные встречи\n"
        "- Russian Business Council (RBC) — важная площадка для нетворкинга\n"
        "- Доверие строится через рекомендации и личные контакты\n"
        "- Деловой этикет: формальность + конкретика\n"
        "- Многие предприниматели ведут бизнес на двух языках (RU + EN)"
    )

    async def localize_content(
        self,
        content: str,
        content_type: str,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Localize English content into native Russian.

        Parameters
        ----------
        content : str
            The English content to localize.
        content_type : str
            Type: 'article', 'email', 'ad_copy', 'landing_page',
            'proposal', 'report', 'social_post'.
        """
        task = (
            f"Адаптируйте следующий контент (тип: {content_type}) на русский язык.\n\n"
            "ВАЖНО: Не переводите дословно. Перепишите контент так, чтобы он:\n"
            "- Звучал как написанный русскоязычным маркетологом\n"
            "- Учитывал культурные особенности русскоязычной аудитории в Дубае\n"
            "- Использовал правильную деловую терминологию на русском\n"
            "- Сохранял ключевые смыслы и призывы к действию\n\n"
            "Оригинальный контент (EN):\n"
            "---\n"
            f"{content}\n"
            "---\n\n"
            "Произведите:\n\n"
            "1. Русская версия контента\n"
            "   - Полный текст на русском языке\n"
            "   - Адаптированные CTA\n"
            "   - Адаптированная терминология\n\n"
            "2. Заметки по адаптации\n"
            "   - Что было изменено и почему\n"
            "   - Культурные адаптации\n"
            "   - Терминологические решения\n\n"
            "3. Рекомендации\n"
            "   - Нужна ли дополнительная адаптация для Telegram?\n"
            "   - Есть ли элементы, которые не подходят для русскоязычной аудитории?\n"
            "   - Предложения по улучшению для русского рынка"
        )
        return await self.run(
            task=task,
            context={"language": "ru"},
            db=db,
            task_id=task_id,
        )

    async def write_russian_outreach(
        self,
        prospect_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Write native Russian outreach sequences.

        Parameters
        ----------
        prospect_data : dict
            Prospect info, company, pain points, outreach channel.
        """
        task = (
            "Напишите последовательность outreach-сообщений на русском языке "
            "для данного потенциального клиента.\n\n"
            "Произведите:\n\n"
            "1. Email-последовательность (4 письма за 14 дней)\n\n"
            "   Письмо 1 — Зацепка (День 1)\n"
            "   - Тема: строчными, неформально, вызывающая любопытство (до 7 слов)\n"
            "   - Персонализированное наблюдение о ИХ бизнесе\n"
            "   - Одна конкретная проблема в инфраструктуре\n"
            "   - Лёгкий CTA (вопрос, не 'запишитесь на звонок')\n"
            "   - 80-120 слов максимум\n\n"
            "   Письмо 2 — Ценность (День 4)\n"
            "   - Новая тема или ответ на первое письмо\n"
            "   - Конкретный инсайт для их отрасли\n"
            "   - Мини-находка аудита или бенчмарк\n"
            "   - 80-120 слов\n\n"
            "   Письмо 3 — Доказательство (День 8)\n"
            "   - Методология или фреймворк, который мы используем\n"
            "   - Конкретный пример: проблема → системное решение\n"
            "   - Предложение бесплатного экспресс-аудита\n"
            "   - 80-120 слов\n\n"
            "   Письмо 4 — Прощание (День 14)\n"
            "   - Признание, что они заняты\n"
            "   - Последнее ценностное предложение\n"
            "   - Дверь остаётся открытой\n"
            "   - 60-80 слов\n\n"
            "2. Telegram-сообщения (3 варианта)\n"
            "   - Для группового чата (пост с ценностью)\n"
            "   - Для личного сообщения (после знакомства)\n"
            "   - Для follow-up (после первого контакта)\n\n"
            "3. WhatsApp-сообщения (2 варианта)\n"
            "   - Первое касание (краткое, профессиональное)\n"
            "   - Follow-up с предложением аудита\n\n"
            "Правила:\n"
            "- Используйте форму 'Вы'\n"
            "- Упоминайте русскоязычный сервис как преимущество\n"
            "- Фреймируйте предложение как 'система', не 'услуга'\n"
            "- Ссылайтесь на RBC и Telegram-сообщество где уместно"
        )
        return await self.run(
            task=task,
            context={"language": "ru", "additional_data": f"Данные о клиенте:\n{prospect_data}"},
            db=db,
            task_id=task_id,
        )

    async def write_russian_proposal_section(
        self,
        english_section: str,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Write a Russian version of a proposal section.

        Parameters
        ----------
        english_section : str
            The English proposal section to create a Russian version of.
        """
        task = (
            "Создайте русскую версию этого раздела коммерческого предложения.\n\n"
            "Английская версия:\n"
            "---\n"
            f"{english_section}\n"
            "---\n\n"
            "Требования:\n"
            "- НЕ переводите дословно — напишите заново на русском\n"
            "- Деловой стиль, уверенный тон\n"
            "- Используйте русскую терминологию из нашего глоссария\n"
            "- Сохраните все ключевые цифры, сроки и конкретику\n"
            "- Адаптируйте примеры для русскоязычной аудитории в ОАЭ\n"
            "- Форма обращения: 'Вы'\n"
            "- Оставьте цены в USD (стандарт для Дубая)\n"
            "- Технические термины (CRM, KPI, ROI) оставьте на английском\n\n"
            "Формат: готовый к вставке раздел предложения на русском языке."
        )
        return await self.run(
            task=task,
            context={"language": "ru"},
            db=db,
            task_id=task_id,
        )

    async def adapt_for_telegram(
        self,
        content: str,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Adapt content for Telegram (Russian-speaking business community).

        Parameters
        ----------
        content : str
            The content to adapt for Telegram posting.
        """
        task = (
            "Адаптируйте этот контент для Telegram-канала, ориентированного на "
            "русскоязычных предпринимателей в Дубае.\n\n"
            "Исходный контент:\n"
            "---\n"
            f"{content}\n"
            "---\n\n"
            "Произведите:\n\n"
            "1. Telegram-пост (основной)\n"
            "   - 150-300 слов\n"
            "   - Хук в первых 2 строках (привлечь внимание в ленте)\n"
            "   - Ценность в основной части (инсайт, совет, анализ)\n"
            "   - CTA в конце (обсуждение, DM, ссылка)\n"
            "   - Форматирование для Telegram (абзацы, маркеры, эмодзи умеренно)\n\n"
            "2. Короткая версия (для репоста)\n"
            "   - 50-80 слов\n"
            "   - Ключевая мысль + CTA\n\n"
            "3. Серия карточек (если контент длинный)\n"
            "   - 3-5 карточек по 50-80 слов каждая\n"
            "   - Каждая карточка — самостоятельная мысль\n"
            "   - Последняя карточка — CTA\n\n"
            "4. Варианты заголовков для поста (3 варианта)\n\n"
            "Тон:\n"
            "- Профессиональный, но дружелюбный\n"
            "- Неформальнее, чем email, но всё ещё экспертный\n"
            "- Используйте 'вы' (строчную) — в Telegram допустимо\n"
            "- Эмодзи: 1-3 на пост, не больше\n"
            "- Никакого хайпа и пустых обещаний"
        )
        return await self.run(
            task=task,
            context={"language": "ru"},
            db=db,
            task_id=task_id,
        )
