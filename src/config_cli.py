"""
Command-line utility for managing encrypted .env files
This would be compiled into config.exe
"""
import sys
import os
import argparse
from env_crypto import EnvCrypto

def get_password():
    """Get password from user input"""
    import getpass
    return getpass.getpass("Enter password: ")

def init_config(args):
    """Initialize a new encrypted config from .env file"""
    password = args.password or get_password()
    crypto = EnvCrypto(password)
    
    if os.path.exists('.env.enc') and not args.force:
        print("Error: .env.enc already exists. Use --force to overwrite.")
        return False
    
    success = crypto.encrypt_env_file()
    if success:
        print("Successfully created encrypted config file (.env.enc)")
        print("Key file created (.env.key) - keep this secure!")
        return True
    else:
        print("Failed to create encrypted config")
        return False

def view_config(args):
    """View all configuration values"""
    password = args.password or get_password()
    crypto = EnvCrypto(password)
    
    if args.key_file and os.path.exists(args.key_file):
        crypto.load_key_from_file(args.key_file)
    
    env_values = crypto.get_env_values()
    if not env_values:
        print("Failed to decrypt configuration")
        return False
    
    print("\nConfiguration Values:")
    print("=====================")
    
    # Get max key length for formatting
    max_key_len = max([len(k) for k in env_values.keys()]) if env_values else 0
    
    # Sort keys for consistent display
    for key in sorted(env_values.keys()):
        value = env_values[key]
        # Mask sensitive values if not showing secrets
        if not args.show_secrets and any(secret in key.lower() for secret in ['password', 'secret', 'key', 'token']):
            value = '*' * 8
        print(f"{key.ljust(max_key_len)} = {value}")
    
    return True

def get_config_value(args):
    """Get a specific configuration value"""
    password = args.password or get_password()
    crypto = EnvCrypto(password)
    
    if args.key_file and os.path.exists(args.key_file):
        crypto.load_key_from_file(args.key_file)
    
    env_values = crypto.get_env_values()
    if not env_values:
        print("Failed to decrypt configuration")
        return False
    
    if args.key in env_values:
        value = env_values[args.key]
        # Mask sensitive values if not showing secrets
        if not args.show_secrets and any(secret in args.key.lower() for secret in ['password', 'secret', 'key', 'token']):
            value = '*' * 8
        print(f"{args.key} = {value}")
        return True
    else:
        print(f"Key '{args.key}' not found in configuration")
        return False

def set_config_value(args):
    """Set a configuration value"""
    password = args.password or get_password()
    crypto = EnvCrypto(password)
    
    if args.key_file and os.path.exists(args.key_file):
        crypto.load_key_from_file(args.key_file)
    
    success = crypto.set_env_value(args.key, args.value)
    if success:
        print(f"Successfully set {args.key} = {args.value}")
        return True
    else:
        print(f"Failed to set {args.key}")
        return False

def export_config(args):
    """Export encrypted config to a plain .env file"""
    password = args.password or get_password()
    crypto = EnvCrypto(password)
    
    if args.key_file and os.path.exists(args.key_file):
        crypto.load_key_from_file(args.key_file)
    
    output_file = args.output or '.env.exported'
    if os.path.exists(output_file) and not args.force:
        print(f"Error: {output_file} already exists. Use --force to overwrite.")
        return False
    
    success = crypto.decrypt_env_file(output_file=output_file)
    if success:
        print(f"Successfully exported config to {output_file}")
        return True
    else:
        print("Failed to export configuration")
        return False

def import_config(args):
    """Import a plain .env file to encrypted config"""
    password = args.password or get_password()
    crypto = EnvCrypto(password)
    
    input_file = args.input or '.env'
    if not os.path.exists(input_file):
        print(f"Error: {input_file} does not exist")
        return False
    
    if os.path.exists('.env.enc') and not args.force:
        print("Error: .env.enc already exists. Use --force to overwrite.")
        return False
    
    success = crypto.encrypt_env_file(input_file=input_file)
    if success:
        print(f"Successfully imported {input_file} to encrypted config")
        return True
    else:
        print(f"Failed to import {input_file}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Manage encrypted environment configuration")
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new encrypted config')
    init_parser.add_argument('--force', action='store_true', help='Overwrite existing files')
    init_parser.add_argument('--password', help='Encryption password (will prompt if not provided)')
    
    # View command
    view_parser = subparsers.add_parser('view', help='View all configuration values')
    view_parser.add_argument('--key-file', help='Path to key file')
    view_parser.add_argument('--password', help='Decryption password (will prompt if not provided)')
    view_parser.add_argument('--show-secrets', action='store_true', help='Show sensitive values')
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Get a specific configuration value')
    get_parser.add_argument('key', help='Configuration key to get')
    get_parser.add_argument('--key-file', help='Path to key file')
    get_parser.add_argument('--password', help='Decryption password (will prompt if not provided)')
    get_parser.add_argument('--show-secrets', action='store_true', help='Show sensitive values')
    
    # Set command
    set_parser = subparsers.add_parser('set', help='Set a configuration value')
    set_parser.add_argument('key', help='Configuration key to set')
    set_parser.add_argument('value', help='Value to set')
    set_parser.add_argument('--key-file', help='Path to key file')
    set_parser.add_argument('--password', help='Encryption password (will prompt if not provided)')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export to plain .env file')
    export_parser.add_argument('--output', help='Output file path (default: .env.exported)')
    export_parser.add_argument('--key-file', help='Path to key file')
    export_parser.add_argument('--password', help='Decryption password (will prompt if not provided)')
    export_parser.add_argument('--force', action='store_true', help='Overwrite existing files')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import from plain .env file')
    import_parser.add_argument('--input', help='Input file path (default: .env)')
    import_parser.add_argument('--password', help='Encryption password (will prompt if not provided)')
    import_parser.add_argument('--force', action='store_true', help='Overwrite existing files')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        init_config(args)
    elif args.command == 'view':
        view_config(args)
    elif args.command == 'get':
        get_config_value(args)
    elif args.command == 'set':
        set_config_value(args)
    elif args.command == 'export':
        export_config(args)
    elif args.command == 'import':
        import_config(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
