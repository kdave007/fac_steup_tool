"""
Simple encryption/decryption module for .env files
"""
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EnvCrypto:
    """
    A simple class to encrypt and decrypt .env files
    """
    def __init__(self, password=None):
        """
        Initialize the EnvCrypto class
        
        Args:
            password (str, optional): Password to derive the key from
        """
        self.key = None
        self.password = password
        
        if password:
            # Derive a key from the password
            self.derive_key_from_password(password)
        else:
            # Generate a random key
            self.generate_random_key()
        
        # Create the Fernet cipher with our key
        self.cipher = Fernet(self.key)
    
    def derive_key_from_password(self, password):
        """
        Derive a key from a password using PBKDF2
        
        Args:
            password (str): Password to derive the key from
        """
        # Use a fixed salt for simplicity
        # In a production environment, you might want to store this salt securely
        salt = b'fixed_salt_for_env_crypto'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        # Derive the key
        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        self.key = key
        self.password = password
        self.cipher = Fernet(key)
    
    def generate_random_key(self):
        """
        Generate a random key
        """
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def change_password(self, new_password):
        """
        Change the password and re-derive the key
        
        Args:
            new_password (str): The new password
        """
        self.derive_key_from_password(new_password)
    
    def encrypt_env_file(self, input_file='.env', output_file='.env.enc'):
        """
        Encrypt the contents of a .env file
        
        Args:
            input_file (str): Path to the input .env file
            output_file (str): Path to save the encrypted file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read the .env file
            with open(input_file, 'rb') as f:
                env_data = f.read()
            
            # Encrypt the data
            encrypted_data = self.cipher.encrypt(env_data)
            
            # Write the encrypted data to the output file
            with open(output_file, 'wb') as f:
                f.write(encrypted_data)
                
            # Also save the key to a file (in a real app, you'd handle this more securely)
            with open('.env.key', 'wb') as f:
                f.write(self.key)
                
            return True
        except Exception as e:
            print(f"Error encrypting file: {e}")
            return False
    
    def decrypt_env_file(self, input_file='.env.enc', output_file=None):
        """
        Decrypt an encrypted .env file
        
        Args:
            input_file (str): Path to the encrypted .env file
            output_file (str, optional): Path to save the decrypted file.
                                        If None, the content is returned but not saved.
            
        Returns:
            str or None: The decrypted content if successful and output_file is None,
                        True if successful and output_file is provided,
                        False or None if unsuccessful
        """
        try:
            # Read the encrypted file
            with open(input_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt the data
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            if output_file:
                # Write the decrypted data to the output file
                with open(output_file, 'wb') as f:
                    f.write(decrypted_data)
                return True
            else:
                # Return the decrypted data as a string
                return decrypted_data.decode('utf-8')
        except Exception as e:
            print(f"Error decrypting file: {e}")
            return None
    
    def load_key_from_file(self, key_file='.env.key'):
        """
        Load an encryption key from a file
        
        Args:
            key_file (str): Path to the key file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(key_file, 'rb') as f:
                self.key = f.read()
            self.cipher = Fernet(self.key)
            return True
        except Exception as e:
            print(f"Error loading key: {e}")
            return False
    
    def get_env_values(self, input_file='.env.enc'):
        """
        Get the environment values from an encrypted .env file
        
        Args:
            input_file (str): Path to the encrypted .env file
            
        Returns:
            dict: Dictionary of environment variables and list of keys in original order
        """
        # Decrypt the file
        content = self.decrypt_env_file(input_file)
        if not content:
            return {}, []
        
        # Parse the content into a dictionary
        env_dict = {}
        key_order = []  # To preserve original order of keys
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if '=' in line:
                key, value = line.split('=', 1)
                env_dict[key] = value
                if key not in key_order:
                    key_order.append(key)
        
        return env_dict, key_order
    
    def set_env_value(self, key, value, input_file='.env.enc'):
        """
        Set or update an environment variable in the encrypted .env file
        
        Args:
            key (str): The environment variable name
            value (str): The value to set
            input_file (str): Path to the encrypted .env file
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Get current values
        env_dict, _ = self.get_env_values(input_file)
        if env_dict is None:
            return False
        
        # Update or add the new value
        env_dict[key] = value
        
        # Convert back to .env format
        content = '\n'.join([f"{k}={v}" for k, v in env_dict.items()])
        
        # Re-encrypt and save
        try:
            encrypted_data = self.cipher.encrypt(content.encode('utf-8'))
            with open(input_file, 'wb') as f:
                f.write(encrypted_data)
            return True
        except Exception as e:
            print(f"Error updating encrypted file: {e}")
            return False
    
    def set_env_values(self, env_dict, key_order=None, output_file='.env.enc'):
        """
        Set multiple environment values in the encrypted .env file
        
        Args:
            env_dict (dict): Dictionary of environment variables
            key_order (list, optional): List of keys in the order they should appear
            output_file (str): Path to the output file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Convert to .env format using key_order if provided
            if key_order:
                # Use the provided key order, adding any new keys at the end
                all_keys = key_order.copy()
                for k in env_dict.keys():
                    if k not in all_keys:
                        all_keys.append(k)
                content = '\n'.join([f"{k}={env_dict[k]}" for k in all_keys if k in env_dict])
            else:
                content = '\n'.join([f"{k}={v}" for k, v in env_dict.items()])
            
            # Encrypt and save
            encrypted_data = self.cipher.encrypt(content.encode('utf-8'))
            with open(output_file, 'wb') as f:
                f.write(encrypted_data)
            return True
        except Exception as e:
            print(f"Error setting environment values: {e}")
            return False
