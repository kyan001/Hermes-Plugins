# Hermes Plugins (AIGC)

[English](README.md) | **中文**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Hermes Agent 即插即用插件合集。由 [Kyan](https://github.com/kyan001) 维护。

## 总览

本仓库包含一系列专为 [Hermes Agent](https://hermes-agent.nousresearch.com) 设计的插件，通过 `hermes plugins install` 一键安装。所有插件遵循相同的设计哲学：

- **即插即用** — 继承 Hermes 内置类，最小化侵入
- **零 / 极简依赖** — 优先利用 Hermes 已有的运行时环境

## 插件列表

| 插件 | 版本 | 类型 | 说明 |
|------|------|------|------|
| [Defuddle](./Defuddle/) | 1.0.0 | Web 提取 Provider | 本地网页内容提取，无需 API Key，基于 Defuddle CLI |
| [Holographic-CHS](./Holographic-CHS/) | 2.1.1 | 记忆 Provider | 中文 trigram FTS5 支持，解决中文记忆检索问题 |

## 快速开始

### 安装插件
通过 CLI 安装
```Shell
hermes plugins install kyan001/Hermes-Plugins/${PluginName} --enable
```
或通过 Dashboard：<https://hermes.kyan001.com/plugins>

### 配置

在 Hermes 配置文件 `${HERMES_HOME}/config.yaml` 中设置对应的项。

### 重启生效

```Shell
hermes gateway restart
# 或在会话中执行 /restart
```

### 更新插件

```Shell
hermes plugins update ${PluginName}
```

## 通用文件结构

每个插件由两个核心文件组成：

```
plugin-name/
├── plugin.yaml       # Hermes 插件元数据（名称、版本、描述、作者）
└── __init__.py       # register(ctx) + 具体实现
```

### `plugin.yaml`

声明插件元数据，包括 `name`、`version`、`description`、`author` 以及提供的 provider 类型。

### `__init__.py`

包含 `register(ctx)` 入口函数和实现逻辑。实现方式为继承 Hermes 内置的 Provider 基类并覆写关键方法，在初始化时完成注册。

## 设计模式

本仓库的插件普遍采用以下设计模式：

1. **子类化** — 继承 Hermes 内置 Provider 基类（如 `WebSearchProvider`、`HolographicMemoryProvider`）
2. **Monkey-patch 可选** — 在初始化时对核心模块做定向补丁，最小化代码侵入
3. **配置即切换** — 通过 `plugin.yaml` + `config.yaml` 实现 provider 热切换
4. **零外部依赖优先** — 优先利用 Hermes 自带运行时（如 Node.js/npm/npx）

## 许可证

[MIT](LICENSE) © 2026 Kyan
