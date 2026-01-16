"""
AI Chatbot for DeepGuard
Educational chatbot to help users understand deepfakes and stay protected
"""

import re
import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class DeepfakeEducationBot:
    """
    AI-powered educational chatbot for deepfake awareness and protection.
    Uses pattern matching and an extensive knowledge base to provide
    helpful, informative responses about deepfakes and digital safety.
    """
    
    def __init__(self):
        self.context = []
        self.user_name = None
        self.conversation_count = 0
        
        # Knowledge base categories
        self.knowledge_base = self._build_knowledge_base()
        self.patterns = self._build_patterns()
        
    def _build_knowledge_base(self) -> Dict:
        """Build comprehensive knowledge base about deepfakes"""
        return {
            "what_is_deepfake": {
                "title": "What is a Deepfake?",
                "content": """A **deepfake** is synthetic media created using artificial intelligence, where a person's likeness (face, voice, or both) is replaced or manipulated to make it appear they said or did something they never actually did.

**Key points:**
• The term combines "deep learning" + "fake"
• Uses AI techniques like GANs (Generative Adversarial Networks)
• Can create realistic but completely fabricated videos or audio
• First emerged around 2017, now widespread due to accessible tools

**Common types:**
1. **Face swaps** - Replacing one person's face with another
2. **Lip sync** - Making someone appear to say different words
3. **Voice cloning** - Synthesizing someone's voice
4. **Full body puppetry** - Controlling someone's entire appearance""",
                "follow_up": "Would you like to know how to detect deepfakes or learn about the risks they pose?"
            },
            
            "how_deepfakes_made": {
                "title": "How Deepfakes Are Created",
                "content": """Deepfakes are created using sophisticated AI/ML techniques:

**1. Data Collection**
• Gather many images/videos of the target person
• The more training data, the more realistic the result

**2. AI Training**
• **Autoencoders**: Learn to compress and reconstruct faces
• **GANs**: Two networks compete - one creates, one detects
• Training can take hours to days depending on quality

**3. Face Mapping**
• AI learns facial landmarks, expressions, and movements
• Maps source face movements onto target face

**4. Rendering**
• Blending, color matching, and smoothing
• Post-processing to hide artifacts

**Tools commonly used:**
• DeepFaceLab, FaceSwap (open source)
• Commercial apps (often for "entertainment")
• Voice cloning services""",
                "follow_up": "Understanding how they're made helps you spot them. Want tips on detection?"
            },
            
            "detection_techniques": {
                "title": "How to Detect Deepfakes",
                "content": """Here are proven techniques to spot deepfakes:

**👁️ Visual Clues:**
• **Blinking** - Deepfakes often have unnatural blink patterns
• **Skin texture** - May look too smooth or plastic
• **Hair edges** - Blurry or inconsistent around hairline
• **Lighting** - Shadows and lighting may not match
• **Teeth** - Often blurry or misshapen
• **Jewelry/glasses** - Reflections may be wrong

**👂 Audio Clues:**
• **Robotic quality** - Slight mechanical sound
• **Breathing** - Missing natural breath sounds
• **Background noise** - Inconsistent ambient sounds
• **Lip sync** - Slight delays between lips and audio

**🔬 Technical Methods:**
• **Metadata analysis** - Check file origins
• **Reverse image search** - Find original content
• **AI detection tools** - Like DeepGuard!
• **Frequency analysis** - Compression artifacts

**🧠 Critical Thinking:**
• Does this seem too shocking to be true?
• What's the source? Is it verified?
• Who benefits from this being believed?""",
                "follow_up": "Our tool uses CNN, spectral analysis, and face landmarks to detect these automatically!"
            },
            
            "risks_dangers": {
                "title": "Risks and Dangers of Deepfakes",
                "content": """Deepfakes pose serious threats across multiple domains:

**🏦 Financial Fraud**
• CEO fraud - Fake video calls authorizing transfers
• Voice cloning for phone scams
• Identity theft for loan applications
• Real cases: $243,000 stolen via AI voice clone (2019)

**🗳️ Political Manipulation**
• Fake statements from politicians
• Election interference
• Diplomatic incidents
• Public trust erosion

**👤 Personal Attacks**
• Non-consensual intimate imagery (most common abuse)
• Reputation destruction
• Blackmail and extortion
• Harassment campaigns

**⚖️ Legal Implications**
• Evidence tampering in courts
• False alibis or accusations
• Defamation at scale

**🌐 Societal Impact**
• "Liar's dividend" - Real videos dismissed as fake
• Trust crisis in media
• Increased polarization""",
                "follow_up": "Knowing these risks helps you stay vigilant. Want to learn how to protect yourself?"
            },
            
            "protection_tips": {
                "title": "How to Protect Yourself",
                "content": """Here's your comprehensive protection guide:

**🛡️ Prevention**
• Limit public photos/videos of yourself
• Use privacy settings on social media
• Be cautious about video calls with strangers
• Watermark your personal content

**🔍 Verification**
• Always check multiple sources for news
• Use reverse image/video search
• Look for original sources, not shares
• Be skeptical of emotional/shocking content
• Use detection tools like DeepGuard

**🚨 If You're a Victim**
1. Document everything (screenshots, URLs)
2. Report to the platform immediately
3. Contact law enforcement
4. Seek legal advice
5. Reach out to support organizations

**📢 Spread Awareness**
• Educate family and friends
• Share detection techniques
• Support media literacy initiatives

**🔐 Digital Hygiene**
• Use strong, unique passwords
• Enable two-factor authentication
• Be careful what you share online
• Regularly review your digital footprint""",
                "follow_up": "Prevention is the best protection. Any specific concerns you'd like to discuss?"
            },
            
            "laws_regulations": {
                "title": "Laws and Regulations",
                "content": """Legal landscape for deepfakes is evolving rapidly:

**🇺🇸 United States**
• DEEPFAKES Accountability Act (proposed)
• Some states have specific laws (CA, TX, VA)
• Section 230 debates ongoing
• FTC regulations on deceptive practices

**🇪🇺 European Union**
• AI Act - Requires disclosure of synthetic media
• GDPR - Right to image applies
• Digital Services Act - Platform responsibility

**🇬🇧 United Kingdom**
• Online Safety Bill includes deepfake provisions
• Intimate image abuse laws
• Defamation and harassment laws apply

**🌏 Asia**
• China - Deep synthesis regulations (2023)
• South Korea - Specific deepfake laws
• India - IT Act amendments

**⚖️ General Legal Options**
• Defamation lawsuits
• Copyright infringement
• Right to publicity claims
• Criminal harassment charges

*Note: Laws vary significantly by jurisdiction*""",
                "follow_up": "Legal protections are improving. Would you like to know about reporting procedures?"
            },
            
            "our_technology": {
                "title": "How DeepGuard Works",
                "content": """DeepGuard uses three powerful detection methods:

**🎬 Video Analysis (CNN)**
Our Convolutional Neural Network examines:
• Compression artifacts around face regions
• Color consistency at blending boundaries
• Noise patterns that differ from original footage
• Temporal consistency across frames

**🎵 Audio Analysis (Spectral)**
We analyze voice characteristics:
• MFCC (Mel-frequency cepstral coefficients)
• Voice naturalness scoring (jitter, shimmer)
• Spectral patterns unique to synthetic speech
• Temporal rhythm and breathing patterns

**👤 Face Landmarks (468 Points)**
Using MediaPipe Face Mesh:
• Blink pattern analysis (deepfakes often blink wrong)
• Lip-sync verification
• Micro-expression tracking
• Facial symmetry analysis

**📊 Combined Scoring**
• All three methods contribute to final score
• Confidence levels based on data quality
• Clear indicators explain what was detected""",
                "follow_up": "Upload a file to try it out! Any questions about our methodology?"
            },
            
            "future_of_deepfakes": {
                "title": "The Future of Deepfakes",
                "content": """What to expect in the coming years:

**📈 Technology Evolution**
• Real-time deepfakes becoming more accessible
• Higher quality with less training data
• Voice + video combined seamlessly
• AR/VR integration

**🛡️ Defense Improvements**
• Better AI detection methods
• Blockchain-based content authentication
• Digital watermarking standards
• Platform-level detection

**🏛️ Policy Developments**
• Stricter regulations expected
• Platform accountability laws
• International cooperation
• Digital identity frameworks

**🎓 Education & Awareness**
• Media literacy in schools
• Public awareness campaigns
• Industry standards forming

**💡 Positive Applications**
• Film and entertainment efficiency
• Accessibility (dubbing, translation)
• Historical preservation
• Art and creativity

The arms race between creation and detection continues!""",
                "follow_up": "Staying informed is crucial. What else would you like to know?"
            },
            
            "quiz": {
                "title": "Test Your Knowledge",
                "content": """Let's test what you've learned about deepfakes!

**Question 1:** What technology primarily powers deepfakes?
A) Photoshop
B) GANs (Generative Adversarial Networks)
C) Simple video editing
D) Motion capture

**Question 2:** Which is a common sign of a deepfake video?
A) High resolution
B) Unnatural blinking patterns
C) Good audio quality
D) Smooth playback

**Question 3:** What should you do if you suspect a deepfake?
A) Share it immediately
B) Ignore it
C) Verify with multiple sources
D) Assume it's real

*(Answers: 1-B, 2-B, 3-C)*""",
                "follow_up": "How did you do? Want me to explain any of the answers?"
            }
        }
    
    def _build_patterns(self) -> List[Tuple]:
        """Build conversation patterns for response matching"""
        return [
            # Greetings
            (r'\b(hi|hello|hey|greetings|howdy)\b', 'greeting'),
            (r'\b(good\s*(morning|afternoon|evening))\b', 'greeting'),
            
            # What is deepfake
            (r'\b(what|define|explain).*(deepfake|deep\s*fake)\b', 'what_is_deepfake'),
            (r'\bdeepfake.*(meaning|definition|is)\b', 'what_is_deepfake'),
            
            # How are they made
            (r'\b(how|way).*(create|make|made|generate|produce).*(deepfake|fake)\b', 'how_deepfakes_made'),
            (r'\b(who|how).*(create|make).*deepfake\b', 'how_deepfakes_made'),
            (r'\btechnology.*(behind|used|create)\b', 'how_deepfakes_made'),
            
            # Detection
            (r'\b(how|way).*(detect|spot|identify|recognize|tell|know).*(deepfake|fake)\b', 'detection_techniques'),
            (r'\b(sign|clue|indicator|tell).*(deepfake|fake)\b', 'detection_techniques'),
            (r'\bdetect\b', 'detection_techniques'),
            (r'\b(spot|identify|recognize).*fake\b', 'detection_techniques'),
            
            # Risks and dangers
            (r'\b(risk|danger|threat|harm|problem).*(deepfake|fake)?\b', 'risks_dangers'),
            (r'\b(why).*(dangerous|bad|harmful|concern)\b', 'risks_dangers'),
            (r'\bwhat.*(impact|effect|consequence)\b', 'risks_dangers'),
            
            # Protection
            (r'\b(protect|safe|prevent|avoid|secure)\b', 'protection_tips'),
            (r'\b(what|how).*(do|should).*if.*(victim|targeted)\b', 'protection_tips'),
            (r'\bstay\s*safe\b', 'protection_tips'),
            
            # Laws
            (r'\b(law|legal|regulation|illegal|crime|police|report)\b', 'laws_regulations'),
            (r'\bsue\b', 'laws_regulations'),
            
            # Our technology
            (r'\b(how|what).*(this|tool|app|system|work|detect)\b', 'our_technology'),
            (r'\bdeepguard\b', 'our_technology'),
            (r'\b(your|this).*(technology|algorithm|method)\b', 'our_technology'),
            
            # Future
            (r'\b(future|next|coming|evolve|trend)\b', 'future_of_deepfakes'),
            (r'\bwill.*(get|become).*(better|worse)\b', 'future_of_deepfakes'),
            
            # Quiz
            (r'\b(quiz|test|question|learn)\b', 'quiz'),
            (r'\btest.*knowledge\b', 'quiz'),
            
            # Thanks
            (r'\b(thank|thanks|thx|appreciate)\b', 'thanks'),
            
            # Help
            (r'\b(help|assist|support|guide)\b', 'help'),
            (r'\bwhat can you\b', 'help'),
            
            # Goodbye
            (r'\b(bye|goodbye|exit|quit|leave)\b', 'goodbye'),
        ]
    
    def get_greeting(self) -> str:
        """Generate a greeting message"""
        greetings = [
            "Hello! 👋 I'm **GuardBot**, your AI assistant for deepfake education. I'm here to help you understand deepfakes and stay protected in the digital world. What would you like to know?",
            "Hi there! 🛡️ Welcome to DeepGuard's educational assistant. I can help you learn about deepfakes, detection techniques, and how to protect yourself. What's on your mind?",
            "Hey! 👋 I'm here to help you navigate the world of deepfakes. Whether you want to understand what they are, how to spot them, or how to stay safe - just ask!"
        ]
        return random.choice(greetings)
    
    def get_help_message(self) -> str:
        """Return help/capabilities message"""
        return """I can help you with many topics related to deepfakes! Here's what you can ask me about:

🔹 **"What is a deepfake?"** - Understanding the basics
🔹 **"How are deepfakes made?"** - The technology behind them
🔹 **"How to detect deepfakes?"** - Spotting fakes
🔹 **"What are the risks?"** - Understanding dangers
🔹 **"How to protect myself?"** - Safety tips
🔹 **"What laws exist?"** - Legal protections
🔹 **"How does DeepGuard work?"** - Our technology
🔹 **"What's the future?"** - Trends and predictions
🔹 **"Give me a quiz"** - Test your knowledge

Just type your question naturally, and I'll do my best to help! 💡"""
    
    def get_thanks_response(self) -> str:
        """Respond to thanks"""
        responses = [
            "You're welcome! 😊 Remember, staying informed is your best defense against deepfakes. Anything else I can help with?",
            "Happy to help! 🛡️ If you have more questions or want to test a file for deepfakes, I'm here for you!",
            "Anytime! Knowledge is power when it comes to digital safety. Feel free to ask more questions!"
        ]
        return random.choice(responses)
    
    def get_goodbye(self) -> str:
        """Generate goodbye message"""
        goodbyes = [
            "Goodbye! 👋 Stay safe online and remember - if something seems too shocking to be true, verify it first! Take care!",
            "See you later! 🛡️ Remember to stay vigilant and use DeepGuard to check suspicious media. Stay protected!",
            "Bye for now! 💪 You're now more informed about deepfakes. Share this knowledge with others to help them stay safe too!"
        ]
        return random.choice(goodbyes)

    def process_message(self, user_message: str) -> Dict:
        """
        Process user message and generate response.
        Returns dict with response and metadata.
        """
        self.conversation_count += 1
        message_lower = user_message.lower().strip()
        
        # Check for pattern matches
        matched_topic = None
        for pattern, topic in self.patterns:
            if re.search(pattern, message_lower, re.IGNORECASE):
                matched_topic = topic
                break
        
        # Generate response based on matched topic
        if matched_topic == 'greeting':
            response = self.get_greeting()
            topic_title = "Welcome"
        elif matched_topic == 'thanks':
            response = self.get_thanks_response()
            topic_title = "You're Welcome"
        elif matched_topic == 'goodbye':
            response = self.get_goodbye()
            topic_title = "Goodbye"
        elif matched_topic == 'help':
            response = self.get_help_message()
            topic_title = "How I Can Help"
        elif matched_topic and matched_topic in self.knowledge_base:
            kb_entry = self.knowledge_base[matched_topic]
            response = f"**{kb_entry['title']}**\n\n{kb_entry['content']}\n\n💡 *{kb_entry['follow_up']}*"
            topic_title = kb_entry['title']
        else:
            # Default response for unmatched queries
            response = self._get_fallback_response(user_message)
            topic_title = "Let Me Help"
        
        # Add to context
        self.context.append({
            'user': user_message,
            'bot': response,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return {
            'response': response,
            'topic': topic_title,
            'conversation_count': self.conversation_count,
            'suggestions': self._get_suggestions(matched_topic)
        }
    
    def _get_fallback_response(self, message: str) -> str:
        """Generate fallback response for unmatched queries"""
        fallbacks = [
            f"I'm not quite sure about that specific topic, but I'd love to help you learn about deepfakes! Try asking me:\n\n• What is a deepfake?\n• How can I spot fake videos?\n• How do I protect myself?\n\nOr type **'help'** to see all topics I can discuss!",
            
            f"Hmm, I'm specialized in deepfake education. Let me suggest some topics:\n\n🔹 Detection techniques\n🔹 Protection tips\n🔹 Risks and dangers\n🔹 Our technology\n\nWhat interests you most?",
            
            f"I want to make sure I give you accurate information! While I focus on deepfakes, I can cover:\n\n• How deepfakes work\n• How to detect them\n• How to stay safe\n• Legal aspects\n\nWhich would you like to explore?"
        ]
        return random.choice(fallbacks)
    
    def _get_suggestions(self, current_topic: Optional[str]) -> List[str]:
        """Get relevant follow-up suggestions based on current topic"""
        all_suggestions = {
            'what_is_deepfake': ["How are they made?", "What are the risks?", "How to detect them?"],
            'how_deepfakes_made': ["How to detect them?", "How does DeepGuard work?", "What are the dangers?"],
            'detection_techniques': ["Try DeepGuard detection", "How to protect myself?", "What are the risks?"],
            'risks_dangers': ["How to protect myself?", "What laws exist?", "How to detect deepfakes?"],
            'protection_tips': ["Test your knowledge", "What are the laws?", "How does DeepGuard work?"],
            'laws_regulations': ["How to report deepfakes?", "Protection tips", "What's the future?"],
            'our_technology': ["Try uploading a file", "Detection techniques", "What are deepfakes?"],
            'future_of_deepfakes': ["How to stay protected?", "Current detection methods", "Take the quiz"],
            'quiz': ["Learn more basics", "Protection tips", "How DeepGuard works"],
            None: ["What is a deepfake?", "How to detect them?", "Protection tips"]
        }
        return all_suggestions.get(current_topic, all_suggestions[None])
    
    def get_quick_tips(self) -> List[str]:
        """Return quick tips for the UI"""
        return [
            "🔍 Always verify shocking content before sharing",
            "👁️ Check for unnatural blinking in videos",
            "🔊 Listen for robotic or mechanical voice quality",
            "🌐 Use reverse image search for suspicious photos",
            "🛡️ Limit personal photos shared publicly online"
        ]


# Create singleton instance
chatbot = DeepfakeEducationBot()


def get_chat_response(message: str) -> Dict:
    """API function to get chatbot response"""
    return chatbot.process_message(message)


def get_quick_tips() -> List[str]:
    """API function to get quick tips"""
    return chatbot.get_quick_tips()
