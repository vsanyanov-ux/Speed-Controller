import os
import time
import json
import tiktoken
from gigachat import GigaChat
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize GigaChat client
# GIGACHAT_CREDENTIALS must be in .env
credentials = os.environ.get("GIGACHAT_CREDENTIALS")

# verify_ssl_certs=False is often needed for GigaChat in certain environments
client = GigaChat(credentials=credentials, verify_ssl_certs=False)

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Counts tokens in a string using tiktoken."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def summarize_text(text: str, model: str = "GigaChat"):
    """
    Summarizes text if token count > 200 using Sber GigaChat.
    Returns summary and metadata.
    """
    start_time = time.time()
    
    tokens = count_tokens(text)
    
    if tokens <= 200:
        return text, {
            "token_count": tokens,
            "processing_time_ms": (time.time() - start_time) * 1000,
            "status": "skipped (too short)"
        }

    # GigaChat request
    start_api_time = time.time()
    try:
        # Context management with 'with' ensures connection is closed
        with client as giga:
            response = giga.chat({
                "model": model,
                "messages": [
                    {"role": "system", "content": "Summarize the following text concisely. Respond ONLY with the summary."},
                    {"role": "user", "content": text}
                ],
                "temperature": 0.5
            })
            end_api_time = time.time()
            
            summary = response.choices[0].message.content
            total_time_ms = (time.time() - start_time) * 1000
            
            metadata = {
                "token_count": tokens,
                "api_latency_ms": (end_api_time - start_api_time) * 1000,
                "total_processing_time_ms": total_time_ms,
                "model": model,
                "provider": "GigaChat"
            }
            
            return summary, metadata
    except Exception as e:
        raise Exception(f"GigaChat error: {e}. Check if GIGACHAT_CREDENTIALS in .env is correct.")

if __name__ == "__main__":
    # Sample long text (> 500 words to ensure > 200 tokens)
    sample_text = """
    Artificial Intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals and humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.
    
    The term "artificial intelligence" had previously been used to describe machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving". This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.
    
    AI applications include advanced web search engines (e.g., Google Search), recommendation systems (used by YouTube, Amazon, and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Waymo), generative or creative tools (ChatGPT and AI art), and competing at the highest level in strategic games (such as chess and Go).
    
    Artificial intelligence was founded as an academic discipline in 1956, and in the years since has experienced several waves of optimism, followed by disappointment and the loss of funding (known as an "AI winter"), followed by new approaches, success and renewed funding. AI research has tried and discarded many different approaches since its founding, including simulating the brain, modeling human problem solving, formal logic, large databases of knowledge and imitating animal behavior. In the first decades of the 21st century, highly mathematical-statistical machine learning has dominated the field, and this technique has proved highly successful, helping to solve many challenging problems throughout industry and academia.
    
    The various sub-fields of AI research are centered around particular goals and the use of particular tools. The traditional goals of AI research include reasoning, knowledge representation, planning, learning, natural language processing, perception, and the ability to move and manipulate objects. General intelligence (the ability to solve an arbitrary problem) is among the field's long-term goals. To solve these problems, AI researchers have adapted and integrated a wide range of problem-solving techniques, including search and mathematical optimization, formal logic, artificial neural networks, and methods based on statistics, probability and economics. AI also draws upon computer science, psychology, linguistics, philosophy, and many other fields.
    """ * 3 # Multiple times to ensure it's long enough

    try:
        summary, meta = summarize_text(sample_text)
        print("Summary:", summary)
        print("\nMetadata:", json.dumps(meta, indent=4))
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Please ensure GROQ_API_KEY environment variable is set.")
