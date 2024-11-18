import os
from email.message import EmailMessage
import smtplib
from email.utils import formataddr
import tkinter as tk
import sys
import customtkinter as ctk
from tkinter import Text, simpledialog, messagebox


sys.path.append('linux')
sys.path.append('windows')

if sys.platform == 'linux':
    from linux.network_con import ping_test, dns_lookup, trace_route
    from linux.speedtest import get_server, get_downspeed, get_upspeed, get_ping, get_jitter
    from linux.network_interface import network_interfaces_info
    from linux.wifianalysis import get_iw_info, get_wifi_signal_strength, get_wifi_info
    from linux.portscan import port_scan
    from linux.security import NetworkSecurityCheck
    from linux.logs_reporting import ReportManager
elif sys.platform == 'win32':
    from windows.network_con import ping_test, dns_lookup, trace_route
    from windows.speedtest import speed_test
    from windows.network_interface import network_interfaces_info
    from windows.wifianalysis import get_wireless_interface, get_iw_info, get_wifi_signal_strength, get_wifi_info
    from windows.portscan import port_scan
    from windows.security import NetworkSecurityCheck
    from windows.logs_reporting import ReportManager

class NetworkDiagnoseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NetDiagnose")
        self.geometry("1300x900")
       

        self.report_manager = ReportManager() 

        self.configure_grid()
        self.create_widgets()

    def configure_grid(self):
        self.columnconfigure(0, weight=0)  
        self.columnconfigure(1, weight=1)  
        self.columnconfigure(2, weight=0)  
        self.rowconfigure(0, weight=1)

    def create_widgets(self):

        button_frame = ctk.CTkFrame(self, width=200)
        button_frame.grid(row=0, column=0, sticky="ns")

        self.output_text = Text(self, wrap="word", width=50, height=30, font=("Futura", 14), bg="#2B2B2B", fg="white", bd=0, padx=10, pady=10, state=tk.DISABLED)
        self.output_text.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        system_info_frame = ctk.CTkFrame(self, width=700, fg_color="#2B2B2B")
        system_info_frame.grid(row=0, column=2, sticky="ns", padx=5, pady=5)

 
        self.system_info_label = ctk.CTkLabel(system_info_frame, text="System Information", font=("Futura", 14, "bold"))
        self.system_info_label.pack(pady=5)

   
        self.system_info_text = Text(system_info_frame, wrap="word", width=30, height=30, font=("Futura", 14), bg="#2B2B2B", fg="white", bd=0, state=tk.DISABLED)
        self.system_info_text.pack(padx=5, pady=5)
        self.display_system_info()
        self.display_welcome_message()
    
        buttons = [
            ("Network Information", self.network_information),
            ("Speed Test", self.run_speed_test),
            ("Wi-Fi Analysis", self.wifi_analysis),
            ("Port Scan", self.run_port_scan),
            ("Security Check", self.security_check),
            ("Log Report", self.log_save_email)
        ]

        for i, (name, command) in enumerate(buttons):
            button = ctk.CTkButton(button_frame, text=name, command=command, width=180, height=35)
            button.grid(row=i, column=0, padx=10, pady=5, sticky="ew")

        exit_button = ctk.CTkButton(button_frame, text="Exit", command=self.quit, width=180, height=35)
        exit_button.grid(row=len(buttons) + 1, column=0, padx=10, pady=10, sticky="ew")

    def display_system_info(self):
        self.system_info_text.config(state=tk.NORMAL)
        network = network_interfaces_info()
        interface = network[0]
        address = network[1]

        for info in interface:
            self.system_info_text.insert(tk.END, f"{info}")

        for addr in address:
            self.system_info_text.insert(tk.END, f"{addr}")
        self.system_info_text.config(state=tk.DISABLED)

    def append_to_output(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.report_manager.append_to_report(text) 
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    #functions
    def network_information(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        ip = self.custom_prompt_input("Enter IP (default: 8.8.8.8):", "8.8.8.8")
        dns = self.custom_prompt_input("Enter DNS (default: www.google.com):", "www.google.com")
        route = self.custom_prompt_input("Enter Route (default: 8.8.8.8):", "8.8.8.8")

        self.append_to_output(" Running Network Information Tests...")
        self.output_text.update_idletasks() 

        self.append_to_output(f" Ping Test: {ping_test(ip)}")
        self.output_text.update_idletasks()
        self.append_to_output(f" DNS Lookup for {dns}")
        self.append_to_output(f" DNS Lookup: {dns_lookup(dns)}")
        self.output_text.update_idletasks()
        self.append_to_output(f" Tracing Route to {route}\n")
        self.append_to_output(f" Trace Route: {trace_route(route)}")    
        self.output_text.config(state=tk.DISABLED)
       
    def run_speed_test(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.append_to_output(" Getting Server Info")
        self.output_text.update_idletasks()
        server = get_server()
        if type(server) == 'String':
            self.append_to_output(f" Server: {server}")
        else:
            self.append_to_output(f" Server:{server['sponsor']}, Location: {server['name']} in {server['country']}")

        self.append_to_output(" Running Speed Test...")
        self.output_text.update_idletasks()
        self.append_to_output(f" Calculating download speed")
        self.output_text.update_idletasks()
        download = get_downspeed()
        self.append_to_output(f" Download Speed {download: .2f} mbps \n")
        self.output_text.update_idletasks()
        self.append_to_output(f" Calculating Upload speed\n")
        self.output_text.update_idletasks()
        upload = get_upspeed()
        self.append_to_output(f" Upload Speed {upload: .2f} mbps \n")
        self.output_text.update_idletasks()
        self.append_to_output(f" Calculating Ping and Jitter speed\n")
        self.output_text.update_idletasks()
        ping = get_ping()
        self.append_to_output(f" Ping {ping: .2f} ms ")
        self.output_text.update_idletasks()
        jitter = get_jitter()
        self.append_to_output(f" Calculating Jitter")
        self.output_text.update_idletasks()
        self.append_to_output(f" Jitter {jitter} ms")
        self.output_text.config(state=tk.DISABLED)

    def wifi_analysis(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.append_to_output(" Running Wi-Fi Analysis...")
        self.output_text.update_idletasks()
        self.append_to_output(f" Signal Strength: {get_wifi_signal_strength()} \n")
        self.output_text.update_idletasks()
        self.append_to_output(f" Interface Info: {get_iw_info()}")
        self.output_text.update_idletasks()
        netchan = get_wifi_info()
        networks = netchan[0]
        channels = netchan[1]
        self.append_to_output(f"\n Networks: ")
        for n in networks:
              self.append_to_output(f"{n}")
        self.output_text.update_idletasks()
        self.append_to_output("\n\n Channels info:")
        for c in channels:
            self.append_to_output(f"{c}")
        self.output_text.config(state=tk.DISABLED)
   
    def run_port_scan(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.append_to_output(" Running Port Scan...")
        self.output_text.update_idletasks()
       
        ports = port_scan()
        used = ports[0]
        free = ports[1]
        self.append_to_output(f" Used Ports: ")
        for u in used:
            self.append_to_output(f" {u}")
        self.append_to_output(f" \n\n Free ports:")
        for f in free:
            self.append_to_output(f" {f}")
        self.output_text.config(state=tk.DISABLED)

    def security_check(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        target_ip = self.custom_prompt_input(" Enter Target IP (default: 8.8.8.8):", "8.8.8.8")
        port = int(self.custom_prompt_input(" Enter Port (default: 300):", "300"))
        hostname = self.custom_prompt_input(" Enter Hostname (default: www.google.com):", "www.google.com")

        self.append_to_output(" Running Security Check...")
        self.append_to_output(f" Nmap Scan: {NetworkSecurityCheck.nmap_scan(target_ip)}\n")
        self.output_text.update_idletasks()
        self.append_to_output(f" Firewall Detection: {NetworkSecurityCheck.firewall_detection(target_ip, port)}n")
        self.output_text.update_idletasks()
        self.append_to_output(f"Inspeacting SSL/TLS...")
        self.output_text.update_idletasks()
        self.append_to_output(f" SSL/TLS Inspection:\n")
        ssl_tls = NetworkSecurityCheck.ssl_tls_inspection(hostname, port, target_ip)
        for key, value in ssl_tls.items():
            self.append_to_output(f"{key}: {value}")
        self.output_text.config(state=tk.DISABLED)

    def log_save_email(self):

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.append_to_output("Saving Logs..")
        self.report_manager.save_report()
        choice = messagebox.askyesno("Run Full Report", "Do you want to email the report? (Click 'No' to save locally)")
        if choice:
            recipient_email = self.custom_prompt_input("Email Report", "Enter recipient email:")
            if recipient_email:
                self.report_manager.email_report(recipient_email)
                
                self.append_to_output(f"Email sent succesfully to {recipient_email}")

        self.append_to_output(f"Report saved locally")       
        self.output_text.config(state=tk.DISABLED)

    def custom_prompt_input(self, message, default):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Input")

        main_window_width = self.winfo_width()
        main_window_height = self.winfo_height()
        dialog_width = 300
        dialog_height = 150


        x_position = self.winfo_x() + (main_window_width // 2) - (dialog_width // 2)
        y_position = self.winfo_y() + (main_window_height // 2) - (dialog_height // 2)


        dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
    
   
        label = ctk.CTkLabel(dialog, text=message)
        label.pack(pady=10)
     
        entry = ctk.CTkEntry(dialog, width=250)
        entry.pack(pady=5)
        entry.insert(0, default)
    
        def on_ok():
            dialog.user_input = entry.get()
            dialog.destroy()
    
        ok_button = ctk.CTkButton(dialog, text="OK", command=on_ok)
        ok_button.pack(pady=10)
    
        dialog.user_input = default
        dialog.wait_window()
        return dialog.user_input
    
    def display_welcome_message(self):
        message = """
        Welcome to NetDiagnose!

        NetDiagnose is a comprehensive network diagnostic assistant designed to help you troubleshoot and understand your network connections. This application provides a variety of tools and tests to diagnose network issues, including:

        1. Network Information: Retrieve detailed information about your network interfaces, including IP addresses, MAC addresses, and interface status.
        2. Speed Test: Measure your internet connection's download and upload speeds, as well as ping and jitter values, to assess the performance of your network.
        3. Wi-Fi Analysis: Analyze your Wi-Fi signal strength, interface information, and available networks to optimize your wireless connection.
        4. Port Scan: Scan for open and closed ports on your network to identify potential security vulnerabilities.
        5. Security Check: Perform security checks, including Nmap scans and firewall detection, to ensure your network is secure.
        6. Full Report: Generate a comprehensive report of all diagnostic tests, which can be saved locally or emailed for further analysis.

        To get started, simply select one of the diagnostic options from the menu. Each test will provide detailed results and insights to help you diagnose and resolve network issues.

        Thank you for using NetDiagnose!
        """
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message)
        self.output_text.config(state=tk.DISABLED)

def main():
    app = NetworkDiagnoseApp()
    app.mainloop()    
    
if __name__ == "__main__":
    main()
