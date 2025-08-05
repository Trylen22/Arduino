#!/usr/bin/env python3
"""
Clean IRIS Demo Runner
======================

Runs the IRIS demo with all verbose output suppressed.
"""

import os
import sys
import subprocess
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

def run_clean_demo():
    """Run the demo with all verbose output suppressed."""
    
    # Set environment variables to suppress output
    env = os.environ.copy()
    env['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    env['PYTHONWARNINGS'] = 'ignore'
    
    # Aggressively suppress ALSA and audio system messages
    env['ALSA_PCM_CARD'] = '0'
    env['ALSA_PCM_DEVICE'] = '0'
    env['ALSA_DEBUG'] = '0'
    env['ALSA_VERBOSE'] = '0'
    env['PULSE_VERBOSE'] = '0'
    env['JACK_VERBOSE'] = '0'
    
    # Suppress pygame messages
    env['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    
    # Suppress speech recognition messages
    env['SPEECH_RECOGNITION_VERBOSE'] = '0'
    
    print("IRIS Student Companion AI - Clean Demo")
    print("=" * 50)
    print("Starting demo with minimal output...")
    print("=" * 50)
    
    try:
        # Run the demo with complete output suppression
        with open(os.devnull, 'w') as devnull:
            result = subprocess.run([
                sys.executable, 'demo_student_companion.py'
            ], 
            env=env,
            stdout=sys.stdout,  # Keep demo output
            stderr=devnull,     # Suppress all error messages
            text=True
            )
        
    except KeyboardInterrupt:
        print("\nDemo stopped by user.")
    except Exception as e:
        print(f"Demo error: {e}")

def run_silent_test():
    """Run tests with all output suppressed."""
    
    # Set environment variables
    env = os.environ.copy()
    env['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    env['PYTHONWARNINGS'] = 'ignore'
    env['ALSA_DEBUG'] = '0'
    env['ALSA_VERBOSE'] = '0'
    env['PULSE_VERBOSE'] = '0'
    env['JACK_VERBOSE'] = '0'
    
    print("Running silent tests...")
    
    # Capture all output
    stdout_capture = StringIO()
    stderr_capture = StringIO()
    
    with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
        try:
            with open(os.devnull, 'w') as devnull:
                result = subprocess.run([
                    sys.executable, 'test_demo.py'
                ], 
                env=env,
                capture_output=True,
                stderr=devnull,
                text=True
                )
                
            if result.returncode == 0:
                print("All tests passed silently!")
                return True
            else:
                print("Tests failed. Check the demo files.")
                return False
                
        except Exception as e:
            print(f"Test error: {e}")
            return False

def run_ultra_clean_demo():
    """Run demo with ultra-clean output - only essential messages."""
    
    # Set environment variables
    env = os.environ.copy()
    env['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    env['PYTHONWARNINGS'] = 'ignore'
    env['ALSA_DEBUG'] = '0'
    env['ALSA_VERBOSE'] = '0'
    env['PULSE_VERBOSE'] = '0'
    env['JACK_VERBOSE'] = '0'
    env['SPEECH_RECOGNITION_VERBOSE'] = '0'
    
    print("IRIS Student Companion AI - Ultra Clean Demo")
    print("=" * 50)
    print("Starting demo with minimal output...")
    print("=" * 50)
    
    try:
        # Create a custom demo runner that suppresses everything
        demo_script = """
import os
import sys
import warnings

# Suppress all warnings and messages
warnings.filterwarnings("ignore")
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
os.environ['ALSA_DEBUG'] = '0'
os.environ['ALSA_VERBOSE'] = '0'

# Redirect stderr to suppress all error messages
import contextlib
import io

# Suppress all output except what we want
original_stderr = sys.stderr
sys.stderr = io.StringIO()

try:
    # Import and run demo
    from demo_student_companion import IRISDemo
    demo = IRISDemo()
    demo.run_main_demo()
finally:
    # Restore stderr
    sys.stderr = original_stderr
"""
        
        # Write temporary script
        with open('temp_clean_demo.py', 'w') as f:
            f.write(demo_script)
        
        # Run the clean script
        with open(os.devnull, 'w') as devnull:
            result = subprocess.run([
                sys.executable, 'temp_clean_demo.py'
            ], 
            env=env,
            stdout=sys.stdout,
            stderr=devnull,
            text=True
            )
        
        # Clean up
        if os.path.exists('temp_clean_demo.py'):
            os.remove('temp_clean_demo.py')
            
    except KeyboardInterrupt:
        print("\nDemo stopped by user.")
    except Exception as e:
        print(f"Demo error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            run_silent_test()
        elif sys.argv[1] == "ultra":
            run_ultra_clean_demo()
        else:
            run_clean_demo()
    else:
        run_clean_demo() 