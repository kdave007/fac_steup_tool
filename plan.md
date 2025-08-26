# Factory Setup Tool - Project Plan

## Project Overview
This project provides a secure configuration manager for a Python application that normally uses a .env file.
Instead of storing sensitive information (DB credentials, encryption keys, API tokens) in plain text, this system stores them in an encrypted .env.enc file.

Two executables are part of the solution:

config.exe → A command-line utility for creating, updating, and managing the encrypted configuration.

main.exe → The primary application, which reads and decrypts .env.enc at runtime to load the environment variables into memory.

## Project Components

### 1. Data Processing
Eliminate plain-text secrets from the .env file.

Provide a user-friendly way to manage and update configuration.

Ensure the main application can continue using os.getenv() without modification.

Keep the system simple, portable, and secure.

## Implementation Plan

### Phase 1: Setup and Configuration
- [x] Create environment configuration (.env file)
- [ ] Set up project structure and directories
- [ ] Install required dependencies
- [ ] Configure development environment


## Notes
- The project handles sensitive data (database credentials, API keys)
- Location-specific processing (CLAVE_SUCURSAL=ROTON, CLAVE_PLAZA=XALAP)
- Date-specific processing capability (SPECIFIC_DATE)
- Toggle for SQL operations (SQL_ENABLED)
- Debug mode available for development (DEBUG_MODE)
