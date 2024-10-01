# product fusion

Basic login and email system for assessments
## Tech Stack

This application is built with the following technologies:

- **Python** 3.12
- **Django** 4.2.15
- **PostgreSQL** 15


### Installation
1. **Clone the repository:**

2. **Navigate to the project directory:**

3. **Create a virtual environment:**

4. **Activate the virtual environment:**
- On Windows:
  ```
  .\venv\Scripts\activate
  ```
- On Unix or MacOS:
  ```
  source venv/bin/activate
  ```

5. **Install required dependencies:**

6. **Set up the PostgreSQL database:**
- Create a new PostgreSQL database (*Or run via docker compose*)
- Update the database settings in `.env` with your database information.

7. **Run database migrations:**

8. **Start the server:**


## Note

- This project have mainly two apps called user and organization
- For invitation mail I have created a simple api, and it works well
- For login alert I have created a model method named `send_login_alert_email` because we can use this method whenever we want
- for change password I have created a new method and it will automatically send mail after every successful password changing 
