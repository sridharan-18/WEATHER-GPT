"""
Translation Service for Multilingual Support
Supports Tamil and other Indian regional languages
"""

import json
import os
from typing import Dict, Optional

class TranslationService:
    """Service for handling translations and language management"""
    
    def __init__(self):
        self.current_language = 'en'
        self.translations = self._load_translations()
        self.supported_languages = {
            'en': 'English',
            'ta': 'Tamil (தமிழ்)',
            'hi': 'Hindi (हिंदी)',
            'te': 'Telugu (తెలుగు)',
            'ml': 'Malayalam (മലയാളം)',
            'kn': 'Kannada (ಕನ್ನಡ)',
            'bn': 'Bengali (বাংলা)',
            'mr': 'Marathi (मराठी)',
            'gu': 'Gujarati (ગુજરાતી)'
        }
    
    def _load_translations(self) -> Dict:
        """Load translation dictionaries"""
        return {
            'en': self._get_english_translations(),
            'ta': self._get_tamil_translations(),
            'hi': self._get_hindi_translations(),
            'te': self._get_telugu_translations(),
            'ml': self._get_malayalam_translations(),
            'kn': self._get_kannada_translations(),
            'bn': self._get_bengali_translations(),
            'mr': self._get_marathi_translations(),
            'gu': self._get_gujarati_translations()
        }
    
    def _get_english_translations(self) -> Dict:
        """English translations (source language)"""
        return {
            # Common UI elements
            'app_title': 'Weather GPT',
            'search_placeholder': 'Search location...',
            'get_weather': 'Get Weather',
            'current_weather': 'Current Weather',
            'temperature': 'Temperature',
            'humidity': 'Humidity',
            'wind_speed': 'Wind Speed',
            'visibility': 'Visibility',
            'pressure': 'Pressure',
            'feels_like': 'Feels Like',
            'weather_conditions': 'Weather Conditions',
            'hazard_map': 'Hazard Map',
            'flood_risk': 'Flood Risk',
            'heat_risk': 'Heat Risk',
            'lightning_risk': 'Lightning Risk',
            'visibility_risk': 'Visibility Risk',
            'safety_score': 'Safety Score',
            'risk_level': 'Risk Level',
            'safe': 'Safe',
            'low_risk': 'Low Risk',
            'moderate_risk': 'Moderate Risk',
            'high_risk': 'High Risk',
            'critical_risk': 'Critical Risk',
            
            # Chat interface
            'chat_title': 'Weather Assistant',
            'chat_placeholder': 'Ask about weather...',
            'send_message': 'Send',
            'voice_input': 'Voice Input',
            'voice_output': 'Voice Output',
            
            # Weather conditions
            'clear_sky': 'Clear Sky',
            'few_clouds': 'Few Clouds',
            'scattered_clouds': 'Scattered Clouds',
            'broken_clouds': 'Broken Clouds',
            'overcast_clouds': 'Overcast Clouds',
            'light_rain': 'Light Rain',
            'moderate_rain': 'Moderate Rain',
            'heavy_rain': 'Heavy Rain',
            'thunderstorm': 'Thunderstorm',
            'snow': 'Snow',
            'mist': 'Mist',
            'fog': 'Fog',
            
            # Advice messages
            'advice_hot': 'It\'s quite hot! Stay hydrated and avoid direct sunlight.',
            'advice_cold': 'It\'s chilly - dress warmly!',
            'advice_very_cold': 'It\'s very cold! Wear heavy layers and protect exposed skin.',
            'advice_high_humidity': 'High humidity - it might feel muggy. Consider staying indoors.',
            'advice_low_humidity': 'Low humidity - stay moisturized and drink plenty of water.',
            'advice_rain': 'Don\'t forget an umbrella or raincoat!',
            'advice_clear': 'Great weather for outdoor activities!',
            'advice_cloudy': 'Partly cloudy - pleasant weather overall.',
            'advice_storm': 'Stormy conditions - stay indoors and avoid travel if possible.',
            
            # Agricultural terms
            'agriculture': 'Agriculture',
            'crop_recommendations': 'Crop Recommendations',
            'irrigation': 'Irrigation',
            'harvest': 'Harvest',
            'storm_impact': 'Storm Impact',
            'action_plan': 'Action Plan',
            
            # Notifications
            'subscribe': 'Subscribe',
            'unsubscribe': 'Unsubscribe',
            'notifications': 'Notifications',
            'daily_digest': 'Daily Digest',
            'severe_weather_alert': 'Severe Weather Alert',
            
            # Language
            'language': 'Language',
            'select_language': 'Select Language',
            
            # Voice commands
            'voice_command_listening': 'Listening...',
            'voice_command_speaking': 'Speaking...',
            'voice_command_error': 'Voice recognition error',
            'voice_command_not_supported': 'Voice commands not supported in this browser'
        }
    
    def _get_tamil_translations(self) -> Dict:
        """Tamil translations"""
        return {
            # Common UI elements
            'app_title': 'வானிலை GPT',
            'search_placeholder': 'இடத்தைத் தேடுங்கள்...',
            'get_weather': 'வானிலை பெறு',
            'current_weather': 'தற்போதைய வானிலை',
            'temperature': 'வெப்பநிலை',
            'humidity': 'ஈரப்பதம்',
            'wind_speed': 'காற்று வேகம்',
            'visibility': 'புலப்பாடு',
            'pressure': 'அழுத்தம்',
            'feels_like': 'உணர்வு',
            'weather_conditions': 'வானிலை நிலைமைகள்',
            'hazard_map': 'ஆபத்து வரைபடம்',
            'flood_risk': 'வெள்ளப் பெருக்கு ஆபத்து',
            'heat_risk': 'வெப்ப ஆபத்து',
            'lightning_risk': 'மின்னல் ஆபத்து',
            'visibility_risk': 'புலப்பாடு ஆபத்து',
            'safety_score': 'பாதுகாப்பு மதிப்பெண்',
            'risk_level': 'ஆபத்து நிலை',
            'safe': 'பாதுகாப்பானது',
            'low_risk': 'குறைந்த ஆபத்து',
            'moderate_risk': 'மிதமான ஆபத்து',
            'high_risk': 'அதிக ஆபத்து',
            'critical_risk': 'மிகவும் அதிக ஆபத்து',
            
            # Chat interface
            'chat_title': 'வானிலை உதவியாளர்',
            'chat_placeholder': 'வானிலை பற்றி கேளுங்கள்...',
            'send_message': 'அனுப்பு',
            'voice_input': 'குரல் உள்ளீடு',
            'voice_output': 'குரல் வெளியீடு',
            
            # Weather conditions
            'clear_sky': 'தெளிந்த வானம்',
            'few_clouds': 'சில மேகங்கள்',
            'scattered_clouds': 'சிதறிய மேகங்கள்',
            'broken_clouds': 'உடைந்த மேகங்கள்',
            'overcast_clouds': 'மேகமூட்டமான வானம்',
            'light_rain': 'லேசான மழை',
            'moderate_rain': 'மிதமான மழை',
            'heavy_rain': 'கனமழை',
            'thunderstorm': 'இடியுடன் கூடிய மழை',
            'snow': 'பனி',
            'mist': 'மூடு',
            'fog': 'பனிமூட்டம்',
            
            # Advice messages
            'advice_hot': 'மிகவும் சூடாக உள்ளது! நீர் அருந்தி, நேரடி சூரியனிலிருந்து தவிருங்கள்.',
            'advice_cold': 'குளிராக உள்ளது - சூடான ஆடை அணியுங்கள்!',
            'advice_very_cold': 'மிகவும் குளிராக உள்ளது! கனமான ஆடைகள் அணியுங்கள் மற்றும் தோலைப் பாதுகாக்குங்கள்.',
            'advice_high_humidity': 'அதிக ஈரப்பதம் - ஈரமாக உணரலாம். வீட்டிலேயே இருக்க விரும்புங்கள்.',
            'advice_low_humidity': 'குறைந்த ஈரப்பதம் - ஈரப்பதான முறையில் இருங்கள் மற்றும் நிறைய நீர் அருந்துங்கள்.',
            'advice_rain': 'குடை அல்லது மழை அங்கி மறவுங்கள்!',
            'advice_clear': 'வெளிப்புற செயல்பாடுகளுக்கு சிறந்த வானிலை!',
            'advice_cloudy': 'பகுதி மேகமூட்டம் - ஒட்டுமொத்தமாக நல்ல வானிலை.',
            'advice_storm': 'புயல் நிலைமைகள் - வீட்டிலேயே இருங்கள் மற்றும் சாத்தியமானால் பயணம் செய்யவும்.',
            
            # Agricultural terms
            'agriculture': 'வேளாண்மை',
            'crop_recommendations': 'பயிர் பரிந்துரைகள்',
            'irrigation': 'நீர்ப்பாசனம்',
            'harvest': 'அறுவடை',
            'storm_impact': 'புயல் தாக்கம்',
            'action_plan': 'செயல் திட்டம்',
            
            # Notifications
            'subscribe': 'பதிவு செய்',
            'unsubscribe': 'பதிவு நீக்கு',
            'notifications': 'அறிவிப்புகள்',
            'daily_digest': 'அன்றாட சுருக்கம்',
            'severe_weather_alert': 'கடுமையான வானிலை எச்சரிக்கை',
            
            # Language
            'language': 'மொழி',
            'select_language': 'மொழியைத் தேர்ந்தெடுக்கவும்',
            
            # Voice commands
            'voice_command_listening': 'கேட்கிறது...',
            'voice_command_speaking': 'பேசுகிறது...',
            'voice_command_error': 'குரல் அங்கீகாரப் பிழை',
            'voice_command_not_supported': 'இந்த உலாவியில் குரல் கட்டளைகள் ஆதரிக்கப்படவில்லை'
        }
    
    def _get_hindi_translations(self) -> Dict:
        """Hindi translations"""
        return {
            'app_title': 'मौसम GPT',
            'search_placeholder': 'स्थान खोजें...',
            'get_weather': 'मौसम प्राप्त करें',
            'current_weather': 'वर्तमान मौसम',
            'temperature': 'तापमान',
            'humidity': 'नमी',
            'wind_speed': 'हवा की गति',
            'visibility': 'दृश्यता',
            'pressure': 'दबाव',
            'feels_like': 'महसूस',
            'weather_conditions': 'मौसम की स्थिति',
            'hazard_map': 'खतरा मानचित्र',
            'flood_risk': 'बाढ़ का खतरा',
            'heat_risk': 'गर्मी का खतरा',
            'lightning_risk': 'बिजली का खतरा',
            'visibility_risk': 'दृश्यता का खतरा',
            'safety_score': 'सुरक्षा स्कोर',
            'risk_level': 'जोखिम स्तर',
            'safe': 'सुरक्षित',
            'low_risk': 'कम जोखिम',
            'moderate_risk': 'मध्यम जोखिम',
            'high_risk': 'उच्च जोखिम',
            'critical_risk': 'गंभीर जोखिम',
            'chat_title': 'मौसम सहायक',
            'chat_placeholder': 'मौसम के बारे में पूछें...',
            'send_message': 'भेजें',
            'voice_input': 'आवाज़ इनपुट',
            'voice_output': 'आवाज़ आउटपुट',
            'clear_sky': 'साफ आसमान',
            'few_clouds': 'कुछ बादल',
            'scattered_clouds': 'बिखरे बादल',
            'broken_clouds': 'टूटे बादल',
            'overcast_clouds': 'घने बादल',
            'light_rain': 'हल्की बारिश',
            'moderate_rain': 'मध्यम बारिश',
            'heavy_rain': 'भारी बारिश',
            'thunderstorm': 'आंधी-तूफान',
            'snow': 'बर्फ',
            'mist': 'धुंध',
            'fog': 'कोहरा',
            'advice_hot': 'बहुत गर्म है! पानी पिएं और धूप से बचें।',
            'advice_cold': 'ठंडा है - गर्म कपड़े पहनें!',
            'advice_very_cold': 'बहुत ठंडा है! मोटे कपड़े पहनें और त्वचा की रक्षा करें।',
            'advice_high_humidity': 'उच्च नमी - गीला महसूस हो सकता है। घर में रहें।',
            'advice_low_humidity': 'कम नमी - नमी बनाए रखें और खूब पानी पिएं।',
            'advice_rain': 'छाता या रेनकोट न भूलें!',
            'advice_clear': 'बाहरी गतिविधियों के लिए अच्छा मौसम!',
            'advice_cloudy': 'आंशिक बादल - समग्र रूप से अच्छा मौसम।',
            'advice_storm': 'तूफानी स्थितियां - घर में रहें और संभव हो तो यात्रा से बचें।',
            'agriculture': 'कृषि',
            'crop_recommendations': 'फसल अनुशंसाएं',
            'irrigation': 'सिंचाई',
            'harvest': 'फसल कटाई',
            'storm_impact': 'तूफान प्रभाव',
            'action_plan': 'कार्य योजना',
            'subscribe': 'सदस्यता लें',
            'unsubscribe': 'सदस्यता रद्द करें',
            'notifications': 'सूचनाएं',
            'daily_digest': 'दैनिक सारांश',
            'severe_weather_alert': 'गंभीर मौसम चेतावनी',
            'language': 'भाषा',
            'select_language': 'भाषा चुनें',
            'voice_command_listening': 'सुन रहा हूं...',
            'voice_command_speaking': 'बोल रहा हूं...',
            'voice_command_error': 'आवाज़ पहचान त्रुटि',
            'voice_command_not_supported': 'इस ब्राउज़र में आवाज़ कमांड समर्थित नहीं है'
        }
    
    def _get_telugu_translations(self) -> Dict:
        """Telugu translations"""
        return {
            'app_title': 'వాతావరణ GPT',
            'search_placeholder': 'స్థానాన్ని శోధించండి...',
            'get_weather': 'వాతావరణం పొందండి',
            'current_weather': 'ప్రస్తుత వాతావరణం',
            'temperature': 'ఉష్ణోగ్రత',
            'humidity': 'తేమ',
            'wind_speed': 'గాలి వేగం',
            'visibility': 'దృశ్యత',
            'pressure': 'పీడనం',
            'feels_like': 'అనిసరించబడుతుంది',
            'weather_conditions': 'వాతావరణ పరిస్థితులు',
            'hazard_map': 'హాని మ్యాప్',
            'flood_risk': 'వరద ప్రమాదం',
            'heat_risk': 'వేడి ప్రమాదం',
            'lightning_risk': 'మెరుగుల ప్రమాదం',
            'visibility_risk': 'దృశ్యత ప్రమాదం',
            'safety_score': 'భద్రతా స్కోరు',
            'risk_level': 'ప్రమాద స్థాయి',
            'safe': 'సురక్షితం',
            'low_risk': 'తక్కువ ప్రమాదం',
            'moderate_risk': 'మధ్యమ ప్రమాదం',
            'high_risk': 'అధిక ప్రమాదం',
            'critical_risk': 'తీవ్ర ప్రమాదం',
            'chat_title': 'వాతావరణ సహాయకుడు',
            'chat_placeholder': 'వాతావరణ గురించి అడిగండి...',
            'send_message': 'పంపండి',
            'voice_input': 'వాయిస్ ఇన్‌పుట్',
            'voice_output': 'వాయిస్ అవుట్‌పుట్',
            'clear_sky': 'స్పష్టమైన ఆకాశం',
            'few_clouds': 'కొన్ని మేఘాలు',
            'scattered_clouds': 'చెదిరిన మేఘాలు',
            'broken_clouds': 'విరిగిన మేఘాలు',
            'overcast_clouds': 'మేఘావృత ఆకాశం',
            'light_rain': 'తేలిక వాన',
            'moderate_rain': 'మధ్యమ వాన',
            'heavy_rain': 'భారీ వాన',
            'thunderstorm': 'తుఫాను',
            'snow': 'మంచు',
            'mist': 'పొగమరుగు',
            'fog': 'పొగ',
            'advice_hot': 'చాలా వేడిగా ఉంది! నీటిని తాగండి మరియు నేరిటి సూర్యరశ్మి నుండి దూరంగా ఉండండి.',
            'advice_cold': 'చలిగా ఉంది - వెచ్చని బట్టులు ధరించండి!',
            'advice_very_cold': 'చాలా చలిగా ఉంది! భారీ బట్టులు ధరించండి మరియు చర్మాన్ని రక్షించండి.',
            'advice_high_humidity': 'అధిక తేమ - తేమగా అనిపించవచ్చు. ఇంట్లోనే ఉండండి.',
            'advice_low_humidity': 'తక్కువ తేమ - తేమగా ఉండండి మరియు ఎక్కువ నీటిని తాగండి.',
            'advice_rain': 'గొడుగు లేదా వర్షావస్త్రాన్ని మరవండి!',
            'advice_clear': 'బాహ్య కార్యక్రమాలకు అద్భుతమైన వాతావరణం!',
            'advice_cloudy': 'పాక్షిక మేఘావృతం - మొత్తంగా ఆహ్లాదకరమైన వాతావరణం.',
            'advice_storm': 'తుఫాను పరిస్థితులు - ఇంట్లోనే ఉండండి మరియు సాధ్యమైతే ప్రయాణించవద్దు.',
            'agriculture': 'వ్యవసాయం',
            'crop_recommendations': 'పంట సిఫార్సులు',
            'irrigation': 'నీటిపారుదల',
            'harvest': 'పంట కోత',
            'storm_impact': 'తుఫాను ప్రభావం',
            'action_plan': 'చర్యా ప్రణాలి',
            'subscribe': 'చందాసదస్యుడవ్వడం',
            'unsubscribe': 'చందాసదస్యతను రద్దు చేయండి',
            'notifications': 'నోటిఫికేషన్లు',
            'daily_digest': 'రోజువారీ సారాంశం',
            'severe_weather_alert': 'తీవ్ర వాతావరణ హెచ్చరిక',
            'language': 'భాష',
            'select_language': 'భాషను ఎంచుకోండి',
            'voice_command_listening': 'వింటోంది...',
            'voice_command_speaking': 'మాట్లాడుతోంది...',
            'voice_command_error': 'వాయిస్ గుర్తింపు లోపం',
            'voice_command_not_supported': 'ఈ బ్రౌజర్‌లో వాయిస్ కమాండ్‌లు మద్దతు లేదు'
        }
    
    def _get_malayalam_translations(self) -> Dict:
        """Malayalam translations"""
        return {
            'app_title': 'കാലാവസ്ഥ GPT',
            'search_placeholder': 'സ്ഥലം തിരയുക...',
            'get_weather': 'കാലാവസ്ഥ നേടുക',
            'current_weather': 'നിലവിലുള്ള കാലാവസ്ഥ',
            'temperature': 'താപനില',
            'humidity': 'ഈർപ്പം',
            'wind_speed': 'കാറ്റിന്റെ വേഗത',
            'visibility': 'ദൃശ്യത',
            'pressure': 'മർദ്ദം',
            'feels_like': 'തോന്നുന്നു',
            'weather_conditions': 'കാലാവസ്ഥ സാഹചര്യങ്ങൾ',
            'hazard_map': 'അപകട മാപ്പ്',
            'flood_risk': 'വെള്ളപ്പൊട്ട് അപകടം',
            'heat_risk': 'ചൂട് അപകടം',
            'lightning_risk': 'മിന്നൽ അപകടം',
            'visibility_risk': 'ദൃശ്യത അപകടം',
            'safety_score': 'സുരക്ഷാ സ്കോർ',
            'risk_level': 'അപകട നില',
            'safe': 'സുരക്ഷിതം',
            'low_risk': 'കുറഞ്ഞ അപകടം',
            'moderate_risk': 'മിതമായ അപകടം',
            'high_risk': 'ഉയർന്ന അപകടം',
            'critical_risk': 'ഗുരുതരമായ അപകടം',
            'chat_title': 'കാലാവസ്ഥ സഹായി',
            'chat_placeholder': 'കാലാവസ്ഥയെക്കുറിച്ച് ചോദിക്കുക...',
            'send_message': 'അയയ്ക്കുക',
            'voice_input': 'ശബ്ദ ഇൻപുട്ട്',
            'voice_output': 'ശബ്ദ ഔട്ട്പുട്ട്',
            'clear_sky': 'തെളിഞ്ഞ ആകാശം',
            'few_clouds': 'ചില മേഘങ്ങൾ',
            'scattered_clouds': 'ചിതറിയ മേഘങ്ങൾ',
            'broken_clouds': 'തകർന്ന മേഘങ്ങൾ',
            'overcast_clouds': 'മേഘാവൃത ആകാശം',
            'light_rain': 'ഇല്ലാത്ത മഴ',
            'moderate_rain': 'മിതമായ മഴ',
            'heavy_rain': 'കനത്ത മഴ',
            'thunderstorm': 'ഇടിമിന്നൽ',
            'snow': 'മഞ്ഞൽ',
            'mist': 'മൂടൽ',
            'fog': 'പുകമൂടൽ',
            'advice_hot': 'വളരെ ചൂടാണ്! വെള്ളം കുടിക്കുക, നേരിട്ട് സൂര്യനിലയിൽ നിന്ന് ഒഴിയുക.',
            'advice_cold': 'തണുപ്പാണ് - ചൂടുള്ള വസ്ത്രങ്ങൾ ധരിക്കുക!',
            'advice_very_cold': 'വളരെ തണുപ്പാണ്! കനത്ത വസ്ത്രങ്ങൾ ധരിക്കുക, ചർമ്മം സംരക്ഷിക്കുക.',
            'advice_high_humidity': 'ഉയർന്ന ഈർപ്പം - ഈർപ്പമുള്ളതായി തോന്നാം. വീട്ടിൽ തന്നെ തുടരുക.',
            'advice_low_humidity': 'കുറഞ്ഞ ഈർപ്പം - ഈർപ്പമുള്ളതായി തുടരുക, ധാരാളം വെള്ളം കുടിക്കുക.',
            'advice_rain': 'കുട അല്ലെങ്കിൽ മഴ അങ്കി ധരിക്കുക!',
            'advice_clear': 'പുറത്തെ പ്രവർത്തനങ്ങൾക്ക് നല്ല കാലാവസ്ഥ!',
            'advice_cloudy': 'ഭാഗികമായി മേഘാവൃതം - മൊത്തത്തിൽ നല്ല കാലാവസ്ഥ.',
            'advice_storm': 'കൊടുങ്കാലാവസ്ഥ - വീട്ടിൽ തന്നെ തുടരുക, സാധ്യമെങ്കിൽ യാത്ര ഒഴിവാക്കുക.',
            'agriculture': 'കൃഷി',
            'crop_recommendations': 'വിള ശുപാര്ശകൾ',
            'irrigation': 'ജലസേചനം',
            'harvest': 'വിളവെടുപ്പ്',
            'storm_impact': 'കൊടുങ്ക പ്രഭാവം',
            'action_plan': 'പ്രവർത്തന പദ്ധതി',
            'subscribe': 'വരിക്കുക',
            'unsubscribe': 'വരിപ്പ് നീക്കുക',
            'notifications': 'അറിയിപ്പുകൾ',
            'daily_digest': 'ദൈനിക സംഗ്രഹം',
            'severe_weather_alert': 'കടുത്ത കാലാവസ്ഥ മുന്നറിപ്പ്',
            'language': 'ഭാഷ',
            'select_language': 'ഭാഷ തിരഞ്ഞെടുക്കുക',
            'voice_command_listening': 'കേൾക്കുന്നു...',
            'voice_command_speaking': 'സംസാരിക്കുന്നു...',
            'voice_command_error': 'ശബ്ദ തിരിച്ചറിയൽ പിശക്',
            'voice_command_not_supported': 'ഈ ബ്രൗസറിൽ ശബ്ദ കമാൻഡുകൾ പിന്തുണയ്ക്കുന്നില്ല'
        }
    
    def _get_kannada_translations(self) -> Dict:
        """Kannada translations"""
        return {
            'app_title': 'ಹವಾಮಾನ GPT',
            'search_placeholder': 'ಸ್ಥಳವನ್ನು ಹುಡುಕಿ...',
            'get_weather': 'ಹವಾಮಾನವನ್ನು ಪಡೆಯಿರಿ',
            'current_weather': 'ಪ್ರಸ್ತುತ ಹವಾಮಾನ',
            'temperature': 'ತಾಪಮಾನ',
            'humidity': 'ಆರ್ದ್ರತೆ',
            'wind_speed': 'ಗಾಳಿಯ ವೇಗ',
            'visibility': 'ದೃಷ್ಟಿಗೋಚರತೆ',
            'pressure': 'ಒತ್ತಡ',
            'feels_like': 'ಅನಿಸಿಸುತ್ತದೆ',
            'weather_conditions': 'ಹವಾಮಾನದ ಸ್ಥಿತಿಗಳು',
            'hazard_map': 'ಅಪಾಯ ನಕ್ಷೆ',
            'flood_risk': 'ಪ್ರವಾಹದ ಅಪಾಯ',
            'heat_risk': 'ಬಿಸಿಲಿನ ಅಪಾಯ',
            'lightning_risk': 'ಮಿಂಚುಗಳ ಅಪಾಯ',
            'visibility_risk': 'ದೃಷ್ಟಿಗೋಚರತೆಯ ಅಪಾಯ',
            'safety_score': 'ಸುರಕ್ಷತಾ ಅಂಕ',
            'risk_level': 'ಅಪಾಯದ ಮಟ್ಟ',
            'safe': 'ಸುರಕ್ಷಿತ',
            'low_risk': 'ಕಡಿಮೆ ಅಪಾಯ',
            'moderate_risk': 'ಮಧ್ಯಮ ಅಪಾಯ',
            'high_risk': 'ಹೆಚ್ಚಿನ ಅಪಾಯ',
            'critical_risk': 'ತೀವ್ರ ಅಪಾಯ',
            'chat_title': 'ಹವಾಮಾನ ಸಹಾಯಕ',
            'chat_placeholder': 'ಹವಾಮಾನದ ಬಗ್ಗೆ ಕೇಳಿ...',
            'send_message': 'ಕಳುಹಿಸಿ',
            'voice_input': 'ಧ್ವನಿ ಇನ್‌ಪುಟ್',
            'voice_output': 'ಧ್ವನಿ ಔಟ್‌ಪುಟ್',
            'clear_sky': 'ಸ್ಪಷ್ಟ ಆಕಾಶ',
            'few_clouds': 'ಕೆಲವು ಮೋಡಗಳು',
            'scattered_clouds': 'ಚದುರಿದ ಮೋಡಗಳು',
            'broken_clouds': 'ಒಡೆದ ಮೋಡಗಳು',
            'overcast_clouds': 'ಮೋಡಮಂಜರಿತ ಆಕಾಶ',
            'light_rain': 'ಲಘು ಮಳೆ',
            'moderate_rain': 'ಮಧ್ಯಮ ಮಳೆ',
            'heavy_rain': 'ಭಾರೀ ಮಳೆ',
            'thunderstorm': 'ಚಂಡಮಾರುತ',
            'snow': 'ಹಿಮ',
            'mist': 'ಮಂಜು',
            'fog': 'ಹೊಗೆ',
            'advice_hot': 'ತುಂಬಾ ಬಿಸಿಯಾಗಿದೆ! ನೀರು ಕುಡಿಯಿರಿ ಮತ್ತು ನೇರಳಿನ ಸೂರ್ಯನಿಂದ ದೂರವಿರಿರಿ.',
            'advice_cold': 'ತಣ್ಣಗಾಗಿದೆ - ಬೆಚ್ಚಿನ ಬಟ್ಟುಗಳನ್ನು ಧರಿಸಿ!',
            'advice_very_cold': 'ತುಂಬಾ ತಣ್ಣಗಾಗಿದೆ! ಭಾರಿ ಬಟ್ಟುಗಳನ್ನು ಧರಿಸಿ ಮತ್ತು ಚರ್ಮವನ್ನು ರಕ್ಷಿಸಿ.',
            'advice_high_humidity': 'ಹೆಚ್ಚಿನ ಆರ್ದ್ರತೆ - ಆರ್ದ್ರವಾಗಿ ಅನಿಸಬಹುದು. ಮನೆಯಲ್ಲೇ ಇರಿ.',
            'advice_low_humidity': 'ಕಡಿಮೆ ಆರ್ದ್ರತೆ - ಆರ್ದ್ರವಾಗಿರಿ ಮತ್ತು ಹೆಚ್ಚು ನೀರು ಕುಡಿಯಿರಿ.',
            'advice_rain': 'ಛತ್ರಿ ಅಥವಾ ಮಳೆ ಕೋಟು ಮರೆಯಬೇಡಿ!',
            'advice_clear': 'ಹೊರಾಡು ಚಟುವಟಿಕೆಗಳಿಗೆ ಉತ್ತಮ ಹವಾಮಾನ!',
            'advice_cloudy': 'ಭಾಗಶಃ ಮೋಡಮಂಜರಿತ - ಒಟ್ಟಾರಿಯಲ್ಲಿ ಆಹ್ಲಾದಕರ ಹವಾಮಾನ.',
            'advice_storm': 'ಚಂಡಮಾರುತದ ಸ್ಥಿತಿಗಳು - ಮನೆಯಲ್ಲೇ ಇರಿ ಮತ್ತು ಸಾಧ್ಯವಾದರೆ ಪ್ರಯಾಣಿಸಬೇಡಿ.',
            'agriculture': 'ಕೃಷಿ',
            'crop_recommendations': 'ಬೆಳೆ ಶಿಫಾರಸುಗಳು',
            'irrigation': 'ನೀರಾವರಿ',
            'harvest': 'ಬೆಳೆ ಕಟಾವು',
            'storm_impact': 'ಚಂಡಮಾರುತದ ಪರಿಣಾಮ',
            'action_plan': 'ಕ್ರಮ ಯೋಜನೆ',
            'subscribe': 'ಚಂದಾದಾರರಾಗಿ',
            'unsubscribe': 'ಚಂದಾದಾರವನ್ನು ರದ್ದುಪಡಿಸಿ',
            'notifications': 'ಅಧಿಸೂಚನೆಗಳು',
            'daily_digest': 'ದೈನಿಕ ಸಾರಾಂಶ',
            'severe_weather_alert': 'ತೀವ್ರ ಹವಾಮಾನ ಎಚ್ಚರಿಕೆ',
            'language': 'ಭಾಷೆ',
            'select_language': 'ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ',
            'voice_command_listening': 'ಕೇಳುತ್ತಿದೆ...',
            'voice_command_speaking': 'ಮಾತನಾಡುತ್ತಿದೆ...',
            'voice_command_error': 'ಧ್ವನಿ ಗುರುತಿಸುವಲ್ಲಿ ದೋಷ',
            'voice_command_not_supported': 'ಈ ಬ್ರೌಸರ್‌ನಲ್ಲಿ ಧ್ವನಿ ಆದೇಶಗಳು ಬೆಂಬಲಿತವಾಗಿಲ್ಲ'
        }
    
    def _get_bengali_translations(self) -> Dict:
        """Bengali translations"""
        return {
            'app_title': 'আবহাওয়া GPT',
            'search_placeholder': 'অবস্থান অনুসন্ধান করুন...',
            'get_weather': 'আবহাওয়া পান',
            'current_weather': 'বর্তমান আবহাওয়া',
            'temperature': 'তাপমাত্রা',
            'humidity': 'আর্দ্রতা',
            'wind_speed': 'বাতাসের গতি',
            'visibility': 'দৃশ্যমান্যতা',
            'pressure': 'চাপ',
            'feels_like': 'মনে হয়',
            'weather_conditions': 'আবহাওয়ার অবস্থা',
            'hazard_map': 'বিপদ মানচিত্র',
            'flood_risk': 'বন্যার ঝুকি',
            'heat_risk': 'তাপের ঝুকি',
            'lightning_risk': 'বজ্রপাতের ঝুকি',
            'visibility_risk': 'দৃশ্যমান্যতার ঝুকি',
            'safety_score': 'নিরাপত্তা স্কোর',
            'risk_level': 'ঝুকির স্তর',
            'safe': 'নিরাপদ',
            'low_risk': 'কম ঝুকি',
            'moderate_risk': 'মাঝারি ঝুকি',
            'high_risk': 'উচ্চ ঝুকি',
            'critical_risk': 'সংকটাপন্ন ঝুকি',
            'chat_title': 'আবহাওয়া সহকারী',
            'chat_placeholder': 'আবহাওয়া সম্পর্কে জিজ্ঞাসা করুন...',
            'send_message': 'পাঠান',
            'voice_input': 'ভয়েস ইনপুট',
            'voice_output': 'ভয়েস আউটপুট',
            'clear_sky': 'পরিষ্কার আকাশ',
            'few_clouds': 'কিছু মেঘ',
            'scattered_clouds': 'ছড়ানো মেঘ',
            'broken_clouds': 'ভাঙা মেঘ',
            'overcast_clouds': 'মেঘাচ্ছন্ন আকাশ',
            'light_rain': 'হালকা বৃষ্টি',
            'moderate_rain': 'মাঝারি বৃষ্টি',
            'heavy_rain': 'ভারী বৃষ্টি',
            'thunderstorm': 'ঝড়',
            'snow': 'তুষার',
            'mist': 'কুয়াশা',
            'fog': 'কুয়া',
            'advice_hot': 'খুব গরম! পানি পান এবং সরাসরি সূর্যের আলো থেকে দূরে থাকুন.',
            'advice_cold': 'ঠান্ডা - গরম কাপড় পরুন!',
            'advice_very_cold': 'খুব ঠান্ডা! ভারী কাপড় পরুন এবং ত্বক রক্ষা করুন.',
            'advice_high_humidity': 'উচ্চ আর্দ্রতা - আর্দ্র মনে হতে পারে. ঘরে থাকুন.',
            'advice_low_humidity': 'কম আর্দ্রতা - আর্দ্র থাকুন এবং প্রচুর পানি পান.',
            'advice_rain': 'ছাতা বা বৃষ্টি কোট ভুলবেন না!',
            'advice_clear': 'বাইরের কাজের জন্য দুর্দান্ত আবহাওয়া!',
            'advice_cloudy': 'আংশিক মেঘাচ্ছন্ন - সামগ্রিকভাবে ভালো আবহাওয়া.',
            'advice_storm': 'ঝড়ের অবস্থা - ঘরে থাকুন এবং সম্ভব হলে ভ্রমণ এড়িয়ে যান.',
            'agriculture': 'কৃষি',
            'crop_recommendations': 'ফসলের সুপারিশ',
            'irrigation': 'সেচন',
            'harvest': 'ফসল সংগ্রহ',
            'storm_impact': 'ঝড়ের প্রভাব',
            'action_plan': 'কর্ম পরিকল্পনা',
            'subscribe': 'সাবস্ক্রাইব করুন',
            'unsubscribe': 'আনসাবস্ক্রাইব করুন',
            'notifications': 'বিজ্ঞপ্তি',
            'daily_digest': 'দৈনিক সারসংক্ষেপ',
            'severe_weather_alert': 'তীব্র আবহাওয়া সতর্কতা',
            'language': 'ভাষা',
            'select_language': 'ভাষা নির্বাচন করুন',
            'voice_command_listening': 'শুনছি...',
            'voice_command_speaking': 'বলছি...',
            'voice_command_error': 'ভয়েস স্বীকৃতি ত্রুটি',
            'voice_command_not_supported': 'এই ব্রাউজারে ভয়েস কমান্ড সমর্থিত নয়'
        }
    
    def _get_marathi_translations(self) -> Dict:
        """Marathi translations"""
        return {
            'app_title': 'हवामान GPT',
            'search_placeholder': 'स्थान शोधा...',
            'get_weather': 'हवामान मिळवा',
            'current_weather': 'वर्तमान हवामान',
            'temperature': 'तापमान',
            'humidity': 'आर्द्रता',
            'wind_speed': 'वाऱ्याची वेग',
            'visibility': 'दृश्यता',
            'pressure': 'दाब',
            'feels_like': 'वाटते',
            'weather_conditions': 'हवामानाच्या परिस्थिती',
            'hazard_map': 'धोकाने नकाशा',
            'flood_risk': 'पूर धोका',
            'heat_risk': 'उष्णतेचा धोका',
            'lightning_risk': 'विजेरीचा धोका',
            'visibility_risk': 'दृश्यतेचा धोका',
            'safety_score': 'सुरक्षा गुण',
            'risk_level': 'धोक्याची पातळी',
            'safe': 'सुरक्षित',
            'low_risk': 'कमी धोका',
            'moderate_risk': 'मध्यम धोका',
            'high_risk': 'जास्त धोका',
            'critical_risk': 'गंभीर धोका',
            'chat_title': 'हवामान सहाय्यक',
            'chat_placeholder': 'हवामानाबद्दल विचारा...',
            'send_message': 'पाठवा',
            'voice_input': 'आवाज इनपुट',
            'voice_output': 'आवाज आउटपुट',
            'clear_sky': 'स्पष्ट आकाश',
            'few_clouds': 'काही ढगले',
            'scattered_clouds': 'दुर्गल ढगले',
            'broken_clouds': 'तुटलेले ढगले',
            'overcast_clouds': 'ढगलघन आकाश',
            'light_rain': 'हलकी पाऊस',
            'moderate_rain': 'मध्यम पाऊस',
            'heavy_rain': 'जोरदार पाऊस',
            'thunderstorm': 'वादळ',
            'snow': 'बर्फ',
            'mist': 'धुरे',
            'fog': 'धुक्कर',
            'advice_hot': 'खूप उष्ण आहे! पाणी प्या आणि थेट सूर्यप्रकाशापासून दूर राहा.',
            'advice_cold': 'थंड आहे - गरम कपडे घाला!',
            'advice_very_cold': 'खूप थंड आहे! जाड कपडे घाला आणि त्वचेचे रक्षण करा.',
            'advice_high_humidity': 'उच्च आर्द्रता - ओले वाटू शकते. घरी राहा.',
            'advice_low_humidity': 'कमी आर्द्रता - ओले राहा आणि खूप पाणी प्या.',
            'advice_rain': 'छतरी किंवा पावस अंगक विसरू नका!',
            'advice_clear': 'बाहेरी कार्यांसाठी उत्तम हवामान!',
            'advice_cloudy': 'आंशिक ढगलघन - एकंदर चांगले हवामान.',
            'advice_storm': 'वादळीच्या परिस्थिती - घरी राहा आणि शक्य असल्यास प्रवास टाळा.',
            'agriculture': 'शेती',
            'crop_recommendations': 'पिकांची शिफारस',
            'irrigation': 'सिंचन',
            'harvest': 'पिक काढणी',
            'storm_impact': 'वादळीचा परिणाम',
            'action_plan': 'कृती योजना',
            'subscribe': 'सदस्यता घ्या',
            'unsubscribe': 'सदस्यता रद्द करा',
            'notifications': 'सूचना',
            'daily_digest': 'दैनिक सारांश',
            'severe_weather_alert': 'गंभीर हवामान चेतावणी',
            'language': 'भाषा',
            'select_language': 'भाषा निवडा',
            'voice_command_listening': 'ऐकत आहे...',
            'voice_command_speaking': 'बोलत आहे...',
            'voice_command_error': 'आवाज ओळख त्रुटी',
            'voice_command_not_supported': 'या ब्राउझरमध्ये आवाज आदेश समर्थित नाहीत'
        }
    
    def _get_gujarati_translations(self) -> Dict:
        """Gujarati translations"""
        return {
            'app_title': 'હવામાન GPT',
            'search_placeholder': 'સ્થાન શોધો...',
            'get_weather': 'હવામાન મેળવો',
            'current_weather': 'વર્તમાન હવામાન',
            'temperature': 'તાપમાન',
            'humidity': 'ભેજાપણ',
            'wind_speed': 'પવનની ગતિ',
            'visibility': 'દૃશ્યતા',
            'pressure': 'દબાણ',
            'feels_like': 'લાગે છે',
            'weather_conditions': 'હવામાનની સ્થિતિ',
            'hazard_map': 'જોખમ નકશા',
            'flood_risk': 'પૂરનો જોખમ',
            'heat_risk': 'ગરમીનો જોખમ',
            'lightning_risk': 'વીજળનો જોખમ',
            'visibility_risk': 'દૃશ્યતાનો જોખમ',
            'safety_score': 'સુરક્ષા સ્કોર',
            'risk_level': 'જોખમની સ્તર',
            'safe': 'સુરક્ષિત',
            'low_risk': 'ઓછો જોખમ',
            'moderate_risk': 'મધ્યમ જોખમ',
            'high_risk': 'વધુ જોખમ',
            'critical_risk': 'ગંભીર જોખમ',
            'chat_title': 'હવામાન સહાયક',
            'chat_placeholder': 'હવામાન વિશે પૂછો...',
            'send_message': 'મોકલો',
            'voice_input': 'અવાજ ઇનપુટ',
            'voice_output': 'અવાજ આઉટપુટ',
            'clear_sky': 'સ્પષ્ટ આકાશ',
            'few_clouds': 'થોડા વાદળ',
            'scattered_clouds': 'વિખેરા વાદળ',
            'broken_clouds': 'તૂટેલા વાદળ',
            'overcast_clouds': 'વાદળછાય આકાશ',
            'light_rain': 'હળવો વરસાદ',
            'moderate_rain': 'મધ્યમ વરસાદ',
            'heavy_rain': 'ભારે વરસાદ',
            'thunderstorm': 'તોફાન',
            'snow': 'બરફ',
            'mist': 'ધુંધ',
            'fog': 'ધોંધ',
            'advice_hot': 'ખૂબ ગરમ છે! પાણી પીઓ અને સીધા સૂર્યપ્રકાશથી દૂર રહો.',
            'advice_cold': 'ઠંડુ છે - ગરમ કપડા પહેરો!',
            'advice_very_cold': 'ખૂબ ઠંડુ છે! મોટા કપડા પહેરો અને ત્વચાનું રક્ષણ કરો.',
            'advice_high_humidity': 'વધુ ભેજાપણ - ભેજવાળું લાગી શકે છે. ઘરમાં રહો.',
            'advice_low_humidity': 'ઓછુ ભેજાપણ - ભેજવાળું રહો અને વધુ પાણી પીઓ.',
            'advice_rain': 'છત્રી અથવા વરસાદ અંગક ભૂલશો નહીં!',
            'advice_clear': 'બાહ્યની પ્રવૃત્તિઓ માટે સારુ હવામાન!',
            'advice_cloudy': 'આંશિક વાદળછાય - સમગ્ર રીતે સારુ હવામાન.',
            'advice_storm': 'તોફાની સ્થિતિ - ઘરમાં રહો અને શક્ય હોય તો પ્રવાસ ટાળો.',
            'agriculture': 'ખેતી',
            'crop_recommendations': 'પાકની ભલામણી',
            'irrigation': 'સિંચાઈ',
            'harvest': 'પાક કાપણી',
            'storm_impact': 'તોફાનની અસર',
            'action_plan': 'ક્રિયા યોજના',
            'subscribe': 'સભ્ય બનો',
            'unsubscribe': 'સભ્યત્વ રદ કરો',
            'notifications': 'સૂચનાઓ',
            'daily_digest': 'દૈનિક સારાંશ',
            'severe_weather_alert': 'ગંભીર હવામાન ચેતવણી',
            'language': 'ભાષા',
            'select_language': 'ભાષા પસંદ કરો',
            'voice_command_listening': 'સાંભળી રહ્યું છે...',
            'voice_command_speaking': 'બોલી રહ્યું છે...',
            'voice_command_error': 'અવાજ ઓળખ ભૂલ',
            'voice_command_not_supported': 'આ બ્રાઉઝરમાં અવાજ આદેશો સમર્થિત નથી'
        }
    
    def translate(self, key: str, language: str = None) -> str:
        """
        Translate a key to the specified language
        
        Args:
            key: Translation key
            language: Target language code (defaults to current language)
            
        Returns:
            Translated text or original key if not found
        """
        lang = language or self.current_language
        if lang not in self.translations:
            lang = 'en'  # Fallback to English
        
        translation = self.translations[lang].get(key)
        if translation is None:
            # Fallback to English if key not found
            translation = self.translations['en'].get(key, key)
        
        return translation
    
    def set_language(self, language: str) -> bool:
        """
        Set the current language
        
        Args:
            language: Language code
            
        Returns:
            True if language was set successfully, False otherwise
        """
        if language in self.supported_languages:
            self.current_language = language
            return True
        return False
    
    def get_current_language(self) -> str:
        """Get the current language code"""
        return self.current_language
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get all supported languages"""
        return self.supported_languages
    
    def translate_weather_response(self, response: str, language: str = None) -> str:
        """
        Translate AI weather response to target language
        
        Args:
            response: AI response text
            language: Target language code
            
        Returns:
            Translated response
        """
        lang = language or self.current_language
        if lang == 'en':
            return response
        
        # Simple translation for common weather terms
        # In production, you would use a proper translation API like Google Translate
        translated = response
        
        # Replace common weather terms with translations
        weather_terms = {
            'temperature': self.translate('temperature', lang),
            'humidity': self.translate('humidity', lang),
            'wind': self.translate('wind_speed', lang),
            'clear': self.translate('clear_sky', lang),
            'rain': self.translate('light_rain', lang),
            'hot': self.translate('advice_hot', lang),
            'cold': self.translate('advice_cold', lang),
        }
        
        for english_term, translated_term in weather_terms.items():
            translated = translated.replace(english_term, translated_term)
        
        return translated


# Global translation service instance
translation_service = TranslationService()