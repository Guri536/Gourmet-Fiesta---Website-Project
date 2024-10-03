from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib import auth, messages
import datetime, random
from django.utils.safestring import mark_safe
from django.template import RequestContext
from .models import ids
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
import json, os, PIL, random, itertools
from django.http import JsonResponse
from PIL import Image

def get_context(r):
    try:
        context_var = ((ids.objects.get(user_id = r.user.id).get_data()))
        if context_var['type'] == 'c':
            with open('app1/static/JSON/cont.json', 'r') as file:
                file_var = json.load(file)
                for i in file_var[context_var['id']]:
                    context_var[i] = file_var[context_var['id']][i]
        # print('fun',type(context_var))
        return context_var
    except:
        return None


def home(r):
    # context_var = ids.objects.get(user_id = r.user.id)
    # print(context_var)
    var = (get_context(r))
    try:
        with open('app1/static/JSON/fin_data.json', 'r') as file:
            add_var = json.load(file)
        sel_var = random.sample(list(add_var.keys()), 16)
        send_var = {}

        for i in sel_var:
            send_var[i] = add_var[i]
        # print(type(var))
        var["rec"] = send_var
    except:
        return redirect('login')
    return render(r, 'main_page.html', context={"user_data": json.dumps(var)})

def sign(r):
    if r.method=="POST":
        user_n = r.POST['username']
        user_e = r.POST['email']
        user_p = r.POST['password']
        User.objects.create_user(username=user_n, email=user_e, password=user_p)
        user = auth.authenticate(username = user_n, password = user_p)
        auth.login(r, user)
        ids.objects.create(user_id=r.user.id,user_username=user_n)
        return redirect('login')
    return render(r, "signup.HTML")

def login(r):
    if r.user.is_authenticated:
        return redirect('home')
    if r.method == "POST":
        emailw = r.POST['email']
        passw = r.POST['password']
        try:
            user_name = User.objects.get(email=emailw.lower()).username
            user = auth.authenticate(username = user_name, password = passw)
            if user is not None:
                auth.login(r, user)
                return redirect('home')
            else:
                messages.error(r, "Incorrect email or password", extra_tags='error')
        except:
            messages.error(r, "Incorrect email or password", extra_tags='error')
            
    return render(r, 'login.html')

def logout(r):
    auth.logout(r)
    return redirect('login')

def cont_sign(r):
    if r.method=="POST":
        var1 = list((User.objects.values('email')))
        email_list = []
        for i in var1:
            email_list.append(list(i.values())[0])
        if r.POST['email'] in email_list:
            if ids.objects.get(user_id=User.objects.get(email=r.POST['email']).id).user_type == 'n':
                with open('app1/static/JSON/cont.json', 'r') as file:
                    var = json.load(file)
                var[User.objects.get(email=r.POST['email']).id]={}
                for i in range(1, len(dict(r.POST).keys())):
                    var[User.objects.get(email=r.POST['email']).id][list((dict(r.POST)).keys())[i]] = r.POST[list((dict(r.POST)).keys())[i]]
                with open('app1/static/JSON/cont.json', 'w') as file:
                    json.dump(var, file)
                ids.objects.get(user_id = User.objects.get(email=r.POST['email']).id).set_type('c').save()
            else:
                messages.error(r, 'Your Account is either already a Contributor Type or does not match the eligible criteria')
        else:
            messages.error(r, 'This email doesn\'t exist in our database, so sign up first')
    return render(r, 'contributer_signup.html')

def test(r):
    if r.method=='GET':
        None
        # print(ids.objects.get(user_id = r.user.id))
        # ids.objects.get(user_id = r.user.id).set_type('c').save()
        # print(ids.objects.values_list('user_username','user_type'))
        # return JsonResponse({})

def add(r):
    var = get_context(r)
    with open('app1/static/JSON/ing.json', 'r') as file:
        var['ing'] = json.load(file)
    # print(type(var))
    if r.method == 'POST':
        # print(dict(r.POST))
        for i in dict(r.POST):
            if i=='data':
                data = json.loads(r.POST['data'])
                # for i in data:
                #     print( i, data[i])
                with open('app1/static/JSON/fin_data.json', 'r') as file:
                    var_1 = json.load(file)
                # print(max(list(dict(var_1).keys())))
                id_list = []
                for i in var_1.keys():
                    id_list.append(int(i))
                var_1[max(id_list)+1] = data
                var_1[max(id_list)+1]['id'] =  max(id_list)+1
                with open('app1/static/JSON/fin_data.json', 'w') as file:
                    json.dump(var_1, file)
            # else:
            #     print(i, dict(r.POST)[i])

    return render(r,'add_recipie.html', context={'user_data': json.dumps(var)})

def rec(r):
    # print(r.GET.get('id'))
        
    var = (get_context(r))
    with open('app1/static/JSON/fin_data.json', 'r') as file:
        get_var = json.load(file)
    # print(get_var[r.GET.get('id')])
    var['rec'] = get_var[r.GET.get('id')]
    return render(r, 'rec.html', context={"user_data": json.dumps(var)})
    
def search(r):
    var = (get_context(r))
    return render(r, 'search.html', context={"user_data": json.dumps(var)})

def search_res(r):
    send_json = {}
    if r.method=="GET":
        query = r.GET['query']
        if query.lower() == 'veg':
            query = "vegetarian"
        with open('app1/static/JSON/fin_data.json', 'r') as file:
            file_var = json.load(file)
        for i in file_var:
            if (query.lower() in file_var[i]['chef'].lower().split(' ') or query.lower() in file_var[i]['name'].lower().split(' ') or query.lower() in list(map(lambda x: x.lower(), file_var[i]['metadata']['keywords']))) or query.lower() in list(map(lambda x: x.lower(), list(itertools.chain(*[k.split() for k in [list(j.keys())[0] for j in file_var[i]['ingredients']]])))):
                send_json[i] = file_var[i]
    return JsonResponse(send_json)

def csoon(r):
    var = (get_context(r))
    return render(r, 'com_soon.html', context={"user_data": json.dumps(var)})

def ab_us(r):
    var = (get_context(r))
    return render(r, 'ab_us.html', context={"user_data": json.dumps(var)})

def pr_po(r):
    var = (get_context(r))
    return render(r, 'pr_po.html', context={"user_data": json.dumps(var)})