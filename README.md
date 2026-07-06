# 塔罗牌插件

MaiBot 塔罗牌抽取插件 —— 随机抽取一张大阿卡那牌，查看运势和建议。

## 功能

发送指令后，麦麦会：

1. 随机抽取一张大阿卡那牌，发送对应牌面图片
2. 告诉你抽到了什么牌（中文名 + 英文名）
3. 根据牌面含义，分析你当前的近况和运势
4. 给出针对性的行动建议

## 触发方式

| 指令 | 说明 |
|------|------|
| `/塔罗` | 简化命令，快速抽牌 |
| `不属于这个时代的愚者;雾之上的神秘主宰；执掌好运的黄黑之王。请帮我抽一张塔罗牌` | 完整触发短语（名著梗） |

两种方式效果完全相同。

## 支持的塔罗牌（22张大阿卡那）

| 中文名 | 英文名 |
|--------|--------|
| 愚者 | The Fool |
| 魔术师 | The Magician |
| 女祭司 | The High Priestess |
| 皇后 | The Empress |
| 皇帝 | The Emperor |
| 教皇 | The Hierophant |
| 恋人 | The Lovers |
| 战车 | The Chariot |
| 力量 | Strength |
| 隐士 | The Hermit |
| 命运之轮 | Wheel of Fortune |
| 正义 | Justice |
| 倒吊人 | The Hanged Man |
| 死亡 | Death |
| 节制 | Temperance |
| 恶魔 | The Devil |
| 高塔 | The Tower |
| 星星 | The Star |
| 月亮 | The Moon |
| 太阳 | The Sun |
| 审判 | Judgement |
| 世界 | The World |

## 安装

将 `tarot-card-plugin` 文件夹放入 MaiBot 的 `plugins/` 目录下，确保结构如下：

```
plugins/
└── tarot-card-plugin/
    ├── _manifest.json
    ├── config.toml
    ├── plugin.py
    ├── .gitignore
    └── images/
        ├── 愚者.png
        ├── 魔术师.png
        ├── ... (共22张)
        └── 世界.png
```

然后在 MaiBot WebUI 的插件管理页面启用「塔罗牌插件」即可。

## 配置

插件只有一个开关配置项：

```toml
# config.toml
[plugin]
enabled = true          # 是否启用插件
config_version = "1.0.0"
```

## 依赖

- MaiBot SDK >= 2.0.0
- 无外部 Python 包依赖

## 开发

```bash
git clone https://github.com/SiriusFzh/maibot-tarot-card-plugin.git
```

插件使用 MaiBot SDK 的 `@Command` 装饰器注册命令，通过 `self.ctx.send.image()` 和 `self.ctx.send.text()` 发送图片和文本。

## 许可

MIT
