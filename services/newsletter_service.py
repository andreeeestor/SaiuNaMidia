import datetime
from typing import List
from schemas.ai import NewsArticleItem

HEADER_BANNER = "https://res.cloudinary.com/ddfdxkmhi/image/upload/v1782498228/imghub/t5nqfch9ob9dlspvagvr.png"
FOOTER_LOGO = "https://res.cloudinary.com/ddfdxkmhi/image/upload/v1782498232/imghub/w2pvzmkdaf6pgp7syp9q.png"

SOCIAL_FB = "https://res.cloudinary.com/ddfdxkmhi/image/upload/v1782498229/imghub/yxey05d02ao42zrtfjmn.png"
SOCIAL_X = "https://res.cloudinary.com/ddfdxkmhi/image/upload/v1782498231/imghub/p7qmspadv11ixqcl3pgp.png"
SOCIAL_YT = "https://res.cloudinary.com/ddfdxkmhi/image/upload/v1782498232/imghub/xws0sphbqztbf4lgoxlr.png"
SOCIAL_IG = "https://res.cloudinary.com/ddfdxkmhi/image/upload/v1782498230/imghub/xwxg5vr2onvjwuxsoezq.png"

MONTHS_PT = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
]


def format_current_date() -> str:
    now = datetime.datetime.now()
    month_name = MONTHS_PT[now.month - 1]
    return f"{now.day} de {month_name} de {now.year}"


def render_email_newsletter(articles: List[NewsArticleItem], date_header: str = None) -> str:
    date_str = date_header or format_current_date()

    articles_html = []
    for idx, art in enumerate(articles):
        border_style = "border-bottom: 1px solid #e0e0e0;" if idx < len(articles) - 1 else ""
        
        logo_img_tag = ""
        if art.logo:
            logo_img_tag = f'<img src="{art.logo}" alt="{art.portal_name or ""}" height="28" style="display: inline-block; height: 28px; width: auto; border: 0; margin-left: 5px; vertical-align: middle;">'

        img_tag = ""
        if art.image:
            img_tag = f'<img src="{art.image}" alt="{art.title}" width="100%" height="200" style="display: block; width: 100%; height: 200px; border-radius: 8px; border: 0; object-fit: cover;">'

        articles_html.append(f"""
                    <!-- Matéria {idx + 1} -->
                    <tr>
                        <td style="padding: 30px; {border_style}">
                            <h2 style="color: #15315E; font-size: 22px; font-weight: 700; margin: 0 0 20px 0; line-height: 1.3;">{art.title}</h2>
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td width="45%" valign="top" style="padding-right: 15px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td>
                                                    {img_tag}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding-top: 10px; color: #666666; font-size: 12px; line-height: 1.4;">
                                                    Publicado em: <strong>{art.portal_name or 'Portal de Notícias'}</strong>
                                                    {logo_img_tag}
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                    <td width="55%" valign="top">
                                        <p style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0 0 20px 0;">
                                            {art.summary}
                                        </p>
                                        <a href="{art.url}" style="color:#15315E;font-family:Arial,sans-serif;font-size:14px;font-weight:bold;text-decoration:underline;" target="_blank">Leia mais</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
        """.strip())

    return f"""<!DOCTYPE html>
<html lang="pt-BR" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter Copasa - #saiunamídia</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5f5f5; padding: 20px 0;">
        <tr>
            <td align="center">
                <table width="700" cellpadding="0" cellspacing="0" border="0" style="max-width: 700px; background-color: #ffffff;">

                    <!-- Header -->
                    <tr>
                        <td style="background-color: #15315E; padding: 0;">
                            <img src="{HEADER_BANNER}" alt="Copasa Newsletter - #saiunamídia" width="700" style="display: block; width: 100%; height: auto; border: 0;">
                        </td>
                    </tr>

                    <!-- Data -->
                    <tr>
                        <td style="padding: 15px 30px; background-color: #f5f5f5;">
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td align="right" style="font-family: Arial, sans-serif; font-size: 12px; color: #666666;">
                                        {date_str}
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    {chr(10).join(articles_html)}

                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #15315E; color: #93B8EF; padding: 25px 30px;">
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td width="180" valign="middle" style="padding-right: 20px;">
                                        <img src="{FOOTER_LOGO}" alt="Copasa" width="150" style="display: block; max-width: 150px; height: auto; border: 0;">
                                    </td>
                                    <td valign="middle" align="right">
                                        <table cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td style="font-size: 13px; line-height: 1.6; padding-bottom: 10px;">
                                                    <a href="https://www.copasa.com.br" style="color: #93B8EF; text-decoration: none;" target="_blank">www.copasa.com.br</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <table cellpadding="0" cellspacing="0" border="0">
                                                        <tr>
                                                            <td style="padding: 0 5px;">
                                                                <a href="https://www.facebook.com/aquitemcopasa" target="_blank">
                                                                    <img src="{SOCIAL_FB}" alt="Facebook" width="30" height="30" style="display: block; border: 0;">
                                                                </a>
                                                            </td>
                                                            <td style="padding: 0 5px;">
                                                                <a href="https://x.com/aquitemcopasa" target="_blank">
                                                                    <img src="{SOCIAL_X}" alt="X (Twitter)" width="30" height="30" style="display: block; border: 0;">
                                                                </a>
                                                            </td>
                                                            <td style="padding: 0 5px;">
                                                                <a href="https://www.youtube.com/user/TVCOPASAMG" target="_blank">
                                                                    <img src="{SOCIAL_YT}" alt="YouTube" width="30" height="30" style="display: block; border: 0;">
                                                                </a>
                                                            </td>
                                                            <td style="padding: 0 5px;">
                                                                <a href="https://www.instagram.com/aquitemcopasa/" target="_blank">
                                                                    <img src="{SOCIAL_IG}" alt="Instagram" width="30" height="30" style="display: block; border: 0;">
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""


def render_wcm_newsletter(articles: List[NewsArticleItem], date_header: str = None) -> str:
    date_str = date_header or format_current_date()

    cards_html = []
    for art in articles:
        logo_html = f'<img src="{art.logo}" alt="{art.portal_name}" style="height: 24px; width: auto; vertical-align: middle; margin-left: 6px;" />' if art.logo else ''
        img_html = f'<div style="flex: 0 0 240px;"><img src="{art.image}" alt="{art.title}" style="width: 100%; height: 160px; object-fit: cover; border-radius: 8px;" /></div>' if art.image else ''

        cards_html.append(f"""
  <!-- Card Matéria -->
  <article style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
    <h3 style="color: #15315E; font-size: 1.25rem; font-weight: 700; margin: 0 0 16px 0; line-height: 1.35;">
      {art.title}
    </h3>
    <div style="display: flex; gap: 20px; flex-wrap: wrap;">
      {img_html}
      <div style="flex: 1; min-width: 260px;">
        <p style="color: #334155; font-size: 0.95rem; line-height: 1.6; margin: 0 0 16px 0;">
          {art.summary}
        </p>
        <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.82rem; color: #64748b;">
          <span>Publicado em: <strong style="color: #0f172a;">{art.portal_name or 'Portal de Notícias'}</strong> {logo_html}</span>
          <a href="{art.url}" target="_blank" style="color: #0ea5e9; font-weight: 600; text-decoration: none;">Leia mais &rarr;</a>
        </div>
      </div>
    </div>
  </article>
        """.strip())

    return f"""<!-- COPASA WCM Portal Block - SaiuNaMídia -->
<div class="copasa-wcm-newsletter" style="font-family: Arial, sans-serif; max-width: 860px; margin: 0 auto; color: #0f172a;">

  <!-- Header Banner WCM -->
  <div style="background-color: #15315E; border-radius: 12px 12px 0 0; overflow: hidden; text-align: center;">
    <img src="{HEADER_BANNER}" alt="Copasa Newsletter - #saiunamídia" style="max-width: 100%; height: auto; display: block;" />
  </div>

  <!-- Data Header -->
  <div style="background-color: #f8fafc; padding: 12px 20px; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; text-align: right; font-size: 0.8rem; color: #64748b;">
    Publicações de <strong>{date_str}</strong>
  </div>

  <!-- Lista de Matérias WCM -->
  <div style="background-color: #f1f5f9; padding: 24px 20px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 12px 12px;">
    {chr(10).join(cards_html)}
  </div>

</div>
<!-- Fim COPASA WCM Portal Block -->"""
