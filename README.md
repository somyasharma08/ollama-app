
# Ollama LLaMA3 Custom Model with Docker

---

## Overview

This repository contains a Docker-based setup for running a custom LLaMA3 model using Ollama. The model is designed to respond only to mathematical queries and the keyword "ping", providing controlled and focused interactions.

---

## How to Set Up and Run

### Prerequisites

- Docker and Docker Compose installed on your system  
- Internet connection for initial image downloads and model setup

### Running Directly (without Docker)

1. Install Python 3.11+ and required dependencies.  
2. Ensure the `ollama` binary is installed and accessible.  
3. Run your Python script, e.g.:

   ```bash
   python3 /path/to/test_ollama.py
   ```

### Running via Docker

1. Build and start containers in the background with:

   ```bash
   docker compose up --build -d --remove-orphans
   ```

2. Access the running `llama-app` container and run the Python script interactively:

   ```bash
   docker compose exec -it llama-app python3 /app/test_ollama.py
   ```

3. You should see the bot responding to math queries and "ping" commands in interactive mode.

---

## System Prompt Design

The `Modelfile` defines the system prompt that strictly controls the bot’s behavior:

```text
You must follow these rules exactly:

1. If the user input is exactly "ping", "Ping", "PING", or any variation of "ping" regardless of casing, reply only with: pong!!!

2. If the user asks a math-related question (e.g., arithmetic, geometry, algebra, trigonometry), answer it clearly and directly. You may show steps if relevant.

3. For any other input, respond only with: I am designed to only answer mathematical questions or respond to 'ping'.

Be brief and strictly follow the above rules. Do not respond with explanations, greetings, or extra information.
```

### Reasoning Behind This Design

The design of the SYSTEM prompt in the Modelfile follows a strict rule-based approach to ensure controlled and predictable model behavior. The core goals were:

- **Purpose-Specific Interaction**  
  The assistant is designed to only respond to mathematical questions or to the keyword "ping" in any casing. This restriction helps keep the model focused and prevents off-topic or hallucinated responses.

- **Rule Enforcement**  
  The prompt explicitly defines three hard rules:  
  - Rule 1 ensures any variation of the word "ping" receives a consistent response: `pong!!!`.  
  - Rule 2 allows handling of a wide range of math-related queries — arithmetic, algebra, geometry, etc. — with optional step-by-step breakdowns.  
  - Rule 3 makes the model reject all unrelated input gracefully, responding with:  
    *I am designed to only answer mathematical questions or respond to 'ping'.*

- **Simplicity and Brevity**  
  The system prompt includes instructions like:  
  *Be brief and strictly follow the above rules.*  
  This avoids unnecessary elaboration, greetings, or informal dialogue, helping the assistant stay concise and reliable.

---

## Other Modelfile Configurations

- **Base Model:**  
  ```dockerfile
  FROM llama3.1:8b
  ```  
  This sets the foundation using the 8B parameter version of LLaMA 3. It provides a balance between performance and resource usage.

- **Model Parameters:**  
  ```dockerfile
  PARAMETER temperature 0.2
  PARAMETER top_k 10
  ```  
  - `temperature: 0.2` keeps responses deterministic and focused, avoiding creative or speculative replies — ideal for math and logic tasks.  
  - `top_k: 10` restricts the model to selecting from the top 10 probable next tokens, helping reduce randomness further and increasing consistency.

---

## 🧱 Challenges Faced & How They Were Addressed

### 1. Isolating the app and Ollama server into two services

**Problem**: Everything was initially bundled in one container, limiting flexibility.

**Solution**: Introduced `ollama-server` and `llama-app` as two separate services in Docker Compose. This separation improves modularity, rebuild speed, and debugging.

---

### 2. Race condition: Ollama not ready before use

**Problem**: Model creation or API requests failed because `ollama serve` wasn't fully initialized.

**Solution**: Added `sleep 5` in the entrypoint to delay requests until the service is ready.

---

### 3. Interactive mode issues with Docker

**Problem**: Using `docker compose run` didn't fully support terminal I/O.

**Solution**: Switched to `docker compose exec -it` to enter the running container's shell with full interactivity.

### 4: Ollama binary path not found

- **Problem:**  
  Initially, the `ollama` binary was not found at `/bin/ollama` inside the container, causing errors.

- **Solution:**  
  Adjusted the entrypoint script to handle Ollama installation and paths correctly, ensuring the binary is accessible at runtime.

---

## 📁 File Structure

```
├── docker-compose.yml
├── Modelfile
├── test_ollama.py
├── docker
│   └── entrypoint.sh
└── README.md
```

---

## 🙋‍♀️ Questions or Contributions

If you encounter issues or want to improve the setup, feel free to submit a pull request or open an issue!



---

## Screenshots

### Interactive Mode Example

![Interactive session screenshot](./screenshots/interactive_mode.png)

### Docker Compose Setup

![Docker compose up running](./screenshots/docker_compose_up.png)

---

## Contact & Support

For questions or issues, please open an issue on this repository.

---

*This README was generated to document the custom LLaMA3 model setup using Ollama in Docker.*
