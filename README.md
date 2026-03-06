# 🔮 AstrBot 塔罗牌占卜插件

<div align="center">
![AstrBot](https://img.shields.io/badge/AstrBot-4.18+-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-green.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)

**为 AstrBot 打造的塔罗牌占卜插件，支持每日抽牌与 LLM 智能解读**

**本插件使用纯AI编写，鲁棒性未经测试，目前使用功能正常**

</div>

---
## 📖 目录

- [功能特性](#-功能特性)
- [效果预览](#-效果预览)
- [安装方法](#-安装方法)
- [使用说明](#-使用说明)
- [配置说明](#-配置说明)
- [文件结构](#-文件结构)
- [常见问题](#-常见问题)
- [开发贡献](#-开发贡献)
- [许可证](#-许可证)

---

## ✨ 功能特性

| 功能             | 描述                                                  |
| ---------------- | ----------------------------------------------------- |
| 🎴 **每日抽牌**   | 根据用户 QQ 号 + 日期生成确定性种子，每人每天结果固定 |
| 🔮 **塔罗占卜**   | 针对具体问题抽取 1-3 张牌，自动调用 LLM 进行专业解读  |
| 🤖 **LLM 解读**   | 结合 AstrBot 内置大模型，提供个性化牌意解读           |
| 🔄 **正逆位系统** | 22 张大阿尔克那牌，每张牌均有正位/逆位两种状态        |
| 📦 **开箱即用**   | 无需复杂配置，放置图片即可使用                        |

---

## 📸 效果预览

### 每日抽牌
```
🔮 ━━━━━━━━━━━━━━━━
✨ 今日塔罗牌 ✨
━━━━━━━━━━━━━━━━

📇 序号：20
🏷️ 牌名：审判 (Judgement)
🔄 状态：正位

📜 牌面描述：
大天使加百列在天空中吹响号角...

💡 喻意：
觉醒、重生、反省、因果决断...

━━━━━━━━━━━━━━━━
🌟 祝你今天好运！
```

### 塔罗占卜
```
🔮 ━━━━━━━━━━━━━━━━
✨ 塔罗占卜 ✨
━━━━━━━━━━━━━━━━

📝 问题：我最近的运势如何

🎴 抽取的牌：
🎴 星星（正位）
🎴 月亮（逆位）
🎴 太阳（正位）

⏳ 正在为您解读牌意...

━━━━━━━━━━━━━━━━
🌟 牌意解读 🌟
━━━━━━━━━━━━━━━━

[LLM 生成的专业解读内容]

💫 以上解读仅供参考，命运掌握在自己手中~
```

---

## 📥 安装方法

### 方式一：通过 AstrBot WebUI 安装（推荐）

1. 打开 AstrBot WebUI 管理面板
2. 进入 **插件市场**
3. 搜索 `新塔罗` 或 `tarotnew`
4. 点击 **安装** 按钮

### 方式二：手动安装

```bash
# 1. 进入 AstrBot 插件目录
cd AstrBot/data/plugins

# 2. 创建插件目录
mkdir -p astrbot_plugin_tarot/images

# 3. 将插件文件放入目录
# 将 main.py, CardInfo.json, metadata.yaml 等文件复制到 astrbot_plugin_tarot/

# 4. 准备牌面图片（22 张）
# 将图片命名为 0.png ~ 21.png，放入 images/ 目录
```

### 方式三：Git 克隆

```bash
cd AstrBot/data/plugins
git clone https://github.com/yourname/astrbot_plugin_tarot.git
```

---

## 📝 使用说明

### 指令列表

| 指令              | 功能                 | 示例                        |
| ----------------- | -------------------- | --------------------------- |
| `抽取塔罗牌`      | 每日抽取一张塔罗牌   | `抽取塔罗牌`                |
| `塔罗占卜 + 问题` | 针对问题进行占卜解读 | `塔罗占卜 我最近的财运如何` |
| `塔罗帮助`        | 显示帮助信息         | `塔罗帮助`                  |

### 使用示例

```
# 每日抽牌（每天结果固定）
用户：抽取塔罗牌
机器人：[发送牌面图片 + 文字信息]

# 塔罗占卜（根据问题长度自动决定抽牌数量）
用户：塔罗占卜 我最近的运势如何
机器人：[抽取 1-3 张牌 + LLM 解读]

# 查看帮助
用户：塔罗帮助
机器人：[显示指令说明]
```

### 抽牌规则

| 问题长度 | 抽牌数量 | 说明     |
| -------- | -------- | -------- |
| ≤ 10 字  | 1 张     | 简单问题 |
| > 10 字  | 3 张     | 复杂问题 |

---

## ⚙️ 配置说明

### 可选配置文件 `_conf_schema.json`

```json
{
    "enable_daily_reminder": {
        "description": "是否启用每日抽牌提醒",
        "type": "bool",
        "default": false
    },
    "reminder_time": {
        "description": "每日提醒时间（24 小时制）",
        "type": "string",
        "default": "08:00"
    },
    "enable_image": {
        "description": "是否显示牌面图片",
        "type": "bool",
        "default": true
    },
    "default_card_count": {
        "description": "默认占卜抽牌数量",
        "type": "int",
        "default": 3,
        "options": [1, 2, 3]
    }
}
```

### 配置存储位置

配置文件将自动保存在：
```
AstrBot/data/config/astrbot_plugin_tarot_config.json
```

---

## 📁 文件结构

```
astrbot_plugin_tarot/
├── main.py                 # 主插件文件
├── metadata.yaml           # 插件元数据（必填）
├── _conf_schema.json       # 配置 Schema（可选）
├── requirements.txt        # 依赖文件（本插件无额外依赖）
├── CardInfo.json           # 牌面信息数据
├── logo.png                # 插件 Logo（可选，256x256）
└── images/                 # 牌面图片目录
    ├── 0.png               # 愚者
    ├── 1.png               # 魔术师
    ├── 2.png               # 女祭司
    ├── ...
    └── 21.png              # 世界
```

### 牌面序号对照表

| 序号 | 牌名                        | 序号 | 牌名                    |
| ---- | --------------------------- | ---- | ----------------------- |
| 0    | 愚者 (The Fool)             | 11   | 正义 (Justice)          |
| 1    | 魔术师 (The Magician)       | 12   | 倒吊人 (The Hanged Man) |
| 2    | 女祭司 (The High Priestess) | 13   | 死神 (Death)            |
| 3    | 皇后 (The Empress)          | 14   | 节制 (Temperance)       |
| 4    | 皇帝 (The Emperor)          | 15   | 恶魔 (The Devil)        |
| 5    | 教皇 (The Hierophant)       | 16   | 高塔 (The Tower)        |
| 6    | 恋人 (The Lovers)           | 17   | 星星 (The Star)         |
| 7    | 战车 (The Chariot)          | 18   | 月亮 (The Moon)         |
| 8    | 力量 (Strength)             | 19   | 太阳 (The Sun)          |
| 9    | 隐士 (The Hermit)           | 20   | 审判 (Judgement)        |
| 10   | 命运之轮 (Wheel of Fortune) | 21   | 世界 (The World)        |

---

## ❓ 常见问题

### Q1: 抽牌时提示"图片不存在"
**A:** 请检查 `images/` 目录下是否有对应序号的图片文件（如 `0.png` ~ `21.png`）。如果没有图片，插件会自动降级为纯文字模式。

### Q2: LLM 解读失败
**A:** 请确保 AstrBot 已正确配置大语言模型提供商。LLM 失败时插件会自动提供基础解读，不会影响使用。

### Q3: 如何更换牌面图片？
**A:** 直接替换 `images/` 目录下对应序号的 `.png` 文件即可。建议尺寸：512x512 或更高。

### Q4: 同一用户同一天能抽多次吗？
**A:** 可以，但结果相同。种子由 QQ 号 + 日期生成，确保每日结果一致性。

### Q5: 支持其他平台吗？
**A:** 插件理论上支持所有 AstrBot 适配的平台（QQ、Telegram、Discord 等），但图片发送功能可能因平台而异。

### Q6: 如何添加小阿尔克那牌？
**A:** 目前仅支持 22 张大阿尔克那。如需扩展，请修改 `CardInfo.json` 和代码中的 `major_arcana_count` 变量。

---



## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)

```
Copyright (c) 2024 Sqridmus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🙏 致谢

- [AstrBot](https://github.com/AstrBotDevs/AstrBot) - 强大的机器人框架

---

<div align="center">
**🌙 愿星辰指引你的道路~**