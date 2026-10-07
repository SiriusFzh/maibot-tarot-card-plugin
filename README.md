# 塔罗牌插件

MaiBot 塔罗牌抽取插件 —— 随机抽取一张大阿卡那牌，查看运势和建议。

## 功能

发送指令后，麦麦会：

1. 随机抽取一张大阿卡那牌，发送对应牌面图片
2. 告诉你是哪张牌（中文名 + 英文名）
3. 给出针对性的运势解读和建议

## 触发方式

| 指令 | 说明 |
|------|------|
| `/塔罗` | 命令触发 |
| 发送包含 `请帮我抽一张塔罗牌` 的任意消息 | 自然语言触发 |

两种方式均会抽取一张牌。自然语言使用子串匹配：消息只要包含 `请帮我抽一张塔罗牌` 就会触发，包括引用这句话的消息。命中后，插件会中断该条消息的下游处理，避免麦麦继续回复同一条请求；这也会阻止该消息上的后续插件处理。需要避免误触发时请使用精确指令 `/塔罗`。

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

将 `tarot-card-plugin` 文件夹放入 MaiBot 的 `plugins/` 目录下，然后在 WebUI 插件管理页面启用即可。

## 配置

`config.toml` 由 MaiBot 根据插件配置模型自动生成，不纳入版本管理。仓库中的 `config.example.toml` 仅供参考。


```toml
[plugin]
enabled = true
config_version = "1.0.0"
```

## 依赖

- MaiBot SDK >= 2.0.0
- 无外部 Python 包依赖

## 许可

MIT