"""
Simple script to create an encrypted .env file
"""
from env_crypto import EnvCrypto

def main():
    # Create an instance of EnvCrypto with a password
    password = "test"  # You should change this
    crypto = EnvCrypto(password)
    
    print("Encrypting .env file...")
    
    # Encrypt the .env file
    success = crypto.encrypt_env_file()
    
    if success:
        print("Encryption successful!")
        print("Created .env.enc file")
        print("Created .env.key file (keep this secure!)")
        
        # Test decryption
        print("\nTesting decryption...")
        env_values = crypto.get_env_values()
        
        if env_values:
            print("Decryption successful!")
            print(f"Found {len(env_values)} environment variables")
            
            # Print a few values as a test (don't print sensitive ones)
            safe_keys = ['DEBUG_MODE', 'INTERNET_CHECK', 'STOP_SCRIPT']
            for key in safe_keys:
                if key in env_values:
                    print(f"{key} = {env_values[key]}")
        else:
            print("Decryption failed!")
    else:
        print("Encryption failed!")

if __name__ == "__main__":
    main()
