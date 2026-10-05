"""
Test script for Weather GPT notification system
Run this to verify notification services are working correctly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_setup():
    """Test if environment variables are properly configured"""
    print("🔍 Testing Environment Setup...")
    
    required_vars = {
        'WEATHER_API_KEY': os.getenv('WEATHER_API_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'SMTP_USERNAME': os.getenv('SMTP_USERNAME'),
        'SMTP_PASSWORD': os.getenv('SMTP_PASSWORD'),
    }
    
    optional_vars = {
        'TWILIO_ACCOUNT_SID': os.getenv('TWILIO_ACCOUNT_SID'),
        'TWILIO_AUTH_TOKEN': os.getenv('TWILIO_AUTH_TOKEN'),
        'TWILIO_FROM_NUMBER': os.getenv('TWILIO_FROM_NUMBER'),
    }
    
    print("\nRequired Variables:")
    for var, value in required_vars.items():
        status = "✅ Set" if value and value != f'your_{var.lower()}' else "❌ Not set"
        print(f"  {var}: {status}")
    
    print("\nOptional Variables (SMS):")
    for var, value in optional_vars.items():
        status = "✅ Set" if value and value != f'your_{var.lower()}' else "⚠️ Not set (optional)"
        print(f"  {var}: {status}")
    
    return all(value and value != f'your_{var.lower()}' for var, value in required_vars.items())

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🔍 Testing Module Imports...")
    
    try:
        from services import NotificationService, SubscriptionManager, AlertDetector
        print("  ✅ Core services imported successfully")
        return True
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_alert_detector():
    """Test the alert detection system"""
    print("\n🔍 Testing Alert Detector...")
    
    try:
        from services import AlertDetector
        detector = AlertDetector()
        
        # Test with sample weather data
        test_weather = {
            'main': {
                'temp': 45,
                'feels_like': 48,
                'humidity': 85
            },
            'weather': [{
                'description': 'clear sky',
                'id': 800
            }],
            'wind': {
                'speed': 10  # m/s
            },
            'visibility': 10000
        }
        
        alerts = detector.detect_severe_weather(test_weather)
        score = detector.calculate_safety_score(test_weather)
        risk_level = detector.get_risk_level(score)
        
        print(f"  ✅ Detected {len(alerts)} alerts")
        print(f"  ✅ Safety score: {score}/100")
        print(f"  ✅ Risk level: {risk_level}")
        
        if alerts:
            print("  Sample alerts:")
            for alert in alerts[:2]:  # Show first 2 alerts
                print(f"    - {alert['type']}: {alert['message']}")
        
        return True
    except Exception as e:
        print(f"  ❌ Alert detector test failed: {e}")
        return False

def test_subscription_manager():
    """Test the subscription manager"""
    print("\n🔍 Testing Subscription Manager...")
    
    try:
        from services import SubscriptionManager
        manager = SubscriptionManager('test_subscriptions.json')
        
        # Test adding a subscriber
        test_email = 'test@example.com'
        success = manager.add_subscriber(
            email=test_email,
            name='Test User',
            phone='+1234567890',
            locations=['Sulur', 'Chennai']
        )
        
        if success:
            print("  ✅ Successfully added test subscriber")
            
            # Test retrieving subscriber
            subscriber = manager.get_subscriber(test_email)
            if subscriber:
                print(f"  ✅ Retrieved subscriber: {subscriber['name']}")
                
                # Test getting subscribers for location
                location_subs = manager.get_subscribers_for_location('Sulur')
                print(f"  ✅ Found {len(location_subs)} subscribers for Sulur")
                
                # Clean up
                manager.remove_subscriber(test_email)
                print("  ✅ Cleaned up test subscriber")
                
                # Remove test file
                if os.path.exists('test_subscriptions.json'):
                    os.remove('test_subscriptions.json')
                    print("  ✅ Removed test subscriptions file")
                
                return True
        else:
            print("  ❌ Failed to add subscriber")
            return False
            
    except Exception as e:
        print(f"  ❌ Subscription manager test failed: {e}")
        return False

def test_weather_api():
    """Test weather API connectivity"""
    print("\n🔍 Testing Weather API...")
    
    try:
        from app import get_weather_data
        
        weather_data = get_weather_data('Sulur')
        if weather_data:
            temp = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            print(f"  ✅ Weather API working")
            print(f"  📍 Sulur: {description}, {temp}°C")
            return True
        else:
            print("  ⚠️ Weather API returned no data (check API key)")
            return False
            
    except Exception as e:
        print(f"  ❌ Weather API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Weather GPT Notification System Test")
    print("=" * 50)
    
    results = {
        'Environment Setup': test_environment_setup(),
        'Module Imports': test_imports(),
        'Alert Detector': test_alert_detector(),
        'Subscription Manager': test_subscription_manager(),
        'Weather API': test_weather_api()
    }
    
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Notification system is ready.")
    else:
        print("\n⚠️ Some tests failed. Please check the configuration.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)