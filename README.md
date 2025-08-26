# Encrypted Environment Configuration Manager

A secure system for managing encrypted `.env` configuration files with both command-line and interactive menu interfaces.

## Overview

This tool provides a secure way to store sensitive configuration data (passwords, API keys, etc.) by encrypting your `.env` file. It includes:

- Password-based encryption using industry-standard cryptography
- Command-line interface for scripting and automation
- Interactive menu interface for easy configuration management
- Preservation of original key order in configuration files
- Secure password handling with masking for sensitive values

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Script Documentation

The project includes several Python scripts, each with a specific purpose:

### Core Module

#### `env_crypto.py`

Core encryption/decryption module that handles all cryptographic operations.

- **Purpose**: Provides the `EnvCrypto` class for encrypting/decrypting environment variables
- **Usage**: Not meant to be used directly, but imported by other scripts
- **Key Functions**:
  - `encrypt_env_file()`: Encrypts a .env file
  - `decrypt_env_file()`: Decrypts an encrypted .env file
  - `get_env_values()`: Retrieves values from encrypted file
  - `set_env_values()`: Updates values in encrypted file

### Utility Scripts

#### `create_encrypted_env.py`

- **Purpose**: Creates an initial encrypted .env file from a plain text .env file
- **Usage**: `python src/create_encrypted_env.py`
- **When to Use**: When setting up the system for the first time
- **Behavior**: 
  - Prompts for a password
  - Encrypts the .env file to .env.enc
  - Creates a .env.key file (optional)
  - Tests decryption to verify everything works

#### `test_crypto.py`

- **Purpose**: Tests the encryption/decryption functionality
- **Usage**: `python src/test_crypto.py`
- **When to Use**: To verify the encryption system works correctly
- **Behavior**: Creates test data, encrypts it, decrypts it, and verifies the result

#### `change_password.py`

- **Purpose**: Changes the encryption password for an existing .env.enc file
- **Usage**: `python src/change_password.py`
- **When to Use**: When you want to update your encryption password
- **Behavior**: 
  - Prompts for current password
  - Verifies it can decrypt the file
  - Prompts for new password
  - Re-encrypts the file with the new password

#### `regenerate_key.py`

- **Purpose**: Regenerates the .env.key file if it's lost
- **Usage**: `python src/regenerate_key.py`
- **When to Use**: When you've lost the .env.key file but still have the password
- **Behavior**:
  - Prompts for the encryption password
  - Verifies it can decrypt the .env.enc file
  - Creates a new .env.key file

#### `load_env.py`

- **Purpose**: Loads encrypted environment variables into your application
- **Usage**: Import and call `load_encrypted_env()` in your application
- **When to Use**: In your main application to access encrypted config
- **Example**:
  ```python
  from src.load_env import load_encrypted_env
  load_encrypted_env(password="your-password")
  ```

### User Interface Scripts

#### `config_menu.py`

- **Purpose**: Interactive menu for managing encrypted configuration
- **Usage**: `python src/config_menu.py`
- **When to Use**: For regular configuration management tasks
- **Features**:
  - View all configuration values
  - Edit configuration values
  - Add new configuration values
  - Delete configuration values
  - Initialize/reset configuration
  - Export configuration to a plain text file
  - Import configuration from a plain text file
  - Change encryption password

#### `config_cli.py`

- **Purpose**: Command-line interface for scripting and automation
- **Usage**: `python src/config_cli.py [command] [options]`
- **When to Use**: For automation or when you prefer command-line tools
- **Commands**:
  - `init`: Initialize or reset the encrypted configuration
  - `view`: View all or specific configuration values
  - `get`: Get a specific configuration value
  - `set`: Set a configuration value
  - `export`: Export configuration to a plain text file
  - `import`: Import configuration from a plain text file
- **Examples**:
  ```
  python src/config_cli.py view --password your-password
  python src/config_cli.py set API_KEY "new-value" --password your-password
  ```

## Quick Start

### Initialize Encrypted Configuration

To create an encrypted configuration file from an existing `.env` file:

```
python src/create_encrypted_env.py
```

You'll be prompted for a password to encrypt the file.

### Using the Interactive Menu

The recommended way to manage your configuration:

```
python src/config_menu.py
```

This will present a user-friendly menu with options to manage your configuration.

### Integrating with Your Application

To use the encrypted configuration in your main application:

```python
from src.load_env import load_encrypted_env

# Load encrypted environment variables into os.environ
load_encrypted_env(password="your-password")

# Now you can use os.getenv() as usual
import os
api_key = os.getenv("API_KEY")
```

## Security Features

- **Password-based Key Derivation**: Uses PBKDF2 with SHA-256 and 100,000 iterations
- **Symmetric Encryption**: Uses Fernet (AES-128 in CBC mode with PKCS7 padding)
- **Sensitive Value Masking**: Automatically masks passwords and keys in display
- **Password Confirmation**: Requires confirmation for password changes
- **No Plaintext Storage**: Configuration is always stored encrypted

## File Structure

- `.env.enc`: The encrypted configuration file
- `.env.key`: Optional key file (if not using password-based encryption)

## Key Recovery and Password Management

### Understanding the Encryption System

The encryption system works as follows:

1. When you encrypt a file with a password, a unique encryption key is derived from that password
2. This derived key is what's actually used to encrypt/decrypt the file
3. The `.env.key` file contains this derived key

This means:
- The key is cryptographically linked to the encrypted file
- You cannot create a new key with a different password for an existing `.env.enc` file
- To change the password, you must decrypt with the old password and re-encrypt with the new one

### Recovery Options

1. **If you lose the `.env.key` file but remember the password**:
   - Use `regenerate_key.py` to create a new key file
   - The password must be the same one used to create the original encrypted file

2. **If you forget the password and don't have the `.env.key` file**:
   - Unfortunately, there's no way to recover the data (this is by design for security)
   - You'll need to recreate your `.env` file from scratch and re-encrypt it

3. **If you want to change your password**:
   - Use the "Change Encryption Password" option in the menu
   - Or run `change_password.py`

## Advanced Usage

### Changing the Encryption Password

Using the interactive menu:
1. Run `python src/config_menu.py`
2. Select option 8 (Change Encryption Password)
3. Enter your current password and then your new password

Using the standalone script:
```
python src/change_password.py
```

### Recovering a Lost Key File

If you've lost your `.env.key` file but still have your `.env.enc` file and remember your password:

```
python src/regenerate_key.py
```

This utility will:
1. Ask for your encryption password
2. Verify it can decrypt your `.env.enc` file
3. Generate a new `.env.key` file with the correct key

### Using Key Files Instead of Passwords

For automated systems, you can use a key file instead of a password:

```python
from src.load_env import load_encrypted_env

# Load using key file
load_encrypted_env(key_file=".env.key")
```

## Best Practices

1. **Backup Your Key**: Always keep a backup of your `.env.key` file or remember your password
2. **Don't Commit Sensitive Files**: Add `.env`, `.env.enc`, and `.env.key` to your `.gitignore`
3. **Regular Password Changes**: Change your encryption password periodically
4. **Secure Password Storage**: Use a password manager to store your encryption password

## Troubleshooting

- **"Failed to decrypt with current password"**: Double-check your password
- **"Failed to load configuration"**: Ensure `.env.enc` exists and is valid
- **"Error loading key"**: Check that `.env.key` exists and is valid

## License

This project is licensed under the MIT License - see the LICENSE file for details.
