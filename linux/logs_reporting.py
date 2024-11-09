import sys
import os
from email.message import EmailMessage
import smtplib
from email.utils import formataddr



# Allow import of modules from both Linux and Windows directories
sys.path.append('linux')


from linux.network_con import ping_test, dns_lookup, trace_route
from linux.speedtest import speed_test
from linux.network_interface import network_interfaces_info
from linux.wifianalysis import get_wireless_interface, get_iw_info, get_wifi_signal_strength, get_wifi_info
from linux.portscan import port_scan
from linux.security import NetworkSecurityCheck




class ReportManager:
    def __init__(self, filename="report.txt"):
        self.filename = filename
        self.content = []

    def append_to_report(self, text):
        """Appends given text to the report content list."""
        self.content.append(text + "\n")

    def save_report(self):
        """Saves the report content to a file on the device."""
        with open(self.filename, "w") as file:
            file.writelines(self.content)
        print(f"Report saved to {self.filename}")




        

    def email_report(self, recipient_email):
        """Emails the report file to the specified email."""
        sender_email = "MS_Pvh4Gm@trial-zr6ke4nn7v34on12.mlsender.net"
        smtp_server = "smtp.mailersend.net"
        smtp_port = 587  # TLS port
        smtp_user = "MS_Pvh4Gm@trial-zr6ke4nn7v34on12.mlsender.net"
        smtp_password = "u5NttfFgmP0TZl09"  # Replace with your App Password

        try:
            # Create the email message
            msg = EmailMessage()
            msg["Subject"] = "Network Analysis Report"
            msg["From"] = formataddr(("Report Manager", sender_email))
            msg["To"] = recipient_email
            msg.set_content("Please find the attached network analysis report.")

            # Attach the report file
            with open(self.filename, "rb") as file:
                file_data = file.read()
                file_name = os.path.basename(self.filename)
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

            # Connect to the SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Upgrade the connection to TLS
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
            print(f"Report sent successfully to {recipient_email}")
        except Exception as e:
            print(f"Error sending email: {e}")

    def save_and_email_report(self):
        """Saves the report to a file and optionally emails it."""
        self.save_report()
        recipient_email = input("Enter the recipient email address (or leave blank to skip): ").strip()
        
        if recipient_email:
            self.email_report(recipient_email)
        else:
            print("No email entered. Report saved locally.")

# Usage example

if __name__ == "__main__":
    report_manager = ReportManager()

    # Append content to the report
    report_manager.append_to_report("Ping Test: Success")
    report_manager.append_to_report("Speed Test: Download - 100 Mbps, Upload - 50 Mbps")
    report_manager.append_to_report("Network Interface: eth0, Status: Up")

    # Save and optionally email the report
    report_manager.save_and_email_report()

