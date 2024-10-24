# Phone Numbers Validator
#### Video Demo:  https://youtu.be/IU-DkwQvkMM
#### Description:

Key Features
User Authentication & Authorization:

Secure user registration and login with password hashing.
Session management using Flask’s built-in session handling to maintain user state.
User-specific data management ensuring that each user can only access their own data.
Phone Number Validation:

Integration with the NumVerify API to validate phone numbers in real-time.
The system checks if a number is valid and retrieves metadata, such as the number’s local and international formats, the country code, and carrier information.
Database Integration:

The application uses SQLite for database management, with tables for storing user information, phone numbers, and country codes.
SQLAlchemy, a powerful ORM for Python, facilitates interaction with the database, ensuring that database operations are simple and efficient.
Record Management:

Users can add new phone number records to the database, update existing records, and delete entries.
The phonebook interface lists all stored numbers, allowing users to view details at a glance.
A dedicated search function enables users to quickly find specific records.
Error Handling:

Robust error handling with custom error pages for common issues such as invalid input, missing data, or server errors.
User-friendly messages guide users in correcting mistakes during form submissions.
Project Structure
app.py: The main application file containing all route definitions, session management, and core logic for handling requests and responses.
helpers.py: Utility functions to streamline tasks like rendering error messages (apology) and enforcing user authentication (login_required).
templates/: HTML files that define the frontend interface, including pages for registration, login, phonebook management, and record searching.
project.db: The SQLite database file that stores user data, validated phone numbers, and country codes.
Design Decisions
Session Management:

The decision to use Flask’s built-in session management allows for straightforward user state tracking and improves security by storing session data server-side.
Database Design:

The database schema was carefully designed to separate user information, phone records, and country data into different tables. This approach allows for scalability and easy maintenance as the application grows.
API Integration:

NumVerify was chosen for its reliable and comprehensive phone validation services, ensuring that the system can handle various international phone formats and provide accurate information.
User Experience:

The web interface is intuitive, with clear navigation and helpful feedback messages, making it accessible even to users without technical expertise.
How to Set Up and Run
Clone the Repository: Start by cloning the repository to your local machine.
Environment Setup: Create a virtual environment and install all dependencies using pip install -r requirements.txt.
Database Initialization: Run the provided SQL scripts to set up the initial database schema.
Run the Application: Use the command flask run to start the development server.
Access the Application: Open a web browser and navigate to http://127.0.0.1:5000 to use the application.
Potential Improvements
While this project covers the core functionality for phone number management, there are several areas for future enhancement:

Two-Factor Authentication: Implementing two-factor authentication would increase security, especially for applications dealing with sensitive data.
User Roles: Introducing different user roles (e.g., admin, regular user) could allow for more granular control over what each user can do within the application.
Bulk Record Upload: Adding the ability to upload multiple phone numbers at once via a CSV file would improve efficiency for users managing large datasets.
Advanced Search Filters: Implementing advanced search features (e.g., by country, carrier, or type) would make the application more versatile and user-friendly.
