/**
 * Voice Assistant Module
 * Handles text-to-speech and speech-to-text functionality
 */

class VoiceAssistant {
    constructor() {
        this.enabled = false;
        this.language = 'en';
        this.settings = {
            rate: 1.0,
            pitch: 1.0,
            volume: 1.0
        };
        this.synthesis = window.speechSynthesis;
        this.recognition = null;
        this.isListening = false;
        this.isSpeaking = false;
        this.init();
    }

    async init() {
        // Load voice assistant status from API
        try {
            const response = await fetch('/api/voice/status');
            const data = await response.json();
            this.enabled = data.enabled;
            this.language = data.language;
            this.settings = data.settings;
        } catch (error) {
            console.error('Failed to load voice status:', error);
        }

        // Initialize speech recognition if available
        this.initSpeechRecognition();
        
        // Set up voice controls
        this.setupVoiceControls();
    }

    initSpeechRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = true;
            this.recognition.lang = this.getLanguageCode(this.language);

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.onSpeechResult(transcript, event.results[0].isFinal);
            };

            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.onSpeechError(event.error);
            };

            this.recognition.onend = () => {
                this.isListening = false;
                this.updateVoiceUI();
            };
        } else {
            console.warn('Speech recognition not supported in this browser');
        }
    }

    getLanguageCode(language) {
        const languageCodes = {
            'en': 'en-US',
            'ta': 'ta-IN',
            'hi': 'hi-IN',
            'te': 'te-IN',
            'ml': 'ml-IN',
            'kn': 'kn-IN',
            'bn': 'bn-IN',
            'mr': 'mr-IN',
            'gu': 'gu-IN'
        };
        return languageCodes[language] || 'en-US';
    }

    async enable() {
        try {
            const response = await fetch('/api/voice/enable', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.enabled = true;
                this.updateVoiceUI();
                return true;
            }
        } catch (error) {
            console.error('Failed to enable voice assistant:', error);
        }
        return false;
    }

    async disable() {
        try {
            const response = await fetch('/api/voice/disable', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.enabled = false;
                this.stopListening();
                this.stopSpeaking();
                this.updateVoiceUI();
                return true;
            }
        } catch (error) {
            console.error('Failed to disable voice assistant:', error);
        }
        return false;
    }

    async speak(text, language = null) {
        if (!this.enabled || !this.synthesis) {
            return false;
        }

        const lang = language || this.language;
        
        try {
            // Get TTS configuration from API
            const response = await fetch('/api/voice/speak', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    language: lang
                })
            });

            if (response.ok) {
                const config = await response.json();
                
                // Create utterance
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = this.getLanguageCode(config.language);
                utterance.rate = config.settings.rate;
                utterance.pitch = config.settings.pitch;
                utterance.volume = config.settings.volume;

                utterance.onstart = () => {
                    this.isSpeaking = true;
                    this.updateVoiceUI();
                };

                utterance.onend = () => {
                    this.isSpeaking = false;
                    this.updateVoiceUI();
                };

                utterance.onerror = (event) => {
                    console.error('Speech synthesis error:', event.error);
                    this.isSpeaking = false;
                    this.updateVoiceUI();
                };

                this.synthesis.speak(utterance);
                return true;
            }
        } catch (error) {
            console.error('Failed to speak:', error);
        }
        return false;
    }

    stopSpeaking() {
        if (this.synthesis && this.isSpeaking) {
            this.synthesis.cancel();
            this.isSpeaking = false;
            this.updateVoiceUI();
        }
    }

    startListening(language = null) {
        if (!this.enabled || !this.recognition) {
            console.warn('Voice recognition not available');
            return false;
        }

        const lang = language || this.language;
        this.recognition.lang = this.getLanguageCode(lang);
        
        try {
            this.recognition.start();
            this.isListening = true;
            this.updateVoiceUI();
            return true;
        } catch (error) {
            console.error('Failed to start listening:', error);
            return false;
        }
    }

    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
            this.isListening = false;
            this.updateVoiceUI();
        }
    }

    onSpeechResult(transcript, isFinal) {
        // This can be overridden by the application
        console.log('Speech result:', transcript, 'Final:', isFinal);
        
        if (isFinal) {
            // Trigger event for application to handle
            const event = new CustomEvent('voiceResult', {
                detail: { transcript, language: this.language }
            });
            document.dispatchEvent(event);
        }
    }

    onSpeechError(error) {
        console.error('Speech recognition error:', error);
        
        // Trigger error event
        const event = new CustomEvent('voiceError', {
            detail: { error, language: this.language }
        });
        document.dispatchEvent(event);
    }

    async parseCommand(text, language = null) {
        try {
            const response = await fetch('/api/voice/parse', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    language: language || this.language
                })
            });

            if (response.ok) {
                const parsed = await response.json();
                return parsed;
            }
        } catch (error) {
            console.error('Failed to parse command:', error);
        }
        return null;
    }

    async getCommands(language = null) {
        try {
            const lang = language || this.language;
            const response = await fetch(`/api/voice/commands?language=${lang}`);
            
            if (response.ok) {
                const data = await response.json();
                return data.commands;
            }
        } catch (error) {
            console.error('Failed to get commands:', error);
        }
        return {};
    }

    async updateSettings(settings) {
        try {
            const response = await fetch('/api/voice/settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(settings)
            });

            if (response.ok) {
                const data = await response.json();
                this.settings = data.settings;
                return true;
            }
        } catch (error) {
            console.error('Failed to update settings:', error);
        }
        return false;
    }

    setLanguage(language) {
        this.language = language;
        if (this.recognition) {
            this.recognition.lang = this.getLanguageCode(language);
        }
    }

    setupVoiceControls() {
        // Create voice control buttons if they don't exist
        if (!document.getElementById('voice-controls')) {
            const voiceControls = document.createElement('div');
            voiceControls.id = 'voice-controls';
            voiceControls.className = 'voice-controls';
            
            // Enable/Disable button
            const toggleButton = document.createElement('button');
            toggleButton.id = 'voice-toggle';
            toggleButton.className = 'voice-toggle';
            toggleButton.innerHTML = '🎤';
            toggleButton.title = 'Toggle Voice Assistant';
            toggleButton.addEventListener('click', () => {
                if (this.enabled) {
                    this.disable();
                } else {
                    this.enable();
                }
            });
            
            // Listen button
            const listenButton = document.createElement('button');
            listenButton.id = 'voice-listen';
            listenButton.className = 'voice-listen';
            listenButton.innerHTML = '🎧';
            listenButton.title = 'Voice Input';
            listenButton.addEventListener('click', () => {
                if (this.isListening) {
                    this.stopListening();
                } else {
                    this.startListening();
                }
            });
            
            // Speak button
            const speakButton = document.createElement('button');
            speakButton.id = 'voice-speak';
            speakButton.className = 'voice-speak';
            speakButton.innerHTML = '🔊';
            speakButton.title = 'Voice Output';
            speakButton.addEventListener('click', () => {
                if (this.isSpeaking) {
                    this.stopSpeaking();
                } else {
                    // Speak last chat response
                    const lastResponse = document.querySelector('.chat-response:last-child');
                    if (lastResponse) {
                        this.speak(lastResponse.textContent);
                    }
                }
            });
            
            voiceControls.appendChild(toggleButton);
            voiceControls.appendChild(listenButton);
            voiceControls.appendChild(speakButton);
            
            // Insert into header
            const header = document.querySelector('header') || document.body;
            if (header) {
                header.appendChild(voiceControls);
            }
            
            this.updateVoiceUI();
        }
    }

    updateVoiceUI() {
        const toggleButton = document.getElementById('voice-toggle');
        const listenButton = document.getElementById('voice-listen');
        const speakButton = document.getElementById('voice-speak');
        
        if (toggleButton) {
            toggleButton.className = this.enabled ? 'voice-toggle enabled' : 'voice-toggle';
            toggleButton.innerHTML = this.enabled ? '🎤' : '🎤';
        }
        
        if (listenButton) {
            listenButton.className = this.isListening ? 'voice-listen listening' : 'voice-listen';
            listenButton.innerHTML = this.isListening ? '🔴' : '🎧';
        }
        
        if (speakButton) {
            speakButton.className = this.isSpeaking ? 'voice-speak speaking' : 'voice-speak';
            speakButton.innerHTML = this.isSpeaking ? '🔇' : '🔊';
        }
    }

    isEnabled() {
        return this.enabled;
    }

    isListeningActive() {
        return this.isListening;
    }

    isSpeakingActive() {
        return this.isSpeaking;
    }

    getLanguage() {
        return this.language;
    }

    getSettings() {
        return this.settings;
    }
}

// Initialize voice assistant when DOM is ready
let voiceAssistant;
document.addEventListener('DOMContentLoaded', () => {
    voiceAssistant = new VoiceAssistant();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoiceAssistant;
}