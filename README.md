
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

### Step 3: create certificate for https, config,bat to get IP  (tested on windows)
```bash
certification.bat
config.bat
```

### Step 4: run server
```bash
runpy.bat
```

### visit https://<ip>:8000/vms/api/vendors
![vendors](https://github.com/amar512-prog/VMS/blob/main/out.png)
