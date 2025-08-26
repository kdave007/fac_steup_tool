"""
Test script for the encryption/decryption module
"""
from env_crypto import EnvCrypto

def test_encryption_decryption():
    """Test basic encryption and decryption"""
    print("Testing basic encryption and decryption...")
    
    # Create test data
    test_data = "TEST_KEY=test_value"
    
    # Create crypto instance with a test password
    password = "test-password"
    crypto = EnvCrypto(password)
    
    # Encrypt the data
    print("Encrypting test data...")
    encrypted = crypto.cipher.encrypt(test_data.encode('utf-8'))
    print(f"Encrypted data: {encrypted[:20]}...")
    
    # Decrypt the data
    print("Decrypting test data...")
    decrypted = crypto.cipher.decrypt(encrypted).decode('utf-8')
    print(f"Decrypted data: {decrypted}")
    
    # Verify the result
    if decrypted == test_data:
        print("✅ Success! Encryption and decryption working correctly")
    else:
        print("❌ Failed! Decrypted data doesn't match original")

if __name__ == "__main__":
    test_encryption_decryption()
