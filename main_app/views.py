from django.shortcuts import render

from process.pseudocode import *
from django.http import JsonResponse as json_res
from django.http import StreamingHttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponseRedirect

import os
import glob
import time
# Create your views here.

return_progress_path_wy = '/home/pengmc/data/test/golf_swing_progress'

def index(request):
    context = {}
    return render(request, "main_app/index.html", context)

def rm_state_wy(request):
    for i in os.listdir(return_progress_path_wy):
        t = os.path.join(return_progress_path_wy, i)
        os.unlink(t)
    return json_res({'state': 'success'})

def get_state_wy(request):
    print('Enter get_state_wy')
    state_table = {
        '1': '完成视频分帧',
        '2': '完成球杆关键点检测',
        '3': '完成数据后处理',
    }
    if request.method != 'POST':
        return json_res({'state': '需要post方法'})

    return_progress_path_wy = '/home/pengmc/data/test/golf_swing_progress'
    
    list_file = os.listdir(return_progress_path_wy)
    list_file.sort(key=lambda fn: os.path.getmtime(os.path.join(return_progress_path_wy, fn)) if not os.path.isdir(os.path.join(return_progress_path_wy + fn)) else 0)
    print('*' * 20)
    print(list_file)
    print('*' * 20)
    newest_file = list_file[-1]
    newest_file = newest_file.split('.')[0]
    text = state_table[newest_file]
    
    per = [0, 20, 80, 100][int(newest_file)]

    return json_res({'state': 'success', 'text': text, 'per': per})


def get_state_pmc(request):
    #print('Enter get_state_pmc')
    state_table = {
        '1': '完成视频对齐',
        '2': '完成球杆关键点检测',
        '3': '完成人体关键点检测',
        '4': '完成13帧检测',
        '5': '完成生成对比视频',
    }
    if request.method != 'POST':
        return json_res({'state': '需要post方法'})

    files = request.FILES.getlist('files')
    print("files####", files)
    print("request.FILES####", request.FILES)

    if not files:
        return json_res({'state': '缺少参数'})

    return_progress_path = os.path.join('/home/pengmc/data/test/auto_draw_line_progress',
                                        files[0].name.split('.')[0] + '-' + files[1].name.split('.')[0])
    list_file = os.listdir(return_progress_path)
    list_file.sort(key=lambda fn: os.path.getmtime(os.path.join(return_progress_path, fn)) if not os.path.isdir(os.path.join(return_progress_path + fn)) else 0)
    print('*' * 20)
    print(list_file)
    print('*' * 20)
    newest_file = list_file[-1]
    newest_file = newest_file.split('.')[0]
    text = state_table[newest_file]
    per = int(newest_file) * 20
    return json_res({'state': 'success', 'text': text, 'per': per})
    


def upload_wy(request):
    if request.method != 'POST':
        return json_res({'state': '需要post方法'})

    if not request.FILES['file']:
        return json_res({'state': '缺少参数'})

    file = request.FILES['file']
    return_output_path=os.path.join('/media','wy',file.name.split('.')[0])

    old_files=glob.glob(os.path.join(settings.MEDIA_ROOT,'wy',)+'/*')
    for f in old_files:
        if file.name.split('.')[0] in f:
            print(f'之前处理过 {file.name}')

            sleep = True # set for test

            if sleep:
                time.sleep(8.0)
            file_t = open(os.path.join(return_progress_path_wy, '1.txt'), 'w')
            file_t.close()

            if sleep:
                time.sleep(37.0)
            file_t = open(os.path.join(return_progress_path_wy, '2.txt'), 'w')
            file_t.close()

            if sleep:
                time.sleep(9.0)
            file_t = open(os.path.join(return_progress_path_wy, '3.txt'), 'w')
            file_t.close()

            if sleep:
                time.sleep(7.0)
            
            files=glob.glob(settings.MEDIA_ROOT+'/wy/'+file.name.split('.')[0]+'/*.mp4')
            filenames=[os.path.basename(f) for f in files]
            urls_=[os.path.join(return_output_path,f) for f in filenames]
            print(f'wy urls_:{urls_}')
            return json_res({'state': 'success','urls':urls_})

    fs = FileSystemStorage()
    fs.save(file.name, file)
    this_input_path = os.path.join(settings.MEDIA_ROOT, file.name)
    this_output_path = os.path.join(
        settings.MEDIA_ROOT, 'wy', file.name.split('.')[0])
    os.makedirs(this_output_path, exist_ok=True)

    if pseudocode_wy(this_input_path, [this_output_path, this_output_path]) == True:
        os.remove(this_input_path)
        files=glob.glob(this_output_path+'/*.mp4')
        filenames=[os.path.basename(f) for f in files]
        urls_=[os.path.join(return_output_path, f) for f in filenames]
        urls_.sort()
        return json_res({'state': 'success','urls':urls_})
    else:
        return json_res({'state': '出错了！'})

def upload_pmc(request):
    if request.method != 'POST':
        return json_res({'state': '需要post方法'})

    files = request.FILES.getlist('files')
    print("files####",files)
    print("request.FILES####",request.FILES)
    
    if not files:
        return json_res({'state': '缺少参数'})

    return_output_path=os.path.join('/media','pmc',files[0].name.split('.')[0]+'---'+files[1].name.split('.')[0])
    this_output_video_path = os.path.join(
        settings.MEDIA_ROOT, 'pmc', files[0].name.split('.')[0]+'---'+files[1].name.split('.')[0],'video')
    this_output_image_path1=os.path.join(
        settings.MEDIA_ROOT, 'pmc', files[0].name.split('.')[0]+'---'+files[1].name.split('.')[0],'img1')
    this_output_image_path2=os.path.join(
        settings.MEDIA_ROOT, 'pmc', files[0].name.split('.')[0]+'---'+files[1].name.split('.')[0],'img2')
    
    old_files=glob.glob(os.path.join(settings.MEDIA_ROOT,'pmc',)+'/*')
    
    for f in old_files:
        if str(files[0].name.split('.')[0]+'---'+files[1].name.split('.')[0]) in f:
            print('之前处理过',this_output_video_path)
            #time.sleep(35.6)
            #video
            files=glob.glob(this_output_video_path+'/*.mp4')
            filenames=[os.path.basename(f) for f in files]
            video_urls=[os.path.join(return_output_path,'video',f) for f in filenames]
            #img1
            files=glob.glob(this_output_image_path1+'/*.jpg')
            filenames=[os.path.basename(f) for f in files]
            filenames.sort()
            img1_urls=[os.path.join(return_output_path,'img1',f) for f in filenames]
            #img2
            files=glob.glob(this_output_image_path2+'/*.jpg')
            filenames=[os.path.basename(f) for f in files]
            filenames.sort()
            img2_urls=[os.path.join(return_output_path,'img2',f) for f in filenames]
            print("exist:video_urls,img1_urls,img2_urls",video_urls,img1_urls,img2_urls)
            return json_res({'state': 'success',
                            'video_urls':video_urls,
                            'img1_urls':img1_urls,
                            'img2_urls':img2_urls,
                            })
    
    fs = FileSystemStorage()
    fs.save(files[0].name, files[0])
    fs.save(files[1].name,files[1])
    print("fs.save(files[0].name, files[0])###",files[0].name, files[0])
    this_input_path = [os.path.join(settings.MEDIA_ROOT, files[0].name),
                       os.path.join(settings.MEDIA_ROOT,files[1].name)]
    os.makedirs(this_output_video_path, exist_ok=True)
    os.makedirs(this_output_image_path1,exist_ok=True)
    os.makedirs(this_output_image_path2,exist_ok=True)

    if pseudocode_pmc(this_input_path, this_output_video_path) == True:
        #video
        files=glob.glob(this_output_video_path+'/*.mp4')
        filenames=[os.path.basename(f) for f in files]
        video_urls=[os.path.join(return_output_path,'video',f) for f in filenames]
        #img1
        files=glob.glob(this_output_image_path1+'/*.jpg')
        filenames=[os.path.basename(f) for f in files]
        filenames.sort()
        img1_urls=[os.path.join(return_output_path,'img1',f) for f in filenames]
        #img2
        files=glob.glob(this_output_image_path2+'/*.jpg')
        filenames=[os.path.basename(f) for f in files]
        filenames.sort()
        img2_urls=[os.path.join(return_output_path,'img2',f) for f in filenames]
        os.remove(this_input_path[0])
        os.remove(this_input_path[1])
        print("not exist:video_urls,img1_urls,img2_urls",video_urls,img1_urls,img2_urls)
        return json_res({'state': 'success',
                        'video_urls':video_urls,
                        'img1_urls':img1_urls,
                        'img2_urls':img2_urls,
                        })
    else:
        return json_res({'state': '出错了！'})

def refresh_page(request):
    if(request.method=='POST'):
        return HttpResponseRedirect(request.path)
    return render(request,"main_app/index.html")
