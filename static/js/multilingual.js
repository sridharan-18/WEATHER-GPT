/**
 * Multilingual Support Module
 * Handles language switching and UI translations
 */

class MultilingualManager {
    constructor() {
        this.currentLanguage = 'en';
        this.translations = {};
        this.supportedLanguages = {
            'en': 'English',
            'ta': 'Tamil (தமிழ்)',
            'hi': 'Hindi (हिंदी)',
            'te': 'Telugu (తెలుగు)',
            'ml': 'Malayalam (മലയാളം)',
            'kn': 'Kannada (ಕನ್ನಡ)',
            'bn': 'Bengali (বাংলা)',
            'mr': 'Marathi (मराठी)',
            'gu': 'Gujarati (ગુજરાતી)'
        };
        this.init();
    }

    async init() {
        // Load supported languages from API
        try {
            const response = await fetch('/api/languages');
            const data = await response.json();
            if (data.languages) {
                this.supportedLanguages = data.languages;
                this.currentLanguage = data.current_language;
            }
        } catch (error) {
            console.error('Failed to load languages:', error);
        }

        // Load translations for current language
        await this.loadTranslations(this.currentLanguage);
        
        // Set up language selector
        this.setupLanguageSelector();
        
        // Apply translations to UI
        this.applyTranslations();
    }

    async loadTranslations(language) {
        try {
            const response = await fetch(`/api/translate?language=${language}`);
            // In production, you would load actual translation files
            // For now, we'll use a simple approach
            this.translations = this.getFallbackTranslations(language);
        } catch (error) {
            console.error('Failed to load translations:', error);
            this.translations = this.getFallbackTranslations(language);
        }
    }

    getFallbackTranslations(language) {
        // Fallback translations for demo purposes
        // In production, load from translation files or API
        return {
            'app_title': this.supportedLanguages[language] || 'Weather GPT',
            'search_placeholder': this.getTranslation('search_placeholder', language),
            'get_weather': this.getTranslation('get_weather', language),
            'current_weather': this.getTranslation('current_weather', language),
            'chat_title': this.getTranslation('chat_title', language),
            'chat_placeholder': this.getTranslation('chat_placeholder', language),
            'voice_input': this.getTranslation('voice_input', language),
            'voice_output': this.getTranslation('voice_output', language),
            'language': this.getTranslation('language', language),
            'select_language': this.getTranslation('select_language', language)
        };
    }

    getTranslation(key, language) {
        // Simple translation mapping for demo
        const translations = {
            'en': {
                'search_placeholder': 'Search location...',
                'get_weather': 'Get Weather',
                'current_weather': 'Current Weather',
                'chat_title': 'Weather Assistant',
                'chat_placeholder': 'Ask about weather...',
                'voice_input': 'Voice Input',
                'voice_output': 'Voice Output',
                'language': 'Language',
                'select_language': 'Select Language'
            },
            'ta': {
                'search_placeholder': 'இடத்தைத் தேடுங்கள்...',
                'get_weather': 'வானிலை பெறு',
                'current_weather': 'தற்போதைய வானிலை',
                'chat_title': 'வானிலை உதவியாளர்',
                'chat_placeholder': 'வானிலை பற்றி கேளுங்கள்...',
                'voice_input': 'குரல் உள்ளீடு',
                'voice_output': 'குரல் வெளியீடு',
                'language': 'மொழி',
                'select_language': 'மொழியைத் தேர்ந்தெடுக்கவும்'
            },
            'hi': {
                'search_placeholder': 'स्थान खोजें...',
                'get_weather': 'मौसम प्राप्त करें',
                'current_weather': 'वर्तमान मौसम',
                'chat_title': 'मौसम सहायक',
                'chat_placeholder': 'मौसम के बारे में पूछें...',
                'voice_input': 'आवाज़ इनपुट',
                'voice_output': 'आवाज़ आउटपुट',
                'language': 'भाषा',
                'select_language': 'भाषा चुनें'
            }
        };

        const langTranslations = translations[language] || translations['en'];
        return langTranslations[key] || key;
    }

    async setLanguage(language) {
        try {
            const response = await fetch('/api/language', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ language })
            });

            if (response.ok) {
                const data = await response.json();
                this.currentLanguage = data.current_language;
                await this.loadTranslations(this.currentLanguage);
                this.applyTranslations();
                this.updateLanguageSelector();
                return true;
            }
        } catch (error) {
            console.error('Failed to set language:', error);
        }
        return false;
    }

    translate(key) {
        return this.translations[key] || key;
    }

    applyTranslations() {
        // Apply translations to all elements with data-i18n attribute
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.translate(key);
            
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = translation;
            } else {
                element.textContent = translation;
            }
        });
    }

    setupLanguageSelector() {
        // Create language selector if it doesn't exist
        let selector = document.getElementById('language-selector');
        if (!selector) {
            selector = document.createElement('select');
            selector.id = 'language-selector';
            selector.className = 'language-selector';
            
            // Add options for each language
            Object.entries(this.supportedLanguages).forEach(([code, name]) => {
                const option = document.createElement('option');
                option.value = code;
                option.textContent = name;
                if (code === this.currentLanguage) {
                    option.selected = true;
                }
                selector.appendChild(option);
            });
            
            // Add event listener
            selector.addEventListener('change', (e) => {
                this.setLanguage(e.target.value);
            });
            
            // Insert into header
            const header = document.querySelector('header') || document.body;
            if (header) {
                header.appendChild(selector);
            }
        }
    }

    updateLanguageSelector() {
        const selector = document.getElementById('language-selector');
        if (selector) {
            selector.value = this.currentLanguage;
        }
    }

    async translateWeatherResponse(response) {
        try {
            const response_data = await fetch('/api/translate-weather', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    response: response,
                    language: this.currentLanguage
                })
            });

            if (response_data.ok) {
                const data = await response_data.json();
                return data.translated;
            }
        } catch (error) {
            console.error('Failed to translate weather response:', error);
        }
        return response;
    }

    getCurrentLanguage() {
        return this.currentLanguage;
    }

    getSupportedLanguages() {
        return this.supportedLanguages;
    }
}

// Initialize multilingual manager when DOM is ready
let multilingualManager;
document.addEventListener('DOMContentLoaded', () => {
    multilingualManager = new MultilingualManager();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MultilingualManager;
}