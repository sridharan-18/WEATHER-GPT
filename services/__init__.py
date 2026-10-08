"""
Services module for Weather GPT
Contains modular services for weather assistant, notifications, agriculture, etc.
"""

from .weather_assistant import WeatherAssistant
from .notification_service import NotificationService
from .email_service import EmailService
from .sms_service import SMSService
from .alert_detector import AlertDetector
from .subscription_manager import SubscriptionManager
# Scheduler is imported lazily because it requires the 'schedule' package,
# an optional dependency. Keep the services package importable even when it is
# not installed, and fall back gracefully.
try:
    from .scheduler import WeatherScheduler, start_scheduler, stop_scheduler, get_scheduler_status
    SCHEDULER_AVAILABLE = True
except ImportError:
    SCHEDULER_AVAILABLE = False
    WeatherScheduler = None
    start_scheduler = None
    stop_scheduler = None
    get_scheduler_status = None

# Multilingual and accessibility services
try:
    from .translation_service import TranslationService, translation_service
    from .voice_assistant import VoiceAssistant, voice_assistant
    MULTILINGUAL_AVAILABLE = True
except ImportError:
    MULTILINGUAL_AVAILABLE = False
    TranslationService = None
    translation_service = None
    VoiceAssistant = None
    voice_assistant = None

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
    'WeatherAssistant',
    'NotificationService',
    'EmailService', 
    'SMSService',
    'AlertDetector',
    'SubscriptionManager',
    'WeatherScheduler',
    'start_scheduler',
    'stop_scheduler',
    'get_scheduler_status',
    'SCHEDULER_AVAILABLE',
    'TranslationService',
    'translation_service',
    'VoiceAssistant',
    'voice_assistant',
    'MULTILINGUAL_AVAILABLE',
    'AGRICULTURE_AVAILABLE'
]
