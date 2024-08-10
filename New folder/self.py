import subprocess
from scapy.all import ARP, Ether, srp, conf
import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import sys
import threading

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    # Re-run the script with administrator privileges
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def get_interface():
    # Get the network interface name
    result = subprocess.run("ipconfig | findstr /C:\"Ethernet adapter\"", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    interface_output = result.stdout.decode().strip()
    if not interface_output:
        raise RuntimeError("No suitable network interface found.")
    
    # Extract interface name
    lines = interface_output.splitlines()
    interface_name = None
    for line in lines:
        if "Ethernet adapter" in line:
            interface_name = line.split(':')[0].strip()
            break
    
    if not interface_name:
        raise RuntimeError("No suitable network interface found.")
    
    return interface_name

def scan_network():
    # Create ARP packet
    arp = ARP(pdst="192.168.1.0/24")
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

def refresh_device_list():
    refresh_button.config(state=tk.DISABLED)
    refresh_label.config(text="Refreshing...")
    thread = threading.Thread(target=refresh_device_list_thread)
    thread.start()

def refresh_device_list_thread():
    devices = scan_network()
    for i in tree.get_children():
        tree.delete(i)
    for device in devices:
        tree.insert('', 'end', values=(device['ip'], device['mac']))
    refresh_button.config(state=tk.NORMAL)
    refresh_label.config(text="")

def limit_bandwidth(ip):
    try:
        interface = get_interface()
        print(f"Interface detected: {interface}")
        # Shell commands to limit bandwidth
        command = f'netsh interface ipv4 set subinterface "{interface}" mtu=1300 store=persistent'
        print(f"Executing command: {command}")
        subprocess.run(command, shell=True, check=True)
        messagebox.showinfo("Success", f"Bandwidth limited for {ip}")
    except subprocess.CalledProcessError as e:
        print(f"CalledProcessError: {e}")
        messagebox.showerror("Error", f"Command failed: {e}")
    except RuntimeError as e:
        print(f"RuntimeError: {e}")
        messagebox.showerror("Error", str(e))
    except Exception as e:
        print(f"Unexpected error: {e}")
        messagebox.showerror("Error", f"Unexpected error: {e}")

def main():
    # Setting up the GUI
    global root, frame, tree, refresh_button, refresh_label
    root = tk.Tk()
    root.title("Network Monitor")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    tree = ttk.Treeview(frame, columns=('IP', 'MAC'), show='headings')
    tree.heading('IP', text='IP Address')
    tree.heading('MAC', text='MAC Address')
    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    refresh_button = ttk.Button(frame, text="Refresh", command=refresh_device_list)
    refresh_button.grid(row=1, column=0, sticky=tk.W)

    refresh_label = ttk.Label(frame, text="")
    refresh_label.grid(row=1, column=1, sticky=tk.W)

    limit_button = ttk.Button(frame, text="Limit Bandwidth", command=lambda: limit_bandwidth(tree.item(tree.selection())['values'][0]))
    limit_button.grid(row=2, column=0, sticky=tk.W)

    # Run the initial scan
    refresh_device_list()

    root.mainloop()

if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
    else:
        main()
