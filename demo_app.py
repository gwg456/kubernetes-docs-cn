from flask import Flask, request, jsonify, session
from functools import wraps
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo-secret-key-for-testing'

# 模拟认证装饰器（演示用）
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Bearer token required',
                'code': 'AUTH_REQUIRED'
            }), 401
        return f(*args, **kwargs)
    return decorated_function

def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Bearer token required',
                    'code': 'AUTH_REQUIRED'
                }), 401
            
            # 简单的角色检查（演示用）
            token = auth_header.split(' ')[1]
            if required_role == 'admin' and 'admin' not in token.lower():
                return jsonify({
                    'error': 'Forbidden',
                    'message': f'Role "{required_role}" required',
                    'code': 'INSUFFICIENT_PERMISSIONS'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 根路径
@app.route('/')
def index():
    return jsonify({
        'message': 'Flask OIDC API Server (Demo Mode)',
        'version': '1.0.0',
        'mode': 'demo',
        'endpoints': {
            'auth': {
                'info': 'In demo mode, use Bearer tokens for testing'
            },
            'api': {
                'public': '/api/public',
                'protected': '/api/protected (需要Bearer token)',
                'admin': '/api/admin (需要包含admin的Bearer token)',
                'users': '/api/users'
            }
        },
        'demo_tokens': {
            'user_token': 'demo-user-token',
            'admin_token': 'demo-admin-token'
        }
    })

# API路由
@app.route('/api/public')
def public_api():
    """公开API端点，无需认证"""
    return jsonify({
        'message': 'This is a public endpoint',
        'timestamp': '2024-01-01T00:00:00Z',
        'data': 'Anyone can access this',
        'demo': True
    })

@app.route('/api/protected')
@require_auth
def protected_api():
    """受保护的API端点，需要认证"""
    auth_header = request.headers.get('Authorization', '')
    token = auth_header.split(' ')[1] if ' ' in auth_header else 'unknown'
    
    return jsonify({
        'message': 'This is a protected endpoint',
        'token_used': token,
        'data': 'Only authenticated users can access this',
        'demo': True
    })

@app.route('/api/users', methods=['GET'])
@require_auth
def get_users():
    """获取用户列表（需要认证）"""
    users = [
        {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
        {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
    ]
    return jsonify({
        'users': users,
        'total': len(users),
        'demo': True
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
    
    new_user = {
        'id': 3,
        'name': data['name'],
        'email': data['email'],
        'created_by': 'demo-user',
        'demo': True
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
        'admin_info': 'Sensitive admin data here',
        'demo': True
    })

# 健康检查端点
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'flask-oidc-api-demo',
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

if __name__ == '__main__':
    print("🚀 启动Flask OIDC API演示服务器...")
    print("📍 地址: http://localhost:5000")
    print("📖 API文档: http://localhost:5000")
    print("🔑 演示token:")
    print("   - 普通用户: demo-user-token")
    print("   - 管理员: demo-admin-token")
    print("💡 使用方法: 在请求头中添加 Authorization: Bearer <token>")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )