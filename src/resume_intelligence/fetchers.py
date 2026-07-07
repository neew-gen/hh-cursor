from __future__ import annotations

import html
import re
import ssl
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .models import SourceDescriptor, SourceFetchResult


USER_AGENT = "hh-cursor-resume-intelligence/1.0"


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


def fetch_source(descriptor: SourceDescriptor, timeout: int = 15) -> SourceFetchResult:
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
