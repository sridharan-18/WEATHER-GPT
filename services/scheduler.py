"""
Scheduler for Weather GPT
Handles scheduled tasks like daily weather digests and periodic weather checks
"""

import schedule
import time
import logging
from datetime import datetime
from typing import Optional
import threading

from notification_service import NotificationService
from alert_detector import AlertDetector
from app import get_weather_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherScheduler:
    """Scheduler for automated weather tasks"""
    
    def __init__(self):
        self.notification_service = NotificationService()
        self.alert_detector = AlertDetector()
        self.running = False
        self.scheduler_thread: Optional[threading.Thread] = None
        self.monitored_locations = ['Sulur', 'Coimbatore', 'Chennai', 'Bangalore']
    
    def start(self):
        """Start the scheduler"""
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        self.running = True
        
        # Schedule daily digest at 8:00 AM
        schedule.every().day.at("08:00").do(self._send_daily_digest)
        
        # Schedule weather checks every hour for severe weather
        schedule.every().hour.do(self._check_severe_weather)
        
        # Start scheduler in background thread
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("Weather scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        schedule.clear()
        logger.info("Weather scheduler stopped")
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def _send_daily_digest(self):
        """Send daily weather digest to all subscribers"""
        try:
            logger.info("Starting daily digest task")
            
            digests_sent = self.notification_service.send_daily_digest()
            
            logger.info(f"Daily digest completed. Sent {digests_sent} digests")
            
        except Exception as e:
            logger.error(f"Error in daily digest task: {e}")
    
    def _check_severe_weather(self):
        """Check for severe weather conditions and send alerts"""
        try:
            logger.info("Starting severe weather check")
            
            total_alerts = 0
            
            for location in self.monitored_locations:
                try:
                    weather_data = get_weather_data(location)
                    if weather_data:
                        alerts_sent = self.notification_service.send_severe_weather_alert(
                            location, weather_data
                        )
                        total_alerts += alerts_sent
                        
                        if alerts_sent > 0:
                            logger.info(f"Sent {alerts_sent} alerts for {location}")
                
                except Exception as e:
                    logger.error(f"Error checking weather for {location}: {e}")
            
            logger.info(f"Severe weather check completed. Total alerts sent: {total_alerts}")
            
        except Exception as e:
            logger.error(f"Error in severe weather check: {e}")
    
    def add_monitored_location(self, location: str):
        """Add a location to monitor for severe weather"""
        if location not in self.monitored_locations:
            self.monitored_locations.append(location)
            logger.info(f"Added {location} to monitored locations")
    
    def remove_monitored_location(self, location: str):
        """Remove a location from monitoring"""
        if location in self.monitored_locations:
            self.monitored_locations.remove(location)
            logger.info(f"Removed {location} from monitored locations")
    
    def run_daily_digest_now(self):
        """Manually trigger daily digest (for testing)"""
        logger.info("Manually triggering daily digest")
        self._send_daily_digest()
    
    def run_severe_weather_check_now(self):
        """Manually trigger severe weather check (for testing)"""
        logger.info("Manually triggering severe weather check")
        self._check_severe_weather()
    
    def get_status(self) -> dict:
        """Get scheduler status"""
        return {
            'running': self.running,
            'monitored_locations': self.monitored_locations,
            'next_daily_digest': self._get_next_run_time('08:00'),
            'next_weather_check': self._get_next_run_time('hourly')
        }
    
    def _get_next_run_time(self, schedule_type: str) -> str:
        """Get next run time for a scheduled task"""
        try:
            if schedule_type == '08:00':
                job = schedule.next_run()
                return job.strftime('%Y-%m-%d %H:%M:%S') if job else 'Not scheduled'
            elif schedule_type == 'hourly':
                # For hourly, just return next hour
                from datetime import datetime, timedelta
                next_hour = (datetime.now().replace(minute=0, second=0, microsecond=0) + 
                           timedelta(hours=1))
                return next_hour.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return 'Unknown'
        return 'Unknown'


# Global scheduler instance
scheduler = WeatherScheduler()


def start_scheduler():
    """Start the global scheduler"""
    scheduler.start()


def stop_scheduler():
    """Stop the global scheduler"""
    scheduler.stop()


def get_scheduler_status():
    """Get global scheduler status"""
    return scheduler.get_status()