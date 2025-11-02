"""
Authentication service for phone number + verification code login.
"""
import re
import random
import string
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class AuthService:
    """Service for handling phone number authentication with verification codes."""
    
    def __init__(self):
        # In-memory storage for demonstration
        # In production, this would be a database
        self.users: Dict[str, Dict[str, Any]] = {}
        self.verification_codes: Dict[str, Dict[str, Any]] = {}
        
    def validate_phone_number(self, phone_number: str) -> bool:
        """
        Validate phone number format.
        
        Args:
            phone_number (str): Phone number to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Simple validation for Chinese phone numbers (11 digits starting with 1)
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, phone_number))
    
    def generate_verification_code(self) -> str:
        """
        Generate a 6-digit verification code.
        
        Returns:
            str: 6-digit verification code
        """
        return ''.join(random.choices(string.digits, k=6))
    
    def send_verification_code(self, phone_number: str) -> bool:
        """
        Send verification code to the provided phone number.
        
        Args:
            phone_number (str): Phone number to send code to
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.validate_phone_number(phone_number):
            return False
            
        # Generate verification code
        code = self.generate_verification_code()
        
        # Store verification code with expiration time (10 minutes)
        expiration_time = datetime.now() + timedelta(minutes=10)
        self.verification_codes[phone_number] = {
            'code': code,
            'expires_at': expiration_time,
            'attempts': 0
        }
        
        # In a real implementation, you would integrate with an SMS service here
        # For now, we'll just print to console for demonstration
        print(f"Verification code for {phone_number}: {code}")
        
        return True
    
    def verify_code(self, phone_number: str, code: str) -> bool:
        """
        Verify the provided code for the given phone number.
        
        Args:
            phone_number (str): Phone number to verify
            code (str): Verification code
            
        Returns:
            bool: True if verification successful, False otherwise
        """
        # Check if phone number exists in verification codes
        if phone_number not in self.verification_codes:
            return False
            
        verification_data = self.verification_codes[phone_number]
        
        # Check if code has expired
        if datetime.now() > verification_data['expires_at']:
            # Remove expired code
            del self.verification_codes[phone_number]
            return False
            
        # Check attempt limit (5 attempts)
        if verification_data['attempts'] >= 5:
            # Remove code after too many attempts
            del self.verification_codes[phone_number]
            return False
            
        # Increment attempts
        verification_data['attempts'] += 1
        
        # Check if code matches
        if verification_data['code'] == code:
            # Reset attempts on successful verification
            verification_data['attempts'] = 0
            return True
            
        return False
    
    def register_user(self, phone_number: str) -> bool:
        """
        Register a new user with the provided phone number.
        
        Args:
            phone_number (str): Phone number to register
            
        Returns:
            bool: True if registration successful, False otherwise
        """
        if not self.validate_phone_number(phone_number):
            return False
            
        # Check if user already exists
        if phone_number in self.users:
            return True  # User already registered
            
        # Register new user
        self.users[phone_number] = {
            'phone_number': phone_number,
            'created_at': datetime.now(),
            'last_login': None
        }
        
        return True
    
    def login_user(self, phone_number: str, code: str) -> Optional[Dict[str, Any]]:
        """
        Login user with phone number and verification code.
        
        Args:
            phone_number (str): Phone number
            code (str): Verification code
            
        Returns:
            dict: User data if login successful, None otherwise
        """
        # Verify the code
        if not self.verify_code(phone_number, code):
            return None
            
        # Register user if not already registered
        if not self.register_user(phone_number):
            return None
            
        # Update last login time
        user = self.users[phone_number]
        user['last_login'] = datetime.now()
        
        return user
    
    def is_rate_limited(self, phone_number: str) -> bool:
        """
        Check if the phone number is rate limited.
        
        Args:
            phone_number (str): Phone number to check
            
        Returns:
            bool: True if rate limited, False otherwise
        """
        # Simple rate limiting: 5 requests per 10 minutes
        if phone_number not in self.verification_codes:
            return False
            
        verification_data = self.verification_codes[phone_number]
        
        # Check if attempts exceed limit
        return verification_data['attempts'] >= 5