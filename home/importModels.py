from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from home.models import *
from home.serializer import *
from home.models import *
from rest_framework import filters
from rest_framework.generics import ListAPIView
from home.login_update import update_login
from rest_framework import status
from .GenerateOtp import *
from rest_framework.response import Response
from rest_framework.views import APIView
import hashlib
import hmac
import time
import base64
import json
from .stripapikey import *
from django.core.exceptions import ObjectDoesNotExist