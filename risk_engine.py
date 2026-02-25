"""
Risk Engine - Core analysis logic
"""
import re


class RiskEngine:
    """Analyzes user data and calculates digital risk score"""
    
    def __init__(self, user_data):
        self.data = user_data
        self.analysis = {
            'password_risk': 0,
            'email_risk': 0,
            'username_risk': 0,
            'privacy_risk': 0,
            'behavior_risk': 0,
            'breach_risk': 0,
            'total_score': 0,
            'risk_level': '',
            'risk_emoji': '',
            'recommendations': []
        }
    
    def analyze(self):
        """Perform complete risk analysis"""
        self.analyze_password()
        self.analyze_email()
        self.analyze_username()
        self.analyze_privacy()
        self.analyze_behavior()
        self.analyze_breach_simulation()
        self.calculate_total()
        self.classify_risk()
        self.generate_recommendations()
        
        return self.analysis
    
    def analyze_password(self):
        """Analyze password strength (0-25 points risk)"""
        password = self.data.get('password', '')
        risk = 0
        
        # Length check (weak if < 8)
        if len(password) < 8:
            risk += 8
        elif len(password) < 12:
            risk += 4
        
        # No uppercase
        if not re.search(r'[A-Z]', password):
            risk += 4
        
        # No lowercase
        if not re.search(r'[a-z]', password):
            risk += 4
        
        # No numbers
        if not re.search(r'\d', password):
            risk += 4
        
        # No special characters
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            risk += 5
        
        self.analysis['password_risk'] = min(risk, 25)
    
    def analyze_email(self):
        """Analyze email predictability (0-15 points risk)"""
        email = self.data.get('email', '').lower()
        risk = 0
        
        # Extract local part
        if '@' in email:
            local = email.split('@')[0]
            
            # Contains year pattern (19xx or 20xx)
            if re.search(r'(19|20)\d{2}', local):
                risk += 5
            
            # Excessive digits (more than 4)
            digit_count = sum(c.isdigit() for c in local)
            if digit_count > 4:
                risk += 4
            
            # Very short (< 5 chars)
            if len(local) < 5:
                risk += 3
            
            # Common patterns
            common_patterns = ['test', 'admin', 'user', 'demo', '123']
            if any(pattern in local for pattern in common_patterns):
                risk += 3
        
        self.analysis['email_risk'] = min(risk, 15)
    
    def analyze_username(self):
        """Analyze username exposure risk (0-15 points risk)"""
        username = self.data.get('username', '').lower()
        email = self.data.get('email', '').lower()
        risk = 0
        
        # Same as email prefix
        if '@' in email:
            email_prefix = email.split('@')[0]
            if username == email_prefix:
                risk += 6
        
        # Contains birth year
        if re.search(r'(19|20)\d{2}', username):
            risk += 5
        
        # Too short (< 4 chars)
        if len(username) < 4:
            risk += 4
        
        self.analysis['username_risk'] = min(risk, 15)
    
    def analyze_privacy(self):
        """Analyze privacy exposure (0-15 points risk)"""
        risk = 0
        
        if self.data.get('dob_public'):
            risk += 4
        if self.data.get('phone_public'):
            risk += 4
        if self.data.get('address_public'):
            risk += 4
        if self.data.get('email_public'):
            risk += 3
        
        self.analysis['privacy_risk'] = min(risk, 15)
    
    def analyze_behavior(self):
        """Analyze security behavior (0-10 points risk)"""
        risk = 0
        
        if self.data.get('password_reuse'):
            risk += 4
        if self.data.get('clicks_unknown'):
            risk += 3
        if self.data.get('public_wifi'):
            risk += 3
        
        self.analysis['behavior_risk'] = min(risk, 10)
    
    def analyze_breach_simulation(self):
        """Simulate breach risk (0-20 points risk)"""
        risk = 0
        
        # High risk if password is weak
        if self.analysis['password_risk'] > 15:
            risk += 8
        
        # Username reuse increases risk
        if self.analysis['username_risk'] > 8:
            risk += 6
        
        # Predictable email increases risk
        if self.analysis['email_risk'] > 8:
            risk += 6
        
        self.analysis['breach_risk'] = min(risk, 20)
    
    def calculate_total(self):
        """Calculate total risk score"""
        total = (
            self.analysis['password_risk'] +
            self.analysis['email_risk'] +
            self.analysis['username_risk'] +
            self.analysis['privacy_risk'] +
            self.analysis['behavior_risk'] +
            self.analysis['breach_risk']
        )
        self.analysis['total_score'] = total
    
    def classify_risk(self):
        """Classify risk level based on total score"""
        score = self.analysis['total_score']
        
        if score <= 30:
            self.analysis['risk_level'] = 'LOW'
            self.analysis['risk_emoji'] = '✅'
        elif score <= 60:
            self.analysis['risk_level'] = 'MODERATE'
            self.analysis['risk_emoji'] = '⚠️'
        else:
            self.analysis['risk_level'] = 'HIGH'
            self.analysis['risk_emoji'] = '🚨'
    
    def generate_recommendations(self):
        """Generate personalized recommendations"""
        recs = []
        
        if self.analysis['password_risk'] > 10:
            recs.append("Increase password complexity (use uppercase, lowercase, numbers, special chars)")
        
        if self.data.get('password_reuse'):
            recs.append("Avoid password reuse across different sites")
        
        if self.analysis['username_risk'] > 8:
            recs.append("Remove birth year from username")
        
        if self.analysis['email_risk'] > 8:
            recs.append("Use a less predictable email address")
        
        if self.data.get('dob_public') or self.data.get('phone_public'):
            recs.append("Limit public exposure of personal information (DOB, phone)")
        
        if self.data.get('clicks_unknown'):
            recs.append("Avoid clicking on unknown or suspicious links")
        
        if self.data.get('public_wifi'):
            recs.append("Use VPN when connecting to public WiFi networks")
        
        if self.analysis['breach_risk'] > 12:
            recs.append("Enable two-factor authentication on all accounts")
        
        self.analysis['recommendations'] = recs
