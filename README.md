![Logo](docs/logo@2x.png)

# 缝合像素字体 / Fusion Pixel Font

[![License OFL](https://img.shields.io/badge/license-OFL--1.1-orange)](LICENSE-OFL)
[![License MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE-MIT)
[![Releases](https://img.shields.io/github/v/release/TakWolf/fusion-pixel-font)](https://github.com/TakWolf/fusion-pixel-font/releases)
[![Discord](https://img.shields.io/badge/discord-像素字体工房-4E5AF0?logo=discord&logoColor=white)](https://discord.gg/3GKtPKtjdU)
[![QQ Group](https://img.shields.io/badge/QQ群-像素字体工房-brightgreen?logo=qq&logoColor=white)](https://qm.qq.com/q/jPk8sSitUI)

开源的泛中日韩像素字体，黑体无衬线风格，支持 8、10 和 12 像素。

该项目为 [「方舟像素字体」](https://github.com/TakWolf/ark-pixel-font) 的临时性过渡方案。使用多个像素字体合并而成，因此以「缝合」命名。

Logo 捏他自 [《游戏王》](https://zh.wikipedia.org/wiki/%E9%81%8A%E6%88%B2%E7%8E%8B) 中的 [「融合」](https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&cid=4837&request_locale=ja) 魔法卡卡图。

这个项目提供了从提取字模，合并字形到构建字体所需要的完整程序。

> [!IMPORTANT]
> 
> 我们正在进行有关该字体使用情况的调查。
> 
> 如果可以，请帮忙填写下面链接的问卷。非常感谢！
> 
> https://wj.qq.com/s2/24009025/7f6a/

## 预览

可以通过 [Playground](https://fusion-pixel-font.takwolf.com/playground.html) 实时预览字体效果。

### 8 像素

[示例文本](https://fusion-pixel-font.takwolf.com/demo-8px.html) · [等宽模式-字母表](https://fusion-pixel-font.takwolf.com/alphabet-8px-monospaced.html) · [比例模式-字母表](https://fusion-pixel-font.takwolf.com/alphabet-8px-proportional.html)

![Preview-8px](docs/preview-8px.png)

### 10 像素

[示例文本](https://fusion-pixel-font.takwolf.com/demo-10px.html) · [等宽模式-字母表](https://fusion-pixel-font.takwolf.com/alphabet-10px-monospaced.html) · [比例模式-字母表](https://fusion-pixel-font.takwolf.com/alphabet-10px-proportional.html)

![Preview-10px](docs/preview-10px.png)

### 12 像素

[示例文本](https://fusion-pixel-font.takwolf.com/demo-12px.html) · [等宽模式-字母表](https://fusion-pixel-font.takwolf.com/alphabet-12px-monospaced.html) · [比例模式-字母表](https://fusion-pixel-font.takwolf.com/alphabet-12px-proportional.html)

![Preview-12px](docs/preview-12px.png)

## 字符统计

可以通过下面的链接来查看字体各尺寸目前支持的字符情况。

| 尺寸 | 等宽模式 | 比例模式 |
|---|---|---|
| 8px | [info-8px-monospaced](docs/info-8px-monospaced.md) | [info-8px-proportional](docs/info-8px-proportional.md) |
| 10px | [info-10px-monospaced](docs/info-10px-monospaced.md) | [info-10px-proportional](docs/info-10px-proportional.md) |
| 12px | [info-12px-monospaced](docs/info-12px-monospaced.md) | [info-12px-proportional](docs/info-12px-proportional.md) |

## 语言特定字形

目前支持以下语言特定字形版本：

| 版本 | 含义 |
|---|---|
| latin | 拉丁语 |
| zh_hans | 中文-简体 |
| zh_hant | 中文-繁體 |
| ja | 日语 |
| ko | 朝鲜语 |

尽管如此，这个项目仍然是一个基于补丁的字体解决方案。你不应该对语言特定字形抱有特别的期待。

## 程序依赖

- [Pixel Font Builder](https://github.com/TakWolf/pixel-font-builder)
- [Pixel Font Knife](https://github.com/TakWolf/pixel-font-knife)
- [FontTools](https://github.com/fonttools/fonttools)
- [Unidata Blocks](https://github.com/TakWolf/unidata-blocks)
- [Character Encoding Utils](https://github.com/TakWolf/character-encoding-utils)
- [PyYAML](https://github.com/yaml/pyyaml)
- [Pillow](https://github.com/python-pillow/Pillow)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [Jinja](https://github.com/pallets/jinja)
- [HTTPX](https://github.com/encode/httpx)
- [tqdm](https://github.com/tqdm/tqdm)
- [Loguru](https://github.com/Delgan/loguru)
- [Cyclopts](https://github.com/BrianPugh/cyclopts)

## 官方社区

- [「像素字体工房」Discord 服务器](https://discord.gg/3GKtPKtjdU)
- [「像素字体工房」QQ 群 (302383204)](https://qm.qq.com/q/jPk8sSitUI)

## 许可证

分为「字体」和「构建程序」两个部分。

### 字体

使用 [「SIL 开放字体许可证第 1.1 版」](LICENSE-OFL) 授权，保留字体名称「缝合像素 / Fusion Pixel」。

第三方字源许可证如下：

| 字体 | 许可证 | 备注 |
|---|---|---|
| [方舟像素字体 / Ark Pixel Font](https://github.com/TakWolf/ark-pixel-font) | [OFL-1.1](https://github.com/TakWolf/ark-pixel-font/blob/develop/LICENSE-OFL) | 提供 10、12 像素基础字形和参数 |
| [美咲フォント / Misaki](https://littlelimit.net/misaki.htm) | [无类型许可证](assets/fonts/misaki/LICENSE.txt)，兼容 OFL-1.1 | 提供 8 像素日语汉字字形 |
| [美績点陣體 / MisekiBitmap](https://github.com/ItMarki/MisekiBitmap) | [OFL-1.1](https://github.com/ItMarki/MisekiBitmap/blob/main/LICENSE) | 提供 8 像素简体中文汉字字形 |
| [精品點陣體7×7 / BoutiqueBitmap7x7](https://github.com/scott0107000/BoutiqueBitmap7x7) | [OFL-1.1](https://github.com/scott0107000/BoutiqueBitmap7x7/blob/main/OFL.txt) | 提供 8 像素繁体中文汉字字形 |
| [精品點陣體9×9 / BoutiqueBitmap9x9](https://github.com/scott0107000/BoutiqueBitmap9x9) | [OFL-1.1](https://github.com/scott0107000/BoutiqueBitmap9x9/blob/main/OFL.txt) | 提供 10 像素繁体中文汉字补充 |
| [俐方體11號／Cubic 11](https://github.com/ACh-K/Cubic-11) | [OFL-1.1](https://github.com/ACh-K/Cubic-11/blob/main/OFL.txt) | 提供 12 像素繁体中文汉字补充 |
| [Galmuri](https://github.com/quiple/galmuri) | [OFL-1.1](https://github.com/quiple/galmuri/blob/main/ofl.md) | 提供 8、10、12 像素朝鲜语相关字形 |

### 构建程序

使用 [「MIT 许可证」](LICENSE-MIT) 授权。

## 赞助

如果这个项目对您有帮助，请考虑赞助来支持开发工作。

[![赞赏码](https://raw.githubusercontent.com/TakWolf/TakWolf/master/images/badge-payqr@2x.png)](https://github.com/TakWolf/TakWolf/blob/master/payment-qr-codes.md)
[![爱发电](https://raw.githubusercontent.com/TakWolf/TakWolf/master/images/badge-afdian@2x.png)](https://afdian.com/a/takwolf)
[![PayPal](https://raw.githubusercontent.com/TakWolf/TakWolf/master/images/badge-paypal@2x.png)](https://paypal.me/takwolf)

[赞助商名单](https://github.com/TakWolf/TakWolf/blob/master/sponsors.md)
