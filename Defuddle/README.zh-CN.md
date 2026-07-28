# Defuddle for Hermes (AIGC)

[English](README.md) | **中文**

基于 [Defuddle](https://github.com/kepano/defuddle) 的本地网页提取插件，为 [Hermes Agent](https://hermes-agent.nousresearch.com/) 提供网页内容提取能力，无需 API Key。

以 web extract provider 插件形式即插即用。设计上与仅搜索后端（如 SearXNG、Brave Free、DDGS 等）配合使用，让 `web_extract()` 透明工作。

通过 Defuddle CLI 从网页提取干净的 JSON 内容。

## 快速开始

* 通过 Dashboard（推荐，插件文件夹的所有权归 Hermes）：
    1. 安装：<https://${HERMES_DASHBOARD_PUBLIC_URL}/plugins> @ `kyan001/Defuddle-for-Hermes`
    2. 安装前勾选 "Enable"，或在插件列表中手动启用。
    3. 在 <https://${HERMES_DASHBOARD_PUBLIC_URL}/config> - Web - Extract Backend 中设置为 `defuddle`。
    4. 重启：`/restart` 或 `/new`，之后 `web_extract(urls=[...])` 将在底层使用 Defuddle。
    * 更新：点击插件列表中的 "Git Pull"。
* 通过 Hermes CLI：
    1. 安装：`hermes plugins install kyan001/Defuddle-for-Hermes --enable`
    2. 设置为网页提取后端：`hermes config set web.extract_backend defuddle`
    3. 重启：`hermes gateway restart`
    * 更新：`hermes plugins update defuddle-for-hermes`

## 系统要求

* Node.js（含 npm/npx）
* Defuddle CLI 在首次使用时自动通过 `npx` 获取

## 工作原理

该插件注册为 `WebSearchProvider`，具体能力如下：

| 属性 | 值 |
|----------|-------|
| `supports_search()` | `False` |
| `supports_extract()` | `True` |
| `extract(urls)` | 运行 `npx defuddle parse <url> --json`，返回干净的 markdown |

## 返回格式

每个 URL 返回：

```JSON
{
  "url": "https://example.com/article",
  "title": "Page Title",
  "content": "# Markdown 内容…",
  "raw_content": "# Markdown 内容…",
  "metadata": {
    "description": "Meta 描述",
    "domain": "example.com",
    "word_count": 1234,
    "language": "en",
    "author": "作者名"
  },
  "error": null
}
```

## 文件结构

```Shell
Defuddle-for-Hermes/
├── __init__.py    # DefuddleExtractProvider + register()
└── plugin.yaml    # 插件清单
```
