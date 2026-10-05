"""
Direct test for crop database without service imports
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_crop_database():
    """Test the crop database directly"""
    print("Testing Crop Database (Direct Import)...")
    
    try:
        # Import directly from the file
        import importlib.util
        spec = importlib.util.spec_from_file_location("crop_database", "services/agriculture/crop_database.py")
        crop_database_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(crop_database_module)
        
        CropDatabase = crop_database_module.CropDatabase
        db = CropDatabase()
        
        # Test getting all crops
        all_crops = db.get_all_crops()
        print(f"  [OK] Found {len(all_crops)} crops in database")
        
        # Test getting specific crop
        rice_info = db.get_crop_info('rice')
        if rice_info:
            print(f"  [OK] Retrieved rice information: {rice_info['name']}")
            print(f"  [OK] Rice category: {rice_info['category']}")
            print(f"  [OK] Rice water requirement: {rice_info['water_requirement']}")
        
        # Test weather suitability
        test_weather = {
            'main': {'temp': 28, 'humidity': 75},
            'weather': [{'description': 'clear sky', 'id': 800}],
            'wind': {'speed': 5}  # m/s
        }
        
        suitability = db.assess_weather_suitability('rice', test_weather)
        print(f"  [OK] Weather suitability assessment: {suitability['suitable']}")
        print(f"  [OK] Assessment message: {suitability['overall_assessment']}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Crop database test failed: {e}")
        import traceback
        traceback.print_exc()
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