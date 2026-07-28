"""defuddle - Web extraction provider using Defuddle CLI.

Subclasses :class:`agent.web_search_provider.WebSearchProvider`
and delegates ``extract()`` to ``npx defuddle parse <url> --json``.

No API key needed - just Node.js and npm (which Heremes already has).
"""
import json
import logging
import shutil
import subprocess
from typing import Any

from agent.web_search_provider import WebSearchProvider

logger = logging.getLogger(__name__)

_EXTRACT_TIMEOUT = 60  # seconds per URL


class DefuddleExtractProvider(WebSearchProvider):
    """Extract-only provider that uses the local Defuddle CLI.

    Designed to pair with a search-only backend (e.g. SearXNG, Brave Free,
    DDGS) via ``config.yaml``:

    .. code-block:: yaml

       web:
         search_backend: searxng
         extract_backend: defuddle
    """

    # ── Identity ──────────────────────────────────────────────────────

    @property
    def name(self) -> str:
        """Stable id used in ``web.extract_backend`` config."""
        return "defuddle"

    @property
    def display_name(self) -> str:
        """Human label shown in ``hermes tools``."""
        return "Defuddle (local)"

    # ── Availability ──────────────────────────────────────────────────

    def is_available(self) -> bool:
        """Cheap check — Node.js + npx present, no network call."""
        if not shutil.which("node"):
            logger.debug("defuddle-for-hermes: node not found")
            return False
        if not shutil.which("npx"):
            logger.debug("defuddle-for-hermes: npx not found")
            return False
        return True

    # ── Capability flags ──────────────────────────────────────────────

    def supports_search(self) -> bool:
        return False

    def supports_extract(self) -> bool:
        return True

    # ── Extract ───────────────────────────────────────────────────────

    def extract(self, urls: list[str], **kwargs: Any) -> list[dict[str, Any]]:
        """Extract clean markdown from URLs via Defuddle CLI."""
        results: list[dict[str, Any]] = []

        for url in urls:
            result = self._extract_one(url)
            results.append(result)

        return results

    # ── Internals ─────────────────────────────────────────────────────

    @staticmethod
    def _extract_one(url: str) -> dict[str, Any]:
        """Extract a single URL and return the result dict.

        Returns a dict with ``url``, ``title``, ``content``,
        ``raw_content``, ``metadata``, and ``error`` fields.
        """
        try:
            proc = subprocess.run(
                ["npx", "defuddle", "parse", url, "--json"],
                capture_output=True,
                text=True,
                timeout=_EXTRACT_TIMEOUT,
            )

            if proc.returncode != 0:
                err = (proc.stderr or "").strip()
                if not err:
                    err = f"defuddle exited with code {proc.returncode}"
                logger.warning(
                    "defuddle-for-hermes: %s returned %d: %s",
                    url, proc.returncode, err,
                )
                return {
                    "url": url,
                    "title": "",
                    "content": "",
                    "raw_content": "",
                    "metadata": {},
                    "error": err,
                }

            data = json.loads(proc.stdout)

            # Prefer contentMarkdown (clean), fall back to raw HTML content
            content = data.get("contentMarkdown") or data.get("content", "")

            metadata: dict[str, Any] = {}
            if desc := data.get("description"):
                metadata["description"] = desc
            if domain := data.get("domain"):
                metadata["domain"] = domain
            if wc := data.get("wordCount"):
                metadata["word_count"] = wc
            if lang := data.get("language"):
                metadata["language"] = lang
            if author := data.get("author"):
                metadata["author"] = author
            if published := data.get("published"):
                metadata["published"] = published

            return {
                "url": url,
                "title": data.get("title", ""),
                "content": content,
                "raw_content": content,
                "metadata": metadata,
                "error": None,
            }

        except subprocess.TimeoutExpired:
            logger.warning(
                "defuddle-for-hermes: timed out after %ss for %s",
                _EXTRACT_TIMEOUT, url,
            )
            return {
                "url": url,
                "title": "",
                "content": "",
                "raw_content": "",
                "metadata": {},
                "error": f"defuddle timed out after {_EXTRACT_TIMEOUT}s",
            }

        except Exception as exc:
            logger.exception("defuddle-for-hermes: unexpected error for %s", url)
            return {
                "url": url,
                "title": "",
                "content": "",
                "raw_content": "",
                "metadata": {},
                "error": str(exc),
            }


# ── Plugin entry point ──────────────────────────────────────────────


def register(ctx: Any) -> None:
    """Register the Defuddle extract provider with Heremes."""
    provider = DefuddleExtractProvider()
    ctx.register_web_search_provider(provider)
    logger.info("defuddle-for-hermes: registered provider 'defuddle'")
