"""
Voice Assistant Service for Accessibility
Supports text-to-speech and speech-to-text functionality
"""

import os
from typing import Optional, Dict
import json

class VoiceAssistant:
    """Voice assistant for accessibility features"""
    
    def __init__(self):
        self.enabled = False
        self.language = 'en'
        self.voice_settings = {
            'rate': 1.0,      # Speech rate (0.1 to 10)
            'pitch': 1.0,     # Speech pitch (0.1 to 2)
            'volume': 1.0,    # Speech volume (0.1 to 1)
            'voice': None     # Specific voice (if supported)
        }
        self.supported_languages = {
            'en': 'English',
            'ta': 'Tamil',
            'hi': 'Hindi',
            'te': 'Telugu',
            'ml': 'Malayalam',
            'kn': 'Kannada',
            'bn': 'Bengali',
            'mr': 'Marathi',
            'gu': 'Gujarati'
        }
    
    def enable(self):
        """Enable voice assistant"""
        self.enabled = True
    
    def disable(self):
        """Disable voice assistant"""
        self.enabled = False
    
    def is_enabled(self) -> bool:
        """Check if voice assistant is enabled"""
        return self.enabled
    
    def set_language(self, language: str) -> bool:
        """
        Set the language for voice assistant
        
        Args:
            language: Language code
            
        Returns:
            True if language was set successfully
        """
        if language in self.supported_languages:
            self.language = language
            return True
        return False
    
    def get_language(self) -> str:
        """Get current language"""
        return self.language
    
    def update_voice_settings(self, settings: Dict):
        """
        Update voice settings
        
        Args:
            settings: Dictionary of voice settings
        """
        for key, value in settings.items():
            if key in self.voice_settings:
                self.voice_settings[key] = value
    
    def get_voice_settings(self) -> Dict:
        """Get current voice settings"""
        return self.voice_settings.copy()
    
    def generate_tts_response(self, text: str, language: str = None) -> Dict:
        """
        Generate text-to-speech response for frontend
        
        Args:
            text: Text to be spoken
            language: Target language (defaults to current language)
            
        Returns:
            Dictionary with TTS configuration for frontend
        """
        lang = language or self.language
        
        return {
            'text': text,
            'language': lang,
            'language_name': self.supported_languages.get(lang, 'English'),
            'enabled': self.enabled,
            'settings': self.voice_settings
        }
    
    def generate_stt_config(self, language: str = None) -> Dict:
        """
        Generate speech-to-text configuration for frontend
        
        Args:
            language: Target language (defaults to current language)
            
        Returns:
            Dictionary with STT configuration for frontend
        """
        lang = language or self.language
        
        return {
            'language': lang,
            'language_name': self.supported_languages.get(lang, 'English'),
            'enabled': self.enabled,
            'continuous': False,
            'interim_results': True
        }
    
    def get_voice_commands(self, language: str = None) -> Dict:
        """
        Get supported voice commands in the specified language
        
        Args:
            language: Target language (defaults to current language)
            
        Returns:
            Dictionary of voice commands and their meanings
        """
        lang = language or self.language
        
        # Voice commands with multilingual support
        commands = {
            'en': {
                'weather': ['weather', 'what is the weather', 'current weather'],
                'temperature': ['temperature', 'how hot', 'how cold', 'temperature now'],
                'forecast': ['forecast', 'will it rain', 'weather tomorrow'],
                'wind': ['wind', 'wind speed', 'how windy'],
                'humidity': ['humidity', 'how humid'],
                'location': ['in', 'at', 'for', 'near'],
                'help': ['help', 'what can you do', 'commands'],
                'stop': ['stop', 'cancel', 'never mind'],
                'clear': ['clear', 'reset', 'start over']
            },
            'ta': {
                'weather': ['வானிலை', 'என்ன வானிலை', 'தற்போதைய வானிலை'],
                'temperature': ['வெப்பநிலை', 'எவ்வளவு சூடாக', 'எவ்வளவு குளிராக'],
                'forecast': ['முன்னறிவிப்பு', 'மழை பெய்யுமா', 'நாளை வானிலை'],
                'wind': ['காற்று', 'காற்று வேகம்', 'எவ்வளவு காற்று'],
                'humidity': ['ஈரப்பதம்', 'எவ்வளவு ஈரப்பதம்'],
                'location': ['இல்', 'அருகில்', 'வழியாக'],
                'help': ['உதவி', 'என்ன செய்யலாம்', 'கட்டளைகள்'],
                'stop': ['நிறுத்து', 'ரத்து செய்', 'வேண்டாம்'],
                'clear': ['அழி', 'மீண்டும் தொடங்கு', 'புதியதாக']
            },
            'hi': {
                'weather': ['मौसम', 'कैसा मौसम', 'वर्तमान मौसम'],
                'temperature': ['तापमान', 'कितना गर्म', 'कितना ठंडा'],
                'forecast': ['पूर्वानुमान', 'क्या बारिश होगी', 'कल मौसम'],
                'wind': ['हवा', 'हवा की गति', 'कितनी हवा'],
                'humidity': ['नमी', 'कितनी नमी'],
                'location': ['में', 'पर', 'के लिए', 'के पास'],
                'help': ['मदद', 'क्या कर सकते हैं', 'कमांड'],
                'stop': ['रुको', 'रद्द करो', 'ठीक है'],
                'clear': ['साफ़ करें', 'रीसेट करें', 'फिर से शुरू करें']
            },
            'te': {
                'weather': ['వాతావరణం', 'ఎలా వాతావరణం', 'ప్రస్తుత వాతావరణం'],
                'temperature': ['ఉష్ణోగ్రత', 'ఎంత వేడిగా', 'ఎంత చలిగా'],
                'forecast': ['అంచనా', 'వాన పడుతుందా', 'రేపు వాతావరణం'],
                'wind': ['గాలి', 'గాలి వేగం', 'ఎంత గాలి'],
                'humidity': ['తేమ', 'ఎంత తేమ'],
                'location': ['లో', 'దగ్గరలో', 'కోసం'],
                'help': ['సహాయం', 'ఏమి చేయగలరు', 'ఆదేశాలు'],
                'stop': ['ఆపివేయండి', 'రద్దు చేయండి', 'అవసరం లేదు'],
                'clear': ['తొలగండి', 'రీసెట్ చేయండి', 'మళ్లీ ప్రారంభించండి']
            },
            'ml': {
                'weather': ['കാലാവസ്ഥ', 'എങ്ങനെ കാലാവസ്ഥ', 'നിലവിലുള്ള കാലാവസ്ഥ'],
                'temperature': ['താപനില', 'എത്ര ചൂടാണ്', 'എത്ര തണുപ്പാണ്'],
                'forecast': ['പ്രവചനം', 'മഴ പെയ്യുമോ', 'നാളെ കാലാവസ്ഥ'],
                'wind': ['കാറ്റ്', 'കാറ്റിന്റെ വേഗത', 'എത്ര കാറ്റ്'],
                'humidity': ['ഈർപ്പം', 'എത്ര ഈർപ്പം'],
                'location': ['ഇൽ', 'അടുത്ത്', 'വേണ്ടി'],
                'help': ['സഹായം', 'എന്ത് ചെയ്യാം', 'കമാൻഡുകൾ'],
                'stop': ['നിർത്തുക', 'റദ്ദു ചെയ്യുക', 'വേണ്ട'],
                'clear': ['മായ്ക്കുക', 'പുനഃസജ്ജമാക്കുക', 'വീണ്ടും തുടങ്ങുക']
            },
            'kn': {
                'weather': ['ಹವಾಮಾನ', 'ಹೇಗಿದೆ ಹವಾಮಾನ', 'ಪ್ರಸ್ತುತ ಹವಾಮಾನ'],
                'temperature': ['ತಾಪಮಾನ', 'ಎಷ್ಟು ಬಿಸಿ', 'ಎಷ್ಟು ತಣ್ಣಗೆ'],
                'forecast': ['ಮುನ್ಸೂಚನೆ', 'ಮಳೆ ಬರುತ್ತದೆಯಾ', 'ನಾಳೆ ಹವಾಮಾನ'],
                'wind': ['ಗಾಳಿ', 'ಗಾಳಿಯ ವೇಗ', 'ಎಷ್ಟು ಗಾಳಿ'],
                'humidity': ['ಆರ್ದ್ರತೆ', 'ಎಷ್ಟು ಆರ್ದ್ರತೆ'],
                'location': ['ನಲ್ಲಿ', 'ಹತ್ತಾರ', 'ಕಡೆಗೆ'],
                'help': ['ಸಹಾಯ', 'ಏನು ಮಾಡಬಹುದು', 'ಆದೇಶಗಳು'],
                'stop': ['ನಿಲ್ಲಿಸಿ', 'ರದ್ದು ಮಾಡಿ', 'ಬೇಕು'],
                'clear': ['ಅಳಿಸಿ', 'ಮರು ಹೊಂದಿಸಿ', 'ಮತ್ತ್ತೆ ಪ್ರಾರಂಭಿಸಿ']
            },
            'bn': {
                'weather': ['আবহাওয়া', 'কেমন আবহাওয়া', 'বর্তমান আবহাওয়া'],
                'temperature': ['তাপমাত্রা', 'কতটা গরম', 'কতটা ঠান্ডা'],
                'forecast': ['পূর্বাভাস', 'বৃষ্টি হবে কি', 'কাল আবহাওয়া'],
                'wind': ['বাতাস', 'বাতাসের গতি', 'কতটা বাতাস'],
                'humidity': ['আর্দ্রতা', 'কতটা আর্দ্রতা'],
                'location': ['এ', 'কাছে', 'জন্য'],
                'help': ['সাহায্য', 'কী করতে পারি', 'কমান্ড'],
                'stop': ['থামুন', 'বাতিল করুন', 'ঠিক আছে'],
                'clear': ['মুছুন', 'রিসেট করুন', 'আবার শুরু করুন']
            },
            'mr': {
                'weather': ['हवामान', 'कसा हवामान', 'वर्तमान हवामान'],
                'temperature': ['तापमान', 'किती उष्ण', 'किती थंड'],
                'forecast': ['अंदाज', 'पाऊस पडेल का', 'उद्या हवामान'],
                'wind': ['वारा', 'वाऱ्याची वेग', 'किती वारा'],
                'humidity': ['आर्द्रता', 'किती आर्द्रता'],
                'location': ['मध्ये', 'जवळ', 'साठी'],
                'help': ['मदत', 'काय करू', 'आदेश'],
                'stop': ['थांबा', 'रद्द करा', 'ठीक आहे'],
                'clear': ['साफ करा', 'रीसेट करा', 'पुन्हा सुरू करा']
            },
            'gu': {
                'weather': ['હવામાન', 'કેવું હવામાન', 'વર્તમાન હવામાન'],
                'temperature': ['તાપમાન', 'કેટું ગરમ', 'કેટું ઠંડુ'],
                'forecast': ['અંદાજ', 'વરસાદ પડશે', 'કાલે હવામાન'],
                'wind': ['પવન', 'પવનની ગતિ', 'કેટું પવન'],
                'humidity': ['ભેજાપણ', 'કેટું ભેજાપણ'],
                'location': ['માં', 'નજીક', 'માટે'],
                'help': ['મદદ', 'શું કરી શકું', 'આદેશો'],
                'stop': ['બંધ કરો', 'રદ કરો', 'ઠીક છે'],
                'clear': ['સાફ કરો', 'રીસેટ કરો', 'ફરી શરૂ કરો']
            }
        }
        
        return commands.get(lang, commands['en'])
    
    def parse_voice_command(self, text: str, language: str = None) -> Dict:
        """
        Parse voice command and extract intent
        
        Args:
            text: Spoken text
            language: Language code
            
        Returns:
            Dictionary with parsed command intent
        """
        lang = language or self.language
        text_lower = text.lower()
        
        commands = self.get_voice_commands(lang)
        
        # Detect command intent
        intent = None
        confidence = 0.0
        
        for command_type, keywords in commands.items():
            for keyword in keywords:
                if keyword in text_lower:
                    intent = command_type
                    confidence = 0.8  # Simple confidence score
                    break
            if intent:
                break
        
        # Extract location if present
        location = self._extract_location(text, lang)
        
        return {
            'intent': intent,
            'confidence': confidence,
            'location': location,
            'original_text': text,
            'language': lang
        }
    
    def _extract_location(self, text: str, language: str) -> Optional[str]:
        """
        Extract location from spoken text
        
        Args:
            text: Spoken text
            language: Language code
            
        Returns:
            Extracted location or None
        """
        # Simple location extraction - in production, use NLP
        location_keywords = {
            'en': ['in', 'at', 'for', 'near'],
            'ta': ['இல்', 'அருகில்', 'வழியாக'],
            'hi': ['में', 'पर', 'के लिए', 'के पास'],
            'te': ['లో', 'దగ్గరలో', 'కోసం'],
            'ml': ['ഇൽ', 'അടുത്ത്', 'വേണ്ടി'],
            'kn': ['ನಲ್ಲಿ', 'ಹತ್ತಾರ', 'ಕಡೆಗೆ'],
            'bn': ['এ', 'কাছে', 'জন্য'],
            'mr': ['मध्ये', 'जवळ', 'साठी'],
            'gu': ['માં', 'નજીક', 'માટે']
        }
        
        keywords = location_keywords.get(language, location_keywords['en'])
        
        for keyword in keywords:
            if keyword in text.lower():
                parts = text.lower().split(keyword)
                if len(parts) > 1:
                    potential_location = parts[1].strip()
                    # Remove common stop words
                    stop_words = ['what', 'the', 'weather', 'like', 'is', 'tell', 'me', 'please']
                    for word in stop_words:
                        potential_location = potential_location.replace(word, '').strip()
                    
                    if potential_location and len(potential_location) > 2:
                        return potential_location.title()
        
        return None
    
    def get_accessibility_features(self) -> Dict:
        """
        Get accessibility features configuration
        
        Returns:
            Dictionary with accessibility settings
        """
        return {
            'voice_assistant': {
                'enabled': self.enabled,
                'language': self.language,
                'supported_languages': self.supported_languages,
                'voice_settings': self.voice_settings
            },
            'multilingual_support': {
                'enabled': True,
                'current_language': self.language,
                'auto_detect': False
            },
            'high_contrast': {
                'enabled': False
            },
            'text_size': {
                'current': 'medium',
                'options': ['small', 'medium', 'large', 'extra-large']
            }
        }


# Global voice assistant instance
voice_assistant = VoiceAssistant()