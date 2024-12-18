import subprocess
import time

def test_ai():
    print("Testing AI connection...")
    
    # Simple test prompt
    prompt = """
    Temperature: 22.5°C
    Status: Normal
    
    Analyze this temperature reading and provide a brief assessment.
    Keep response under 50 words.
    """
    
    try:
        print("Starting Ollama process...")
        process = subprocess.Popen(
            ["ollama", "run", "mistral"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        print("Sending prompt...")
        process.stdin.write(prompt)
        process.stdin.close()
        
        print("\nReading response:")
        while True:
            line = process.stdout.readline()
            if not line:
                break
            print(f"Got: {line.strip()}")
            
        process.stdout.close()
        
        if process.wait() != 0:
            error = process.stderr.read()
            print(f"Error: {error}")
            
    except Exception as e:
        print(f"Test failed: {str(e)}")

if __name__ == "__main__":
    test_ai() 