
# Personal Assistant Setup Guide

To get started with the Personal Assistant application, please ensure you have Python 3.12 and Docker Desktop installed on your PC.

## Steps to Run the Application

1. **Clone the Repository:**
   - Make a local copy of the repository by cloning it to your machine.

2. **Set Up a Virtual Environment:**
   - Create a virtual environment and activate it.
   - Install the necessary packages by running:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configure Environment Variables:**
   - Create a `.env` file in the root directory.
   - Copy the contents from `.env.example` into the new `.env` file.
   - Update the file with your specific configuration details.

4. **Navigate to the Application Directory:**
   - In your terminal, move to the `personal_assistant` directory:
     ```bash
     cd personal_assistant
     ```

5. **Start Docker Services:**
   - Run the following command to start Docker services in detached mode:
     ```bash
     docker-compose up -d
     ```

6. **Apply Database Migrations:**
   - Apply the necessary migrations by executing:
     ```bash
     python manage.py migrate
     ```

7. **Launch the Application:**
   - Start the application with the following command:
     ```bash
     python manage.py runserver
     ```

Your Personal Assistant is now up and running, ready for use!

---
