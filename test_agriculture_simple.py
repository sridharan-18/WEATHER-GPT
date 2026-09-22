"""
Simple test script for Agricultural Features
Tests core functionality without complex dependencies
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_crop_database():
    """Test the crop database directly"""
    print("Testing Crop Database...")
    
    try:
        from services.agriculture.crop_database import CropDatabase
        db = CropDatabase()
        
        # Test getting all crops
        all_crops = db.get_all_crops()
        print(f"  [OK] Found {len(all_crops)} crops in database")
        
        # Test getting specific crop
        rice_info = db.get_crop_info('rice')
        if rice_info:
            print(f"  [OK] Retrieved rice information: {rice_info['name']}")
        
        # Test weather suitability
        test_weather = {
            'main': {'temp': 28, 'humidity': 75},
            'weather': [{'description': 'clear sky', 'id': 800}],
            'wind': {'speed': 5}  # m/s
        }
        
        suitability = db.assess_weather_suitability('rice', test_weather)
        print(f"  [OK] Weather suitability assessment: {suitability['suitable']}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Crop database test failed: {e}")
        return False

def main():
    """Run agricultural tests"""
    print("=" * 50)
    print("Weather GPT Agricultural Features Test")
    print("=" * 50)
    
    result = test_crop_database()
    
    print("\n" + "=" * 50)
    if result:
        print("Agricultural core functionality test: [PASS]")
    else:
        print("Agricultural core functionality test: [FAIL]")
    
    return result

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)