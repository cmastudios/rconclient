# rconclient
# Copyright (C) 2017  Connor Monahan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import *
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from rconclient.rcon import MCRcon, MCRconException
import logging
import socket
import random
import string

logging.basicConfig(filename='rconclient.log', level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object('rconclient.default_settings')
app.secret_key = ''.join(random.choice(string.ascii_letters) for _ in range(64))

Bootstrap(app)
nav = Nav()
nav.register_element('top', Navbar(View('RCON Client', '.index')))
nav.init_app(app)


class SendCommandForm(FlaskForm):
    command = StringField('Command', validators=[DataRequired()])
    password = PasswordField('RCON Password')
    submit = SubmitField('Run Command')


def run_command(command, password):
    try:
        client = MCRcon()
        client.connect(app.config['SERVER_HOST'], app.config['SERVER_PORT'])
        client.login(password)
        response = client.command(command)
        if response:
            return True, response
        return True, 'Executed successfully.'
    except (MCRconException, socket.error) as e:
        if 'Login failed' not in str(e):
            logging.exception(e)
        return False, str(e)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SendCommandForm(request.form)
    form.password.widget.hide_value = False
    if form.validate_on_submit():
        result, message = run_command(form.command.data, form.password.data)
        flash(message)
    return render_template('index.html', form=form)

