![banner](docs/logo.png)

# 缝合怪像素字体 / Fusion Pixel Font

[![SIL Open Font License 1.1](https://img.shields.io/badge/license-OFL--1.1-orange)](https://scripts.sil.org/OFL)
[![MIT License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)
[![Releases](https://img.shields.io/github/v/release/TakWolf/fusion-pixel-font)](https://github.com/TakWolf/fusion-pixel-font/releases)

12 像素中文字体。

使用多个第三方像素字体合并而成，因此命名为「缝合怪」。

该字体为 [「方舟像素字体」](https://github.com/TakWolf/ark-pixel-font) 可用前的一种临时替代方案。

根据目前使用的字源，为了保持风格统一，偏向采用繁体中文字形写法。

这个项目提供了从第三方字模提取，到合并编译成字体所需要的完整程序。

Logo 捏他自 [《游戏王集换纸牌游戏》](https://zh.wikipedia.org/wiki/%E9%81%8A%E6%88%B2%E7%8E%8B%E9%9B%86%E6%8F%9B%E7%B4%99%E7%89%8C%E9%81%8A%E6%88%B2) 中的 [「融合」](https://baike.baidu.com/item/%E8%9E%8D%E5%90%88/2290464) 魔法卡卡图。

## 字源

字源的要求：

- 像素字体，字形尺寸为 11 × 11
- 具有免费许可证，并且允许修改和衍生

目前使用的全部字体列表，按照字形使用优先级排列：

| 字体 | 文件 | 版本 |
|---|---|---|
| [方舟像素字体](https://github.com/TakWolf/ark-pixel-font) | ark-pixel-12px-zh_hk.otf | [dev-2022-05-04](https://github.com/TakWolf/ark-pixel-font/releases/tag/dev-2022-05-04) |
| [俐方體11號](https://github.com/ACh-K/Cubic-11) | Cubic_11_1.010_R.ttf | [Version 1.010; 20220222](https://github.com/ACh-K/Cubic-11/releases/tag/v1.010) |
| [Galmuri](https://github.com/quiple/galmuri) | Galmuri11.ttf | [8d24f1f](https://github.com/quiple/galmuri/tree/8d24f1ff97119c7b5cea10070e7a19c51113ffe3) |

## 预览

![preview.png](docs/preview.png)

[示例文本](https://fusion-pixel-font.takwolf.com)

[字符表](https://fusion-pixel-font.takwolf.com/alphabet.html)

[字符统计](docs/font-info.md)

## 缺字

目前仍然缺少 GB2312 和 Big5 编码的大部分二级汉字。

这个问题会随着 [「方舟像素字体」](https://github.com/TakWolf/ark-pixel-font) 的更新迭代而逐渐解决。

如果你在使用中遇到缺字的情况，请在 [Issues](https://github.com/TakWolf/fusion-pixel-font/issues) 提交列表，开发者会优先补充。

## 下载

[下载地址](https://github.com/TakWolf/fusion-pixel-font/releases)

## 授权信息

### 字体

使用 [SIL 开放字体许可证 第1.1版（SIL Open Font License 1.1）](LICENSE-OFL) 授权，保留字体名称「缝合怪像素 / Fusion Pixel」。

使用的所有第三方字体，均兼容该许可证。

### 构建程序

使用 [MIT 许可证](LICENSE-MIT) 授权。
