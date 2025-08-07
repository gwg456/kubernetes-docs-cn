import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # OIDC配置
    OIDC_CLIENT_SECRETS = 'client_secrets.json'
    OIDC_ID_TOKEN_COOKIE_SECURE = os.environ.get('OIDC_ID_TOKEN_COOKIE_SECURE', 'False').lower() == 'true'
    OIDC_REQUIRE_VERIFIED_EMAIL = os.environ.get('OIDC_REQUIRE_VERIFIED_EMAIL', 'False').lower() == 'true'
    OIDC_OPENID_REALM = os.environ.get('OIDC_OPENID_REALM', 'flask-oidc-api')
    OIDC_SCOPES = ['openid', 'email', 'profile']
    OIDC_INTROSPECTION_AUTH_METHOD = 'client_secret_post'
    
    # 服务器配置
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    OIDC_ID_TOKEN_COOKIE_SECURE = False

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    OIDC_ID_TOKEN_COOKIE_SECURE = True

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = True
    OIDC_ID_TOKEN_COOKIE_SECURE = False

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}