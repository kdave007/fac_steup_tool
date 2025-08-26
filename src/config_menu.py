"""
Interactive menu-based configuration tool for encrypted .env files
"""
import os
import sys
import time
from env_crypto import EnvCrypto

class ConfigMenu:
    """Interactive menu for managing encrypted configuration"""
    
    def __init__(self):
        self.password = None
        self.crypto = None
        self.env_values = {}
        self.key_order = []  # To preserve original order of keys
        self.env_file = '.env.enc'
        self.key_file = '.env.key'
        
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_header(self, title):
        """Print a formatted header"""
        self.clear_screen()
        print("=" * 60)
        print(f"{title:^60}")
        print("=" * 60)
        print()
        
    def print_footer(self):
        """Print a formatted footer"""
        print()
        print("-" * 60)
        
    def get_password(self):
        """Get password from user"""
        import getpass
        return getpass.getpass("Enter password: ")
    
    def initialize_crypto(self):
        """Initialize the crypto object with password"""
        if not self.password:
            self.password = self.get_password()
            
        self.crypto = EnvCrypto(self.password)
        
        # If key file exists, try to load it
        if os.path.exists(self.key_file):
            self.crypto.load_key_from_file(self.key_file)
            
    def load_config(self):
        """Load the configuration values"""
        if not self.crypto:
            self.initialize_crypto()
            
        if os.path.exists(self.env_file):
            self.env_values, self.key_order = self.crypto.get_env_values(self.env_file)
            return len(self.env_values) > 0
        return False
    
    def show_main_menu(self):
        """Display the main menu"""
        while True:
            self.print_header("Configuration Manager")
            
            print("1. View All Configuration Values")
            print("2. Edit Configuration Value")
            print("3. Add New Configuration Value")
            print("4. Delete Configuration Value")
            print("5. Initialize/Reset Configuration")
            print("6. Export Configuration")
            print("7. Import Configuration")
            print("8. Change Encryption Password")
            print("9. Exit")
            
            self.print_footer()
            choice = input("\nEnter your choice (1-9): ")
            
            if choice == '1':
                self.view_all_values()
            elif choice == '2':
                self.edit_value()
            elif choice == '3':
                self.add_value()
            elif choice == '4':
                self.delete_value()
            elif choice == '5':
                self.initialize_config()
            elif choice == '6':
                self.export_config()
            elif choice == '7':
                self.import_config()
            elif choice == '8':
                self.change_password()
            elif choice == '9':
                self.print_header("Exiting Configuration Manager")
                print("Thank you for using the Configuration Manager!")
                time.sleep(1)
                sys.exit(0)
            else:
                input("Invalid choice. Press Enter to continue...")
    
    def view_all_values(self):
        """View all configuration values"""
        if not self.load_config():
            self.print_header("Error")
            print("Failed to load configuration. Make sure the file exists and the password is correct.")
            input("\nPress Enter to continue...")
            return
            
        self.print_header("Configuration Values")
        
        # Get max key length for formatting
        max_key_len = max([len(k) for k in self.env_values.keys()]) if self.env_values else 0
        
        # Use original key order
        for key in self.key_order:
            value = self.env_values[key]
            # Mask sensitive values
            if any(secret in key.lower() for secret in ['password', 'secret', 'key', 'token']):
                display_value = '*' * 8
                print(f"{key.ljust(max_key_len)} = {display_value} (hidden)")
            else:
                print(f"{key.ljust(max_key_len)} = {value}")
        
        show_sensitive = input("\nShow sensitive values? (y/n): ").lower() == 'y'
        
        if show_sensitive:
            print("\nSensitive Values:")
            print("-" * 60)
            for key in self.key_order:
                if any(secret in key.lower() for secret in ['password', 'secret', 'key', 'token']):
                    value = self.env_values[key]
                    print(f"{key.ljust(max_key_len)} = {value}")
        
        input("\nPress Enter to continue...")
    
    def edit_value(self):
        """Edit a configuration value"""
        if not self.load_config():
            self.print_header("Error")
            print("Failed to load configuration. Make sure the file exists and the password is correct.")
            input("\nPress Enter to continue...")
            return
            
        self.print_header("Edit Configuration Value")
        
        # Display all keys in original order
        print("Available keys:")
        for i, key in enumerate(self.key_order, 1):
            print(f"{i}. {key}")
            
        try:
            key_index = int(input("\nEnter key number to edit (0 to cancel): ")) - 1
            if key_index < 0:
                return
                
            if key_index >= len(self.key_order):
                input("Invalid key number. Press Enter to continue...")
                return
                
            key = self.key_order[key_index]
            current_value = self.env_values[key]
            
            # Mask sensitive values in display
            display_value = current_value
            if any(secret in key.lower() for secret in ['password', 'secret', 'key', 'token']):
                display_value = '*' * 8
                
            print(f"\nCurrent value for {key}: {display_value}")
            
            # Confirm if user wants to see the actual value for sensitive data
            if display_value != current_value:
                if input("Show actual value? (y/n): ").lower() == 'y':
                    print(f"Actual value: {current_value}")
            
            new_value = input("\nEnter new value (leave empty to cancel): ")
            
            if new_value and new_value != current_value:
                confirm = input(f"Confirm change {key} from '{display_value}' to '{new_value}'? (y/n): ")
                
                if confirm.lower() == 'y':
                    if not self.crypto.set_env_value(key, new_value, self.env_file):
                        print("Failed to update value.")
                    else:
                        print(f"Successfully updated {key}.")
                        # Reload config
                        self.env_values, self.key_order = self.crypto.get_env_values(self.env_file)
            else:
                print("Edit cancelled.")
                
        except ValueError:
            print("Invalid input.")
            
        input("\nPress Enter to continue...")
    
    def add_value(self):
        """Add a new configuration value"""
        if not self.load_config():
            self.print_header("Error")
            print("Failed to load configuration. Make sure the file exists and the password is correct.")
            input("\nPress Enter to continue...")
            return
            
        self.print_header("Add New Configuration Value")
        
        key = input("Enter new key name: ").strip()
        
        if not key:
            print("Key cannot be empty.")
            input("\nPress Enter to continue...")
            return
            
        if key in self.env_values:
            print(f"Key '{key}' already exists. Use Edit option to change its value.")
            input("\nPress Enter to continue...")
            return
            
        value = input(f"Enter value for {key}: ")
        
        confirm = input(f"Confirm adding {key}={value}? (y/n): ")
        
        if confirm.lower() == 'y':
            if not self.crypto.set_env_value(key, value, self.env_file):
                print("Failed to add value.")
            else:
                print(f"Successfully added {key}.")
                # Reload config
                self.env_values, self.key_order = self.crypto.get_env_values(self.env_file)
        else:
            print("Addition cancelled.")
            
        input("\nPress Enter to continue...")
    
    def delete_value(self):
        """Delete a configuration value"""
        if not self.load_config():
            self.print_header("Error")
            print("Failed to load configuration. Make sure the file exists and the password is correct.")
            input("\nPress Enter to continue...")
            return
            
        self.print_header("Delete Configuration Value")
        
        # Display all keys in original order
        print("Available keys:")
        for i, key in enumerate(self.key_order, 1):
            print(f"{i}. {key}")
            
        try:
            key_index = int(input("\nEnter key number to delete (0 to cancel): ")) - 1
            if key_index < 0:
                return
                
            if key_index >= len(self.key_order):
                input("Invalid key number. Press Enter to continue...")
                return
                
            key = self.key_order[key_index]
            value = self.env_values[key]
            
            # Mask sensitive values in display
            display_value = value
            if any(secret in key.lower() for secret in ['password', 'secret', 'key', 'token']):
                display_value = '*' * 8
                
            confirm = input(f"Are you sure you want to delete {key}={display_value}? (y/n): ")
            
            if confirm.lower() == 'y':
                # Remove from dictionary
                env_dict = self.env_values.copy()
                del env_dict[key]
                
                # Convert back to .env format
                content = '\n'.join([f"{k}={v}" for k, v in env_dict.items()])
                
                # Re-encrypt and save
                try:
                    encrypted_data = self.crypto.cipher.encrypt(content.encode('utf-8'))
                    with open(self.env_file, 'wb') as f:
                        f.write(encrypted_data)
                    print(f"Successfully deleted {key}.")
                    # Reload config
                    self.env_values, self.key_order = self.crypto.get_env_values(self.env_file)
                except Exception as e:
                    print(f"Error deleting key: {e}")
            else:
                print("Deletion cancelled.")
                
        except ValueError:
            print("Invalid input.")
            
        input("\nPress Enter to continue...")
    
    def initialize_config(self):
        """Initialize or reset the configuration"""
        self.print_header("Initialize/Reset Configuration")
        
        if os.path.exists(self.env_file):
            confirm = input("This will overwrite the existing configuration. Continue? (y/n): ")
            if confirm.lower() != 'y':
                print("Initialization cancelled.")
                input("\nPress Enter to continue...")
                return
        
        # Get password if not already set
        if not self.password:
            self.password = self.get_password()
            confirm_password = self.get_password()
            
            if self.password != confirm_password:
                print("Passwords do not match.")
                input("\nPress Enter to continue...")
                return
                
        # Initialize crypto
        self.crypto = EnvCrypto(self.password)
        
        # Check if .env exists
        if not os.path.exists('.env'):
            print("No .env file found. Creating an empty configuration.")
            with open('.env', 'w') as f:
                f.write("# Configuration file\n")
        
        # Encrypt the file
        if self.crypto.encrypt_env_file():
            print("Successfully initialized configuration.")
            self.env_values, self.key_order = self.crypto.get_env_values(self.env_file)
        else:
            print("Failed to initialize configuration.")
            
        input("\nPress Enter to continue...")
    
    def export_config(self):
        """Export configuration to a plain text file"""
        if not self.load_config():
            self.print_header("Error")
            print("Failed to load configuration. Make sure the file exists and the password is correct.")
            input("\nPress Enter to continue...")
            return
            
        self.print_header("Export Configuration")
        
        output_file = input("Enter output file path (default: .env.exported): ") or '.env.exported'
        
        if os.path.exists(output_file):
            confirm = input(f"File {output_file} already exists. Overwrite? (y/n): ")
            if confirm.lower() != 'y':
                print("Export cancelled.")
                input("\nPress Enter to continue...")
                return
        
        if self.crypto.decrypt_env_file(self.env_file, output_file):
            print(f"Successfully exported configuration to {output_file}")
        else:
            print("Failed to export configuration.")
            
        input("\nPress Enter to continue...")
    
    def import_config(self):
        """Import configuration from a plain text file"""
        self.print_header("Import Configuration")
        
        input_file = input("Enter path to import from (default: .env): ") or '.env'
        
        if not os.path.exists(input_file):
            print(f"File {input_file} does not exist.")
            input("\nPress Enter to continue...")
            return
            
        # Get password if not already set
        if not self.password:
            self.password = self.get_password()
            
        # Initialize crypto
        self.crypto = EnvCrypto(self.password)
        
        # Encrypt the file
        if self.crypto.encrypt_env_file(input_file, self.env_file):
            print(f"Successfully imported configuration from {input_file}")
            self.env_values, self.key_order = self.crypto.get_env_values(self.env_file)
        else:
            print("Failed to import configuration.")
            
        input("\nPress Enter to continue...")
        
    def change_password(self):
        """Change the encryption password"""
        self.print_header("Change Encryption Password")
        
        # Check if the encrypted file exists
        if not os.path.exists(self.env_file):
            print(f"Error: {self.env_file} not found.")
            input("\nPress Enter to continue...")
            return
        
        # Get the current password if not already set
        if not self.password:
            self.password = self.get_password()
        
        # Create crypto instance with current password if not already created
        if not self.crypto:
            self.crypto = EnvCrypto(self.password)
        
        # Try to decrypt the file to verify the password
        content = self.crypto.decrypt_env_file(self.env_file)
        if not content:
            print("Error: Failed to decrypt with current password.")
            input("\nPress Enter to continue...")
            return
        
        # Get the new password
        import getpass
        new_password = getpass.getpass("Enter new password: ")
        confirm_password = getpass.getpass("Confirm new password: ")
        
        if new_password != confirm_password:
            print("Error: Passwords do not match.")
            input("\nPress Enter to continue...")
            return
        
        if not new_password:
            print("Error: Password cannot be empty.")
            input("\nPress Enter to continue...")
            return
        
        # Get current values and key order
        env_dict, key_order = self.crypto.get_env_values(self.env_file)
        
        # Create a new crypto instance with the new password
        new_crypto = EnvCrypto(new_password)
        
        # Re-encrypt with the new password
        if not new_crypto.set_env_values(env_dict, key_order, self.env_file):
            print("Error: Failed to re-encrypt with new password.")
            input("\nPress Enter to continue...")
            return
        
        # Update the key file if it exists
        if os.path.exists(self.key_file):
            with open(self.key_file, 'wb') as f:
                f.write(new_crypto.key)
            print(f"Updated key file: {self.key_file}")
        
        # Update the current crypto instance and password
        self.crypto = new_crypto
        self.password = new_password
        
        print("Password changed successfully.")
        input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    menu = ConfigMenu()
    menu.show_main_menu()

if __name__ == "__main__":
    main()
