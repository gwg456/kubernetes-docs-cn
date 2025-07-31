---
title: "Pod 概述"
---

* TOC
{:toc}

在 Kubernetes 中，_Pod_ 是可以创建、调度和管理的最小可部署单元，而不是单个应用容器。

## 什么是 _Pod_？

_Pod_（就像豌豆荚或鲸鱼群）对应一组运行在共享上下文中的同位应用程序。在该上下文中，应用程序还可能应用单独的 cgroup 隔离。Pod 为容器化环境中的应用程序特定的"逻辑主机"建模。它可能包含一个或多个相对紧密耦合的应用程序——在预容器时代，它们会在同一个物理或虚拟主机上执行。

Pod 的上下文可以定义为几个 Linux 命名空间的结合：

* PID 命名空间（Pod 内的应用程序可以看到彼此的进程）
* 网络命名空间（Pod 内的应用程序可以访问相同的 IP 和端口空间）
* IPC 命名空间（Pod 内的应用程序可以使用 SystemV IPC 或 POSIX 消息队列进行通信）
* UTS 命名空间（Pod 内的应用程序共享主机名）

Pod 内的应用程序还可以访问共享数据卷，这些数据卷在 Pod 级别定义，并在每个应用程序的文件系统中可用。此外，Pod 可以定义顶级 cgroup 隔离，形成应用于组成应用程序的任何单独隔离的外层边界。

就 [Docker](https://www.docker.com/) 构造而言，Pod 由一组具有共享[数据卷](/docs/user-guide/volumes)的同位 Docker 容器组成。PID 命名空间共享尚未在 Docker 中实现。

与单个应用容器一样，Pod 被认为是相对临时的实体，而不是持久实体。如[Pod 的生命周期](/docs/user-guide/pod-states)中所讨论的，Pod 被调度到节点上并在那里保持直到终止（根据重启策略）或删除。当节点死亡时，调度到该节点的 Pod 将被删除。特定的 Pod 永远不会重新调度到新节点；相反，它们必须被替换（有关更多详细信息，请参阅[副本控制器](/docs/user-guide/replication-controller)）。（在未来，更高级别的 API 可能支持 Pod 迁移。）

## Pod 的动机

### 资源共享和通信

Pod 促进其组成部分之间的数据共享和通信。

Pod 中的应用程序都使用相同的网络命名空间/IP 和端口空间，并且可以使用 localhost 找到并相互通信。每个 Pod 在平面共享网络命名空间中都有一个 IP 地址，该命名空间与网络上的其他物理计算机和容器具有完全通信。主机名设置为 Pod 内应用容器的 Pod 名称。[有关网络的更多详细信息](/docs/admin/networking)。

除了定义在 Pod 中运行的应用容器外，Pod 还指定一组共享存储卷。数据卷使数据能够在容器重启后继续存在，并在 Pod 内的应用程序之间共享。

### 管理

Pod 还通过提供比原始、低级容器接口更高级别的抽象来简化应用程序部署和管理。Pod 充当部署和水平扩展/复制的单元。同位（协同调度）、命运共享、协调复制、资源共享和依赖管理都会自动处理。

## Pod 的用途

Pod 可用于托管垂直集成的应用程序堆栈，但其主要动机是支持同位、协同管理的辅助程序，例如：

* 内容管理系统、文件和数据加载器、本地缓存管理器等
* 日志和检查点备份、压缩、轮转、快照等
* 数据变更监视器、日志跟踪器、日志记录和监控适配器、事件发布器等
* 代理、网桥和适配器
* 控制器、管理器、配置器和更新器

一般来说，单个 Pod 不用于运行同一应用程序的多个实例。

有关更长的解释，请参阅[分布式系统工具包：复合容器模式](http://blog.kubernetes.io/2015/06/the-distributed-system-toolkit-patterns)。

## 考虑的替代方案

_为什么不在单个（Docker）容器中运行多个程序？_

1. 透明度。使 Pod 内的容器对基础设施可见，使基础设施能够为这些容器提供服务，例如进程管理和资源监控。这为用户提供了许多便利。
2. 解耦软件依赖关系。各个容器可以独立重建和重新部署。Kubernetes 甚至可能在某天支持单个容器的实时更新。
3. 易于使用。用户不需要运行自己的进程管理器，担心信号和退出代码传播等。
4. 效率。由于基础设施承担更多责任，容器可以更轻量级。

_为什么不支持基于亲和性的容器协同调度？_

这种方法会提供同位，但不会提供 Pod 的大部分好处，例如资源共享、IPC、保证的命运共享和简化的管理。

## Pod 的持久性（或缺乏持久性）

Pod 不打算被视为持久的[宠物](https://blog.engineyard.com/2014/pets-vs-cattle)。它们不会在调度失败、节点失败或其他驱逐（例如由于资源不足或节点维护）中幸存。

一般来说，用户不应该直接创建 Pod。他们几乎总是应该使用控制器（例如，[副本控制器](/docs/user-guide/replication-controller)），即使是单例。控制器提供具有集群范围的自愈，以及复制和发布管理。

使用集合 API 作为主要面向用户的原语在集群调度系统中相对常见，包括 [Borg](https://research.google.com/pubs/pub43438)、[Marathon](https://mesosphere.github.io/marathon/docs/rest-api)、[Aurora](http://aurora.apache.org/documentation/latest/configuration-reference/#job-schema) 和 [Tupperware](http://www.slideshare.net/Docker/aravindnarayanan-facebook140613153626phpapp02-37588997)。

Pod 作为原语公开是为了促进：

* 调度器和控制器的可插拔性
* 支持 Pod 级操作，而无需通过控制器 API "代理"它们
* Pod 生命周期与控制器生命周期的解耦，例如用于引导
* 控制器和服务的解耦——端点控制器只监视 Pod
* Kubelet 级功能与集群级功能的清洁组合——Kubelet 实际上是"Pod 控制器"
* 高可用性应用程序，它们希望 Pod 在终止之前被替换，当然在删除之前，例如在计划驱逐、镜像预获取或实时 Pod 迁移的情况下 [#3949](http://issue.k8s.io/3949)

宠物的当前最佳实践是创建一个 `replicas` 等于 `1` 的副本控制器和相应的服务。如果您发现这很麻烦，请在 [issue #260](http://issue.k8s.io/260) 上发表评论。

## Pod 的终止

由于 Pod 表示集群中节点上运行的进程，重要的是在不再需要这些进程时允许它们优雅地终止（与使用 KILL 信号暴力杀死并且没有机会清理相比）。用户应该能够请求删除并知道进程何时终止，但也要能够确保删除最终完成。当用户请求删除 Pod 时，系统会记录在允许强制杀死 Pod 之前的预期宽限期，并将 TERM 信号发送到每个容器中的主进程。一旦宽限期过期，KILL 信号就会发送到这些进程，然后从 API 服务器中删除 Pod。如果 Kubelet 或容器管理器在等待进程终止时重新启动，则将使用完整的宽限期重试终止。

一个示例流程：

1. 用户发送删除 Pod 的命令，使用默认宽限期（30秒）
2. API 服务器中的 Pod 会更新为超过此时间后 Pod 被认为"死亡"的时间以及宽限期
3. 在客户端命令中列出时，Pod 显示为"Terminating"（正在终止）
4. （与第3步同时）当 Kubelet 看到 Pod 已被标记为终止（因为第2步中的时间已设置）时，它开始 Pod 关闭过程
   1. 如果 Pod 定义了 [preStop 钩子](/docs/user-guide/container-environment/#hook-details)，它会在 Pod 内部调用。如果 `preStop` 钩子在宽限期过期后仍在运行，则使用较小的（2秒）扩展宽限期调用第2步
   2. Pod 中的进程会收到 TERM 信号
5. （与第3步同时），Pod 从服务的端点列表中删除，不再被认为是副本控制器运行 Pod 集合的一部分。缓慢关闭的 Pod 可以继续为流量提供服务，因为负载均衡器（如服务代理）将它们从轮转中删除
6. 当宽限期过期时，Pod 中仍在运行的任何进程都会被 SIGKILL 杀死
7. Kubelet 将通过设置宽限期 0（立即删除）在 API 服务器上完成 Pod 的删除。Pod 从 API 中消失，客户端不再可见

默认情况下，所有删除都在 30 秒内优雅完成。`kubectl delete` 命令支持 `--grace-period=<seconds>` 选项，允许用户覆盖默认值并指定自己的值。值 `0` 表示删除应该是立即的，并立即从 API 中删除 Pod，以便可以使用相同的名称创建新的 Pod。在节点上，设置为立即终止的 Pod 在被强制杀死之前仍会被给予一个小的宽限期。

## Pod 容器的特权模式

从 kubernetes v1.1 开始，Pod 中的任何容器都可以使用容器规范的 `SecurityContext` 上的 `privileged` 标志启用特权模式。这对于想要使用 Linux 能力（如操纵网络堆栈和访问设备）的容器很有用。容器内的进程几乎获得与容器外进程可用的相同特权。使用特权模式，应该更容易将网络和卷插件编写为不需要编译到 kubelet 中的单独 Pod。

如果主节点运行 kubernetes v1.1 或更高版本，而节点运行低于 v1.1 的版本，则新的特权 Pod 将被 api-server 接受，但不会启动。它们将处于待处理状态。
如果用户调用 `kubectl describe pod FooPodName`，用户可以看到 Pod 处于待处理状态的原因。describe 命令输出中的事件表将显示：
`Error validating pod "FooPodName"."FooPodNamespace" from api, ignoring: spec.containers[0].securityContext.privileged: forbidden '<*>(0xc2089d3248)true'`

如果主节点运行低于 v1.1 的版本，则无法创建特权 Pod。如果用户尝试创建具有特权容器的 Pod，用户将收到以下错误：
`The Pod "FooPodName" is invalid.
spec.containers[0].securityContext.privileged: forbidden '<*>(0xc20b222db0)true'`

## API 对象

Pod 是 kubernetes REST API 中的顶级资源。有关 API 对象的更多详细信息，请参阅：[Pod API 对象](http://kubernetes.io/v1.1/docs/api-reference/v1/definitions/#_v1_pod)。



