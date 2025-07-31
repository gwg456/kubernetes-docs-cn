---
layout: default
title: "Kubernetes 中文文档"
---

<div class="hero-section">
  <div class="hero-content">
    <h1>Kubernetes 中文文档</h1>
    <p class="hero-subtitle">生产级别的容器编排系统</p>
    <p class="hero-description">
      Kubernetes 是一个开源的容器编排引擎，用来对容器化应用进行自动化部署、扩缩和管理。
      这个开源项目由云原生计算基金会（CNCF）托管。
    </p>
    <div class="hero-buttons">
      <a href="/docs/user-guide/" class="btn btn-primary">开始学习</a>
      <a href="/docs/getting-started-guides/" class="btn btn-secondary">安装指南</a>
    </div>
  </div>
</div>

<div class="features-section">
  <div class="container">
    <h2>为什么选择 Kubernetes？</h2>
    <div class="features-grid">
      <div class="feature">
        <h3>🚀 自动化部署</h3>
        <p>自动化容器的部署、扩缩和管理，无需手动干预</p>
      </div>
      <div class="feature">
        <h3>🔄 滚动更新</h3>
        <p>支持应用的滚动更新和回滚，确保服务的持续可用性</p>
      </div>
      <div class="feature">
        <h3>⚖️ 负载均衡</h3>
        <p>内置负载均衡功能，自动分发网络流量</p>
      </div>
      <div class="feature">
        <h3>🔧 自我修复</h3>
        <p>自动重启失败的容器，替换和重新调度不健康的节点</p>
      </div>
      <div class="feature">
        <h3>📊 资源管理</h3>
        <p>智能的资源调度和管理，最大化硬件利用率</p>
      </div>
      <div class="feature">
        <h3>🔐 安全保障</h3>
        <p>提供多层安全机制，包括网络隔离、访问控制等</p>
      </div>
    </div>
  </div>
</div>

<div class="getting-started-section">
  <div class="container">
    <h2>快速开始</h2>
    <div class="quick-links">
      <div class="quick-link-card">
        <h3>📚 学习基础</h3>
        <p>了解 Kubernetes 的核心概念</p>
        <ul>
          <li><a href="/docs/user-guide/pods/">什么是 Pod？</a></li>
          <li><a href="/docs/user-guide/services/">服务和网络</a></li>
          <li><a href="/docs/user-guide/deployments/">部署应用</a></li>
        </ul>
      </div>
      <div class="quick-link-card">
        <h3>⚙️ 安装部署</h3>
        <p>在不同环境中安装 Kubernetes</p>
        <ul>
          <li><a href="/docs/getting-started-guides/locally/">本地开发环境</a></li>
          <li><a href="/docs/getting-started-guides/gce/">Google Cloud</a></li>
          <li><a href="/docs/getting-started-guides/aws/">Amazon AWS</a></li>
        </ul>
      </div>
      <div class="quick-link-card">
        <h3>🛠️ 工具指南</h3>
        <p>掌握 Kubernetes 命令行工具</p>
        <ul>
          <li><a href="/docs/user-guide/kubectl/">kubectl 命令</a></li>
          <li><a href="/docs/user-guide/kubeconfig-file/">配置文件</a></li>
          <li><a href="/docs/user-guide/kubectl/kubectl_create/">创建资源</a></li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="community-section">
  <div class="container">
    <h2>加入社区</h2>
    <div class="community-grid">
      <div class="community-item">
        <h3>🤝 参与贡献</h3>
        <p>帮助改进 Kubernetes 中文文档</p>
        <a href="https://github.com/kubernetes/kubernetes-docs-cn">GitHub 仓库</a>
      </div>
      <div class="community-item">
        <h3>💬 交流讨论</h3>
        <p>与其他开发者交流使用经验</p>
        <a href="https://kubernetes.slack.com/">Slack 频道</a>
      </div>
      <div class="community-item">
        <h3>📰 最新动态</h3>
        <p>关注 Kubernetes 最新发展</p>
        <a href="https://kubernetes.io/blog/">官方博客</a>
      </div>
    </div>
  </div>
</div>

<style>
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 2rem;
  text-align: center;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  opacity: 0.9;
}

.hero-description {
  font-size: 1.1rem;
  max-width: 600px;
  margin: 0 auto 2rem;
  line-height: 1.6;
  opacity: 0.9;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 2rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary {
  background: white;
  color: #667eea;
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.features-section, .getting-started-section, .community-section {
  padding: 4rem 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.features-grid, .community-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.feature, .community-item {
  text-align: center;
  padding: 2rem 1rem;
}

.feature h3, .community-item h3 {
  margin-bottom: 1rem;
  color: #333;
}

.quick-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.quick-link-card {
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  padding: 2rem;
  background: white;
}

.quick-link-card h3 {
  margin-bottom: 1rem;
  color: #333;
}

.quick-link-card ul {
  list-style: none;
  padding: 0;
}

.quick-link-card li {
  margin: 0.5rem 0;
}

.quick-link-card a {
  color: #667eea;
  text-decoration: none;
}

.quick-link-card a:hover {
  text-decoration: underline;
}

h2 {
  text-align: center;
  margin-bottom: 1rem;
  color: #333;
  font-size: 2.5rem;
}
</style>