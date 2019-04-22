from django.shortcuts import render

# Create your views here.
from django.http  import HttpResponse, Http404,HttpResponseRedirect
from .models import Question, Choice, Publiser, Book, Backends,FrontEnds
import django.http

from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.shortcuts import redirect
from .forms import NameForm,  Profiles
from multiprocessing import Pool, Process

from django.views import View
from django.views.generic import ListView, DetailView
from subprocess import run, getoutput

prog_txt = "/root/django/mysite/polls/static/polls/ajax_info.txt"

front_state= "/root/django/mysite/polls/static/polls/deploy_pages.txt"

from django.views.decorators.csrf import csrf_exempt

redis = 'ssh 47.100.20.200 \
         redis-cli  -a ChinayieREDIS135 \
         -h 511933ba9d7e4155.redis.rds.aliyuncs.com'


shiro = 'shiro:rediscache:tradeLoginRetryLimitCache:'







class PubliserList(ListView):
    model = Publiser
    context_object_name = 'pbs'

class PublisherDetail(DetailView):
    model = Publiser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()
        return context



def deploy_jar(source, target, mold):
    command =  'ansible ' + source +  ' -m shell -a " bash /root/auto/backend.sh  ' + target + '  ' + mold + '"'
    run(command, shell=True)
    record = "sed  -i '/" + mold + "/d' " + prog_txt
    run(record, shell=True)



@csrf_exempt
def test_js(request):
    if request.method == 'GET':
        return render(request,'polls/test.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        return HttpResponse(username+"  "+password )


def deploy_backend(request):
    if request.user.is_authenticated:
        jars = Backends.objects.all()
        backends = []
        run(">  " + prog_txt , shell=True)
        for jar in jars:
            backends.append({'folder':jar.folder, 'prefix':jar.prefix})
        if request.method == 'GET':
            return render(request,'polls/backend.html', {'backends':backends})
        elif request.method == 'POST':
            selected = request.POST.getlist('selected_backends')
            source=request.POST['source']
            target=request.POST['target']

            if selected :
                para_list = [[source, target, mold] for mold in selected  ]
                for para in para_list:
                    run("echo " + para[2] + " >> " + prog_txt , shell=True)
                    Process(target=deploy_jar, args=para).start()
            return HttpResponseRedirect(reverse('polls:progress'))
    else:

        request.session['previous'] = request.path
        return HttpResponseRedirect(reverse('polls:login'))
        #return HttpResponse(request.session['previous'])

def deploy_pages(source,target,pages):
    run("> " + front_state, shell=True)
    command =  'ansible ' + source +  ' -m shell -a " bash /root/auto/front.sh  ' + target + '  ' + pages + '"'
    run(command, shell=True)
    run("echo 1 > " + front_state, shell=True)

def deploy_frontend(request):
    if request.user.is_authenticated:
        fronts = FrontEnds.objects.all()
        frontends = []

        for front in fronts:
            frontends.append(front.folder)
        if request.method == 'GET':
            return render(request,'polls/frontends.html', {'frontends':frontends})

        elif request.method == 'POST':
            selected = request.POST.getlist('selected_frontends')
            source=request.POST['source']
            target=request.POST['target']
            pages = ' '.join(selected)

            if selected :
                para=(source,target,pages)
                Process(target=deploy_pages, args=para).start()
                return HttpResponseRedirect(reverse('polls:progress_front'))
    else:

        request.session['previous'] = request.path
        return HttpResponseRedirect(reverse('polls:login'))
        #return HttpResponse(request.session['previous'])


def progress_front(request):
    return render(request, 'polls/progress_front.html')


def locked_user(request):
     lusers = getoutput(redis + ' keys '+ shiro + '*')
     userlist = []
     if lusers:
         userlist = [ x.split(':')[3] for x in  lusers.split('\n')]
         return render(request, 'polls/locked_user.html', {'userlist': userlist})
     else:
         return HttpResponse("暂无账号被锁定")

@csrf_exempt
def unlock(requst):
    users=requst.POST.getlist('selected_user')
    accounts = ' '.join([shiro + x for x in users])

    results = getoutput(redis + ' del ' + accounts )

    return HttpResponse(results)










def auths(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                previous = request.session['previous']
                if previous:
                    return HttpResponseRedirect(previous)
                else:
                    return HttpResponseRedirect(reverse('polls:index'))
            else:
                return HttpResponse('need to login')
    form = NameForm()
    return render(request,'polls/login.html', {'form': form})





class Profiles(View):
    form_class = Profiles
    #template_name ='polls/pro.html'
    template_name ='polls/child.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        test="<b>james"
        #return render(request,self.template_name,{'form': form, 'test':test})
        return render(request,self.template_name,{'test':test})

    def post(self, request, *args, **kwargs):
        form =self.form_class(request.POST)
        if form.is_valid():
            names=form.cleaned_data['names']
            locations=form.cleaned_data['locations']
            return HttpResponse(names + ' ' + locations )
        return render(request,self.template_name,{'form': form})







class Tests(View):
    greeting = "Good Day"
    def get(self, request):
        return HttpResponse(self.greeting)



def progress(request):

    return render(request, 'polls/progress.html')




def index(request):
    if request.user.is_authenticated:

        return render(request, 'polls/index.html')
    else:
        request.session['previous'] = request.path
        #return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return HttpResponseRedirect(reverse('polls:login'))






def detail(request, question_id):
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/details.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request,'polls/results.html', {'question':question})



def check(request):
    template = loader.get_template('polls/check.html')
    username = request.POST['username']
    password = request.POST['password']
    context = {'username':username, 'password':password}
    return HttpResponse(template.render(context, request))


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,'polls/details.html', {'question':question,
                'error_message': "You didnot select a choice.",
                                                     })
    else:
        selected_choice.votes +=1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

