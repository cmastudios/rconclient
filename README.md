rconclient
=====

This program is a simple WSGI web application that allows a user to send commands to a Minecraft server through the
RCON protocol and view the output of the command. The password is sent by the user of the website.

Requirements
-----
Python 3 and pip.

Usage
-----

1. Configure the game server to listen for RCON commands. See http://wiki.vg/RCON
2. Change the server address and port specified in rconclient/default_settings.py. Note that the port should be for the
    RCON listener and not the game port.
3. Install the dependencies for this project with `pip3 install -r requirements.txt`
4. Run the development web server with `python3 application.py`
5. Access the page at http://127.0.0.1:5000/

The project uses WSGI with an endpoint at application.py, and can be run with your favorite WSGI runner, including
    gunicorn, Apache mod_wsgi, and Amazon ElasticBeanstalk.
