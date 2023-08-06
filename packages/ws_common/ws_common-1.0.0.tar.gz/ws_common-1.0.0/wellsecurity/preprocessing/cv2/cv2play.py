import time
import random

import cv2

if __name__ == '__main__':
    print('run program')
    rtsp_address = 'rtmp://58.200.131.2:1935/livetv/hunantv'
    # rtsp_address = 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'

    # 通过cv2中的类获取视频流操作对象cap
    cap = cv2.VideoCapture(rtsp_address)
    # 调用cv2方法获取cap的视频帧（帧：每秒多少张图片）
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    # 获取cap视频流的每帧大小
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(size)
    # 定义编码格式mpge-4
    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
    # 定义视频文件输入对象
    outVideo = cv2.VideoWriter('/home/wwl/mypython/myworkspace/test/video/saveDir.avi', fourcc, fps, size)
    cv2.namedWindow("cap video", 0)

    while True:
        ret, image = cap.read()
        if ret is True:
            for temp in range(random.randint(1, 16)):
                x1 = random.randint(1, 960)
                y1 = random.randint(1, 540)

                x2 = x1 + random.randint(1, 960)
                y2 = y1 + random.randint(1, 540)

                cv2.rectangle(image, (x1, y1), (x2, y2), (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)), 3)
                cv2.putText(image, str(temp)+str(":via:") + str(random.random()), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)
            print(type(image))
            print(image)
            cv2.imshow('cap video', image)
            cv2.imwrite("/home/wwl/mypython/myworkspace/test/pic/" + str(time.time()) + ".jpg", image)
            outVideo.write(image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            outVideo.release()
            cap.release()
            cv2.destroyAllWindows()
            break
            # continue
