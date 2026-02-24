"""
Apex AI Marketing - Onboarding Email Templates

Templates for the client onboarding flow:
  1. Welcome email (after signing)
  2. Access request (brand assets, logins)
  3. Kickoff confirmation (meeting details)

Available in both EN and RU.

Placeholders:
  {name} - Client contact name
  {company} - Company name
  {engines} - List of active engines
  {kickoff_date} - Kickoff meeting date
  {kickoff_time} - Kickoff meeting time
  {kickoff_link} - Video call link
  {portal_url} - Client portal URL
  {account_manager} - Account manager name
"""

ONBOARDING_EN = {
    "welcome": {
        "subject": "Welcome to Apex AI Marketing, {name}!",
        "body": (
            "<div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>"
            "<h2>Welcome to Apex AI Marketing!</h2>"
            "<p>Hi {name},</p>"
            "<p>We are thrilled to have {company} on board. Your growth "
            "infrastructure is about to get a serious upgrade.</p>"
            "<h3>What happens next:</h3>"
            "<ol>"
            "<li><strong>Access Setup (Today)</strong> -- You will receive "
            "a separate email requesting access to your current platforms "
            "and brand assets.</li>"
            "<li><strong>Kickoff Call ({kickoff_date})</strong> -- We will "
            "walk through your custom growth roadmap, align on KPIs, and "
            "set the 90-day milestone targets.</li>"
            "<li><strong>Engine Activation (Week 1)</strong> -- Your engines "
            "go live with the first deliverables within 5 business days.</li>"
            "</ol>"
            "<h3>Your active engines:</h3>"
            "<p>{engines}</p>"
            "<h3>Your client portal:</h3>"
            "<p>Track progress, review deliverables, and communicate with "
            "your team here: <a href='{portal_url}'>{portal_url}</a></p>"
            "<p>Your account manager is <strong>{account_manager}</strong>. "
            "Feel free to reach out anytime via email or Telegram.</p>"
            "<p>Let us build something great together.</p>"
            "<p>Best,<br/>"
            "The Apex AI Marketing Team</p>"
            "</div>"
        ),
    },
    "access_request": {
        "subject": "Access request for {company}'s growth engines",
        "body": (
            "<div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>"
            "<h2>Access Request</h2>"
            "<p>Hi {name},</p>"
            "<p>To activate your growth engines, we need access to "
            "the following platforms. Please share credentials or "
            "invite our team account "
            "(<strong>team@apexaimarketing.pro</strong>):</p>"
            "<h3>Required access:</h3>"
            "<table style='border-collapse: collapse; width: 100%;'>"
            "<tr style='background: #f5f5f5;'>"
            "<th style='padding: 8px; border: 1px solid #ddd; text-align: left;'>Platform</th>"
            "<th style='padding: 8px; border: 1px solid #ddd; text-align: left;'>Access Level</th>"
            "<th style='padding: 8px; border: 1px solid #ddd; text-align: left;'>Priority</th>"
            "</tr>"
            "<tr>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Google Analytics</td>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Editor</td>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>High</td>"
            "</tr>"
            "<tr>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Google Search Console</td>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Full</td>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>High</td>"
            "</tr>"
            "<tr>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Google Business Profile</td>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Manager</td>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>High</td>"
            "</tr>"
            "<tr>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Google Ads</td>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Manager</td>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Medium</td>"
            "</tr>"
            "<tr>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Meta Business Suite</td>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Admin</td>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Medium</td>"
            "</tr>"
            "<tr>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Website CMS</td>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Editor</td>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>High</td>"
            "</tr>"
            "<tr>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Email Marketing Platform</td>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Admin</td>"
            "<td style='padding: 8px; border: 1px solid #ddd;'>Medium</td>"
            "</tr>"
            "</table>"
            "<h3>Brand assets needed:</h3>"
            "<ul>"
            "<li>Logo files (SVG/PNG, light and dark versions)</li>"
            "<li>Brand guidelines (if available)</li>"
            "<li>Brand color codes and fonts</li>"
            "<li>Any existing content style guides</li>"
            "<li>Photography/image library access</li>"
            "</ul>"
            "<p>Please share via Google Drive, Dropbox, or email. "
            "All credentials are stored securely in our encrypted vault.</p>"
            "<p>Questions? Reply to this email or message {account_manager} directly.</p>"
            "<p>Best,<br/>"
            "The Apex AI Marketing Team</p>"
            "</div>"
        ),
    },
    "kickoff_confirmation": {
        "subject": "Kickoff call confirmed: {company} x Apex AI Marketing",
        "body": (
            "<div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>"
            "<h2>Kickoff Call Confirmed</h2>"
            "<p>Hi {name},</p>"
            "<p>Your kickoff call is confirmed:</p>"
            "<div style='background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;'>"
            "<p><strong>Date:</strong> {kickoff_date}<br/>"
            "<strong>Time:</strong> {kickoff_time} (Dubai time)<br/>"
            "<strong>Link:</strong> <a href='{kickoff_link}'>{kickoff_link}</a></p>"
            "</div>"
            "<h3>Agenda:</h3>"
            "<ol>"
            "<li>Audit findings review and key opportunities (10 min)</li>"
            "<li>Growth roadmap walkthrough (15 min)</li>"
            "<li>KPI alignment and 90-day targets (10 min)</li>"
            "<li>Engine activation timeline (5 min)</li>"
            "<li>Q&A (10 min)</li>"
            "</ol>"
            "<h3>Please prepare:</h3>"
            "<ul>"
            "<li>Any questions from the audit report</li>"
            "<li>Your top 3 business priorities for the next quarter</li>"
            "<li>Access credentials (if not yet shared)</li>"
            "</ul>"
            "<p>Looking forward to getting started!</p>"
            "<p>Best,<br/>"
            "{account_manager}<br/>"
            "Apex AI Marketing</p>"
            "</div>"
        ),
    },
}

ONBOARDING_RU = {
    "welcome": {
        "subject": "Добро пожаловать в Apex AI Marketing, {name}!",
        "body": (
            "<div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>"
            "<h2>Добро пожаловать в Apex AI Marketing!</h2>"
            "<p>Здравствуйте, {name}!</p>"
            "<p>Мы рады видеть {company} в числе наших клиентов. "
            "Ваша маркетинговая инфраструктура скоро выйдет на "
            "новый уровень.</p>"
            "<h3>Что будет дальше:</h3>"
            "<ol>"
            "<li><strong>Настройка доступов (сегодня)</strong> -- Вы "
            "получите отдельное письмо с запросом доступов к текущим "
            "платформам и брендовым материалам.</li>"
            "<li><strong>Стартовый звонок ({kickoff_date})</strong> -- "
            "Пройдёмся по персональному плану роста, согласуем KPI "
            "и установим цели на 90 дней.</li>"
            "<li><strong>Запуск движков (неделя 1)</strong> -- Ваши "
            "движки начнут работать, первые результаты в течение "
            "5 рабочих дней.</li>"
            "</ol>"
            "<h3>Ваши активные движки:</h3>"
            "<p>{engines}</p>"
            "<h3>Ваш клиентский портал:</h3>"
            "<p>Отслеживайте прогресс, проверяйте материалы и "
            "общайтесь с командой здесь: "
            "<a href='{portal_url}'>{portal_url}</a></p>"
            "<p>Ваш менеджер -- <strong>{account_manager}</strong>. "
            "Пишите в любое время по email или в Telegram.</p>"
            "<p>Давайте строить рост вместе!</p>"
            "<p>С уважением,<br/>"
            "Команда Apex AI Marketing</p>"
            "</div>"
        ),
    },
    "access_request": {
        "subject": "Запрос доступов для запуска движков {company}",
        "body": (
            "<div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>"
            "<h2>Запрос доступов</h2>"
            "<p>Здравствуйте, {name}!</p>"
            "<p>Для запуска ваших движков роста нам нужен доступ к "
            "следующим платформам. Пожалуйста, поделитесь данными "
            "или пригласите наш аккаунт "
            "(<strong>team@apexaimarketing.pro</strong>):</p>"
            "<h3>Необходимые доступы:</h3>"
            "<ul>"
            "<li>Google Analytics (уровень: редактор)</li>"
            "<li>Google Search Console (полный доступ)</li>"
            "<li>Google Business Profile (менеджер)</li>"
            "<li>Google Ads (менеджер)</li>"
            "<li>Meta Business Suite (администратор)</li>"
            "<li>CMS сайта (редактор)</li>"
            "<li>Платформа email-рассылок (администратор)</li>"
            "</ul>"
            "<h3>Брендовые материалы:</h3>"
            "<ul>"
            "<li>Файлы логотипа (SVG/PNG, светлая и тёмная версии)</li>"
            "<li>Брендбук (если есть)</li>"
            "<li>Цвета бренда и шрифты</li>"
            "<li>Гайд по стилю контента (если есть)</li>"
            "<li>Фотобанк / библиотека изображений</li>"
            "</ul>"
            "<p>Отправить можно через Google Drive, Dropbox или email. "
            "Все данные хранятся в зашифрованном хранилище.</p>"
            "<p>Вопросы? Ответьте на это письмо или напишите "
            "{account_manager} напрямую.</p>"
            "<p>С уважением,<br/>"
            "Команда Apex AI Marketing</p>"
            "</div>"
        ),
    },
    "kickoff_confirmation": {
        "subject": "Стартовый звонок подтверждён: {company} x Apex AI Marketing",
        "body": (
            "<div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>"
            "<h2>Стартовый звонок подтверждён</h2>"
            "<p>Здравствуйте, {name}!</p>"
            "<p>Ваш стартовый звонок подтверждён:</p>"
            "<div style='background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;'>"
            "<p><strong>Дата:</strong> {kickoff_date}<br/>"
            "<strong>Время:</strong> {kickoff_time} (время Дубая)<br/>"
            "<strong>Ссылка:</strong> <a href='{kickoff_link}'>{kickoff_link}</a></p>"
            "</div>"
            "<h3>Повестка:</h3>"
            "<ol>"
            "<li>Обзор результатов аудита и ключевых возможностей (10 мин)</li>"
            "<li>Разбор плана роста (15 мин)</li>"
            "<li>Согласование KPI и целей на 90 дней (10 мин)</li>"
            "<li>Таймлайн запуска движков (5 мин)</li>"
            "<li>Вопросы и ответы (10 мин)</li>"
            "</ol>"
            "<h3>Подготовьте, пожалуйста:</h3>"
            "<ul>"
            "<li>Вопросы по отчёту аудита</li>"
            "<li>Топ-3 бизнес-приоритета на ближайший квартал</li>"
            "<li>Данные для доступа (если ещё не отправлены)</li>"
            "</ul>"
            "<p>Ждём с нетерпением!</p>"
            "<p>С уважением,<br/>"
            "{account_manager}<br/>"
            "Apex AI Marketing</p>"
            "</div>"
        ),
    },
}


def get_onboarding_email(
    template_name: str,
    language: str = "en",
    **kwargs,
) -> dict:
    """Get a rendered onboarding email.

    Args:
        template_name: One of 'welcome', 'access_request', 'kickoff_confirmation'.
        language: Language code ('en' or 'ru').
        **kwargs: Template variables.

    Returns:
        dict with 'subject' and 'body' keys, rendered with the variables.
    """
    templates = ONBOARDING_EN if language == "en" else ONBOARDING_RU
    template = templates.get(template_name)
    if not template:
        raise ValueError(
            f"Unknown onboarding template: {template_name} ({language})"
        )

    return {
        "subject": template["subject"].format(**kwargs),
        "body": template["body"].format(**kwargs),
    }
