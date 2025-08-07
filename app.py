from flask import Flask, request, jsonify, session, redirect, url_for
from flask_oidc import OpenIDConnect
from functools import wraps
import os
import logging
import json

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Flask配置
app.config.update({
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production'),
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,  # 生产环境中应设置为True
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_OPENID_REALM': os.environ.get('OIDC_OPENID_REALM', 'flask-oidc-api'),
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
})

# 初始化OIDC
oidc = OpenIDConnect(app)

# 装饰器：检查OIDC认证
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not oidc.user_loggedin:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'OIDC authentication required'
            }), 401
        return f(*args, **kwargs)
    return decorated_function

# 装饰器：检查特定角色或权限
def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not oidc.user_loggedin:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'OIDC authentication required'
                }), 401
            
            # 获取用户信息
            user_info = oidc.user_getinfo(['sub', 'email', 'name', 'roles', 'groups'])
            
            # 检查角色（这里假设角色信息在token中）
            user_roles = user_info.get('roles', [])
            if isinstance(user_roles, str):
                user_roles = [user_roles]
            
            if required_role not in user_roles:
                return jsonify({
                    'error': 'Forbidden',
                    'message': f'Role "{required_role}" required'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 根路径
@app.route('/')
def index():
    return jsonify({
        'message': 'Flask OIDC API Server',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'login': '/auth/login',
                'logout': '/auth/logout',
                'profile': '/auth/profile'
            },
            'api': {
                'users': '/api/users',
                'protected': '/api/protected',
                'admin': '/api/admin'
            }
        }
    })

# 认证相关路由
@app.route('/auth/login')
@oidc.require_login
def login():
    return jsonify({
        'message': 'Login successful',
        'user': oidc.user_getinfo(['sub', 'email', 'name'])
    })

@app.route('/auth/logout')
def logout():
    oidc.logout()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/auth/profile')
@require_auth
def profile():
    user_info = oidc.user_getinfo(['sub', 'email', 'name', 'preferred_username', 'roles', 'groups'])
    return jsonify({
        'user': user_info,
        'authenticated': True
    })

# API路由
@app.route('/api/public')
def public_api():
    """公开API端点，无需认证"""
    return jsonify({
        'message': 'This is a public endpoint',
        'timestamp': '2024-01-01T00:00:00Z',
        'data': 'Anyone can access this'
    })

@app.route('/api/protected')
@require_auth
def protected_api():
    """受保护的API端点，需要认证"""
    user_info = oidc.user_getinfo(['sub', 'email', 'name'])
    return jsonify({
        'message': 'This is a protected endpoint',
        'user': user_info,
        'data': 'Only authenticated users can access this'
    })

@app.route('/api/users', methods=['GET'])
@require_auth
def get_users():
    """获取用户列表（需要认证）"""
    # 模拟用户数据
    users = [
        {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
        {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
    ]
    return jsonify({
        'users': users,
        'total': len(users)
    })

@app.route('/api/users', methods=['POST'])
@require_auth
def create_user():
    """创建用户（需要认证）"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Name and email are required'
        }), 400
    
    # 模拟创建用户
    new_user = {
        'id': 3,
        'name': data['name'],
        'email': data['email'],
        'created_by': oidc.user_getfield('email')
    }
    
    return jsonify({
        'message': 'User created successfully',
        'user': new_user
    }), 201

@app.route('/api/admin')
@require_role('admin')
def admin_api():
    """管理员API端点，需要admin角色"""
    return jsonify({
        'message': 'This is an admin endpoint',
        'data': 'Only admin users can access this',
        'admin_info': 'Sensitive admin data here'
    })

@app.route('/api/users/<int:user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    """获取特定用户信息"""
    # 模拟获取用户
    if user_id == 1:
        user = {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}
        return jsonify({'user': user})
    else:
        return jsonify({
            'error': 'Not Found',
            'message': f'User with id {user_id} not found'
        }), 404

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@require_auth
def update_user(user_id):
    """更新用户信息"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Request body is required'
        }), 400
    
    # 模拟更新用户
    updated_user = {
        'id': user_id,
        'name': data.get('name', 'Updated Name'),
        'email': data.get('email', 'updated@example.com'),
        'updated_by': oidc.user_getfield('email')
    }
    
    return jsonify({
        'message': 'User updated successfully',
        'user': updated_user
    })

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@require_role('admin')
def delete_user(user_id):
    """删除用户（需要admin角色）"""
    return jsonify({
        'message': f'User {user_id} deleted successfully',
        'deleted_by': oidc.user_getfield('email')
    })

# 健康检查端点
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'flask-oidc-api',
        'version': '1.0.0'
    })

# 错误处理
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'error': 'Unauthorized',
        'message': 'Authentication required'
    }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'error': 'Forbidden',
        'message': 'Insufficient permissions'
    }), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An internal error occurred'
    }), 500

if __name__ == '__main__':
    app.run(
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    )