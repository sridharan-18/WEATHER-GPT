"""
Subscription Manager for Weather GPT
Manages user subscriptions for weather notifications
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SubscriptionManager:
    """Manages user subscriptions for weather notifications"""
    
    def __init__(self, subscriptions_file: str = 'subscriptions.json'):
        self.subscriptions_file = subscriptions_file
        self.subscriptions = self._load_subscriptions()
    
    def _load_subscriptions(self) -> Dict:
        """Load subscriptions from file"""
        try:
            if os.path.exists(self.subscriptions_file):
                with open(self.subscriptions_file, 'r') as f:
                    return json.load(f)
            else:
                # Initialize with empty subscriptions
                return {'subscribers': []}
        except Exception as e:
            logger.error(f"Error loading subscriptions: {e}")
            return {'subscribers': []}
    
    def _save_subscriptions(self) -> bool:
        """Save subscriptions to file"""
        try:
            with open(self.subscriptions_file, 'w') as f:
                json.dump(self.subscriptions, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving subscriptions: {e}")
            return False
    
    def add_subscriber(self, email: str, name: str = '', phone: str = '', 
                      locations: List[str] = None, preferences: Dict = None) -> bool:
        """
        Add a new subscriber
        
        Args:
            email: Subscriber email address
            name: Subscriber name
            phone: Subscriber phone number (optional)
            locations: List of locations to monitor
            preferences: Notification preferences
            
        Returns:
            True if added successfully, False otherwise
        """
        try:
            # Check if subscriber already exists
            if self._find_subscriber(email):
                logger.warning(f"Subscriber {email} already exists")
                return False
            
            subscriber = {
                'email': email,
                'name': name or email.split('@')[0],
                'phone': phone,
                'locations': locations or ['Sulur'],
                'email_enabled': True,
                'sms_enabled': bool(phone),
                'daily_digest': True,
                'severe_alerts': True,
                'created_at': datetime.now().isoformat(),
                'preferences': preferences or {}
            }
            
            self.subscriptions['subscribers'].append(subscriber)
            return self._save_subscriptions()
            
        except Exception as e:
            logger.error(f"Error adding subscriber: {e}")
            return False
    
    def remove_subscriber(self, email: str) -> bool:
        """
        Remove a subscriber
        
        Args:
            email: Subscriber email address
            
        Returns:
            True if removed successfully, False otherwise
        """
        try:
            subscriber = self._find_subscriber(email)
            if not subscriber:
                logger.warning(f"Subscriber {email} not found")
                return False
            
            self.subscriptions['subscribers'].remove(subscriber)
            return self._save_subscriptions()
            
        except Exception as e:
            logger.error(f"Error removing subscriber: {e}")
            return False
    
    def update_subscriber(self, email: str, updates: Dict) -> bool:
        """
        Update subscriber information
        
        Args:
            email: Subscriber email address
            updates: Dictionary of fields to update
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            subscriber = self._find_subscriber(email)
            if not subscriber:
                logger.warning(f"Subscriber {email} not found")
                return False
            
            # Update allowed fields
            allowed_fields = ['name', 'phone', 'locations', 'email_enabled', 
                            'sms_enabled', 'daily_digest', 'severe_alerts', 'preferences']
            
            for field, value in updates.items():
                if field in allowed_fields:
                    subscriber[field] = value
            
            subscriber['updated_at'] = datetime.now().isoformat()
            return self._save_subscriptions()
            
        except Exception as e:
            logger.error(f"Error updating subscriber: {e}")
            return False
    
    def _find_subscriber(self, email: str) -> Optional[Dict]:
        """Find subscriber by email"""
        for subscriber in self.subscriptions['subscribers']:
            if subscriber['email'] == email:
                return subscriber
        return None
    
    def get_subscriber(self, email: str) -> Optional[Dict]:
        """Get subscriber information"""
        return self._find_subscriber(email)
    
    def get_all_subscribers(self) -> List[Dict]:
        """Get all subscribers"""
        return self.subscriptions['subscribers']
    
    def get_subscribers_for_location(self, location: str) -> List[Dict]:
        """
        Get subscribers who want alerts for a specific location
        
        Args:
            location: Location name
            
        Returns:
            List of subscribers monitoring this location
        """
        subscribers = []
        location_lower = location.lower()
        
        for subscriber in self.subscriptions['subscribers']:
            if subscriber.get('severe_alerts', True):
                subscriber_locations = [loc.lower() for loc in subscriber.get('locations', [])]
                if location_lower in subscriber_locations:
                    subscribers.append(subscriber)
        
        return subscribers
    
    def get_daily_digest_subscribers(self) -> List[Dict]:
        """Get subscribers who want daily digests"""
        return [
            subscriber for subscriber in self.subscriptions['subscribers']
            if subscriber.get('daily_digest', True)
        ]
    
    def toggle_subscription(self, email: str, subscription_type: str) -> bool:
        """
        Toggle a specific subscription type for a user
        
        Args:
            email: Subscriber email address
            subscription_type: Type of subscription ('daily_digest', 'severe_alerts', 'email_enabled', 'sms_enabled')
            
        Returns:
            True if toggled successfully, False otherwise
        """
        try:
            subscriber = self._find_subscriber(email)
            if not subscriber:
                return False
            
            if subscription_type in subscriber:
                subscriber[subscription_type] = not subscriber[subscription_type]
                subscriber['updated_at'] = datetime.now().isoformat()
                return self._save_subscriptions()
            
            return False
            
        except Exception as e:
            logger.error(f"Error toggling subscription: {e}")
            return False
    
    def add_location_to_subscriber(self, email: str, location: str) -> bool:
        """Add a location to subscriber's monitored locations"""
        try:
            subscriber = self._find_subscriber(email)
            if not subscriber:
                return False
            
            if location not in subscriber['locations']:
                subscriber['locations'].append(location)
                subscriber['updated_at'] = datetime.now().isoformat()
                return self._save_subscriptions()
            
            return True  # Location already exists
            
        except Exception as e:
            logger.error(f"Error adding location: {e}")
            return False
    
    def remove_location_from_subscriber(self, email: str, location: str) -> bool:
        """Remove a location from subscriber's monitored locations"""
        try:
            subscriber = self._find_subscriber(email)
            if not subscriber:
                return False
            
            if location in subscriber['locations']:
                subscriber['locations'].remove(location)
                subscriber['updated_at'] = datetime.now().isoformat()
                return self._save_subscriptions()
            
            return True  # Location doesn't exist
            
        except Exception as e:
            logger.error(f"Error removing location: {e}")
            return False
    
    def get_subscriber_count(self) -> int:
        """Get total number of subscribers"""
        return len(self.subscriptions['subscribers'])
    
    def get_active_subscriber_count(self) -> int:
        """Get number of active subscribers (with at least one notification enabled)"""
        active_count = 0
        for subscriber in self.subscriptions['subscribers']:
            if (subscriber.get('email_enabled', True) or 
                subscriber.get('sms_enabled', False)) and \
               (subscriber.get('daily_digest', True) or 
                subscriber.get('severe_alerts', True)):
                active_count += 1
        return active_count