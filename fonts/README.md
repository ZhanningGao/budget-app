# 字体文件目录

请将中文字体文件放在此目录中，支持的格式：
- `.ttf` (TrueType Font) - 推荐
- `.otf` (OpenType Font)

## 推荐的免费中文字体

### 1. 思源黑体 (Source Han Sans / Noto Sans CJK)
- **下载地址**: https://github.com/adobe-fonts/source-han-sans/releases
- **文件名**: `SourceHanSansCN-Regular.otf` 或 `NotoSansCJK-Regular.ttf`
- **优点**: 开源免费，支持简体中文，字体清晰

### 2. 微软雅黑 / 黑体 / 宋体
- 如果系统已安装，可以从系统字体目录复制
- macOS: `/Library/Fonts/Microsoft/SimHei.ttf` 或 `SimSun.ttf`
- Windows: `C:\Windows\Fonts\` 目录

### 3. 其他推荐字体
- **文泉驿微米黑**: 开源免费
- **站酷字体**: 部分免费

## 使用方法

1. 下载字体文件（.ttf 或 .otf 格式）
2. 将文件重命名为 `SimHei.ttf` 或 `SimSun.ttf`（或保持原文件名）
3. 将文件放入此 `fonts/` 目录
4. 重启 Flask 应用

应用会自动检测并使用此目录中的字体文件，性能最佳！

## 当前已安装的字体

- ✅ **SimHei.ttf** (13MB) - 从系统PingFang提取的黑体字体
- ✅ **PingFang-Regular.ttf** (13MB) - 苹方字体（macOS系统字体）
- ✅ **Arial Unicode.ttf** (22MB) - Arial Unicode（支持中文）

这些字体已经可以正常使用，PDF导出将自动使用这些字体，无需额外配置！

