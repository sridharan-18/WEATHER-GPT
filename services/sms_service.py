"""
SMS Service for Weather GPT
Handles sending weather alerts via SMS using Twilio
"""

import os
import logging
from typing import Dict

try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SMSService:
    """Service for sending SMS notifications"""
    
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')
        self.from_number = os.getenv('TWILIO_FROM_NUMBER', '')
        self.enabled = TWILIO_AVAILABLE and self.account_sid and self.auth_token
        
        if not self.enabled:
            logger.warning("Twilio SMS service not available or not configured")
        
        if self.enabled:
            try:
                self.client = Client(self.account_sid, self.auth_token)
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")
                self.enabled = False
    
    def send_weather_alert(self, to_number: str, location: str, alert: Dict) -> bool:
        """
        Send severe weather alert via SMS
        
        Args:
            to_number: Recipient phone number (with country code, e.g., +919876543210)
            location: Location name
            alert: Alert dictionary with type and message
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            logger.warning("SMS service not enabled, skipping alert")
            return False
        
        try:
            # Build SMS message (keep it under 160 characters if possible)
            message = self._build_alert_message(location, alert)
            
            # Send SMS
            self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            logger.info(f"SMS alert sent to {to_number} for {location}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS alert: {e}")
            return False
    
    def send_test_sms(self, to_number: str) -> bool:
        """Send a test SMS to verify SMS configuration"""
        if not self.enabled:
            logger.warning("SMS service not enabled, skipping test")
            return False
        
        try:
            message = "✅ Weather GPT: Test SMS successful! Your SMS notifications are working."
            
            self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            logger.info(f"Test SMS sent to {to_number}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send test SMS: {e}")
            return False
    
    def send_daily_digest_summary(self, to_number: str, summary: str) -> bool:
        """
        Send a brief daily digest summary via SMS
        
        Args:
            to_number: Recipient phone number
            summary: Brief summary of weather conditions
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            message = f"🌤️ Weather GPT Daily Digest:\n{summary}"
            
            self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            logger.info(f"Daily digest SMS sent to {to_number}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send daily digest SMS: {e}")
            return False
    
    def _build_alert_message(self, location: str, alert: Dict) -> str:
        """Build SMS message for weather alert"""
        alert_type = alert.get('type', 'Weather Alert')
        message = alert.get('message', 'Severe weather conditions detected')
        
        # Keep message concise for SMS
        sms_message = f"🚨 WEATHER ALERT - {location}\n"
        sms_message += f"{alert_type.upper()}: {message}\n"
        sms_message += "Stay safe & follow local authorities."
        
        # Truncate if too long (SMS limit is 160 characters for single message)
        if len(sms_message) > 160:
            sms_message = sms_message[:157] + "..."
        
        return sms_message
    
    def is_enabled(self) -> bool:
        """Check if SMS service is properly configured and enabled"""
        return self.enabled