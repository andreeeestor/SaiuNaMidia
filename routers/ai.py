import json
import re
from urllib.parse import urljoin
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
import httpx
from bs4 import BeautifulSoup

from core.config import settings
from core.security import verify_token
from schemas.ai import ExtractMediaRequest, ExtractMediaResponse

router = APIRouter(prefix="/ai", tags=["AI"])

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, id: Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}


def clean_url(url: str, base_url: str) -> str:
    if not url:
        return ""
    full_url = urljoin(base_url, url.strip())
    return full_url


@router.post("/extract-media", response_model=ExtractMediaResponse)
async def extract_media(req: ExtractMediaRequest, user=Depends(verify_token)):
    raw_url = req.url.strip()
    if not raw_url.startswith(("http://", "https://")):
        raw_url = "https://" + raw_url

    # Fetch webpage
    try:
        async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=12.0) as client:
            resp = await client.get(raw_url)
            resp.raise_for_status()
            html_text = resp.text
            final_url = str(resp.url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não foi possível acessar a URL informada: {str(e)}"
        )

    soup = BeautifulSoup(html_text, "html.parser")

    # Extract title
    title = ""
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        title = og_title["content"]
    elif soup.title and soup.title.string:
        title = soup.title.string.strip()

    # Extract candidates
    candidate_images: List[str] = []
    candidate_logos: List[str] = []

    # Check OpenGraph & Twitter cards
    for prop in ["og:image", "og:image:secure_url", "twitter:image", "twitter:image:src"]:
        meta = soup.find("meta", property=prop) or soup.find("meta", attrs={"name": prop})
        if meta and meta.get("content"):
            url_val = clean_url(meta["content"], final_url)
            if url_val and url_val not in candidate_images:
                candidate_images.append(url_val)

    # Search for logos in header / nav / logo elements
    logo_selectors = [
        "header img", ".header img", "#header img",
        ".logo img", "#logo img", "a[class*='logo'] img",
        "img[class*='logo']", "img[alt*='logo' i]", "img[src*='logo' i]",
        "link[rel='icon']", "link[rel='shortcut icon']", "link[rel='apple-touch-icon']"
    ]
    for sel in logo_selectors:
        for el in soup.select(sel):
            src = el.get("src") or el.get("href")
            if src:
                full_src = clean_url(src, final_url)
                if full_src and full_src not in candidate_logos:
                    candidate_logos.append(full_src)

    # Search for article/main images
    for img in soup.select("article img, main img, .content img, .post img, img"):
        src = img.get("src") or img.get("data-src")
        if src:
            full_src = clean_url(src, final_url)
            # Filter out tracking pixels / tiny icons
            if full_src and not re.search(r'(pixel|tracking|avatar|icon|1x1|banner-ad)', full_src, re.I):
                if full_src not in candidate_images:
                    candidate_images.append(full_src)
            if len(candidate_images) >= 15:
                break

    # Truncate candidates to avoid excessive prompt size
    candidate_images = candidate_images[:10]
    candidate_logos = candidate_logos[:8]

    selected_image = candidate_images[0] if candidate_images else None
    selected_logo = candidate_logos[0] if candidate_logos else None

    # Call Groq API if API key is provided
    if settings.GROQ_API_KEY.strip():
        try:
            prompt = (
                f"URL da matéria: {final_url}\n"
                f"Título da notícia: {title}\n\n"
                f"Lista de candidatas a IMAGEM PRINCIPAL DA MATÉRIA:\n{json.dumps(candidate_images, indent=2)}\n\n"
                f"Lista de candidatas a LOGO DO PORTAL/VEÍCULO:\n{json.dumps(candidate_logos, indent=2)}\n\n"
                "Selecione a melhor URL para a imagem da matéria ('image') e a melhor URL para a logo do site ('logo'). "
                "Retorne estritamente um JSON com a estrutura: {\"image\": \"...\", \"logo\": \"...\"}."
            )

            async with httpx.AsyncClient(timeout=10.0) as ai_client:
                groq_resp = await ai_client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.GROQ_API_KEY.strip()}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": settings.GROQ_MODEL,
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "Você é um analisador de mídias de jornais e portais de notícias. "
                                    "Seu trabalho é escolher entre os links fornecidos qual é a imagem principal da notícia e qual é a logo da empresa/veículo. "
                                    "Responda APENAS em JSON válido."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.1,
                        "response_format": {"type": "json_object"}
                    }
                )
                if groq_resp.status_code == 200:
                    ai_data = groq_resp.json()
                    content = ai_data["choices"][0]["message"]["content"]
                    parsed = json.loads(content)
                    if parsed.get("image"):
                        selected_image = clean_url(parsed["image"], final_url)
                    if parsed.get("logo"):
                        selected_logo = clean_url(parsed["logo"], final_url)
        except Exception:
            pass  # Fall back to heuristic selections if Groq request fails

    return ExtractMediaResponse(
        url=final_url,
        title=title,
        image=selected_image,
        logo=selected_logo
    )
