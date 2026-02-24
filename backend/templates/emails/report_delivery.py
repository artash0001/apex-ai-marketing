"""
Apex AI Marketing - Report Delivery Email Templates

Email templates for delivering weekly and monthly reports to clients.
Available in EN and RU.

Placeholders:
  {name} - Client contact name
  {company} - Company name
  {report_type} - Type of report (weekly/monthly)
  {period} - Reporting period string
  {portal_url} - Client portal URL
  {highlights} - Key highlights summary
  {account_manager} - Account manager name
"""

REPORT_DELIVERY_EN = {
    "weekly": {
        "subject": "Your weekly growth report is ready, {name}",
        "body": (
            "<div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>"
            "<h2>Weekly Growth Report</h2>"
            "<p>Hi {name},</p>"
            "<p>Your weekly performance report for {company} is ready. "
            "Here is a quick summary:</p>"
            "<div style='background: #f0f7ff; padding: 20px; border-radius: 8px; "
            "border-left: 4px solid #2563eb; margin: 20px 0;'>"
            "<h3 style='margin-top: 0;'>This Week's Highlights</h3>"
            "<p>{highlights}</p>"
            "</div>"
            "<p>The full report with detailed metrics, insights, and "
            "next week's action items is available in your portal:</p>"
            "<p style='text-align: center; margin: 24px 0;'>"
            "<a href='{portal_url}' style='background: #2563eb; color: white; "
            "padding: 12px 32px; text-decoration: none; border-radius: 6px; "
            "font-weight: bold;'>View Full Report</a></p>"
            "<p>Questions or feedback? Reply to this email or reach out to "
            "{account_manager} directly.</p>"
            "<p>Best,<br/>"
            "Apex AI Marketing</p>"
            "</div>"
        ),
    },
    "monthly": {
        "subject": "Monthly growth report + invoice: {company}",
        "body": (
            "<div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>"
            "<h2>Monthly Growth Report</h2>"
            "<p>Hi {name},</p>"
            "<p>Your comprehensive monthly report for {company} covering "
            "{period} is ready.</p>"
            "<div style='background: #f0f7ff; padding: 20px; border-radius: 8px; "
            "border-left: 4px solid #2563eb; margin: 20px 0;'>"
            "<h3 style='margin-top: 0;'>Monthly Highlights</h3>"
            "<p>{highlights}</p>"
            "</div>"
            "<p>This report includes:</p>"
            "<ul>"
            "<li>Full KPI tracking against targets</li>"
            "<li>Engine performance breakdown</li>"
            "<li>Experiment results and learnings</li>"
            "<li>ROI analysis</li>"
            "<li>Next month's strategic priorities</li>"
            "</ul>"
            "<p>Your monthly invoice is also attached to this report.</p>"
            "<p style='text-align: center; margin: 24px 0;'>"
            "<a href='{portal_url}' style='background: #2563eb; color: white; "
            "padding: 12px 32px; text-decoration: none; border-radius: 6px; "
            "font-weight: bold;'>View Full Report</a></p>"
            "<p>Would you like to schedule a review call to discuss the results? "
            "Book here: <a href='https://calendly.com/apex-ai-marketing'>Schedule</a></p>"
            "<p>Best,<br/>"
            "{account_manager}<br/>"
            "Apex AI Marketing</p>"
            "</div>"
        ),
    },
}

REPORT_DELIVERY_RU = {
    "weekly": {
        "subject": "Еженедельный отчёт готов, {name}",
        "body": (
            "<div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>"
            "<h2>Еженедельный отчёт о росте</h2>"
            "<p>Здравствуйте, {name}!</p>"
            "<p>Ваш еженедельный отчёт по {company} готов. "
            "Краткое резюме:</p>"
            "<div style='background: #f0f7ff; padding: 20px; border-radius: 8px; "
            "border-left: 4px solid #2563eb; margin: 20px 0;'>"
            "<h3 style='margin-top: 0;'>Главное за неделю</h3>"
            "<p>{highlights}</p>"
            "</div>"
            "<p>Полный отчёт с детальными метриками, аналитикой и "
            "планом на следующую неделю доступен в вашем портале:</p>"
            "<p style='text-align: center; margin: 24px 0;'>"
            "<a href='{portal_url}' style='background: #2563eb; color: white; "
            "padding: 12px 32px; text-decoration: none; border-radius: 6px; "
            "font-weight: bold;'>Открыть полный отчёт</a></p>"
            "<p>Вопросы или обратная связь? Ответьте на это письмо или "
            "напишите {account_manager} напрямую.</p>"
            "<p>С уважением,<br/>"
            "Команда Apex AI Marketing</p>"
            "</div>"
        ),
    },
    "monthly": {
        "subject": "Ежемесячный отчёт + счёт: {company}",
        "body": (
            "<div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>"
            "<h2>Ежемесячный отчёт о росте</h2>"
            "<p>Здравствуйте, {name}!</p>"
            "<p>Ваш полный ежемесячный отчёт по {company} за период "
            "{period} готов.</p>"
            "<div style='background: #f0f7ff; padding: 20px; border-radius: 8px; "
            "border-left: 4px solid #2563eb; margin: 20px 0;'>"
            "<h3 style='margin-top: 0;'>Главное за месяц</h3>"
            "<p>{highlights}</p>"
            "</div>"
            "<p>В отчёте:</p>"
            "<ul>"
            "<li>Полное отслеживание KPI относительно целей</li>"
            "<li>Разбор работы каждого движка</li>"
            "<li>Результаты экспериментов и выводы</li>"
            "<li>Анализ ROI</li>"
            "<li>Стратегические приоритеты на следующий месяц</li>"
            "</ul>"
            "<p>Ежемесячный счёт также приложен к отчёту.</p>"
            "<p style='text-align: center; margin: 24px 0;'>"
            "<a href='{portal_url}' style='background: #2563eb; color: white; "
            "padding: 12px 32px; text-decoration: none; border-radius: 6px; "
            "font-weight: bold;'>Открыть полный отчёт</a></p>"
            "<p>Хотите назначить звонок для обсуждения результатов? "
            "Запишитесь здесь: "
            "<a href='https://calendly.com/apex-ai-marketing'>Выбрать время</a></p>"
            "<p>С уважением,<br/>"
            "{account_manager}<br/>"
            "Apex AI Marketing</p>"
            "</div>"
        ),
    },
}


def get_report_email(
    client_name: str,
    company: str = "",
    report_type: str = "weekly",
    language: str = "en",
    period: str = "",
    highlights: str = "Report highlights will be populated from the full report.",
    portal_url: str = "https://apexaimarketing.pro/portal",
    account_manager: str = "Apex AI Marketing Team",
) -> dict:
    """Get a rendered report delivery email.

    Args:
        client_name: Client contact name.
        company: Company name.
        report_type: 'weekly' or 'monthly'.
        language: 'en' or 'ru'.
        period: Reporting period string.
        highlights: Key highlights summary.
        portal_url: Client portal URL.
        account_manager: Account manager name.

    Returns:
        dict with 'subject' and 'body' keys.
    """
    templates = REPORT_DELIVERY_EN if language == "en" else REPORT_DELIVERY_RU
    template = templates.get(report_type)
    if not template:
        raise ValueError(f"Unknown report type: {report_type}")

    context = {
        "name": client_name,
        "company": company,
        "period": period,
        "highlights": highlights,
        "portal_url": portal_url,
        "account_manager": account_manager,
    }

    return {
        "subject": template["subject"].format(**context),
        "body": template["body"].format(**context),
    }
