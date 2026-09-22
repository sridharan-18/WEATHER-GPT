"""
Services package for Weather GPT
"""

from .notification_service import NotificationService
from .email_service import EmailService
from .sms_service import SMSService
from .alert_detector import AlertDetector
from .subscription_manager import SubscriptionManager
from .scheduler import WeatherScheduler, start_scheduler, stop_scheduler, get_scheduler_status

# Agriculture services (imported separately to avoid circular dependencies)
try:
    from .agriculture.crop_database import CropDatabase
    from .agriculture.crop_advisor import CropAdvisor
    from .agriculture.farmer_action_planner import FarmerActionPlanner
    from .agriculture.irrigation_scheduler import IrrigationScheduler
    from .agriculture.harvest_advisor import HarvestAdvisor
    from .agriculture.storm_impact_analyzer import StormImpactAnalyzer
    AGRICULTURE_AVAILABLE = True
except ImportError:
    AGRICULTURE_AVAILABLE = False

__all__ = [
    'NotificationService',
    'EmailService', 
    'SMSService',
    'AlertDetector',
    'SubscriptionManager',
    'WeatherScheduler',
    'start_scheduler',
    'stop_scheduler',
    'get_scheduler_status',
    'AGRICULTURE_AVAILABLE'
]