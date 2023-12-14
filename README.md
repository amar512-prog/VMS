
## Step-by-step guide to create a Conda environment and set up a Django project for the Vendor Management System.

### Step 1: Create a Conda Environment
```bash
# Create a Conda environment
conda create --name vendor_env python=3.12
# Activate the Conda environment
conda activate vendor_env
```
### Step 2: Install Django, Django REST Framework, Django extensions, Werkzeug
```bash
# Install packages within the Conda environment
pip install -r requirements.txt
```
### Step 3: Create a Django Project and App
```bash
# Create a Django project
django-admin startproject vendor_management_system
# Navigate to the project directory
cd vendor_management_system

# Create a Django app for managing vendors and purchase orders
python manage.py startapp vms
```