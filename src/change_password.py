"""
Utility to change the encryption password for .env.enc
"""
import os
import getpass
from env_crypto import EnvCrypto

def change_password(env_file='.env.enc', key_file='.env.key'):
    """
    Change the encryption password for an encrypted .env file
    
    Args:
        env_file (str): Path to the encrypted .env file
        key_file (str): Path to the key file
    """
    # Check if the encrypted file exists
    if not os.path.exists(env_file):
        print(f"Error: {env_file} not found.")
        return False
    
    # Get the current password
    current_password = getpass.getpass("Enter current password: ")
    
    # Create crypto instance with current password
    crypto = EnvCrypto(current_password)
    
    # Try to decrypt the file to verify the password
    content = crypto.decrypt_env_file(env_file)
    if not content:
        print("Error: Failed to decrypt with current password.")
        return False
    
    # Get the new password
    new_password = getpass.getpass("Enter new password: ")
    confirm_password = getpass.getpass("Confirm new password: ")
    
    if new_password != confirm_password:
        print("Error: Passwords do not match.")
        return False
    
    if not new_password:
        print("Error: Password cannot be empty.")
        return False
    
    # Get current values and key order
    env_dict, key_order = crypto.get_env_values(env_file)
    
    # Create a new crypto instance with the new password
    new_crypto = EnvCrypto(new_password)
    
    # Re-encrypt with the new password
    if not new_crypto.set_env_values(env_dict, key_order, env_file):
        print("Error: Failed to re-encrypt with new password.")
        return False
    
    # Update the key file if it exists
    if os.path.exists(key_file):
        with open(key_file, 'wb') as f:
            f.write(new_crypto.key)
        print(f"Updated key file: {key_file}")
    
    print("Password changed successfully.")
    return True

if __name__ == "__main__":
    change_password()
