"""
Module to load encrypted environment variables
This would be integrated into your main.exe
"""
import os
from env_crypto import EnvCrypto

def load_encrypted_env(env_file='.env.enc', key_file='.env.key', password=None):
    """
    Load encrypted environment variables into os.environ
    
    Args:
        env_file (str): Path to the encrypted .env file
        key_file (str): Path to the key file (used if password is None)
        password (str, optional): Password to decrypt the file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create crypto instance
        crypto = EnvCrypto(password)
        
        # If no password provided, try to load key from file
        if not password and os.path.exists(key_file):
            crypto.load_key_from_file(key_file)
        
        # Get environment values
        env_values, _ = crypto.get_env_values(env_file)
        
        if not env_values:
            print(f"Failed to load environment from {env_file}")
            return False
        
        # Set environment variables
        for key, value in env_values.items():
            os.environ[key] = value
        
        print(f"Successfully loaded {len(env_values)} environment variables")
        return True
    
    except Exception as e:
        print(f"Error loading encrypted environment: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    success = load_encrypted_env(password="your-secure-password")
    
    if success:
        # Test that we can access environment variables
        print("\nTesting access to environment variables:")
        test_vars = ['DEBUG_MODE', 'INTERNET_CHECK', 'STOP_SCRIPT']
        for var in test_vars:
            print(f"{var} = {os.getenv(var, 'Not found')}")
    else:
        print("Failed to load environment variables")
