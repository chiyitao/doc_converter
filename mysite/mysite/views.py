#-*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie

import os.path
import os
import subprocess

import hashlib

from . import settings
# import md5

CONVERT_RESULTS_PATH = 'convert_results'

def hello(request):
    return HttpResponse('Hello World')

@ensure_csrf_cookie
def convert_page(request):
    ctx = {}
    return render_to_response('convert_page.html', ctx)
    # pass


def converter(request):
    # TODO: check the parameter

    # do the job
    hr = HttpResponse()

    if request.method == 'POST':
        input_file_ext = '' # '.md'

        input_file_ext = request.POST['output-file-format']
        
        form = request.FILES
        for item in form.items():
            print(item)
        user_file = request.FILES.get('user-file', None)        

        temp_file_content = user_file.read()

        temp_file_md5 = hashlib.md5(temp_file_content)

        input_file_name = user_file.name

        # uni_char = user_file.read().decode('utf-8') # decode('utf-8')

        # print(settings.BASE_DIR)

        static_parent_path = os.path.join(os.path.abspath(settings.BASE_DIR), CONVERT_RESULTS_PATH)

        # print(static_parent_path)

        file_storage_dir = os.path.join(static_parent_path, temp_file_md5.hexdigest())



        if not os.path.exists(file_storage_dir):
            print(file_storage_dir)
            retcode = os.mkdir(file_storage_dir) # TODO: check the return code

        input_file_path = os.path.join(file_storage_dir, input_file_name)
        
        temp_file = open(input_file_path, 'wb+') #(input_file_name, 'w')

        # temp_file.write(uni_char)

        for chunk in user_file.chunks():
            temp_file.write(chunk)            

        temp_file.close()
        
        output_file_path = os.path.splitext(input_file_path)[0] + input_file_ext
    
        convert_cmd = 'pandoc -o {output_file_name} {input_file_name}' \
                      .format(output_file_name = output_file_path, \
                              input_file_name = input_file_path)
    
        p = subprocess.Popen(convert_cmd, shell=True)
        p.wait()

        output_file_url = 'http://' + request.get_host() + settings.STATIC_URL + \
                          temp_file_md5.hexdigest() + \
                          '/' + os.path.splitext(input_file_name)[0] + input_file_ext
    
        if p.returncode != 0:
            print(p.returncode)
            hr = HttpResponse('Error when converting the file.')
        else:
            # hr = HttpResponse('Convertion Succeeded.')
            hr = HttpResponse(output_file_url)

    else:
        hr = HttpResponse('User Request error.')
        
    return hr


    
