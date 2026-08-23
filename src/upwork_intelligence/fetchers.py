from __future__ import annotations

import html
import re
import ssl
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .models import SourceDescriptor, SourceFetchResult


USER_AGENT = "hh-cursor-upwork-intelligence/1.0"
DEFAULT_SOURCES_DIR = "tmp/upwork-intelligence-sources"


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            text = data.strip()
            if text:
                self._chunks.append(text)

    def text(self) -> str:
        return " ".join(self._chunks)


def clean_text(raw_html: str) -> str:
    parser = _TextExtractor()
    parser.feed(raw_html)
    text = html.unescape(parser.text())
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def cache_path(sources_dir: str | Path, source_id: str) -> Path:
    return Path(sources_dir) / f"{source_id}.txt"


def normalize_browser_text(raw_text: str) -> str:
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in text.splitlines()]
    cleaned: list[str] = []
    for line in lines:
        if not line:
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue
        cleaned.append(line)
    text = "\n".join(cleaned)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def ingest_browser_text(
    source_id: str,
    input_path: str | Path,
    sources_dir: str | Path = DEFAULT_SOURCES_DIR,
) -> Path:
    from .registry import get_default_sources

    known_ids = {source.id for source in get_default_sources()}
    if source_id not in known_ids:
        raise ValueError(f"Unknown source id: {source_id}")

    input_file = Path(input_path)
    if not input_file.is_file():
        raise ValueError(f"Input file not found: {input_file}")

    text = normalize_browser_text(input_file.read_text(encoding="utf-8"))
    if not text:
        raise ValueError("Input file has no readable text after normalization.")

    output = cache_path(sources_dir, source_id)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    return output


def fetch_source_from_cache(
    descriptor: SourceDescriptor,
    sources_dir: str | Path,
) -> SourceFetchResult | None:
    path = cache_path(sources_dir, descriptor.id)
    fetched_at = datetime.now(timezone.utc)
    if not path.is_file():
        return None

    text = normalize_browser_text(path.read_text(encoding="utf-8"))
    if not text:
        return SourceFetchResult(
            descriptor=descriptor,
            status="empty",
            fetched_at=fetched_at,
            error_message=f"Cached file is empty: {path}",
            fetch_channel="browser_cache",
        )

    return SourceFetchResult(
        descriptor=descriptor,
        status="ok",
        fetched_at=fetched_at,
        text=text,
        fetch_channel="browser_cache",
    )


def fetch_source(
    descriptor: SourceDescriptor,
    timeout: int = 15,
    sources_dir: str | Path | None = None,
    prefer_cache: bool = True,
) -> SourceFetchResult:
    if sources_dir and prefer_cache:
        cached = fetch_source_from_cache(descriptor, sources_dir)
        if cached is not None and cached.status == "ok":
            return cached

    result = _fetch_source_http(descriptor, timeout=timeout)
    if result.fetch_channel is None:
        result.fetch_channel = "http"
    return result


def _fetch_source_http(descriptor: SourceDescriptor, timeout: int = 15) -> SourceFetchResult:
    request = Request(
        descriptor.url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    fetched_at = datetime.now(timezone.utc)
    try:
        return _fetch_with_context(request, descriptor, fetched_at, timeout, ssl.create_default_context())
    except ssl.SSLError:
        insecure_context = ssl._create_unverified_context()
        try:
            return _fetch_with_context(request, descriptor, fetched_at, timeout, insecure_context)
        except Exception as error:
            return SourceFetchResult(
                descriptor=descriptor,
                status="unavailable",
                fetched_at=fetched_at,
                error_message=str(error),
            )
    except HTTPError as error:
        return SourceFetchResult(
            descriptor=descriptor,
            status="unavailable",
            fetched_at=fetched_at,
            http_status=error.code,
            error_message=str(error),
        )
    except URLError as error:
        if isinstance(getattr(error, "reason", None), ssl.SSLError):
            insecure_context = ssl._create_unverified_context()
            try:
                return _fetch_with_context(request, descriptor, fetched_at, timeout, insecure_context)
            except Exception as insecure_error:
                return SourceFetchResult(
                    descriptor=descriptor,
                    status="unavailable",
                    fetched_at=fetched_at,
                    error_message=str(insecure_error),
                )
        return SourceFetchResult(
            descriptor=descriptor,
            status="unavailable",
            fetched_at=fetched_at,
            error_message=str(error),
        )


def _fetch_with_context(
    request: Request,
    descriptor: SourceDescriptor,
    fetched_at: datetime,
    timeout: int,
    context: ssl.SSLContext,
) -> SourceFetchResult:
    try:
        with urlopen(request, timeout=timeout, context=context) as response:
            payload = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            body = payload.decode(charset, errors="replace")
            text = clean_text(body)
            if not text:
                return SourceFetchResult(
                    descriptor=descriptor,
                    status="empty",
                    fetched_at=fetched_at,
                    http_status=getattr(response, "status", None),
                    error_message="No readable text extracted",
                )
            return SourceFetchResult(
                descriptor=descriptor,
                status="ok",
                fetched_at=fetched_at,
                text=text,
                http_status=getattr(response, "status", None),
                fetch_channel="http",
            )
    except Exception as error:  # pragma: no cover - defensive fallback
        if isinstance(error, ssl.SSLError):
            raise
        return SourceFetchResult(
            descriptor=descriptor,
            status="unavailable",
            fetched_at=fetched_at,
            error_message=str(error),
        )
