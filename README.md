# Attendance App

## A Responsive Web-Application for Student Attendance Monitoring

The Attendance App is a fully responsive Django web-application to assist with monitoring of student attendance at Imperial College, London. It records the attendance of students at all university events, including lectures, tutorials, examinations and study groups to assist with the process of Tier 4 visa monitoring and pastoral care on the basis of attendance. Attendance data is captured by students scanning an event QR code to self-authenticate their attendance and staff members completing an electronic register for more critical events. This results in data which is used to produce attendance reports, and 
automatically notify admin users of suspicious attendance patterns.

This repository contains the source code and design files used to implement the web-app.

## Getting Started
### Prerequisites
* Python 3
* PIP
* Virtualenv

### Installation
Set up Python virtual environment
```
virtualenv venv
```
Activate virtual environment
```
source venv/bin/activate
```
Clone repository
```
git clone https://github.com/anujaagaitonde/Attendance-Monitoring.git
```
Navigate to Django project root
```
cd Attendance\ Monitoring\ App/attendance_monitoring_app/
```
Install dependencies from `requirements.txt`
```
pip install -r requirements.txt
```
The project is set up to use the default SQLite database. To use another database, inside `/attendance_app_django/settings.py` reconfigure the lines
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
according to the desired database structure. SQLite is recommended for development.

### Run on Local Machine

To run on the local machine only, start the default Django development server using
```
python manage.py runserver
```

Upon success you will see 
```
System check identified no issues (0 silenced).
June 11, 2020 - 18:23:57
Django version 3.0.7, using settings 'attendance_app_django.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Load the web-app in the browser by navigating to URL http://localhost:8000/

### Run on Other Devices

To run on other devices connected to the same WiFi router as the local machine (e.g. mobile), in `/attendance_app_django/settings.py` reconfigure the line
```
ALLOWED_HOSTS = ['<IP_Address>','localhost']
```
where `<IP_Address>` is the IP address of the WiFi router.

Start the Django SSL server using
```
python manage.py runsslserver 0.0.0.0:8000
```
Upon success you will see
```
System check identified no issues (0 silenced).
June 11, 2020 - 18:32:10
Django version 3.0.7, using settings 'attendance_app_django.settings'
Starting development server at https://0.0.0.0:8000/
Using SSL certificate: #####
Using SSL key: #####
Quit the server with CONTROL-C.
```
where `#####` are the roots to the SSL server's SSL certificate and key.

Load the web-app in the browser by navigating to URL https://<IP_Address>:8000/ (note: the https:// is important).

