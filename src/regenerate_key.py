#!/usr/bin/env python
"""Utility to regenerate the .env.key file from a password
Use this if you've lost your .env.key file but still have your .env.enc file
and remember your password
"""
import os
import getpass

# Use the EnvCrypto class directly to ensure consistency
from env_crypto import EnvCrypto

def main():
    """Main function to regenerate the key file"""
    print("===== .env.key Regeneration Utility =====")
    
    # Check if .env.enc exists
    if not os.path.exists('.env.enc'):
        print("Error: .env.enc file not found!")
        print("This utility requires your encrypted .env.enc file to verify the password.")
        return False
    
    # Get the password
    password = getpass.getpass("Enter your encryption password: ")
    
    if not password:
        print("Error: Password cannot be empty.")
        return False
    
    # Create crypto instance with the password
    crypto = EnvCrypto(password)
    
    # Test if the password works by trying to decrypt
    print("Verifying password...")
    try:
        # Read the encrypted file
        with open('.env.enc', 'rb') as f:
            encrypted_data = f.read()
        
        # Try to decrypt
        decrypted_data = crypto.cipher.decrypt(encrypted_data)
        
        # If we get here, decryption was successful
        print("Password verified successfully!")
        
        # Save the key
        key_file = '.env.key'
        with open(key_file, 'wb') as f:
            f.write(crypto.key)
        
        print(f"Success! Key file regenerated and saved to {key_file}")
        print("You can now use this key file for password-less decryption.")
        
        return True
    except Exception as e:
        print(f"Error decrypting file: {str(e)}")
        print("Failed to decrypt .env.enc with the provided password.")
        print("Please check your password and try again.")
        return False

if __name__ == "__main__":
    main()
