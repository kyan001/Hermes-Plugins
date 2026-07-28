# Defuddle for Hermes (AIGC)

**English** | [中文](README.zh-CN.md)

Local Web Extraction Provider for [Hermes Agent](https://hermes-agent.nousresearch.com/) web extraction via [Defuddle](https://github.com/kepano/defuddle), no API key required.

Drops in as a web extract provider plugin. Designed to pair with a search-only backend (SearXNG, Brave Free, DDGS, etc.) so `web_extract()` works transparently.

Extracts clean json from web pages using the Defuddle CLI.

## Quick Start

* Via Dashboard: Recommended. The plugin folder will be owned by Hermes.
    1. Install: <https://${HERMES_DASHBOARD_PUBLIC_URL}/plugins> @ `kyan001/Defuddle-for-Hermes`
    2. Toggle on "Enable" before install or enable it manually in the plugin list.
    3. Set it as your web extract backend on the <https://${HERMES_DASHBOARD_PUBLIC_URL}/config> - Web - Extract Backend: `defuddle`.
    4. Restart: `/restart` or `/new` and `web_extract(urls=[...])` will use Defuddle under the hood.
    * Update: Click "Git Pull" on the plugin item in the list.
* Via Hermes CLI:
    1. Install: `hermes plugins install kyan001/Defuddle-for-Hermes --enable`
    2. Set it as your web extract backend: `hermes config set web.extract_backend defuddle`
    3. Restart: `hermes gateway restart`
    * Update: `hermes plugins update defuddle-for-hermes`

## Requirements

* Node.js with npm/npx
* Defuddle CLI is fetched automatically via `npx` on first use

## How It Works

The plugin registers as a `WebSearchProvider` with:

| Property | Value |
|----------|-------|
| `supports_search()` | `False` |
| `supports_extract()` | `True` |
| `extract(urls)` | Runs `npx defuddle parse <url> --json`, returns clean markdown |

## Response Envelope

Each URL returns:

```JSON
{
  "url": "https://example.com/article",
  "title": "Page Title",
  "content": "# Markdown content…",
  "raw_content": "# Markdown content…",
  "metadata": {
    "description": "Meta description",
    "domain": "example.com",
    "word_count": 1234,
    "language": "en",
    "author": "Author Name"
  },
  "error": null
}
```

## File Structure

```Shell
Defuddle-for-Hermes/
├── __init__.py    # DefuddleExtractProvider + register()
└── plugin.yaml    # Plugin manifest
```
