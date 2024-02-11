import time
import threading
import subprocess
from pynput import keyboard

def lock_system():
    script = """
    tell application "System Events"
        sleep
    end tell
    """
    subprocess.run(['osascript', '-e', script])
    print("System sleeping")

def on_press(key):
    global key_queue
    key_queue.append(time.time())
    if len(key_queue) >= 10:
        if key_queue[-1] - key_queue[0] < 1:
            print("Possible keystroke injection detected!")
            threading.Thread(target=lock_system).start()
        key_queue.pop(0)

def on_release(key):
    pass

def main():
    global key_queue
    key_queue = []
    with keyboard.Listener(on_press=on_press,
                           on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
