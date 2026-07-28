# Hermes Plugins (AIGC)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) | **English** | [中文](README.zh-CN.md)

A collection of plug-and-play plugins for [Hermes Agent](https://hermes-agent.nousresearch.com). Maintained by [Kyan](https://github.com/kyan001).

## Overview

This repository hosts a set of plugins designed for [Hermes Agent](https://hermes-agent.nousresearch.com), installable via `hermes plugins install` with a single command. All plugins share the same design philosophy:

- **Plug and play** — Subclass Hermes built-in classes, minimal intrusiveness
- **Zero / minimal dependencies** — Leverage Hermes' existing runtime environment
- **Configuration-driven** — Switch providers with a single line in `config.yaml`
- **MIT License** — Free to use and modify

## Plugin List

| Plugin | Version | Type | Description |
|--------|---------|------|-------------|
| [Defuddle](./Defuddle/) | 1.0.0 | Web Extract Provider | Local web page content extraction, no API key required, powered by Defuddle CLI |
| [Holographic-CHS](./Holographic-CHS/) | 2.1.1 | Memory Provider | Chinese trigram FTS5 support, solves Chinese memory retrieval issues |

## Quick Start

### Install a Plugin

```Shell
# Via CLI
hermes plugins install kyan001/Hermes-Plugins/${PluginName} --enable

# Or via Dashboard
# https://hermes.kyan001.com/plugins
```

### Configure

Set the corresponding provider in Hermes config file `${HERMES_HOME}/config.yaml`:

```yaml
# Example: Use Defuddle as web extraction backend
web:
  extract_backend: defuddle

# Example: Use Holographic-CHS as memory backend
memory:
  provider: holographic-chs
```

### Restart to Apply

```Shell
hermes gateway restart
# Or execute /restart in session
```

### Update a Plugin

```Shell
hermes plugins update ${PluginName}
```

## Common File Structure

Each plugin consists of two core files:

```
plugin-name/
├── plugin.yaml       # Hermes plugin metadata (name, version, description, author)
└── __init__.py       # register(ctx) + implementation
```

### `plugin.yaml`

Declares plugin metadata including `name`, `version`, `description`, `author`, and the provider type it offers.

### `__init__.py`

Contains the `register(ctx)` entry point and implementation logic. Implements by subclassing Hermes' built-in Provider base class and overriding key methods, registering at initialization time.

## Design Patterns

Plugins in this repository commonly follow these patterns:

1. **Subclassing** — Inherit from Hermes built-in Provider base classes (e.g., `WebSearchProvider`, `HolographicMemoryProvider`)
2. **Monkey-patch (optional)** — Apply targeted patches to core modules at initialization time to minimize code intrusiveness
3. **Configuration as switching** — Enable provider hot-swapping via `plugin.yaml` + `config.yaml`
4. **Zero external dependencies first** — Prefer leveraging Hermes' built-in runtime (e.g., Node.js/npm/npx)

## License

[MIT](LICENSE) © 2026 Kyan
