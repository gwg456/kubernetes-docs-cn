# Kubernetes 中文文档 📚

> Kubernetes 官方文档的中文翻译项目

[![Jekyll Build](https://github.com/kubernetes/kubernetes-docs-cn/actions/workflows/jekyll.yml/badge.svg)](https://github.com/kubernetes/kubernetes-docs-cn/actions/workflows/jekyll.yml)
[![License](https://img.shields.io/github/license/kubernetes/kubernetes-docs-cn)](LICENSE)

## 📖 项目介绍

本项目致力于将 Kubernetes 官方文档翻译成中文，为中文用户提供高质量的 Kubernetes 学习资源。

- **目标版本**: Kubernetes v1.29+
- **网站地址**: [https://kubernetes-docs-cn.github.io](https://kubernetes-docs-cn.github.io)
- **翻译进度**: 正在进行中...

## 🚀 快速开始

### 本地开发环境设置

1. **安装 Ruby 和 Bundler**
   ```bash
   # macOS (使用 Homebrew)
   brew install ruby
   
   # Ubuntu/Debian
   sudo apt-get install ruby-full build-essential zlib1g-dev
   
   # 安装 Bundler
   gem install bundler
   ```

2. **克隆项目**
   ```bash
   git clone https://github.com/kubernetes/kubernetes-docs-cn.git
   cd kubernetes-docs-cn
   ```

3. **安装依赖**
   ```bash
   bundle install
   ```

4. **本地运行**
   ```bash
   bundle exec jekyll serve
   ```
   
   访问 [http://localhost:4000](http://localhost:4000) 查看网站

### Docker 方式运行

```bash
# 构建容器
docker build -t k8s-docs-cn .

# 运行容器
docker run -p 4000:4000 -v $(pwd):/srv/jekyll k8s-docs-cn
```

## 🤝 如何贡献

我们欢迎任何形式的贡献！无论是翻译新文档、改进现有翻译，还是修复错误。

### 贡献流程

1. **选择要翻译的文档**
   - 查看 [Issues](https://github.com/kubernetes/kubernetes-docs-cn/issues) 中的翻译任务
   - 创建新的 Issue 声明你要翻译的文档

2. **Fork 并创建分支**
   ```bash
   # Fork 项目到你的 GitHub 账号
   # 然后克隆你的 Fork
   git clone https://github.com/YOUR_USERNAME/kubernetes-docs-cn.git
   cd kubernetes-docs-cn
   
   # 创建新分支
   git checkout -b translate-document-name
   ```

3. **进行翻译**
   - 参考 [翻译规范](#翻译规范)
   - 保持原有的 Markdown 格式和结构
   - 翻译时保留英文术语的中文对照

4. **提交和推送**
   ```bash
   git add .
   git commit -m "翻译: 文档标题"
   git push origin translate-document-name
   ```

5. **创建 Pull Request**
   - 在 GitHub 上创建 Pull Request
   - 在 PR 描述中关联相关 Issue
   - 等待审核和合并

### 翻译规范

#### 📋 术语对照表

| 英文 | 中文 | 说明 |
|------|------|------|
| Pod | Pod | 保留英文 |
| Service | 服务 | 翻译 |
| Deployment | 部署 | 翻译 |
| Namespace | 命名空间 | 翻译 |
| Node | 节点 | 翻译 |
| Cluster | 集群 | 翻译 |
| Container | 容器 | 翻译 |
| Volume | 数据卷 | 翻译 |

#### ✅ 翻译原则

1. **准确性**: 确保翻译准确传达原文含义
2. **一致性**: 使用统一的术语翻译
3. **可读性**: 符合中文表达习惯
4. **格式保持**: 保留原有 Markdown 格式和代码块

#### 📝 文件规范

- 文件名保持英文不变
- Front Matter 中的 `title` 可以翻译为中文
- 代码示例中的注释可以翻译
- 保留所有链接和图片引用

### 示例格式

```yaml
---
title: "Pod 概述"  # 中文标题
---

# Pod 概述

Pod 是 Kubernetes 中最小的可部署单元...

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod  # Pod 名称
spec:
  containers:
  - name: app
    image: nginx
```

## 📊 项目状态

- ✅ 基础架构现代化
- 🔄 核心概念文档翻译中
- ⏳ 用户指南翻译待完成
- ⏳ 管理员指南翻译待开始

## 🛠 技术栈

- **Jekyll 4.3+**: 静态网站生成器
- **GitHub Pages**: 网站托管
- **GitHub Actions**: 自动化构建和部署
- **Kramdown**: Markdown 处理器
- **Rouge**: 语法高亮

## 📞 联系我们

- 🐛 [报告问题](https://github.com/kubernetes/kubernetes-docs-cn/issues)
- 💡 [功能建议](https://github.com/kubernetes/kubernetes-docs-cn/discussions)
- 📧 邮件: docs-zh@kubernetes.io

## 📄 许可证

本项目遵循与 Kubernetes 相同的 [Apache 2.0 许可证](LICENSE)。

## 🙏 致谢

感谢所有为 Kubernetes 中文文档做出贡献的志愿者们！

---

**让我们一起让 Kubernetes 对中文用户更友好！** 🎉
