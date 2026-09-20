"""
Standalone script to run the weather notification scheduler
Can be run independently or as a background process
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Run the notification scheduler"""
    print("Starting Weather GPT Notification Scheduler...")
    
    try:
        from services import start_scheduler
        start_scheduler()
        
        print("Scheduler is running. Press Ctrl+C to stop.")
        
        # Keep the script running
        import time
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\nStopping scheduler...")
        from services import stop_scheduler
        stop_scheduler()
        print("Scheduler stopped.")
    except Exception as e:
        print(f"Error starting scheduler: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()