import string
import random
import time
from datetime import datetime
from flask import Flask, g
from functools import wraps
import sqlite3
from flask import *
from hashlib import sha256


app = Flask(__name__)