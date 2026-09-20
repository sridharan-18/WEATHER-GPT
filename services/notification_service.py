"""
Notification Service for Weather GPT
Handles email and SMS notifications for severe weather alerts and daily digests
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

# Import sub-services
from email_service import EmailService
from sms_service import SMSService
from alert_detector import AlertDetector
from subscription_manager import SubscriptionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotificationService:
    """Main notification service coordinating email and SMS alerts"""
    
    def __init__(self):
        self.email_service = EmailService()
        self.sms_service = SMSService()
        self.alert_detector = AlertDetector()
        self.subscription_manager = SubscriptionManager()
    
    def send_severe_weather_alert(self, location: str, weather_data: Dict) -> int:
        """
        Send severe weather alerts to all subscribed users for a location
        
        Args:
            location: Location name
            weather_data: Weather data from API
            
        Returns:
            Number of alerts sent
        """
        try:
            # Detect if severe weather conditions exist
            alerts = self.alert_detector.detect_severe_weather(weather_data)
            
            if not alerts:
                logger.info(f"No severe weather detected for {location}")
                return 0
            
            # Get subscribers for this location
            subscribers = self.subscription_manager.get_subscribers_for_location(location)
            
            if not subscribers:
                logger.info(f"No subscribers for location: {location}")
                return 0
            
            alerts_sent = 0
            
            for subscriber in subscribers:
                try:
                    # Send email if enabled
                    if subscriber.get('email_enabled', True) and subscriber.get('email'):
                        self.email_service.send_weather_alert(
                            subscriber['email'],
                            location,
                            weather_data,
                            alerts
                        )
                        alerts_sent += 1
                    
                    # Send SMS if enabled and for critical alerts
                    if subscriber.get('sms_enabled', False) and subscriber.get('phone'):
                        critical_alerts = [a for a in alerts if a['severity'] == 'critical']
                        if critical_alerts:
                            self.sms_service.send_weather_alert(
                                subscriber['phone'],
                                location,
                                critical_alerts[0]  # Send most critical alert
                            )
                            alerts_sent += 1
                    
                except Exception as e:
                    logger.error(f"Failed to send alert to {subscriber.get('email', 'unknown')}: {e}")
            
            logger.info(f"Sent {alerts_sent} severe weather alerts for {location}")
            return alerts_sent
            
        except Exception as e:
            logger.error(f"Error in send_severe_weather_alert: {e}")
            return 0
    
    def send_daily_digest(self) -> int:
        """
        Send daily weather digest to all subscribers
        
        Returns:
            Number of digests sent
        """
        try:
            # Get all subscribers who want daily digests
            subscribers = self.subscription_manager.get_daily_digest_subscribers()
            
            if not subscribers:
                logger.info("No daily digest subscribers")
                return 0
            
            digests_sent = 0
            
            for subscriber in subscribers:
                try:
                    # Get weather data for subscriber's preferred locations
                    locations = subscriber.get('locations', ['Sulur'])
                    weather_summary = self._generate_weather_summary(locations)
                    
                    # Send daily digest email
                    self.email_service.send_daily_digest(
                        subscriber['email'],
                        weather_summary,
                        subscriber.get('name', 'Subscriber')
                    )
                    digests_sent += 1
                    
                except Exception as e:
                    logger.error(f"Failed to send daily digest to {subscriber.get('email', 'unknown')}: {e}")
            
            logger.info(f"Sent {digests_sent} daily digests")
            return digests_sent
            
        except Exception as e:
            logger.error(f"Error in send_daily_digest: {e}")
            return 0
    
    def _generate_weather_summary(self, locations: List[str]) -> List[Dict]:
        """Generate weather summary for multiple locations"""
        from app import get_weather_data
        
        summary = []
        for location in locations:
            try:
                weather_data = get_weather_data(location)
                if weather_data:
                    safety_score = self.alert_detector.calculate_safety_score(weather_data)
                    summary.append({
                        'location': location,
                        'weather': weather_data,
                        'safety_score': safety_score,
                        'timestamp': datetime.now().isoformat()
                    })
            except Exception as e:
                logger.error(f"Error getting weather for {location}: {e}")
        
        return summary
    
    def send_test_notification(self, email: str, phone: Optional[str] = None) -> bool:
        """Send a test notification to verify setup"""
        try:
            # Send test email
            self.email_service.send_test_email(email)
            
            # Send test SMS if phone provided
            if phone:
                self.sms_service.send_test_sms(phone)
            
            return True
        except Exception as e:
            logger.error(f"Failed to send test notification: {e}")
            return False