# Defuddle for Hermes (AIGC)

**English** | [中文](README.zh-CN.md)

Local Web Extraction Provider for [Hermes Agent](https://hermes-agent.nousresearch.com/) web extraction via [Defuddle](https://github.com/kepano/defuddle), no API key required.

Drops in as a web extract provider plugin. Designed to pair with a search-only backend (SearXNG, Brave Free, DDGS, etc.) so `web_extract()` works transparently.

Extracts clean json from web pages using the Defuddle CLI.

## Quick Start

* Install:
    * Via Dashboard (Recommand): <https://hermes.kyan001.com/plugins> @ `kyan001/Hermes-Plugins/Defuddle-for-Hermes`
    * Or via CLI: `hermes plugins install kyan001/Hermes-Plugins/Defuddle-for-Hermes --enable`
* Set it as your extract backend:
    * Via CLI: `hermes config set web.extract_backend defuddle`
    * Or via Config File: `${HERMES_HOME}/config.yaml`

```YAML
# File: ${HERMES_HOME}/config.yaml
web:
  search_backend: ...  # Might be searxng
  extract_backend: defuddle  # Set this
```
* Restart: `/restart` / `hermes gateway restart` / `/new` and `web_extract(urls=[...])` will use Defuddle under the hood.

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
