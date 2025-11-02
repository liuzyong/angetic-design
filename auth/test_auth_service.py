"""
Test script for the authentication service.
"""
import sys
import os

# Add the parent directory to the path so we can import the auth module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.auth_service import AuthService


def test_auth_service():
    """Test the authentication service functionality."""
    print("Testing Authentication Service")
    print("=" * 40)
    
    # Create auth service instance
    auth_service = AuthService()
    
    # Test phone number validation
    print("\n1. Testing phone number validation:")
    valid_numbers = ["13812345678", "15987654321"]
    invalid_numbers = ["12345678901", "1381234567", "abcd1234567"]
    
    for number in valid_numbers:
        result = auth_service.validate_phone_number(number)
        print(f"  {number}: {'Valid' if result else 'Invalid'}")
    
    for number in invalid_numbers:
        result = auth_service.validate_phone_number(number)
        print(f"  {number}: {'Valid' if result else 'Invalid'}")
    
    # Test verification code generation
    print("\n2. Testing verification code generation:")
    for i in range(3):
        code = auth_service.generate_verification_code()
        print(f"  Generated code: {code}")
    
    # Test sending verification code
    print("\n3. Testing sending verification code:")
    test_phone = "13812345678"
    result = auth_service.send_verification_code(test_phone)
    print(f"  Sent code to {test_phone}: {'Success' if result else 'Failed'}")
    
    # Test verification (this will require manual input)
    print("\n4. Testing code verification:")
    if test_phone in auth_service.verification_codes:
        code = auth_service.verification_codes[test_phone]['code']
        print(f"  Verification code is: {code}")
        result = auth_service.verify_code(test_phone, code)
        print(f"  Verification result: {'Success' if result else 'Failed'}")
    
    # Test user registration and login
    print("\n5. Testing user registration and login:")
    user = auth_service.login_user(test_phone, code)
    if user:
        print(f"  Login successful for user: {user['phone_number']}")
    else:
        print("  Login failed")


if __name__ == "__main__":
    test_auth_service()