#!/bin/bash

# Test script to check billing and API access status

echo "=== Google Cloud Billing Status Test ==="

if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Please set GEMINI_API_KEY first"
    exit 1
fi

BASE_URL="https://generativelanguage.googleapis.com/v1beta"

echo "Testing different Gemini models to identify billing issues..."
echo ""

# Test 1: Try a simple text model (usually free)
echo "1. Testing Gemini Pro (text) - usually has free quota:"
response1=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
  "${BASE_URL}/models/gemini-pro:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}')

status1=$(echo "$response1" | tail -n1 | sed 's/HTTP_STATUS://')
body1=$(echo "$response1" | sed '$d')

if [ "$status1" = "200" ]; then
    echo "✅ Gemini Pro works - Basic API access OK"
elif [ "$status1" = "429" ]; then
    echo "❌ Gemini Pro quota exceeded"
    echo "Response: $body1"
else
    echo "❌ Gemini Pro failed (HTTP $status1)"
    echo "Response: $body1"
fi

echo ""

# Test 2: Try VEO model (requires billing)
echo "2. Testing Gemini VEO (video) - requires billing:"
response2=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
  "${BASE_URL}/models/veo-3.0-generate-preview:predictLongRunning" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"instances":[{"prompt":"test"}]}')

status2=$(echo "$response2" | tail -n1 | sed 's/HTTP_STATUS://')
body2=$(echo "$response2" | sed '$d')

if [ "$status2" = "200" ]; then
    echo "✅ VEO model works - Billing is properly configured"
elif [ "$status2" = "429" ]; then
    echo "❌ VEO model quota/billing issue"
    error_msg=$(echo "$body2" | jq -r '.error.message // "Unknown error"')
    echo "Error: $error_msg"
    
    if echo "$error_msg" | grep -qi "billing\|quota\|plan"; then
        echo ""
        echo "💡 This is a billing/quota issue. You need to:"
        echo "   1. Set up Google Cloud billing account"
        echo "   2. Enable paid API access"
        echo "   3. VEO might require enterprise/premium access"
    fi
else
    echo "❌ VEO model failed (HTTP $status2)"
    echo "Response: $body2"
fi

echo ""

# Test 3: List available models
echo "3. Checking available models:"
models_response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
  "${BASE_URL}/models" \
  -H "x-goog-api-key: $GEMINI_API_KEY")

models_status=$(echo "$models_response" | tail -n1 | sed 's/HTTP_STATUS://')
models_body=$(echo "$models_response" | sed '$d')

if [ "$models_status" = "200" ]; then
    echo "✅ Can list models"
    # Check if VEO models are available
    if echo "$models_body" | jq -r '.models[].name' | grep -q "veo"; then
        echo "✅ VEO models are visible in your account"
    else
        echo "❌ VEO models not available in your account"
        echo "   This might indicate insufficient permissions or billing tier"
    fi
else
    echo "❌ Cannot list models (HTTP $models_status)"
fi

echo ""
echo "=== Recommendations ==="

if [ "$status1" = "200" ] && [ "$status2" = "429" ]; then
    echo "🎯 Diagnosis: Basic API works, but VEO requires billing setup"
    echo ""
    echo "📋 Action Items:"
    echo "   1. Go to: https://console.cloud.google.com/billing"
    echo "   2. Create or link a billing account"
    echo "   3. Enable billing for your project"
    echo "   4. Check VEO pricing at: https://ai.google.dev/pricing"
    echo "   5. VEO might be in limited preview - check access requirements"
elif [ "$status1" = "429" ]; then
    echo "🎯 Diagnosis: General API quota/billing issue"
    echo ""
    echo "📋 Action Items:"
    echo "   1. Set up Google Cloud billing"
    echo "   2. Wait for quota reset (if using free tier)"
    echo "   3. Upgrade to paid plan"
else
    echo "🎯 Further investigation needed"
fi

echo ""
echo "=== Useful Links ==="
echo "• Google Cloud Billing: https://console.cloud.google.com/billing"
echo "• Gemini API Pricing: https://ai.google.dev/pricing"
echo "• API Quotas: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas"
echo "• VEO Documentation: https://ai.google.dev/gemini-api/docs/video-generation"