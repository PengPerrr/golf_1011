# 说明：这个文件伪代码，用于说明如何实现视频处理的接口。
# 这两个函数将接收视频的输入路径，并把输出视频放在指定的路径中
# 比如：pseudocode_wy 函数 将接收一个视频的输入路径，和期望输出视频的路径的list
# 把处理后的视频输出在list_out_video_path[0] 和 list_out_video_path[1] 中

import shutil
import os

#改了路径
#因为django运行时的路径是最外层文件夹，所以调用这两个函数时候运行路径也是django的运行路径，
#我把这整个模块放进process文件夹，然后放进django最外层

# 获取Python程序运行时的路径
current_path = os.getcwd()

def pseudocode_wy(in_video_path, list_out_video_path):
    # 输入：
    # in_video_path: 输入视频的路径
    # list_out_video_path: 一个长度为2的list, 用于指定处理后视频的输出路径
    # list[0]为左边输出视频的路径，list[1]为右边输出视频的路径。

    # 输出：
    # True or False (是否处理成功)

    # check input and output path
    print(f'in_video_path: {in_video_path}')
    print(f'list_out_video_path: {list_out_video_path}')
    assert len(list_out_video_path) == 2

    os.system("cp " + in_video_path + " /home/pengmc/codes/MobileNetV2-4-ClubHead/pipeline/")

    os.system("cp " + in_video_path + " /home/pengmc/codes/main/media/inputnew_wy/")

    os.chdir('/home/pengmc/codes/MobileNetV2-4-ClubHead/pipeline')
    indir = in_video_path.split("/")[-1]
    os.system('python3 pipeline_web.py ' + indir)
    print(f'wy exclude python3 pipeline_web.py {indir}')

    out_video_path = ['/home/pengmc/codes/MobileNetV2-4-ClubHead/pipeline/out/out_video1.mp4',
                      '/home/pengmc/codes/MobileNetV2-4-ClubHead/pipeline/out/out_video2.mp4']

    # os.chdir('/home/pengmc/codes/main')
    os.chdir(current_path)

    # 实现将存在的视频作为输出视频拷贝到目的路径 的代码。测试时可能需要修改一下路径
    shutil.copy(out_video_path[0], list_out_video_path[0])
    shutil.copy(out_video_path[1], list_out_video_path[1])

    return True




def pseudocode_pmc(list_in_video_path, out_video_path):
    # 输入：
    # list_in_video_path: 输入对比视频的2个路径
    # out_video_path: 在这个路径下输出视频
    # list_out_image_path: 在这个路径下输出26张图片 (list_out_image_path[0] ~ list_out_image_path[25]) 前13张图为需要放在上面的图，后13张图为需要放在下面的图（按照顺序排列）

    # 输出：
    # True or False (是否处理成功)

    # check input and output path
    assert len(list_in_video_path) == 2
    print(f'in_video_path: {list_in_video_path}')

    os.system("cp "+(list_in_video_path[0])+" /home/pengmc/data/test/test_video/")
    os.system("cp "+(list_in_video_path[1])+" /home/pengmc/data/test/test_video/")

    os.system("cp " + (list_in_video_path[0]) + " /home/pengmc/codes/main/media/inputnew_pmc/")
    os.system("cp " + (list_in_video_path[1]) + " /home/pengmc/codes/main/media/inputnew_pmc/")

    os.chdir('/home/pengmc/codes/MyGolfDB')
    dir1=list_in_video_path[0].split("/")[-1].split(".")[0]
    dir2=list_in_video_path[1].split("/")[-1].split(".")[0]
    os.system('python3 test_me_pipeline.py '+(dir1)+' '+(dir2)+" get_13_A")
    out_video_path=os.path.join("/home/pengmc/data/res/video",dir1+"_to_"+dir2+"_"+"user_first"+".mp4")
    list_out_image_path_1=os.path.join("/home/pengmc/data/res/img",dir1)
    list_out_image_path_2=os.path.join("/home/pengmc/data/res/img",dir2)

    print(f'out_video_path: {out_video_path}')
    print(f'list_out_image_path: {list_out_image_path_1}')
    print(f'list_out_image_path: {list_out_image_path_2}')
    #assert len(list_out_image_path_1) == 13

    # 实现将存在的视频和图片作为输出视频拷贝到目的路径 的代码。测试时可能需要修改一下路径
    # os.chdir('/home/pengmc/codes/main')
    os.chdir(current_path)
    shutil.copy(out_video_path,os.path.join(os.getcwd(),'media/pmc', dir1+"---"+dir2,"video",dir1+"_to_"+dir2+"_"+"user_first"+".mp4"))
    for case in os.listdir(list_out_image_path_1):
        shutil.copy(os.path.join(list_out_image_path_1,case),os.path.join(os.getcwd(),'media/pmc', dir1+"---"+dir2,"img1", case))
    for case in os.listdir(list_out_image_path_2):
        shutil.copy(os.path.join(list_out_image_path_2,case),os.path.join(os.getcwd(),'media/pmc', dir1+"---"+dir2,"img2", case))

    return True
