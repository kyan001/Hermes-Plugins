# Holographic-CHS for Hermes (AIGC)

[English](README.md) | **中文**

为 [Hermes Agent](https://hermes-agent.nousresearch.com) 记忆模块提供中文 trigram FTS5 支持。以 memory provider 插件形式即插即用。

## 快速安装

* 通过 Dashboard（推荐，插件文件夹的所有权归 Hermes）：
    1. 安装：<https://${HERMES_DASHBOARD_PUBLIC_URL}/plugins> @ `kyan001/Holographic-CHS-for-Hermes`
    2. 安装前勾选 "Enable"，或在插件列表中手动启用。
    3. 在同一 Dashboard 插件页面中设置为 memory provider。
    4. 重启：`/restart` 或 `/new`
    * 更新：点击插件列表中的 "Git Pull"。
* 通过 Hermes CLI：
    1. 安装：`hermes plugins install kyan001/Holographic-CHS-for-Hermes --enable`
    2. 设置为记忆后端：`hermes config set memory.provider holographic-chs`
    3. 重启：`hermes gateway restart`
    * 更新：`hermes plugins update holographic-chs-for-hermes`

```YAML
# 文件：${HERMES_HOME}/config.yaml
memory:
  provider: holographic-chs
```

## 做了什么

对 Hermes 内置的 `HolographicMemoryProvider` 打补丁，将 FTS5 分词器从默认的 `unicode61` 替换为 `tokenize='trigram'`，使中文文本可以逐字检索。

不加此插件时，用 `冰黑咖啡` 搜索记忆中存储的 `冰的黑咖啡` 会返回零结果——默认分词器只在空白字符和标点处切分，中文被当作一整块索引。使用 trigram 后，两者会分解为重叠的 3 字子串（`冰黑咖` / `的黑咖` / `黑咖啡`）并成功匹配。

## 记忆写入镜像

镜像内置的 `memory` 工具操作到 fact_store：

* `add`：透传父类，无变化。
* `replace`：通过 `old_text` 查找旧事实 → `update_fact` 更新内容，保持同一 `fact_id`。
* `remove`：通过内容精确查找 → `remove_fact` 删除。

`add_fact` 的内置去重（UNIQUE content）替代了按内容查找 fact_id 的缺失。`replace` / `remove` 只处理已知操作，未知操作兜底交给父类，不插手上层行为。

## 搜索策略

两阶段回退，最大化召回率：

1. **FTS5 AND（默认）** — 精确 trigram 匹配
2. **Trigram OR 展开** — FTS5 返回空时，用 OR 连接的 trigram 重试（仅限 ≥4 字查询）。展开前先去除 509 个多字停用词以减少噪音

> **已知局限**：trigram 分词器至少需要 3 个字符才能生成索引条目。短于 3 个字的查询（如 `咖啡`、`北京`）无法命中 FTS5 索引。有意未加入 LIKE 回退——单字搜索结果噪音过大，双字查询在实际 agent 使用中也极为罕见。

## 文件结构

```TOML
Holographic-CHS-for-Hermes/
├── plugin.yaml       # Hermes 插件元数据
└── __init__.py       # register(ctx) + 实现
```

除 Hermes 本身外无任何额外依赖。该插件继承内置的 `HolographicMemoryProvider`，在初始化时应用 monkey-patch。
