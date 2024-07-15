import socket
import time

def send_value(value, host='localhost', port=56789):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(value.encode())
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        # Toggle the value between "true" and "false" every 5 seconds
        send_value("true")
        time.sleep(5)
        #send_value("false")
        #time.sleep(5)
