from typing import Any


def extract_text_from_url(url: str, timeout: int = 10) -> Any:
    # lazy imports to avoid hard dependency at import-time
    try:
        import requests
    except ImportError as e:
        raise ImportError("requests is required: pip install requests") from e

    try:
        from bs4 import BeautifulSoup
    except ImportError as e:
        raise ImportError("beautifulsoup4 is required: pip install beautifulsoup4") from e

    try:
        from langchain_core.documents import Document
    except Exception as e:
        raise ImportError("langchain is required: pip install langchain") from e

    headers = {"User-Agent": "langchain-text-extractor/1.0"}
    resp = requests.get(url, timeout=timeout, headers=headers)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content, "html.parser")

    # remove tags that usually don't contain relevant visible text
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside", "form"]):
        tag.decompose()

    # prefer article or main tags when available
    main = soup.find("article") or soup.find("main") or soup.body
    if main is None:
        text = soup.get_text(separator="\n", strip=True)
    else:
        text = main.get_text(separator="\n", strip=True)

    title = None
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    metadata = {"source": url}
    if title:
        metadata["title"] = title

    return Document(page_content=text, metadata=metadata)

