#!/bin/bash

# Debug script to check Gemini API issues
# This will help diagnose why operation_name is null

echo "=== Gemini API Debug Tool ==="

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY environment variable is not set."
    echo "Please set it with: export GEMINI_API_KEY='your_api_key_here'"
    exit 1
else
    echo "✅ GEMINI_API_KEY is set (length: ${#GEMINI_API_KEY} characters)"
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "❌ Error: jq is not installed."
    exit 1
else
    echo "✅ jq is installed: $(jq --version)"
fi

# Check if curl is installed
if ! command -v curl &> /dev/null; then
    echo "❌ Error: curl is not installed."
    exit 1
else
    echo "✅ curl is installed: $(curl --version | head -1)"
fi

echo ""
echo "=== Testing API Connection ==="

BASE_URL="https://generativelanguage.googleapis.com/v1beta"

# Test API connectivity with a simple request
echo "Testing API endpoint connectivity..."

# Make the actual request and capture both response and HTTP status
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
  "${BASE_URL}/models/veo-3.0-generate-preview:predictLongRunning" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -X "POST" \
  -d '{
    "instances": [{
        "prompt": "A simple test video"
      }
    ]
  }')

# Split response and HTTP status
http_body=$(echo "$response" | sed '$d')
http_status=$(echo "$response" | tail -n1 | sed 's/HTTP_STATUS://')

echo ""
echo "=== API Response Analysis ==="
echo "HTTP Status Code: $http_status"
echo ""
echo "Response Body:"
echo "$http_body"
echo ""

# Check HTTP status
case $http_status in
    200)
        echo "✅ HTTP 200: Request successful"
        ;;
    400)
        echo "❌ HTTP 400: Bad Request - Check your request format"
        ;;
    401)
        echo "❌ HTTP 401: Unauthorized - Check your API key"
        ;;
    403)
        echo "❌ HTTP 403: Forbidden - API key may not have required permissions"
        ;;
    404)
        echo "❌ HTTP 404: Not Found - Check the API endpoint URL"
        ;;
    429)
        echo "❌ HTTP 429: Too Many Requests - Rate limit exceeded"
        ;;
    500)
        echo "❌ HTTP 500: Internal Server Error - Try again later"
        ;;
    *)
        echo "❌ HTTP $http_status: Unexpected status code"
        ;;
esac

# Try to parse JSON and extract operation name
if echo "$http_body" | jq . > /dev/null 2>&1; then
    echo "✅ Response is valid JSON"
    
    operation_name=$(echo "$http_body" | jq -r '.name // "null"')
    echo "Operation name: $operation_name"
    
    if [ "$operation_name" = "null" ] || [ -z "$operation_name" ]; then
        echo "❌ Operation name is null or empty"
        
        # Check for error messages in the response
        error_message=$(echo "$http_body" | jq -r '.error.message // "No error message"')
        error_code=$(echo "$http_body" | jq -r '.error.code // "No error code"')
        
        echo "Error message: $error_message"
        echo "Error code: $error_code"
        
        # Check if it's a quota/billing issue
        if echo "$error_message" | grep -qi "quota\|billing\|limit"; then
            echo ""
            echo "💡 Possible Solutions:"
            echo "   - Check your Google Cloud billing account"
            echo "   - Verify API quota limits"
            echo "   - Ensure the Gemini API is enabled in your project"
        fi
        
        # Check if it's an authentication issue
        if echo "$error_message" | grep -qi "auth\|key\|credential"; then
            echo ""
            echo "💡 Possible Solutions:"
            echo "   - Verify your API key is correct"
            echo "   - Check if the API key has required permissions"
            echo "   - Ensure you're using the right project's API key"
        fi
        
    else
        echo "✅ Operation name successfully obtained: $operation_name"
    fi
else
    echo "❌ Response is not valid JSON"
    echo "Raw response: $http_body"
fi

echo ""
echo "=== Additional Checks ==="

# Check if the API endpoint exists
echo "Testing base API endpoint..."
base_response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
  "${BASE_URL}/models" \
  -H "x-goog-api-key: $GEMINI_API_KEY")

base_http_status=$(echo "$base_response" | tail -n1 | sed 's/HTTP_STATUS://')
echo "Base endpoint HTTP status: $base_http_status"

if [ "$base_http_status" = "200" ]; then
    echo "✅ Base API endpoint is accessible"
else
    echo "❌ Base API endpoint issue (HTTP $base_http_status)"
fi

echo ""
echo "=== Debug Complete ==="