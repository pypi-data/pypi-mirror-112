import os
import subprocess
import time
import threading

#
# def convert_avi_to_mp4(avi_file_path, output_name):
#     print("1")
#     os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}'".format(input=avi_file_path, output=output_name))
#     time.sleep(1)
#     print("2")
#     return True
#
#
#
# convert_avi_to_mp4("/home/wwl/myui/myworkspace/testing/avi2mp4/aaa.avi",
#                    "/home/wwl/myui/myworkspace/testing/avi2mp4/yie.mp4")

import threading


class MyThread(threading.Thread):
    def __init__(self, avi_file_path, out_file_path):
        super(MyThread, self).__init__()
        self.avi_file_path = avi_file_path
        self.out_file_path = out_file_path

    def run(self):
        print("1")
        #os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}'".format(input=self.avi_file_path, output=self.out_file_path))
        #subprocess.run("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}'".format(input=self.avi_file_path, output=self.out_file_path))
        os.system("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}'".format(input=self.avi_file_path, output=self.out_file_path))
        # time.sleep(1)
        print("2")


if __name__ == '__main__':
    print("VidoFormatTransformThread Start")
    #vidoFormatTransformThread = MyThread("/home/wwl/myui/myworkspace/testing/avi2mp4/via.avi", "/home/wwl/myui/myworkspace/testing/avi2mp4/yie.mp4")
    vidoFormatTransformThread = MyThread("/home/wwl/myui/myworkspace/testing/avi2mp4/aaa.avi",
                                         "/home/wwl/myui/myworkspace/testing/avi2mp4/yie.mp4")
    vidoFormatTransformThread.start()
    #vidoFormatTransformThread.join()
    print("VidoFormatTransformThread Finish")
    #sudo docker commit -a "jianglinzhang" -m "8997d910edcb" wellsecurity_portal_nginx wellsecurity_portal_nginx:latest
    #sudo docker commit -a "jianglinzhang" -m "via wellsecurity-osk-server-conda" wellsecurity-osk-server-conda wellsecurity-osk-server-conda:latest
    #sudo docker save -o wellsecurity-osk-server-conda.tar wellsecurity-osk-server-conda:latest
    #sudo docker save -o wellsecurity_portal_nginx.tar wellsecurity_portal_nginx:latest
