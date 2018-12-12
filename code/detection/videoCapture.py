import cv2


def vid_capture():
    resolution = (640, 480)
    window_name = "Live Video Feed"

    cv2.namedWindow(window_name)
    capture = cv2.VideoCapture(0)

    if capture.isOpened():
        flag, frame = capture.read()
    else:
        flag = False

    while flag:

        flag, frame = capture.read()
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyWindow(window_name)
    videoCapture.release()
    capture.release()


if __name__ == '__main__':
    vid_capture()
