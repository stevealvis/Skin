# Django Skin Disease Prediction Project - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [File-by-File Analysis](#file-by-file-analysis)
4. [Application Workflow](#application-workflow)
5. [Database Models](#database-models)
6. [Views and Functionality](#views-and-functionality)
7. [URL Routing](#url-routing)
8. [User Roles and Authentication](#user-roles-and-authentication)
9. [Disease Prediction System](#disease-prediction-system)
10. [Consultation System](#consultation-system)
11. [Chat System](#chat-system)

## Project Overview

This is a comprehensive Django-based web application for skin disease prediction and telemedicine consultation. The system allows patients to:
- Predict skin diseases based on symptoms or by uploading skin images
- Consult with doctors through a chat-based consultation system
- Rate and review doctors after consultations
- View their consultation history

The application features two types of predictions:
1. **Symptom-based prediction**: Uses a trained machine learning model to predict diseases based on 132 symptoms
2. **Image-based prediction**: Uses a CNN model to analyze uploaded skin images

## Project Structure

```
skin-D-P/
├── manage.py                    # Django command-line utility
├── requirements.txt             # Python dependencies
├── db.sqlite3                  # SQLite database
├── disease_prediction/         # Main Django project directory
│   ├── __init__.py
│   ├── settings.py             # Django settings configuration
│   ├── urls.py                 # Main URL routing
│   └── wsgi.py                 # WSGI configuration
├── main_app/                   # Main application
│   ├── models.py               # Database models
│   ├── views.py                # Main business logic
│   ├── urls.py                 # Application URLs
│   └── migrations/             # Database migrations
├── accounts/                   # User authentication app
│   ├── views.py                # Login/logout/signup logic
│   └── urls.py                 # Authentication URLs
├── chats/                      # Chat system app
│   ├── models.py               # Chat and feedback models
│   └── urls.py                 # Chat URLs
├── templates/                  # HTML templates
├── media/                      # User uploaded files
└── trained_model               # Machine learning model
```

## File-by-File Analysis

### 1. manage.py
**Purpose**: Django's command-line utility for administrative tasks
**Key Functions**:
- Sets Django settings module
- Handles Django management commands (runserver, migrate, etc.)
- Entry point for Django administration

### 2. disease_prediction/settings.py
**Purpose**: Main Django configuration file
**Key Components**:
- **DEBUG**: Set to True for development
- **DATABASES**: SQLite configuration for development
- **INSTALLED_APPS**: Lists all Django apps
- **MIDDLEWARE**: Security and session middleware
- **TEMPLATES**: Template configuration
- **STATIC_URL**: Static file serving configuration
- **MEDIA_URL**: User uploaded files configuration

### 3. disease_prediction/urls.py
**Purpose**: Main URL routing configuration
**URLs**:
- `/admin/` - Django admin interface
- `""` - Main app homepage
- `accounts/` - Authentication URLs
- Chat system URLs

### 4. main_app/models.py
**Purpose**: Database schema definitions

#### Models:
1. **patient Model**:
   - Links to Django's User model
   - Stores patient-specific data (name, DOB, address, mobile, gender)
   - Calculates age dynamically using @property decorator
   - Fields: user, is_patient, is_doctor, name, dob, address, mobile_no, gender

2. **doctor Model**:
   - Links to Django's User model
   - Stores doctor credentials and specialization
   - Includes medical council registration details
   - Fields: user, is_patient, is_doctor, name, dob, address, mobile_no, gender, registration_no, year_of_registration, qualification, State_Medical_Council, specialization, rating

3. **diseaseinfo Model**:
   - Stores disease prediction results
   - Supports both symptom-based and image-based predictions
   - Stores symptoms as JSON array in TextField
   - Includes confidence score and recommended doctor specialization
   - Fields: patient, diseasename, no_of_symp, symptomsname, confidence, consultdoctor, skin_image, prediction_method
   - Custom methods: get_symptomsname_list(), custom save() method for JSON handling

4. **consultation Model**:
   - Links patients with doctors for consultations
   - Tracks consultation status and date
   - Fields: patient, doctor, diseaseinfo, consultation_date, status

5. **rating_review Model**:
   - Stores patient ratings and reviews for doctors
   - Calculates average rating using @property decorator
   - Fields: patient, doctor, rating, review

### 5. main_app/views.py
**Purpose**: Main business logic and request handling

#### Key Functions:

**1. home(request)**:
- Handles homepage rendering
- Checks user authentication status
- Renders homepage template

**2. checkdisease(request)**:
- Implements symptom-based disease prediction
- **GET**: Displays symptoms selection interface
- **POST**: Processes symptoms and makes prediction
- **Workflow**:
  1. Receives selected symptoms from POST data
  2. Maps symptoms to ML model features (132 symptoms)
  3. Creates feature vector (0s and 1s)
  4. Calls trained ML model for prediction
  5. Calculates confidence score
  6. Maps disease to appropriate doctor specialization
  7. Saves prediction to database
  8. Returns JSON response with results

**3. scan_image(request)**:
- Implements image-based disease prediction
- **GET**: Displays image upload interface
- **POST**: Processes uploaded skin image
- **Workflow**:
  1. Validates uploaded image
  2. Preprocesses image (resize, normalize, convert to numpy array)
  3. Runs CNN model prediction (if available)
  4. Returns disease prediction with confidence
  5. Saves results with image to database

**4. consult_a_doctor(request)**:
- Displays list of doctors filtered by specialization
- Uses session data to filter doctors based on predicted disease

**5. make_consultation(request, doctorusername)**:
- Creates new consultation between patient and doctor
- Links consultation to disease prediction results
- Sets consultation status to "active"

**6. consultationview(request, consultation_id)**:
- Displays consultation chat interface
- Loads chat messages for the consultation

**7. post(request)**:
- Handles AJAX chat message posting
- Saves chat messages to database
- Returns JSON response for real-time updates

**8. chat_messages(request)**:
- Retrieves chat messages for consultation
- Renders chat body template

### 6. accounts/views.py
**Purpose**: User authentication and account management

#### Key Functions:

**1. signup_patient(request)**:
- Handles patient registration
- **Validation**: Checks all required fields, password matching, unique username/email
- **Process**: Creates User object, creates patient profile, saves to database

**2. sign_in_patient(request)**:
- Authenticates patient users
- Checks if user has patient profile
- Sets session data for patient

**3. signup_doctor(request)**:
- Handles doctor registration
- **Additional fields**: Medical council registration, qualification, specialization
- **Validation**: Enhanced validation for medical credentials

**4. sign_in_doctor(request)**:
- Authenticates doctor users
- Checks if user has doctor profile
- Sets session data for doctor

**5. sign_in_admin(request)**:
- Authenticates superuser/admin
- Redirects to admin interface

**6. savepdata(request, patientusername)**:
- Updates patient profile information
- Handles profile editing functionality

### 7. chats/models.py
**Purpose**: Chat system and feedback functionality

#### Models:

**1. Chat Model**:
- Stores chat messages during consultations
- Links to consultation, sender (User), and message content
- Fields: created, consultation_id, sender, message

**2. Feedback Model**:
- Stores user feedback for the platform
- Fields: created, sender, feedback

### 8. accounts/urls.py
**Purpose**: Authentication URL routing
**URLs**:
- Patient signup/signin
- Doctor signup/signin
- Admin signin
- Profile management

## Application Workflow

### Patient Journey:
1. **Registration/Signup** → User creates patient account
2. **Sign In** → Authenticates and sets session
3. **Disease Check** → Selects symptoms or uploads image
4. **Prediction** → Receives disease prediction and confidence score
5. **Doctor Selection** → Views filtered list of doctors
6. **Consultation** → Starts chat-based consultation with doctor
7. **Chat Communication** → Real-time messaging with doctor
8. **Rating/Review** → Rates doctor after consultation
9. **History** → Views consultation history

### Doctor Journey:
1. **Registration/Signup** → Doctor creates account with credentials
2. **Sign In** → Authenticates and accesses doctor dashboard
3. **Consultation Requests** → Views active consultations
4. **Chat Communication** → Responds to patient messages
5. **Profile Management** → Updates doctor information and credentials

### Admin Journey:
1. **Sign In** → Admin authentication
2. **Dashboard** → Views platform statistics and feedback
3. **User Management** → Manages users through Django admin

## Disease Prediction System

### Symptom-Based Prediction:
1. **Symptoms List**: 132 predefined symptoms
2. **Feature Vector**: Binary vector (0/1) for each symptom
3. **ML Model**: Pre-trained model loaded via joblib
4. **Prediction**: Returns disease name and confidence score
5. **Doctor Mapping**: Maps disease to medical specialization

### Image-Based Prediction:
1. **Image Upload**: Accepts skin image files
2. **Preprocessing**: Resize to 224x224, normalize, convert to array
3. **CNN Model**: TensorFlow/Keras model (if available)
4. **Prediction**: Returns disease classification
5. **Fallback**: Placeholder prediction when CNN not available

## Consultation System

### Consultation Creation:
1. Patient selects doctor from filtered list
2. System creates consultation record
3. Links consultation to disease prediction
4. Sets status to "active"

### Chat Integration:
1. Real-time messaging between patient and doctor
2. Messages saved to Chat model
3. AJAX-based message posting
4. Chat history viewable in consultation

### Rating System:
1. Patients rate doctors (1-5 stars)
2. Reviews stored in rating_review model
3. Doctor ratings calculated dynamically
4. Average rating displayed on doctor profiles

## User Roles and Authentication

### Patient Role:
- Can predict diseases
- Can start consultations
- Can chat with doctors
- Can rate/review doctors
- Can view consultation history

### Doctor Role:
- Can respond to consultations
- Can chat with patients
- Can manage profile
- Can view consultation history
- Receives ratings and reviews

### Admin Role:
- Can access Django admin interface
- Can view all platform data
- Can manage users and content

## Security Features

1. **Authentication**: Django's built-in authentication system
2. **Session Management**: Secure session handling
3. **CSRF Protection**: Django CSRF middleware enabled
4. **Input Validation**: Form and request data validation
5. **File Upload Security**: Image validation and verification
6. **Database Security**: Django ORM prevents SQL injection

## Technical Features

1. **Responsive Design**: Bootstrap-based responsive templates
2. **AJAX Integration**: Real-time chat functionality
3. **Image Processing**: PIL for image handling
4. **Machine Learning**: Scikit-learn and TensorFlow integration
5. **Database**: SQLite for development (easily switchable to PostgreSQL)
6. **Session Management**: Django session framework
7. **Static Files**: Static file serving configuration
8. **Media Handling**: User uploaded file management

## Development Setup

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Run Migrations**: `python manage.py migrate`
3. **Create Superuser**: `python manage.py createsuperuser`
4. **Run Server**: `python manage.py runserver`
5. **Access Admin**: `http://localhost:8000/admin/`

## Future Enhancements

1. **Advanced Image Processing**: Enhanced CNN models
2. **Video Consultations**: Video chat integration
3. **Appointment Scheduling**: Calendar-based scheduling
4. **Payment Integration**: Online payment processing
5. **Mobile App**: React Native or Flutter mobile app
6. **Real-time Notifications**: WebSocket-based notifications
7. **Analytics Dashboard**: Advanced reporting and analytics
8. **Multi-language Support**: Internationalization
9. **API Development**: REST API for mobile integration
10. **Enhanced Security**: Two-factor authentication

This documentation provides a comprehensive overview of the Django Skin Disease Prediction project, covering all major components, workflows, and technical details.
