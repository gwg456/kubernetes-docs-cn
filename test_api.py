#!/usr/bin/env python3
"""
Flask OIDC API 测试脚本
使用方法：python test_api.py
"""

import requests
import json
import sys

# API基础URL
BASE_URL = "http://localhost:5000"

def test_public_endpoint():
    """测试公开端点"""
    print("=== 测试公开端点 ===")
    try:
        response = requests.get(f"{BASE_URL}/api/public")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_protected_endpoint_without_auth():
    """测试受保护端点（无认证）"""
    print("\n=== 测试受保护端点（无认证） ===")
    try:
        response = requests.get(f"{BASE_URL}/api/protected")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 401
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_health_check():
    """测试健康检查端点"""
    print("\n=== 测试健康检查 ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_root_endpoint():
    """测试根端点"""
    print("\n=== 测试根端点 ===")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_with_bearer_token(token):
    """使用Bearer token测试受保护端点"""
    print(f"\n=== 使用Bearer Token测试 ===")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/protected", headers=headers)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code in [200, 401]  # 可能成功或失败，取决于token有效性
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_create_user():
    """测试创建用户（需要认证）"""
    print(f"\n=== 测试创建用户（无认证） ===")
    user_data = {
        "name": "Test User",
        "email": "test@example.com"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/users", 
            json=user_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 401  # 应该返回401未授权
    except Exception as e:
        print(f"错误: {e}")
        return False

def run_tests():
    """运行所有测试"""
    print("开始测试 Flask OIDC API...")
    print(f"API地址: {BASE_URL}")
    
    tests = [
        ("根端点", test_root_endpoint),
        ("健康检查", test_health_check),
        ("公开端点", test_public_endpoint),
        ("受保护端点（无认证）", test_protected_endpoint_without_auth),
        ("创建用户（无认证）", test_create_user),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"✅ {test_name}: {'通过' if result else '失败'}")
        except Exception as e:
            results.append((test_name, False))
            print(f"❌ {test_name}: 异常 - {e}")
    
    # 测试Bearer token（如果提供）
    if len(sys.argv) > 1:
        token = sys.argv[1]
        try:
            result = test_with_bearer_token(token)
            results.append(("Bearer Token测试", result))
            print(f"✅ Bearer Token测试: {'通过' if result else '失败'}")
        except Exception as e:
            results.append(("Bearer Token测试", False))
            print(f"❌ Bearer Token测试: 异常 - {e}")
    
    # 总结
    print("\n" + "="*50)
    print("测试总结:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    return passed == total

if __name__ == "__main__":
    print("Flask OIDC API 测试工具")
    print("使用方法:")
    print("  python test_api.py                    # 基础测试")
    print("  python test_api.py <bearer-token>     # 包含Bearer token测试")
    print()
    
    success = run_tests()
    sys.exit(0 if success else 1)