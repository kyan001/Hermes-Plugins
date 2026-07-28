# Holographic-CHS for Hermes (AIGC)

**English** | [中文](README.zh-CN.md)

Chinese trigram FTS5 for [Hermes Agent](https://hermes-agent.nousresearch.com) memory. Drops in as a memory provider plugin.

## Quick Install
* Via Dashboard: Recommended. The plugin folder will be owned by Hermes.
    1. Install: <https://${HERMES_DASHBOARD_PUBLIC_URL}/plugins> @ `kyan001/Holographic-CHS-for-Hermes`
    2. Toggle on "Enable" before install or enable it manually in the plugin list.
    3. Set it as your memory provider in the same Dashboard Plugins page.
    4. Restart: `/restart` or `/new`
    * Update: Click "Git Pull" on the plugin item in the list.
* Via Hermes CLI:
    1. Install: `hermes plugins install kyan001/Holographic-CHS-for-Hermes --enable`
    2. Set it as your memory provider: `hermes config set memory.provider holographic-chs`
    3. Restart: `hermes gateway restart`
    * Update: `hermes plugins update holographic-chs`

```YAML
# File: ${HERMES_HOME}/config.yaml
memory:
  provider: holographic-chs
```

## What It Does

Patches Hermes' built-in `HolographicMemoryProvider` so FTS5 uses `tokenize='trigram'` instead of the default `unicode61` tokenizer. This makes Chinese text searchable character by character.

Without this plugin, a query like `冰黑咖啡` returns zero results against a memory containing `冰的黑咖啡` — the default tokenizer splits on whitespace/punctuation only, so Chinese text is indexed as one giant token. With trigram, both strings decompose into overlapping 3-char substrings (`冰黑咖` / `的黑咖` / `黑咖啡`) and match.

## Memory Write Mirroring

Mirrors the built-in `memory` tool operations to fact_store:

* `add`: passes through to the parent class, no change.
* `replace`: finds the old fact via `old_text` → `update_fact` to update the content, keeping the same `fact_id`.
* `remove`: finds the fact by exact content match → `remove_fact` to delete it.

The built-in deduplication in `add_fact` (UNIQUE content constraint) substitutes for the missing content-to-fact_id lookup. `replace` / `remove` only handle known operations; unknown ops fall through to the parent class without interfering with upper-layer behavior.

## Search Strategy

Two-phase fallback for maximum recall:

1. **FTS5 AND (default)** — exact trigram match
2. **Trigram OR expansion** — retry with OR-joined trigrams when FTS5 returns empty (≥4 char queries only). Multi-word stop words (509 entries) stripped before expansion to reduce noise

> **Known limitation**: The trigram tokenizer requires at least 3 characters to produce index entries. Queries shorter than 3 characters (e.g. `咖啡`, `北京`) will not match any FTS5 rows. A LIKE fallback is intentionally omitted — single-character searches yield too much noise to be useful, and 2-character queries are rare in real-world agent usage.

## Files

```TOML
Holographic-CHS-for-Hermes/
├── plugin.yaml       # Hermes plugin metadata
└── __init__.py       # register(ctx) + implementation
```

No dependencies beyond Hermes itself. The plugin subclasses the bundled `HolographicMemoryProvider` and applies monkey-patches at initialization time.
