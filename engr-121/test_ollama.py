import subprocess
import time
import json

def test_ollama_timing(num_tests=5, test_prompts=None):
    """Test Ollama response times with multiple prompts"""
    if test_prompts is None:
        test_prompts = [
            "What is 2+2?",  # Simple baseline
            "Analyze this temperature: 18.5°C",  # Basic thermal
            """Analyze this thermal data:
            Temperature: 18.5°C
            Rate of Change: -0.2°C/min
            Status: Warning Low""",  # Complex thermal
        ]
    
    print("Testing Ollama connection and timing...")
    
    # First check if Ollama is running
    try:
        process = subprocess.Popen(
            ["ollama", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        output, error = process.communicate()
        print("\nAvailable models:")
        print(output)
        
        results = []
        
        # Test each prompt multiple times
        for prompt in test_prompts:
            print(f"\nTesting prompt: {prompt[:50]}...")
            prompt_results = []
            
            for i in range(num_tests):
                start_time = time.time()
                print(f"\nTest {i+1}/{num_tests}")
                
                process = subprocess.Popen(
                    ["ollama", "run", "mistral"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    bufsize=1
                )
                
                # Send prompt and time the first response
                print("Sending prompt...")
                first_response_time = None
                process.stdin.write(prompt)
                process.stdin.close()
                
                # Read response line by line
                response_lines = []
                while True:
                    line = process.stdout.readline()
                    if not line:
                        break
                    
                    current_time = time.time() - start_time
                    if not first_response_time:
                        first_response_time = current_time
                    
                    response_lines.append(line.strip())
                    print(f"Line received at {current_time:.2f}s: {line[:50]}...")
                
                total_time = time.time() - start_time
                
                result = {
                    'prompt_length': len(prompt),
                    'first_response': first_response_time,
                    'total_time': total_time,
                    'num_lines': len(response_lines),
                    'avg_time_per_line': total_time / len(response_lines) if response_lines else 0
                }
                prompt_results.append(result)
                
                print(f"\nResponse Statistics:")
                print(f"First response: {first_response_time:.2f}s")
                print(f"Total time: {total_time:.2f}s")
                print(f"Lines generated: {len(response_lines)}")
                print(f"Average time per line: {result['avg_time_per_line']:.2f}s")
            
            # Calculate averages for this prompt
            avg_result = {
                'prompt': prompt[:50] + "...",
                'avg_first_response': sum(r['first_response'] for r in prompt_results) / num_tests,
                'avg_total_time': sum(r['total_time'] for r in prompt_results) / num_tests,
                'avg_lines': sum(r['num_lines'] for r in prompt_results) / num_tests,
                'min_time': min(r['total_time'] for r in prompt_results),
                'max_time': max(r['total_time'] for r in prompt_results)
            }
            results.append(avg_result)
            
            print(f"\nPrompt Summary:")
            print(f"Average first response: {avg_result['avg_first_response']:.2f}s")
            print(f"Average total time: {avg_result['avg_total_time']:.2f}s")
            print(f"Time range: {avg_result['min_time']:.2f}s - {avg_result['max_time']:.2f}s")
        
        # Save results
        with open('ollama_timing_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("\nTiming test complete! Results saved to ollama_timing_results.json")
        return results
        
    except Exception as e:
        print(f"Ollama test failed: {e}")
        return None

if __name__ == "__main__":
    test_ollama_timing() 