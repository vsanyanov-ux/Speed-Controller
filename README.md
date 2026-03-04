# 🚀 Speed Controller: Smart LLM Routing & Summarization

A lightweight Python utility designed to optimize LLM usage by implementing smart request routing based on token counts. It uses `tiktoken` for accurate measurement and **Sber GigaChat** for high-speed summarization.

## 🌟 Key Features

- **Smart Routing**: Only sends text to the LLM if it exceeds a 200-token threshold, saving costs and reducing latency.
- **Accurate Token Counting**: Leverages OpenAI's `tiktoken` library for precise measurement.
- **High Performance**: Optimized for low-latency responses using Sber GigaChat (ideal for users in Russia).
- **Latency Tracking**: Detailed metadata reporting, including API latency and total processing time.
- **Ready for Production**: Organized with a virtual environment, environment variables, and `.gitignore`.

## 🛠 Tech Stack

- **Python 3.10+**
- **GigaChat SDK**: For powerful LLM inference.
- **Tiktoken**: For fast BPE tokenization.
- **Python-dotenv**: For secure configuration management.

## 🚀 Getting Started

### 1. Prerequisites
- Python installed on your system.
- GigaChat API credentials (get them at [developers.sber.ru](https://developers.sber.ru/portal/products/gigachat)).

### 2. Installation
Clone the repository and set up the environment:
```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install gigachat tiktoken python-dotenv
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
GIGACHAT_CREDENTIALS=your_auth_key_here
```

### 4. Usage
Run the script to see it in action:
```bash
python speed_controller.py
```

## 📊 Performance Example

```json
{
    "token_count": 1438,
    "api_latency_ms": 1175.13,
    "total_processing_time_ms": 1295.10,
    "model": "GigaChat",
    "provider": "GigaChat"
}
```

## 📜 License
This project is open-source and available under the MIT License.
