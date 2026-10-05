"""
Unit tests for Weather Assistant Q&A flow
Tests the modular weather assistant service
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from services.weather_assistant import WeatherAssistant


class TestWeatherAssistant(unittest.TestCase):
    """Test suite for WeatherAssistant class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.assistant = WeatherAssistant(
            openai_api_key='test_openai_key',
            weather_api_key='test_weather_key'
        )
    
    def test_extract_location_with_keyword(self):
        """Test location extraction with common keywords"""
        test_cases = [
            ("What's the weather in London?", "London"),
            ("Weather at Paris", "Paris"),
            ("How is the weather for Tokyo", "Tokyo"),
            ("Weather near New York", "New York"),
        ]
        
        for message, expected_location in test_cases:
            with self.subTest(message=message):
                result = self.assistant.extract_location(message)
                self.assertEqual(result, expected_location)
    
    def test_extract_location_without_keyword(self):
        """Test location extraction without keywords returns None"""
        message = "Hello, how are you?"
        result = self.assistant.extract_location(message)
        self.assertIsNone(result)
    
    def test_extract_location_short_location(self):
        """Test that short location names (< 3 chars) are rejected"""
        message = "Weather in NY"
        result = self.assistant.extract_location(message)
        # Should return None or the cleaned version if it's too short
        self.assertIsNone(result)
    
    @patch('services.weather_assistant.requests.get')
    def test_get_weather_data_success(self, mock_get):
        """Test successful weather data retrieval"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'London',
            'main': {
                'temp': 20,
                'humidity': 65,
                'feels_like': 19
            },
            'weather': [
                {'description': 'clear sky'}
            ],
            'wind': {'speed': 5},
            'visibility': 10000
        }
        mock_get.return_value = mock_response
        
        result = self.assistant.get_weather_data('London')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'London')
        self.assertEqual(result['main']['temp'], 20)
        mock_get.assert_called_once()
    
    @patch('services.weather_assistant.requests.get')
    def test_get_weather_data_failure(self, mock_get):
        """Test weather data retrieval failure"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = self.assistant.get_weather_data('InvalidCity')
        
        self.assertIsNone(result)
    
    @patch('services.weather_assistant.requests.get')
    def test_get_weather_data_exception(self, mock_get):
        """Test weather data retrieval with exception"""
        mock_get.side_effect = Exception('Network error')
        
        result = self.assistant.get_weather_data('London')
        
        self.assertIsNone(result)
    
    def test_generate_actionable_advice_hot_weather(self):
        """Test actionable advice generation for hot weather"""
        weather_data = {
            'main': {'temp': 35, 'humidity': 50},
            'weather': [{'description': 'clear sky'}],
            'wind': {'speed': 5},
            'visibility': 10000
        }
        
        advice = self.assistant.generate_actionable_advice(weather_data)
        
        self.assertIsInstance(advice, list)
        self.assertTrue(any('hot' in tip.lower() or 'hydrated' in tip.lower() for tip in advice))
    
    def test_generate_actionable_advice_cold_weather(self):
        """Test actionable advice generation for cold weather"""
        weather_data = {
            'main': {'temp': 0, 'humidity': 70},
            'weather': [{'description': 'snow'}],
            'wind': {'speed': 10},
            'visibility': 5000
        }
        
        advice = self.assistant.generate_actionable_advice(weather_data)
        
        self.assertIsInstance(advice, list)
        self.assertTrue(any('cold' in tip.lower() or 'layer' in tip.lower() or 'warm' in tip.lower() for tip in advice))
    
    def test_generate_actionable_advice_rain(self):
        """Test actionable advice generation for rainy weather"""
        weather_data = {
            'main': {'temp': 18, 'humidity': 85},
            'weather': [{'description': 'rain'}],
            'wind': {'speed': 8},
            'visibility': 8000
        }
        
        advice = self.assistant.generate_actionable_advice(weather_data)
        
        self.assertIsInstance(advice, list)
        self.assertTrue(any('umbrella' in tip.lower() or 'raincoat' in tip.lower() for tip in advice))
    
    def test_generate_actionable_advice_storm(self):
        """Test actionable advice generation for stormy weather"""
        weather_data = {
            'main': {'temp': 22, 'humidity': 90},
            'weather': [{'description': 'thunderstorm'}],
            'wind': {'speed': 25},
            'visibility': 3000
        }
        
        advice = self.assistant.generate_actionable_advice(weather_data)
        
        self.assertIsInstance(advice, list)
        self.assertTrue(any('storm' in tip.lower() or 'indoors' in tip.lower() for tip in advice))
    
    def test_generate_actionable_advice_pleasant_weather(self):
        """Test actionable advice generation for pleasant weather"""
        weather_data = {
            'main': {'temp': 24, 'humidity': 55},
            'weather': [{'description': 'clear sky'}],
            'wind': {'speed': 3},
            'visibility': 10000
        }
        
        advice = self.assistant.generate_actionable_advice(weather_data)
        
        self.assertIsInstance(advice, list)
        self.assertTrue(any('outdoor' in tip.lower() or 'clear' in tip.lower() for tip in advice))
    
    def test_generate_rule_based_response_with_weather(self):
        """Test rule-based response generation with weather data"""
        weather_data = {
            'main': {'temp': 25, 'humidity': 60, 'feels_like': 26},
            'weather': [{'description': 'clear sky'}],
            'name': 'London'
        }
        
        response = self.assistant.generate_rule_based_response(
            "What's the weather in London?",
            weather_data
        )
        
        self.assertIsInstance(response, str)
        self.assertIn('London', response)
        self.assertIn('25', response)
        self.assertIn('Advice', response)
    
    def test_generate_rule_based_response_without_weather(self):
        """Test rule-based response generation without weather data"""
        test_cases = [
            ("Hello", "hello"),
            ("Hi there", "hi"),
            ("Help me", "help"),
        ]
        
        for message, keyword in test_cases:
            with self.subTest(message=message):
                response = self.assistant.generate_rule_based_response(message, None)
                self.assertIsInstance(response, str)
                self.assertIn(keyword, response.lower())
    
    def test_generate_rule_based_response_unknown_query(self):
        """Test rule-based response for unknown queries"""
        response = self.assistant.generate_rule_based_response("Random text", None)
        
        self.assertIsInstance(response, str)
        self.assertIn('location', response.lower())
    
    @patch('services.weather_assistant.requests.get')
    def test_process_query_with_location(self, mock_get):
        """Test query processing with a valid location"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'London',
            'main': {'temp': 20, 'humidity': 65, 'feels_like': 19},
            'weather': [{'description': 'clear sky'}]
        }
        mock_get.return_value = mock_response
        
        result = self.assistant.process_query("What's the weather in London?")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['location'], 'London')
        self.assertIn('response', result)
        self.assertIn('weather_data', result)
    
    @patch('services.weather_assistant.requests.get')
    def test_process_query_invalid_location(self, mock_get):
        """Test query processing with invalid location"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = self.assistant.process_query("What's the weather in InvalidCity?")
        
        self.assertFalse(result['success'])
        self.assertEqual(result['location'], 'Invalidcity')
        self.assertIn('response', result)
    
    def test_process_query_without_location(self):
        """Test query processing without location"""
        result = self.assistant.process_query("Hello!")
        
        self.assertTrue(result['success'])
        self.assertIsNone(result['location'])
        self.assertIn('response', result)
    
    @patch('services.weather_assistant.requests.get')
    def test_process_query_exception_handling(self, mock_get):
        """Test query processing with exception"""
        mock_get.side_effect = Exception('Network error')
        
        result = self.assistant.process_query("What's the weather in London?")
        
        self.assertFalse(result['success'])
        self.assertIn('response', result)
    
    def test_initialization_with_api_keys(self):
        """Test assistant initialization with API keys"""
        assistant = WeatherAssistant(
            openai_api_key='test_key',
            weather_api_key='test_weather_key'
        )
        
        self.assertEqual(assistant.openai_api_key, 'test_key')
        self.assertEqual(assistant.weather_api_key, 'test_weather_key')
        self.assertTrue(assistant.use_gpt)
    
    def test_initialization_without_valid_openai_key(self):
        """Test assistant initialization without valid OpenAI key"""
        assistant = WeatherAssistant(
            openai_api_key='your_openai_api_key',
            weather_api_key='test_weather_key'
        )
        
        self.assertFalse(assistant.use_gpt)
    
    def test_initialization_with_env_vars(self):
        """Test assistant initialization using environment variables"""
        import os
        os.environ['OPENAI_API_KEY'] = 'env_openai_key'
        os.environ['WEATHER_API_KEY'] = 'env_weather_key'
        
        assistant = WeatherAssistant()
        
        self.assertEqual(assistant.openai_api_key, 'env_openai_key')
        self.assertEqual(assistant.weather_api_key, 'env_weather_key')
        
        # Clean up
        del os.environ['OPENAI_API_KEY']
        del os.environ['WEATHER_API_KEY']


class TestWeatherAssistantGPT(unittest.TestCase):
    """Test suite for WeatherAssistant GPT integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.assistant = WeatherAssistant(
            openai_api_key='test_openai_key',
            weather_api_key='test_weather_key'
        )
    
    @patch('services.weather_assistant.openai')
    def test_generate_gpt_response_success(self, mock_openai):
        """Test successful GPT response generation"""
        mock_client = MagicMock()
        mock_openai.OpenAI.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "It's a beautiful day in London!"
        mock_client.chat.completions.create.return_value = mock_response
        
        weather_data = {
            'name': 'London',
            'main': {'temp': 20, 'humidity': 65, 'feels_like': 19},
            'weather': [{'description': 'clear sky'}],
            'wind': {'speed': 5}
        }
        
        response = self.assistant.generate_gpt_response(
            "What's the weather?",
            weather_data
        )
        
        self.assertEqual(response, "It's a beautiful day in London!")
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('services.weather_assistant.openai')
    def test_generate_gpt_response_fallback(self, mock_openai):
        """Test GPT response fallback on error"""
        mock_openai.OpenAI.side_effect = Exception('API error')
        
        weather_data = {
            'name': 'London',
            'main': {'temp': 20, 'humidity': 65, 'feels_like': 19},
            'weather': [{'description': 'clear sky'}]
        }
        
        response = self.assistant.generate_gpt_response(
            "What's the weather?",
            weather_data
        )
        
        # Should fallback to rule-based response
        self.assertIsInstance(response, str)
        self.assertIn('London', response)


if __name__ == '__main__':
    unittest.main()
