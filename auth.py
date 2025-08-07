from functools import wraps
from flask import jsonify, request, current_app
from flask_oidc import OpenIDConnect
import jwt
import requests
import logging

logger = logging.getLogger(__name__)

class OIDCAuth:
    """OIDC认证辅助类"""
    
    def __init__(self, oidc: OpenIDConnect):
        self.oidc = oidc
    
    def get_user_info(self, fields=None):
        """获取用户信息"""
        if fields is None:
            fields = ['sub', 'email', 'name', 'preferred_username']
        
        try:
            return self.oidc.user_getinfo(fields)
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return {}
    
    def get_user_roles(self):
        """获取用户角色"""
        user_info = self.get_user_info(['roles', 'realm_access', 'resource_access'])
        roles = []
        
        # 从不同位置提取角色信息
        if 'roles' in user_info:
            if isinstance(user_info['roles'], list):
                roles.extend(user_info['roles'])
            else:
                roles.append(user_info['roles'])
        
        # Keycloak格式的角色
        if 'realm_access' in user_info and 'roles' in user_info['realm_access']:
            roles.extend(user_info['realm_access']['roles'])
        
        return list(set(roles))  # 去重
    
    def has_role(self, required_role):
        """检查用户是否具有特定角色"""
        user_roles = self.get_user_roles()
        return required_role in user_roles
    
    def validate_token(self, token):
        """验证JWT token"""
        try:
            # 这里可以添加更复杂的token验证逻辑
            # 比如验证签名、过期时间等
            decoded = jwt.decode(token, options={"verify_signature": False})
            return decoded
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            return None

def require_auth(f):
    """认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            # 可以在这里添加Bearer token验证逻辑
            logger.info("Bearer token provided")
        
        # 检查OIDC session
        from flask import current_app
        oidc = current_app.extensions.get('oidc')
        
        if not oidc or not oidc.user_loggedin:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'OIDC authentication required',
                'code': 'AUTH_REQUIRED'
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function

def require_role(required_role):
    """角色授权装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import current_app
            oidc = current_app.extensions.get('oidc')
            
            if not oidc or not oidc.user_loggedin:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'OIDC authentication required',
                    'code': 'AUTH_REQUIRED'
                }), 401
            
            auth_helper = OIDCAuth(oidc)
            
            if not auth_helper.has_role(required_role):
                return jsonify({
                    'error': 'Forbidden',
                    'message': f'Role "{required_role}" required',
                    'code': 'INSUFFICIENT_PERMISSIONS',
                    'required_role': required_role,
                    'user_roles': auth_helper.get_user_roles()
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_any_role(*roles):
    """需要任意一个角色的装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import current_app
            oidc = current_app.extensions.get('oidc')
            
            if not oidc or not oidc.user_loggedin:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'OIDC authentication required',
                    'code': 'AUTH_REQUIRED'
                }), 401
            
            auth_helper = OIDCAuth(oidc)
            user_roles = auth_helper.get_user_roles()
            
            if not any(role in user_roles for role in roles):
                return jsonify({
                    'error': 'Forbidden',
                    'message': f'One of these roles required: {", ".join(roles)}',
                    'code': 'INSUFFICIENT_PERMISSIONS',
                    'required_roles': list(roles),
                    'user_roles': user_roles
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def optional_auth(f):
    """可选认证装饰器 - 如果有认证信息则验证，没有则继续"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import current_app, g
        oidc = current_app.extensions.get('oidc')
        
        g.user_authenticated = False
        g.user_info = None
        
        if oidc and oidc.user_loggedin:
            g.user_authenticated = True
            auth_helper = OIDCAuth(oidc)
            g.user_info = auth_helper.get_user_info()
        
        return f(*args, **kwargs)
    return decorated_function