"""
Test script for Agricultural Features
Run this to verify agricultural services are working correctly
"""

import os
import sys

# Try to load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed, using system environment variables")

def test_imports():
    """Test if all agricultural modules can be imported"""
    print("Testing Agricultural Module Imports...")
    
    try:
        # Add the current directory to Python path
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from services.agriculture.crop_database import CropDatabase
        from services.agriculture.crop_advisor import CropAdvisor
        from services.agriculture.farmer_action_planner import FarmerActionPlanner
        from services.agriculture.irrigation_scheduler import IrrigationScheduler
        from services.agriculture.harvest_advisor import HarvestAdvisor
        from services.agriculture.storm_impact_analyzer import StormImpactAnalyzer
        print("  [OK] All agricultural services imported successfully")
        return True
    except ImportError as e:
        print(f"  [FAIL] Import failed: {e}")
        return False

def test_crop_database():
    """Test the crop database"""
    print("\nTesting Crop Database...")
    
    try:
        # Add the current directory to Python path
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
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

def test_crop_advisor():
    """Test the crop advisor"""
    print("\nTesting Crop Advisor...")
    
    try:
        # Add the current directory to Python path
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from services.agriculture.crop_advisor import CropAdvisor
        advisor = CropAdvisor()
        
        test_weather = {
            'main': {'temp': 28, 'humidity': 75},
            'weather': [{'description': 'clear sky', 'id': 800}],
            'wind': {'speed': 5}
        }
        
        # Test crop recommendations
        recommendations = advisor.get_crop_recommendations(test_weather, 'Sulur')
        print(f"  [OK] Generated {len(recommendations['recommendations'])} crop recommendations")
        
        # Test specific crop advice
        rice_advice = advisor.get_specific_crop_advice('rice', test_weather)
        print(f"  [OK] Generated advice for rice: {len(rice_advice['recommendations'])} recommendations")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Crop advisor test failed: {e}")
        return False

def test_irrigation_scheduler():
    """Test the irrigation scheduler"""
    print("\nTesting Irrigation Scheduler...")
    
    try:
        # Add the current directory to Python path
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from services.agriculture.irrigation_scheduler import IrrigationScheduler
        scheduler = IrrigationScheduler()
        
        test_weather = {
            'main': {'temp': 28, 'humidity': 75},
            'weather': [{'description': 'clear sky', 'id': 800}],
            'wind': {'speed': 5}
        }
        
        # Test irrigation schedule
        schedule = scheduler.generate_irrigation_schedule(test_weather, 'rice', 50)
        print(f"  [OK] Generated irrigation schedule with {len(schedule['schedule'])} entries")
        print(f"  [OK] Irrigation urgency: {schedule['irrigation_needs']['urgency']}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Irrigation scheduler test failed: {e}")
        return False

def test_harvest_advisor():
    """Test the harvest advisor"""
    print("\nTesting Harvest Advisor...")
    
    try:
        # Add the current directory to Python path
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from services.agriculture.harvest_advisor import HarvestAdvisor
        advisor = HarvestAdvisor()
        
        test_weather = {
            'main': {'temp': 25, 'humidity': 60},
            'weather': [{'description': 'clear sky', 'id': 800}],
            'wind': {'speed': 3}
        }
        
        # Test harvest recommendations
        harvest_rec = advisor.get_harvest_recommendations(test_weather, 'rice', 'mature')
        print(f"  [OK] Generated harvest recommendations")
        print(f"  [OK] Harvest suitability: {harvest_rec['harvest_assessment']['suitability_level']}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Harvest advisor test failed: {e}")
        return False

def test_storm_impact_analyzer():
    """Test the storm impact analyzer"""
    print("\nTesting Storm Impact Analyzer...")
    
    try:
        # Add the current directory to Python path
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from services.agriculture.storm_impact_analyzer import StormImpactAnalyzer
        analyzer = StormImpactAnalyzer()
        
        # Test with storm conditions
        storm_weather = {
            'main': {'temp': 25, 'humidity': 85},
            'weather': [{'description': 'thunderstorm', 'id': 211}],
            'wind': {'speed': 15}  # m/s
        }
        
        # Test storm impact analysis
        impact = analyzer.analyze_storm_impact(storm_weather, 'rice', 'mature')
        print(f"  [OK] Generated storm impact analysis")
        print(f"  [OK] Storm severity: {impact['storm_severity']['level']}")
        print(f"  [OK] Overall risk: {impact['overall_risk_level']}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Storm impact analyzer test failed: {e}")
        return False

def main():
    """Run all agricultural tests"""
    print("=" * 50)
    print("Weather GPT Agricultural Features Test")
    print("=" * 50)
    
    results = {
        'Module Imports': test_imports(),
        'Crop Database': test_crop_database(),
        'Crop Advisor': test_crop_advisor(),
        'Irrigation Scheduler': test_irrigation_scheduler(),
        'Harvest Advisor': test_harvest_advisor(),
        'Storm Impact Analyzer': test_storm_impact_analyzer()
    }
    
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{test_name}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nAll agricultural tests passed! System is ready.")
    else:
        print("\nSome tests failed. Please check the configuration.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)