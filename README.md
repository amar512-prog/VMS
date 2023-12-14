
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
![vendors](https://github.com/amar512-prog/VMS/blob/main/image.png)
```bash
(env)PS E:\VMS\vendor_management_system> http  --verify="$(mkcert --CAROOT)/rootCA.pem"  https://192.168.214.220:8000/vms/api/purchase_orders/ "Authorization: token 24abc0e7214a2c50d81bfdb575129c61e1ff7e24"      
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Connection: close
Content-Length: 1027
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Thu, 14 Dec 2023 19:37:27 GMT
Referrer-Policy: same-origin
Server: Werkzeug/3.0.1 Python/3.12.0
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

[
    {
        "acknowledgment_date": "2023-12-15T04:22:03.130812+05:30",
        "delivery_date": "2023-12-30T16:00:00+05:30",
        "issue_date": "2023-12-14T16:00:00+05:30",
        "items": [
            {
                "description": "Description of Product 1",
                "name": "Product 1",
                "quantity": 10,
                "unit_price": 25.5
            },
            {
                "description": "Description of Product 2",
                "name": "Product 2",
                "quantity": 5,
                "unit_price": 35.0
            }
        ],
        "order_date": "2023-12-15T16:00:00+05:30",
        "po_number": "PO123456",
        "quality_rating": 4.5,
        "quantity": 15,
        "status": "pending",
        "vendor": "VENDOR123"
    },
    {
        "acknowledgment_date": null,
        "delivery_date": "2023-12-25T14:30:00+05:30",
        "issue_date": "2023-12-18T14:30:00+05:30",
        "items": [
            {
                "description": "Description of Product X",
                "name": "Product X",
                "quantity": 20,
                "unit_price": 15.75
            },
            {
                "description": "Description of Product Y",
                "name": "Product Y",
                "quantity": 8,
                "unit_price": 30.0
            },
            {
                "description": "Description of Product Z",
                "name": "Product Z",
                "quantity": 15,
                "unit_price": 22.0
            }
        ],
        "order_date": "2023-12-18T14:30:00+05:30",
        "po_number": "PO789012",
        "quality_rating": null,
        "quantity": 43,
        "status": "pending",
        "vendor": "VENDOR124"
    }
]
```
```bash
(env)PS E:\VMS\vendor_management_system> http  --verify="$(mkcert --CAROOT)/rootCA.pem"  https://192.168.214.220:8000/vms/api/vendors/VENDOR123/performance/ "Authorization: token 24abc0e7214a2c50d81bfdb575129c61e1ff7e24"
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Connection: close
Content-Length: 179
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Thu, 14 Dec 2023 19:44:54 GMT
Referrer-Policy: same-origin
Server: Werkzeug/3.0.1 Python/3.12.0
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "average_response_time": 44523.130812,
    "date": "2023-12-15T04:22:03.260137+05:30",
    "fulfillment_rate": 0.0,
    "on_time_delivery_rate": 100.0,
    "quality_rating_avg": 4.5,
    "vendor": "VENDOR123"
}
```

