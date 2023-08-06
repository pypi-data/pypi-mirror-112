import os
if __name__ == '__main__':
    print("VidoFormatTransformThread Start")
    avi_file_path = "/home/wwl/myui/myworkspace/testing/avi2mp4/aaa.avi"
    out_file_path = "/home/wwl/myui/myworkspace/testing/avi2mp4/yie.mp4"
    os.system("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}'".format(input=avi_file_path, output=out_file_path))
    print("VidoFormatTransformThread Finish")
    print("2")
