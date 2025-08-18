#!/bin/bash

# Google Gemini API Video Generation Script
# Note: This script uses jq to parse the JSON response.

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY environment variable is not set."
    echo "Please set it with: export GEMINI_API_KEY='your_api_key_here'"
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install it first."
    echo "On Ubuntu/Debian: sudo apt-get install jq"
    echo "On macOS: brew install jq"
    exit 1
fi

# GEMINI API Base URL
BASE_URL="https://generativelanguage.googleapis.com/v1beta"

echo "Starting video generation with Gemini VEO-3.0..."
echo "Prompt: A close up of two people staring at a cryptic drawing on a wall, torchlight flickering..."

# Send request to generate video and capture the operation name into a variable.
echo "Sending generation request..."
operation_name=$(curl -s "${BASE_URL}/models/veo-3.0-generate-preview:predictLongRunning" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -X "POST" \
  -d '{
    "instances": [{
        "prompt": "A close up of two people staring at a cryptic drawing on a wall, torchlight flickering. A man murmurs, \"This must be it. That'\''s the secret code.\" The woman looks at him and whispering excitedly, \"What did you find?\""
      }
    ]
  }' | jq -r .name)

if [ -z "$operation_name" ] || [ "$operation_name" = "null" ]; then
    echo "Error: Failed to get operation name. Please check your API key and try again."
    exit 1
fi

echo "Operation started: $operation_name"
echo "Polling for completion..."

# Poll the operation status until the video is ready
poll_count=0
while true; do
  poll_count=$((poll_count + 1))
  echo "Poll attempt #$poll_count..."
  
  # Get the full JSON status and store it in a variable.
  status_response=$(curl -s -H "x-goog-api-key: $GEMINI_API_KEY" "${BASE_URL}/${operation_name}")

  # Check if the response is valid JSON
  if ! echo "${status_response}" | jq . > /dev/null 2>&1; then
    echo "Error: Invalid JSON response received"
    echo "Response: ${status_response}"
    exit 1
  fi

  # Check the "done" field from the JSON stored in the variable.
  is_done=$(echo "${status_response}" | jq .done)

  if [ "${is_done}" = "true" ]; then
    echo "Video generation completed!"
    
    # Check if there was an error
    error_message=$(echo "${status_response}" | jq -r '.error.message // empty')
    if [ -n "$error_message" ]; then
      echo "Error in generation: $error_message"
      exit 1
    fi
    
    # Extract the download URI from the final response.
    video_uri=$(echo "${status_response}" | jq -r '.response.generateVideoResponse.generatedSamples[0].video.uri // empty')
    
    if [ -z "$video_uri" ] || [ "$video_uri" = "null" ]; then
      echo "Error: Could not extract video URI from response"
      echo "Response: ${status_response}"
      exit 1
    fi
    
    echo "Downloading video from: ${video_uri}"

    # Download the video using the URI and API key and follow redirects.
    if curl -L -o dialogue_example.mp4 -H "x-goog-api-key: $GEMINI_API_KEY" "${video_uri}"; then
      echo "Video successfully downloaded as: dialogue_example.mp4"
      echo "File size: $(ls -lh dialogue_example.mp4 | awk '{print $5}')"
    else
      echo "Error: Failed to download video"
      exit 1
    fi
    break
  else
    echo "Generation in progress... waiting 10 seconds"
  fi
  
  # Wait for 10 seconds before checking again.
  sleep 10
  
  # Add a timeout after 30 minutes (180 polls)
  if [ $poll_count -gt 180 ]; then
    echo "Timeout: Video generation took too long (30+ minutes)"
    exit 1
  fi
done

echo "Script completed successfully!"