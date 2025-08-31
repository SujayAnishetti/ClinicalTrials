# AstraZeneca Clinical Trials Portal

## Overview

This is a Flask-based web application for managing clinical trial participant registrations for AstraZeneca. The system allows potential participants to register their interest in clinical trials through a web form, automatically determines eligibility based on age and location criteria, and provides an admin dashboard for managing submissions. The application includes email notification capabilities and focuses on collecting participant health information for trial matching purposes.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM for database operations
- **Database**: SQLite for development with PostgreSQL support through environment configuration
- **Models**: Single UserSubmission model storing participant data, eligibility status, and submission metadata
- **Forms**: WTForms with comprehensive validation for user input and admin search functionality
- **Email Service**: SMTP-based email system with templated notifications and regional customization

### Frontend Architecture
- **Template Engine**: Jinja2 with a modular template structure using base.html inheritance
- **UI Framework**: Bootstrap 5 for responsive design with custom AstraZeneca brand styling
- **CSS**: Custom stylesheet implementing AstraZeneca brand colors (purple #8A0051, yellow #EFAB00)
- **JavaScript**: Vanilla JavaScript for form validation, Bootstrap component initialization, and UI enhancements

### Application Flow
- **Registration Process**: Multi-step form validation → database storage → eligibility determination → confirmation page
- **Admin Interface**: Dashboard with statistics, search/filter capabilities, and bulk email management
- **Eligibility Logic**: Age-based (18+) and pincode validation with automatic status assignment

### Data Management
- **Validation**: Server-side validation using WTForms with regex patterns for mobile and pincode
- **Storage**: Normalized database schema with timestamp tracking and email delivery status
- **Regional Support**: Pincode-based regional mapping for localized email content

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web framework with SQLAlchemy integration
- **Flask-SQLAlchemy**: Database ORM with connection pooling
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form validation and rendering

### Frontend Dependencies
- **Bootstrap 5**: CSS framework loaded from CDN
- **Font Awesome 6**: Icon library for UI elements
- **Custom CSS**: Brand-specific styling implementation

### Email Service
- **SMTP**: Standard email protocol for notification delivery
- **Email Templates**: HTML-based templates with regional customization
- **Bulk Operations**: Support for mass email campaigns to participants

### Development Tools
- **Werkzeug ProxyFix**: Production deployment middleware
- **Python Logging**: Debug and error tracking
- **Environment Configuration**: Support for production database URLs and secrets

### Database Configuration
- **SQLite**: Default development database
- **PostgreSQL**: Production database support via DATABASE_URL environment variable
- **Connection Management**: Pool recycling and health checking for production reliability