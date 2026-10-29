"""
Unit tests for Weather Assistant Service
Tests Q&A flow, location extraction, actionable advice, and GPT integration
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.weather_assistant import WeatherAssistant


class TestWeatherAssistant(unittest.TestCase):
    """Test cases for WeatherAssistant class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.assistant = WeatherAssistant(
            openai_api_key='test_key',
            weather_api_key='test_weather_key'
        )
    
    def test_location_extraction_basic(self):
        """Test basic location extraction from messages"""
        test_cases = [
            ("What's the weather in Tokyo?", "Tokyo"),
            ("Weather at New York", "New York"),
            ("Conditions for London", "London"),
            ("Weather near Paris", "Paris"),
        ]
        
        for message, expected_location in test_cases:
            with self.subTest(message=message):
                result = self.assistant.extract_location(message)
                self.assertEqual(result, expected_location)
    
    def test_location_extraction_with_filler_words(self):
        """Test location extraction ignores filler words"""
        test_cases = [
            ("What's the weather in Tokyo today?", "Tokyo"),
            ("Weather at New York right now", "New York"),
            ("Conditions for London tomorrow", "London"),
        ]
        
        for message, expected_location in test_cases:
            with self.subTest(message=message):
                result = self.assistant.extract_location(message)
                self.assertEqual(result, expected_location)
    
    def test_location_extraction_no_location(self):
        """Test location extraction returns None when no location found"""
        test_cases = [
            ("What's the weather like today?", None),
            ("Is it raining?", None),
            ("Tell me about the temperature", None),
        ]
        
        for message, expected_location in test_cases:
            with self.subTest(message=message):
                result = self.assistant.extract_location(message)
                self.assertEqual(result, expected_location)
    
    def test_categorize_weather_hot(self):
        """Test weather categorization for hot conditions"""
        weather_data = {
            'main': {'temp': 30},
            'weather': [{'description': 'clear sky'}]
        }
        result = self.assistant.categorize_weather(weather_data)
        self.assertEqual(result, 'hot')
    
    def test_categorize_weather_cold(self):
        """Test weather categorization for cold conditions"""
        weather_data = {
            'main': {'temp': 5},
            'weather': [{'description': 'clear sky'}]
        }
        result = self.assistant.categorize_weather(weather_data)
        self.assertEqual(result, 'cold')
    
    def test_categorize_weather_mild(self):
        """Test weather categorization for mild conditions"""
        weather_data = {
            'main': {'temp': 20},
            'weather': [{'description': 'clear sky'}]
        }
        result = self.assistant.categorize_weather(weather_data)
        self.assertEqual(result, 'mild')
    
    def test_categorize_weather_rain(self):
        """Test weather categorization for rainy conditions"""
        weather_data = {
            'main': {'temp': 20},
            'weather': [{'description': 'light rain'}]
        }
        result = self.assistant.categorize_weather(weather_data)
        self.assertEqual(result, 'rain')
    
    def test_categorize_weather_storm(self):
        """Test weather categorization for stormy conditions"""
        weather_data = {
            'main': {'temp': 25},
            'weather': [{'description': 'thunderstorm'}]
        }
        result = self.assistant.categorize_weather(weather_data)
        self.assertEqual(result, 'rain')
    
    def test_generate_actionable_advice_hot(self):
        """Test actionable advice generation for hot weather"""
        weather_data = {
            'main': {'temp': 30},
            'weather': [{'description': 'clear sky'}]
        }
        
        advice = self.assistant.generate_actionable_advice(weather_data)
        
        self.assertIn('clothing', advice)
        self.assertIn('health', advice)
        self.assertIn('travel', advice)
        self.assertIn('outdoor', advice)
        
        # Check that advice contains relevant keywords
        self.assertIn('light', advice['clothing'].lower())
        self.assertIn('hydrated', advice['health'].lower())
    
    def test_generate_actionable_advice_cold(self):
        """Test actionable advice generation for cold weather"""
        weather_data = {
            'main': {'temp': 5},
            'weather': [{'description': 'clear sky'}]
        }
        
        advice = self.assistant.generate_actionable_advice(weather_data)
        
        self.assertIn('clothing', advice)
        self.assertIn('health', advice)
        
        # Check that advice contains relevant keywords
        self.assertIn('layer', advice['clothing'].lower())
        self.assertIn('warm', advice['health'].lower())
    
    def test_generate_actionable_advice_rain(self):
        """Test actionable advice generation for rainy weather"""
        weather_data = {
            'main': {'temp': 20},
            'weather': [{'description': 'heavy rain'}]
        }
        
        advice = self.assistant.generate_actionable_advice(weather_data)
        
        self.assertIn('clothing', advice)
        self.assertIn('travel', advice)
        
        # Check that advice contains relevant keywords
        self.assertIn('waterproof', advice['clothing'].lower())
        self.assertIn('speed', advice['travel'].lower())
    
    def test_generate_actionable_advice_specific_categories(self):
        """Test actionable advice generation for specific categories only"""
        weather_data = {
            'main': {'temp': 25},
            'weather': [{'description': 'clear sky'}]
        }
        
        advice = self.assistant.generate_actionable_advice(weather_data, categories=['clothing', 'health'])
        
        self.assertIn('clothing', advice)
        self.assertIn('health', advice)
        self.assertNotIn('travel', advice)
        self.assertNotIn('outdoor', advice)
    
    @patch('requests.get')
    def test_get_weather_data_success(self, mock_get):
        """Test successful weather data fetch"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'Tokyo',
            'main': {'temp': 25, 'humidity': 60, 'feels_like': 27},
            'weather': [{'description': 'clear sky'}]
        }
        mock_get.return_value = mock_response
        
        result = self.assistant.get_weather_data('Tokyo')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Tokyo')
        self.assertEqual(result['main']['temp'], 25)
    
    @patch('requests.get')
    def test_get_weather_data_failure(self, mock_get):
        """Test weather data fetch failure"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = self.assistant.get_weather_data('InvalidCity')
        
        self.assertIsNone(result)
    
    @patch('requests.get')
    def test_get_weather_data_exception(self, mock_get):
        """Test weather data fetch with exception"""
        mock_get.side_effect = Exception("Network error")
        
        result = self.assistant.get_weather_data('Tokyo')
        
        self.assertIsNone(result)
    
    def test_generate_rule_based_response_with_weather(self):
        """Test rule-based response with weather data"""
        weather_data = {
            'name': 'Tokyo',
            'main': {'temp': 25, 'humidity': 60, 'feels_like': 27},
            'weather': [{'description': 'clear sky'}]
        }
        
        response = self.assistant.generate_rule_based_response("What's the weather?", weather_data)
        
        self.assertIn('Tokyo', response)
        self.assertIn('25', response)
        self.assertIn('Actionable Advice', response)
        self.assertIn('Clothing', response)
        self.assertIn('Health', response)
    
    def test_generate_rule_based_response_hello(self):
        """Test rule-based response for hello message"""
        response = self.assistant.generate_rule_based_response("Hello", None)
        
        self.assertIn('Hello', response)
        self.assertIn('weather assistant', response.lower())
    
    def test_generate_rule_based_response_help(self):
        """Test rule-based response for help message"""
        response = self.assistant.generate_rule_based_response("Help", None)
        
        self.assertIn('help', response.lower())
        self.assertIn('weather', response.lower())
    
    def test_generate_rule_based_response_no_location(self):
        """Test rule-based response without location"""
        response = self.assistant.generate_rule_based_response("Random message", None)
        
        self.assertIn('location', response.lower())
    
    @patch('openai.OpenAI')
    def test_generate_gpt_response(self, mock_openai):
        """Test GPT response generation"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "It's sunny in Tokyo. Wear light clothing and stay hydrated."
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        weather_data = {
            'name': 'Tokyo',
            'main': {'temp': 25, 'humidity': 60, 'feels_like': 27},
            'weather': [{'description': 'clear sky'}]
        }
        
        response = self.assistant.generate_gpt_response("What's the weather?", weather_data)
        
        self.assertIsNotNone(response)
        self.assertIn('Tokyo', response)
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('openai.OpenAI')
    def test_generate_gpt_response_fallback(self, mock_openai):
        """Test GPT response generation falls back on error"""
        mock_openai.side_effect = Exception("OpenAI error")
        
        weather_data = {
            'name': 'Tokyo',
            'main': {'temp': 25, 'humidity': 60},
            'weather': [{'description': 'clear sky'}]
        }
        
        with self.assertRaises(Exception):
            self.assistant.generate_gpt_response("What's the weather?", weather_data)
    
    @patch('requests.get')
    def test_get_response_with_location(self, mock_get):
        """Test get_response with location extraction"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'Tokyo',
            'main': {'temp': 25, 'humidity': 60, 'feels_like': 27},
            'weather': [{'description': 'clear sky'}]
        }
        mock_get.return_value = mock_response
        
        response = self.assistant.get_response("What's the weather in Tokyo?")
        
        self.assertIsNotNone(response)
        self.assertIn('Tokyo', response)
    
    @patch('requests.get')
    def test_get_response_without_location(self, mock_get):
        """Test get_response without location"""
        response = self.assistant.get_response("Hello")
        
        self.assertIsNotNone(response)
        self.assertIn('Hello', response)
    
    def test_advice_categories_completeness(self):
        """Test that all advice categories are present"""
        expected_categories = ['clothing', 'health', 'travel', 'outdoor']
        
        for category in expected_categories:
            self.assertIn(category, self.assistant.advice_categories)
            self.assertIn('hot', self.assistant.advice_categories[category])
            self.assertIn('cold', self.assistant.advice_categories[category])
            self.assertIn('mild', self.assistant.advice_categories[category])
            self.assertIn('rain', self.assistant.advice_categories[category])


class TestWeatherAssistantIntegration(unittest.TestCase):
    """Integration tests for WeatherAssistant"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.assistant = WeatherAssistant(
            openai_api_key=None,  # Disable GPT for integration tests
            weather_api_key='test_weather_key'
        )
    
    @patch('requests.get')
    def test_complete_qa_flow(self, mock_get):
        """Test complete Q&A flow from message to response"""
        # Mock weather API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'London',
            'main': {'temp': 15, 'humidity': 75, 'feels_like': 14},
            'weather': [{'description': 'light rain'}]
        }
        mock_get.return_value = mock_response
        
        # Test message
        user_message = "What's the weather like in London today?"
        
        # Get response
        response = self.assistant.get_response(user_message)
        
        # Verify response
        self.assertIsNotNone(response)
        self.assertIn('London', response)
        self.assertIn('15', response)
        self.assertIn('Actionable Advice', response)
        self.assertIn('Clothing', response)
        self.assertIn('waterproof', response.lower())


if __name__ == '__main__':
    unittest.main()
