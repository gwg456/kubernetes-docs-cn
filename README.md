# Flask OIDC API

一个集成OpenID Connect (OIDC) 认证的Flask REST API应用。

## 功能特性

- ✅ **OIDC认证集成** - 支持标准的OpenID Connect认证流程
- ✅ **角色基础访问控制** - 基于用户角色的API访问控制
- ✅ **RESTful API设计** - 标准的REST API端点
- ✅ **多种认证装饰器** - 灵活的认证和授权装饰器
- ✅ **完整的错误处理** - 统一的错误响应格式
- ✅ **健康检查端点** - 用于监控和负载均衡
- ✅ **Bearer Token支持** - 支持JWT Bearer token认证
- ✅ **配置管理** - 支持多环境配置

## 项目结构

```
flask-oidc-api/
├── app.py                          # 主应用文件
├── auth.py                         # 认证相关工具函数
├── config.py                       # 配置管理
├── requirements.txt                # Python依赖
├── client_secrets.json             # OIDC客户端配置（通用）
├── client_secrets_keycloak.json    # Keycloak专用配置示例
├── .env.example                    # 环境变量示例
├── test_api.py                     # API测试脚本
└── README.md                       # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置OIDC提供商

复制并修改客户端配置文件：

```bash
cp client_secrets.json.example client_secrets.json
```

编辑 `client_secrets.json`，填入你的OIDC提供商信息：

```json
{
  "web": {
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "auth_uri": "https://your-oidc-provider.com/auth",
    "token_uri": "https://your-oidc-provider.com/token",
    "userinfo_uri": "https://your-oidc-provider.com/userinfo",
    "issuer": "https://your-oidc-provider.com",
    "redirect_uris": [
      "http://localhost:5000/oidc_callback"
    ]
  }
}
```

### 3. 设置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
SECRET_KEY=your-super-secret-key-change-in-production
FLASK_DEBUG=true
OIDC_OPENID_REALM=flask-oidc-api
```

### 4. 启动应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

## API端点

### 认证相关

| 端点 | 方法 | 描述 | 认证要求 |
|------|------|------|----------|
| `/auth/login` | GET | 用户登录 | 无（会重定向到OIDC提供商） |
| `/auth/logout` | GET | 用户登出 | 无 |
| `/auth/profile` | GET | 获取用户信息 | 需要认证 |

### API端点

| 端点 | 方法 | 描述 | 认证要求 |
|------|------|------|----------|
| `/` | GET | API信息 | 无 |
| `/health` | GET | 健康检查 | 无 |
| `/api/public` | GET | 公开端点 | 无 |
| `/api/protected` | GET | 受保护端点 | 需要认证 |
| `/api/admin` | GET | 管理员端点 | 需要admin角色 |
| `/api/users` | GET | 获取用户列表 | 需要认证 |
| `/api/users` | POST | 创建用户 | 需要认证 |
| `/api/users/{id}` | GET | 获取用户详情 | 需要认证 |
| `/api/users/{id}` | PUT | 更新用户 | 需要认证 |
| `/api/users/{id}` | DELETE | 删除用户 | 需要admin角色 |

## 认证装饰器

### @require_auth
要求用户已通过OIDC认证：

```python
from auth import require_auth

@app.route('/api/protected')
@require_auth
def protected_endpoint():
    return jsonify({'message': 'This is protected'})
```

### @require_role(role)
要求用户具有特定角色：

```python
from auth import require_role

@app.route('/api/admin')
@require_role('admin')
def admin_endpoint():
    return jsonify({'message': 'Admin only'})
```

### @require_any_role(*roles)
要求用户具有任意一个指定角色：

```python
from auth import require_any_role

@app.route('/api/moderator')
@require_any_role('admin', 'moderator')
def moderator_endpoint():
    return jsonify({'message': 'Admin or moderator'})
```

### @optional_auth
可选认证，如果用户已认证则提供用户信息：

```python
from auth import optional_auth
from flask import g

@app.route('/api/optional')
@optional_auth
def optional_endpoint():
    if g.user_authenticated:
        return jsonify({'user': g.user_info})
    else:
        return jsonify({'message': 'Anonymous access'})
```

## 测试

运行API测试：

```bash
# 基础测试
python test_api.py

# 使用Bearer token测试
python test_api.py "your-jwt-token"
```

## 配置说明

### 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `SECRET_KEY` | Flask密钥 | `dev-secret-key-change-in-production` |
| `FLASK_DEBUG` | 调试模式 | `false` |
| `HOST` | 服务器地址 | `0.0.0.0` |
| `PORT` | 服务器端口 | `5000` |
| `OIDC_OPENID_REALM` | OIDC域 | `flask-oidc-api` |
| `LOG_LEVEL` | 日志级别 | `INFO` |

### OIDC配置

在 `client_secrets.json` 中配置：

- `client_id`: OIDC客户端ID
- `client_secret`: OIDC客户端密钥
- `auth_uri`: 授权端点URL
- `token_uri`: Token端点URL
- `userinfo_uri`: 用户信息端点URL
- `issuer`: OIDC发行者URL
- `redirect_uris`: 重定向URI列表

## 支持的OIDC提供商

本应用支持任何标准的OpenID Connect提供商，包括：

- **Keycloak**
- **Auth0**
- **Okta**
- **Azure AD**
- **Google**
- **AWS Cognito**

### Keycloak配置示例

```json
{
  "web": {
    "client_id": "flask-oidc-api",
    "client_secret": "your-keycloak-client-secret",
    "auth_uri": "https://keycloak.example.com/auth/realms/myrealm/protocol/openid-connect/auth",
    "token_uri": "https://keycloak.example.com/auth/realms/myrealm/protocol/openid-connect/token",
    "userinfo_uri": "https://keycloak.example.com/auth/realms/myrealm/protocol/openid-connect/userinfo",
    "issuer": "https://keycloak.example.com/auth/realms/myrealm",
    "redirect_uris": [
      "http://localhost:5000/oidc_callback"
    ]
  }
}
```

## 部署

### Docker部署

创建 `Dockerfile`：

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

构建和运行：

```bash
docker build -t flask-oidc-api .
docker run -p 5000:5000 -e SECRET_KEY=your-secret-key flask-oidc-api
```

### 生产环境注意事项

1. **设置强密钥**：确保 `SECRET_KEY` 是随机生成的强密钥
2. **启用HTTPS**：生产环境必须使用HTTPS
3. **配置CORS**：如果需要跨域访问，正确配置CORS
4. **日志配置**：配置适当的日志级别和输出
5. **监控**：使用 `/health` 端点进行健康检查

## 故障排除

### 常见问题

1. **OIDC认证失败**
   - 检查 `client_secrets.json` 配置
   - 确认重定向URI正确配置
   - 检查OIDC提供商的网络连接

2. **角色授权失败**
   - 确认OIDC提供商正确返回角色信息
   - 检查角色字段名称（`roles`, `realm_access.roles` 等）

3. **Session问题**
   - 确保设置了正确的 `SECRET_KEY`
   - 检查Cookie设置

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License
