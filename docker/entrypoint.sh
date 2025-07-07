#!/bin/sh

# Start Ollama in the background.
ollama serve &
# Record Process ID.
pid=$!

echo "⏳ Waiting for ollama-server to be ready..."
until curl --silent --fail http://ollama-server:11434; do
  sleep 2
done
echo "✅ ollama-server is up."

# Pause for Ollama to start.
sleep 5

# Check if model 'llama-AI' exists
if ollama list models | grep -q '^llama-AI$'; then
  echo "Model 'llama-AI' already exists, skipping creation."
else
  echo "Creating custom model 'llama-AI'..."
  ollama create llama-AI -f /app/Modelfile
  echo "🟢 Model creation done!"
fi

# Wait for Ollama process to finish.
wait $pid

echo "Starting Python script..."
python3 /app/test_ollama.py
exec "$@"

# Wait for Ollama to finish (optional, or just run command)
# echo "Starting user command..."
# exec "$@"
