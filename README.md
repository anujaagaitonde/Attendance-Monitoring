# Attendance App

## A Responsive Web-Application for Student Attendance Monitoring

The Attendance App is a fully responsive Django web-application to assist with monitoring of student attendance at Imperial College, London. It records the attendance of students at all university events, including lectures, tutorials, examinations and study groups to assist with the process of Tier 4 visa monitoring and pastoral care on the basis of attendance. Attendance data is captured by students scanning an event QR code to self-authenticate their attendance and staff members completing an electronic register for more critical events. This results in data which is used to produce attendance reports, and 
automatically notify admin users of suspicious attendance patterns.

This repository contains the source code and design files used to implement the web-app.

# Contents

- [Getting Started](#getting-started)
- [Authentication Using Test Users](#authentication-using-test-users)
- [About This Repository](#about-this-repository)
- [Technologies Used](#technologies-used)
- [Credits](#credits)

## Getting Started
### Prerequisites
* Python 3
* PIP

### Installation

Install Virtualenv
```
pip install virtualenv
```

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

### Database

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

### Emails

To set which email account the staff register reminder emails and attendance digest emails are sent from, in `/attendance_app_django/settings.py` reconfigure the lines
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'imperialattendance@gmail.com'
EMAIL_HOST_PASSWORD = 'cagvab-7nudru-jedCar'
```

where `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT` and `EMAIL_USE_TLS` are specified by the emailing provider and `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are the email and password of the desired email account.

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

Load the web-app in the browser by navigating to URL [http://localhost:8000/](http://localhost:8000/)

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
where `#####` are the roots to the SSL server's (simulated) SSL certificate and key. Note that real HTTPS certification has not been obtained for the development of this project, but has been simulated using the Django SSL server to enable camera access for QR code scanning.

Load the web-app in a browser by navigating to URL [https://<IP_Address>:8000/](https://<IP_Address>:8000/), replacing <IP_Address> with `<IP_Address>` (note: the https:// is important to allow camera access).

### Configuration of Cron Jobs

Cron jobs are used to send reminder emails to staff users to complete outstanding event registers and weekly student attendance digest emails to admin users.

Configure shell files:
`send_reminder_email.sh`
```
<absolute_path_to_manage.py> send_reminder_email
```
`send_admin_digest.sh`
```
<absolute_path_to_manage.py> send_admin_digest
```
where `<absolute_path_to_manage.py>` is the **absolute** file path to the Django project's `manage.py` file.

Make `send_reminder_email.sh` and `send_admin_digest.sh` executable
```
chmod +x send_admin_digest.sh && chmod +x send_reminder_email.sh
```

Open local machine crontab
```
crontab -e
```

Configure cron jobs in crontab
```
17 * * * cd <absolute_path_to_send_reminder_email.sh> && ./send_reminder_email.sh
0 09 * * 1 cd <absolute_path_to_send_admin_digest.sh> && ./send_admin_digest.sh
```
where `<absolute_path_to_send_reminder_email.sh>` and `<absolute_path_to_send_admin_digest.sh>` are the **absolute** paths to the `send_reminder_email.sh` and `send_admin_digest.sh` executable shell files, respectively.

**Note:** Ensure crontab has full access permissions to all files on your machine to ensure the cron jobs are properly executed.

## Authentication Using Test Users

For testing purposes, several users were created with the following credentials (replace # in the username with one of the # values:

| Username | Value of # (Incl.) | Password   |
|----------|--------------------|------------|
| admin#   | 1-4                | testing321 |
| student# | 1-11               | testing321 |
| staff#   | 1-7                | testing321 |

Note: for security purposes, these users are just test users and so the accounts contain no data representative of any real person. These test users **must** be deleted before deployment.

All the admin users are able to access the Django admin interface at URL */admin/* to manage the web-app's database content, i.e. add new users, events, etc.

## About This Repository
* [attendance_app_django](https://github.com/anujaagaitonde/Attendance-Monitoring/tree/master/attendance_app_django): Django project (contains code for entire web-app)
* [UI](https://github.com/anujaagaitonde/Attendance-Monitoring/tree/master/UI): Contains web-app wireframes and UI screenshots

## Technologies Used
The Attendance App was built using:
* [Python3.8.0](https://www.python.org/downloads/release/python-380/)
* [PIP](https://pypi.org/project/pip/)
* [Django](https://www.djangoproject.com/)
* [Bootstrap](http://getbootstrap.com/)
* Other dependencies in `requirements.txt`

## Credits
**Author:** Anuja Gaitonde

The Attendance App was created under the supervision of Dr. Thomas J. W. Clarke, submitted in partial fulfillment for an MEng degree in Electrical & Electronic Engineering with Management from Imperial College, London
