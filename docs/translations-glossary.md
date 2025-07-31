---
title: "Kubernetes 翻译术语词汇表"
---

# Kubernetes 翻译术语词汇表

本词汇表规定了 Kubernetes 文档中英文术语的标准中文翻译，以确保翻译的一致性和准确性。

## 核心概念 / Core Concepts

| 英文 | 中文 | 说明 |
|------|------|------|
| Cluster | 集群 | |
| Node | 节点 | |
| Master | 主节点 | |
| Worker Node | 工作节点 | |
| Control Plane | 控制平面 | |
| Pod | Pod | 保留英文 |
| Container | 容器 | |
| Namespace | 命名空间 | |
| Label | 标签 | |
| Selector | 选择器 | |
| Annotation | 注解 | |

## 工作负载 / Workloads

| 英文 | 中文 | 说明 |
|------|------|------|
| Deployment | 部署 | |
| ReplicaSet | 副本集 | |
| StatefulSet | 有状态副本集 | |
| DaemonSet | 守护进程集 | |
| Job | 任务 | |
| CronJob | 定时任务 | |
| ReplicationController | 副本控制器 | 已废弃，但文档中仍可能出现 |

## 服务和网络 / Services & Networking

| 英文 | 中文 | 说明 |
|------|------|------|
| Service | 服务 | |
| Endpoint | 端点 | |
| Ingress | 入口 | |
| LoadBalancer | 负载均衡器 | |
| NodePort | 节点端口 | |
| ClusterIP | 集群 IP | |
| NetworkPolicy | 网络策略 | |
| DNS | DNS | 保留英文缩写 |

## 存储 / Storage

| 英文 | 中文 | 说明 |
|------|------|------|
| Volume | 数据卷 | |
| PersistentVolume (PV) | 持久卷 | |
| PersistentVolumeClaim (PVC) | 持久卷声明 | |
| StorageClass | 存储类 | |
| ConfigMap | 配置映射 | |
| Secret | 保密字典 | |

## 安全 / Security

| 英文 | 中文 | 说明 |
|------|------|------|
| ServiceAccount | 服务账户 | |
| RBAC | RBAC | 保留英文缩写 |
| Role | 角色 | |
| RoleBinding | 角色绑定 | |
| ClusterRole | 集群角色 | |
| ClusterRoleBinding | 集群角色绑定 | |
| SecurityContext | 安全上下文 | |
| Pod Security Policy | Pod 安全策略 | |

## 管理和运维 / Administration

| 英文 | 中文 | 说明 |
|------|------|------|
| kubectl | kubectl | 保留英文 |
| kubeadm | kubeadm | 保留英文 |
| kubelet | kubelet | 保留英文 |
| kube-proxy | kube-proxy | 保留英文 |
| kube-apiserver | kube-apiserver | 保留英文 |
| kube-scheduler | kube-scheduler | 保留英文 |
| kube-controller-manager | kube-controller-manager | 保留英文 |
| etcd | etcd | 保留英文 |

## 监控和日志 / Monitoring & Logging

| 英文 | 中文 | 说明 |
|------|------|------|
| Monitoring | 监控 | |
| Logging | 日志记录 | |
| Metrics | 指标 | |
| Event | 事件 | |
| Audit | 审计 | |

## 扩展 / Extensions

| 英文 | 中文 | 说明 |
|------|------|------|
| Custom Resource Definition (CRD) | 自定义资源定义 | |
| Custom Resource | 自定义资源 | |
| Operator | 操作器 | |
| Admission Controller | 准入控制器 | |
| Webhook | Webhook | 保留英文 |

## 操作和状态 / Operations & Status

| 英文 | 中文 | 说明 |
|------|------|------|
| Create | 创建 | |
| Apply | 应用 | |
| Update | 更新 | |
| Delete | 删除 | |
| Scale | 扩缩容 | |
| Rolling Update | 滚动更新 | |
| Rollback | 回滚 | |
| Pending | 待处理 | |
| Running | 运行中 | |
| Succeeded | 成功 | |
| Failed | 失败 | |
| Terminating | 正在终止 | |

## 调度 / Scheduling

| 英文 | 中文 | 说明 |
|------|------|------|
| Scheduler | 调度器 | |
| Scheduling | 调度 | |
| Affinity | 亲和性 | |
| Anti-affinity | 反亲和性 | |
| Taint | 污点 | |
| Toleration | 容忍度 | |
| Node Selector | 节点选择器 | |

## 资源管理 / Resource Management

| 英文 | 中文 | 说明 |
|------|------|------|
| Resource | 资源 | |
| Request | 请求 | |
| Limit | 限制 | |
| Quota | 配额 | |
| LimitRange | 限制范围 | |
| ResourceQuota | 资源配额 | |

## 翻译原则

### 1. 术语一致性
- 同一术语在整个文档中必须使用相同的中文翻译
- 优先使用已建立的标准翻译
- 对于有争议的术语，团队讨论后确定统一翻译

### 2. 技术术语处理
- **保留英文**：对于广泛使用的技术缩写或专有名词（如 kubectl、API、YAML）
- **意译**：对于有准确中文对应的概念
- **音译+意译**：对于部分专有名词可提供音译和意译的组合

### 3. 语境适应
- 根据上下文调整翻译，确保语义准确
- 保持技术文档的严谨性
- 兼顾中文表达习惯

### 4. 版本管理
- 随着 Kubernetes 版本更新，及时更新术语表
- 对废弃的术语标注说明
- 对新增术语进行团队评议

## 使用说明

1. **翻译时优先查阅此词汇表**
2. **如遇到表中未包含的术语，请先在团队中讨论**
3. **新增术语确定后，及时更新此词汇表**
4. **定期审核和更新词汇表内容**

---

最后更新：2024年1月
维护者：Kubernetes 中文文档翻译团队