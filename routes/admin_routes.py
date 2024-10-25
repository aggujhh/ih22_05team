from . import app, global_data
from flask import render_template, request, flash, redirect
from severs.flask_login import Flask_login
from flask_login import current_user, login_required, logout_user

