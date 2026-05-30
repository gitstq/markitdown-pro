<div align="center">

# 🚀 MarkItDown-Pro

**Lightweight Document to Markdown Conversion Engine**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)]()
[![Zero Dependencies](https://img.shields.io/badge/Zero-Dependencies-brightgreen.svg)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

## English

### 🎉 Introduction

**MarkItDown-Pro** is a lightweight, zero-dependency CLI tool that converts various document formats to Markdown. Inspired by Microsoft's popular markitdown project, we've built a more focused, lightweight solution with broader format support.

### ✨ Key Features

- **🎯 Zero Dependencies** - Pure Python standard library for core functionality
- **📄 Multi-Format Support** - PDF, DOCX, EPUB, HTML, CSV, XLSX, JSON, XML, and more
- **⚡ High Performance** - Fast conversion with minimal resource usage
- **🔧 Plugin Architecture** - Extensible converter system
- **📊 Batch Processing** - Convert multiple files or entire directories
- **🎨 Clean Output** - Well-formatted Markdown with preserved structure

### 🚀 Quick Start

#### Installation

```bash
# Install from PyPI (when published)
pip install markitdown-pro

# Or install with optional dependencies
pip install markitdown-pro[all]      # All formats
pip install markitdown-pro[pdf]      # PDF support
pip install markitdown-pro[docx]     # Word support
pip install markitdown-pro[epub]     # E-book support
pip install markitdown-pro[xlsx]     # Excel support
```

#### Usage

```bash
# Convert a single file
markitdown-pro document.pdf

# Convert to specific output
markitdown-pro input.docx -o output.md

# Convert multiple files
markitdown-pro *.csv

# Convert directory recursively
markitdown-pro documents/ --recursive

# List supported formats
markitdown-pro --list-formats
```

### 📖 Supported Formats

| Format | Extension | Status | Dependencies |
|--------|-----------|--------|--------------|
| Plain Text | .txt | ✅ Native | None |
| HTML | .html, .htm | ✅ Native | None |
| JSON | .json | ✅ Native | None |
| XML | .xml | ✅ Native | None |
| CSV | .csv | ✅ Native | None |
| Markdown | .md | ✅ Native | None |
| PDF | .pdf | ✅ Optional | PyPDF2 |
| Word | .docx | ✅ Optional | python-docx |
| EPUB | .epub | ✅ Optional | ebooklib |
| Excel | .xlsx, .xls | ✅ Optional | openpyxl |

### 📦 API Usage

```python
from markitdown_pro import MarkItDownPro

# Initialize converter
converter = MarkItDownPro()

# Convert single file
result = converter.convert("document.pdf")
print(result.markdown_content)

# Batch conversion
results = converter.convert_batch(["file1.csv", "file2.csv"])

# Directory conversion
results = converter.convert_directory("documents/", recursive=True)
```

### 💡 Design Philosophy

MarkItDown-Pro was designed with these principles:

1. **Simplicity** - Easy to install, easy to use
2. **Performance** - Fast conversion without bloat
3. **Extensibility** - Plugin architecture for custom converters
4. **Compatibility** - Works on Python 3.8+ across all platforms

### 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 简体中文

### 🎉 项目介绍

**MarkItDown-Pro** 是一款轻量级、零依赖的 CLI 工具，可将各种文档格式转换为 Markdown。灵感来源于 Microsoft 热门的 markitdown 项目，我们构建了一个更专注、更轻量的解决方案，支持更广泛的格式。

### ✨ 核心特性

- **🎯 零依赖设计** - 核心功能纯 Python 标准库实现
- **📄 多格式支持** - PDF、DOCX、EPUB、HTML、CSV、XLSX、JSON、XML 等
- **⚡ 高性能** - 快速转换，资源占用极低
- **🔧 插件架构** - 可扩展的转换器系统
- **📊 批量处理** - 支持多文件或整个目录转换
- **🎨 简洁输出** - 格式良好的 Markdown，保留文档结构

### 🚀 快速开始

#### 安装

```bash
# 从 PyPI 安装（发布后）
pip install markitdown-pro

# 或安装带可选依赖的版本
pip install markitdown-pro[all]      # 所有格式
pip install markitdown-pro[pdf]      # PDF 支持
pip install markitdown-pro[docx]     # Word 支持
pip install markitdown-pro[epub]     # 电子书支持
pip install markitdown-pro[xlsx]     # Excel 支持
```

#### 使用方法

```bash
# 转换单个文件
markitdown-pro document.pdf

# 指定输出文件
markitdown-pro input.docx -o output.md

# 转换多个文件
markitdown-pro *.csv

# 递归转换目录
markitdown-pro documents/ --recursive

# 查看支持的格式
markitdown-pro --list-formats
```

### 📖 支持格式

| 格式 | 扩展名 | 状态 | 依赖 |
|------|--------|------|------|
| 纯文本 | .txt | ✅ 原生 | 无 |
| HTML | .html, .htm | ✅ 原生 | 无 |
| JSON | .json | ✅ 原生 | 无 |
| XML | .xml | ✅ 原生 | 无 |
| CSV | .csv | ✅ 原生 | 无 |
| Markdown | .md | ✅ 原生 | 无 |
| PDF | .pdf | ✅ 可选 | PyPDF2 |
| Word | .docx | ✅ 可选 | python-docx |
| EPUB | .epub | ✅ 可选 | ebooklib |
| Excel | .xlsx, .xls | ✅ 可选 | openpyxl |

### 📦 API 使用

```python
from markitdown_pro import MarkItDownPro

# 初始化转换器
converter = MarkItDownPro()

# 转换单个文件
result = converter.convert("document.pdf")
print(result.markdown_content)

# 批量转换
results = converter.convert_batch(["file1.csv", "file2.csv"])

# 目录转换
results = converter.convert_directory("documents/", recursive=True)
```

### 💡 设计理念

MarkItDown-Pro 遵循以下设计原则：

1. **简洁性** - 易于安装，易于使用
2. **性能** - 快速转换，无冗余
3. **可扩展性** - 插件架构支持自定义转换器
4. **兼容性** - 支持 Python 3.8+，跨平台运行

### 📄 开源协议

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 繁體中文

### 🎉 專案介紹

**MarkItDown-Pro** 是一款輕量級、零依賴的 CLI 工具，可將各種文件格式轉換為 Markdown。靈感來源於 Microsoft 熱門的 markitdown 專案，我們構建了一個更專注、更輕量的解決方案，支援更廣泛的格式。

### ✨ 核心特性

- **🎯 零依賴設計** - 核心功能純 Python 標準庫實現
- **📄 多格式支援** - PDF、DOCX、EPUB、HTML、CSV、XLSX、JSON、XML 等
- **⚡ 高效能** - 快速轉換，資源佔用極低
- **🔧 外掛架構** - 可擴充套件的轉換器系統
- **📊 批次處理** - 支援多檔案或整個目錄轉換
- **🎨 簡潔輸出** - 格式良好的 Markdown，保留文件結構

### 🚀 快速開始

#### 安裝

```bash
# 從 PyPI 安裝（釋出後）
pip install markitdown-pro

# 或安裝帶可選依賴的版本
pip install markitdown-pro[all]      # 所有格式
pip install markitdown-pro[pdf]      # PDF 支援
pip install markitdown-pro[docx]     # Word 支援
pip install markitdown-pro[epub]     # 電子書支援
pip install markitdown-pro[xlsx]     # Excel 支援
```

#### 使用方法

```bash
# 轉換單個檔案
markitdown-pro document.pdf

# 指定輸出檔案
markitdown-pro input.docx -o output.md

# 轉換多個檔案
markitdown-pro *.csv

# 遞迴轉換目錄
markitdown-pro documents/ --recursive

# 檢視支援的格式
markitdown-pro --list-formats
```

### 📖 支援格式

| 格式 | 副檔名 | 狀態 | 依賴 |
|------|--------|------|------|
| 純文字 | .txt | ✅ 原生 | 無 |
| HTML | .html, .htm | ✅ 原生 | 無 |
| JSON | .json | ✅ 原生 | 無 |
| XML | .xml | ✅ 原生 | 無 |
| CSV | .csv | ✅ 原生 | 無 |
| Markdown | .md | ✅ 原生 | 無 |
| PDF | .pdf | ✅ 可選 | PyPDF2 |
| Word | .docx | ✅ 可選 | python-docx |
| EPUB | .epub | ✅ 可選 | ebooklib |
| Excel | .xlsx, .xls | ✅ 可選 | openpyxl |

### 📦 API 使用

```python
from markitdown_pro import MarkItDownPro

# 初始化轉換器
converter = MarkItDownPro()

# 轉換單個檔案
result = converter.convert("document.pdf")
print(result.markdown_content)

# 批次轉換
results = converter.convert_batch(["file1.csv", "file2.csv"])

# 目錄轉換
results = converter.convert_directory("documents/", recursive=True)
```

### 💡 設計理念

MarkItDown-Pro 遵循以下設計原則：

1. **簡潔性** - 易於安裝，易於使用
2. **效能** - 快速轉換，無冗餘
3. **可擴充套件性** - 外掛架構支援自定義轉換器
4. **相容性** - 支援 Python 3.8+，跨平臺執行

### 📄 開源協議

MIT 許可證 - 詳見 [LICENSE](LICENSE) 檔案。

---

<div align="center">

**Made with ❤️ by MarkItDown-Pro Team**

[Report Bug](https://github.com/gitstq/markitdown-pro/issues) · [Request Feature](https://github.com/gitstq/markitdown-pro/issues)

</div>
