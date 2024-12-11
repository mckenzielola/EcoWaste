# EcoWaste

EcoWaste is a web application designed to help minimize household food waste by providing tools to track perishable items, monitor waste, calculate environmental impact, and offer educational resources on sustainable living.

## Key Features

### Freshness Tracker
- **Expiration Alerts**: Highlights items nearing expiration to ensure they are used before spoiling.

### Waste Tracker
- **Monitor Waste**: Enables users to record and track the types and quantities of food waste.

### Impact Calculator
- **Environmental Impact**: Quantifies the environmental benefits of waste reduction efforts, providing statistics such as waste diverted from landfills.

### Green Guides (Educational Resources)
- **Sustainable Practices**: Educates users on sustainable living habits, such as reducing single-use plastics and supporting eco-friendly brands.

## Environment Setup

### For Windows

1. **Activate the Environment**:
    ```sh
    env\Scripts\activate
    ```

2. **Install Django**:
    ```sh
    pip install django
    ```

3. **Run Migrations**:
    ```sh
    python manage.py migrate
    ```

4. **Run the Server**:
    ```sh
    python manage.py runserver
    ```

### For macOS

1. **Activate the Environment**:
    ```sh
    source env/bin/activate 
    ```

2. **Install Django**:
    ```sh
    pip3 install django
    ```

3. **Run Migrations**:
    ```sh
    python3 manage.py migrate
    ```

4. **Run the Server**:
    ```sh
    python3 manage.py runserver
    ```

## Installation and Running the Application

Follow the environment setup instructions for your operating system to install dependencies and run the server. Once the server is running, you can access the application by navigating to `http://127.0.0.1:8000` in your web browser.
