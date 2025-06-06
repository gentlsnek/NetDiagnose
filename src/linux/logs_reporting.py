import os
from email.message import EmailMessage
import smtplib
from email.utils import formataddr
from fpdf import FPDF

class ReportManager:
    def __init__(self, filename="network_diagnostic_report.pdf"):
        self.filename = filename
        self.content = []

    def append_to_report(self, text):
        """Appends given text to the report content list."""
        self.content.append(text)

    def save_report(self):
        if not self.content:
            print("Error: Report content is empty.")
            return

        # Create a PDF document
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add content to the PDF
        for line in self.content:
            pdf.multi_cell(0, 10, str(line))

        # Save the PDF to a file
        pdf.output(self.filename)
        print(f"Report saved as {self.filename}")

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

