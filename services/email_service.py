"""
Email Service for Weather GPT
Handles sending weather alerts and daily digests via email
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending email notifications"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@weathergpt.com')
    
    def send_weather_alert(self, to_email: str, location: str, weather_data: Dict, alerts: List[Dict]) -> bool:
        """
        Send severe weather alert email
        
        Args:
            to_email: Recipient email address
            location: Location name
            weather_data: Weather data from API
            alerts: List of detected alerts
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            subject = f"🚨 SEVERE WEATHER ALERT - {location}"
            
            # Build email body
            body = self._build_alert_email_body(location, weather_data, alerts)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            # Attach HTML and plain text versions
            msg.attach(MIMEText(body, 'html'))
            msg.attach(MIMEText(self._html_to_text(body), 'plain'))
            
            # Send email
            return self._send_email(msg)
            
        except Exception as e:
            logger.error(f"Failed to send weather alert email: {e}")
            return False
    
    def send_daily_digest(self, to_email: str, weather_summary: List[Dict], subscriber_name: str) -> bool:
        """
        Send daily weather digest email
        
        Args:
            to_email: Recipient email address
            weather_summary: List of weather summaries for subscribed locations
            subscriber_name: Name of the subscriber
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            subject = f"🌤️ Daily Weather Digest - {subscriber_name}"
            
            # Build email body
            body = self._build_digest_email_body(weather_summary, subscriber_name)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            # Attach HTML and plain text versions
            msg.attach(MIMEText(body, 'html'))
            msg.attach(MIMEText(self._html_to_text(body), 'plain'))
            
            # Send email
            return self._send_email(msg)
            
        except Exception as e:
            logger.error(f"Failed to send daily digest email: {e}")
            return False
    
    def send_test_email(self, to_email: str) -> bool:
        """Send a test email to verify email configuration"""
        try:
            subject = "✅ Weather GPT - Test Email"
            body = """
            <html>
            <body>
                <h2>Weather GPT Test Email</h2>
                <p>This is a test email to verify your email notification setup is working correctly.</p>
                <p>If you received this email, your email service is configured properly!</p>
                <hr>
                <p><em>Weather GPT Notification Service</em></p>
            </body>
            </html>
            """
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            msg.attach(MIMEText(body, 'html'))
            msg.attach(MIMEText(self._html_to_text(body), 'plain'))
            
            return self._send_email(msg)
            
        except Exception as e:
            logger.error(f"Failed to send test email: {e}")
            return False
    
    def _send_email(self, msg: MIMEMultipart) -> bool:
        """Send email via SMTP"""
        try:
            if not self.smtp_username or not self.smtp_password:
                logger.warning("SMTP credentials not configured. Email sending skipped.")
                return False
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {msg['To']}")
            return True
            
        except Exception as e:
            logger.error(f"SMTP error: {e}")
            return False
    
    def _build_alert_email_body(self, location: str, weather_data: Dict, alerts: List[Dict]) -> str:
        """Build HTML body for weather alert email"""
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
        
        alert_items = ""
        for alert in alerts:
            severity_color = {
                'critical': '#dc3545',
                'warning': '#ffc107',
                'advisory': '#17a2b8'
            }.get(alert['severity'], '#6c757d')
            
            alert_items += f"""
            <div style="background-color: {severity_color}; color: white; padding: 10px; margin: 10px 0; border-radius: 5px;">
                <strong>{alert['type'].upper()}</strong>: {alert['message']}
            </div>
            """
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #dc3545;">🚨 SEVERE WEATHER ALERT</h2>
                <h3>{location}</h3>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h4>Current Conditions:</h4>
                    <p><strong>Temperature:</strong> {temp}°C (feels like {feels_like}°C)</p>
                    <p><strong>Humidity:</strong> {humidity}%</p>
                    <p><strong>Conditions:</strong> {description.title()}</p>
                </div>
                
                <h4>⚠️ Active Alerts:</h4>
                {alert_items}
                
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #ffc107;">
                    <h4>🛡️ Safety Recommendations:</h4>
                    <ul>
                        <li>Stay indoors if possible</li>
                        <li>Monitor local news and weather updates</li>
                        <li>Keep emergency supplies handy</li>
                        <li>Avoid unnecessary travel</li>
                        <li>Charge your devices in case of power outages</li>
                    </ul>
                </div>
                
                <hr>
                <p><em>This is an automated alert from Weather GPT. For official emergency information, please follow local authorities.</em></p>
            </div>
        </body>
        </html>
        """
    
    def _build_digest_email_body(self, weather_summary: List[Dict], subscriber_name: str) -> str:
        """Build HTML body for daily digest email"""
        from datetime import datetime
        
        location_sections = ""
        for summary in weather_summary:
            location = summary['location']
            weather = summary['weather']
            safety_score = summary['safety_score']
            
            temp = weather['main']['temp']
            feels_like = weather['main']['feels_like']
            humidity = weather['main']['humidity']
            description = weather['weather'][0]['description']
            
            # Safety score color
            score_color = '#28a745' if safety_score >= 70 else '#ffc107' if safety_score >= 40 else '#dc3545'
            
            location_sections += f"""
            <div style="border: 1px solid #dee2e6; border-radius: 5px; padding: 15px; margin: 15px 0;">
                <h3 style="color: #007bff;">📍 {location}</h3>
                <div style="display: flex; justify-content: space-between; align-items: center; margin: 10px 0;">
                    <span><strong>Temperature:</strong> {temp}°C (feels like {feels_like}°C)</span>
                    <span style="background-color: {score_color}; color: white; padding: 5px 10px; border-radius: 3px;">
                        Safety Score: {safety_score}/100
                    </span>
                </div>
                <p><strong>Conditions:</strong> {description.title()}</p>
                <p><strong>Humidity:</strong> {humidity}%</p>
            </div>
            """
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #007bff;">🌤️ Daily Weather Digest</h2>
                <p>Hello <strong>{subscriber_name}</strong>! Here's your daily weather summary.</p>
                <p><em>{datetime.now().strftime('%A, %B %d, %Y')}</em></p>
                
                {location_sections}
                
                <div style="background-color: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h4>💡 Daily Tips:</h4>
                    <ul>
                        <li>Check the safety scores before planning outdoor activities</li>
                        <li>Stay hydrated regardless of the weather</li>
                        <li>Keep an eye on changing weather conditions</li>
                    </ul>
                </div>
                
                <hr>
                <p><em>To manage your subscription preferences, visit your Weather GPT settings.</em></p>
            </div>
        </body>
        </html>
        """
    
    def _html_to_text(self, html: str) -> str:
        """Simple HTML to text conversion"""
        # Remove HTML tags
        text = html
        text = text.replace('<html>', '').replace('</html>', '')
        text = text.replace('<body>', '').replace('</body>', '')
        text = text.replace('<h2>', '\n\n').replace('</h2>', '\n')
        text = text.replace('<h3>', '\n').replace('</h3>', '\n')
        text = text.replace('<h4>', '\n').replace('</h4>', '\n')
        text = text.replace('<p>', '').replace('</p>', '\n')
        text = text.replace('<li>', '• ').replace('</li>', '\n')
        text = text.replace('<ul>', '').replace('</ul>', '')
        text = text.replace('<div>', '').replace('</div>', '')
        text = text.replace('<span>', '').replace('</span>', '')
        text = text.replace('<strong>', '').replace('</strong>', '')
        text = text.replace('<em>', '').replace('</em>', '')
        text = text.replace('<hr>', '\n---\n')
        text = text.replace('<br>', '\n')
        
        # Clean up extra whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)