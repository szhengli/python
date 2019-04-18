from django.http  import HttpResponse, Http404,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import NameForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.shortcuts import redirect

