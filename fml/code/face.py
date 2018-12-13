import cv2

fd = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

def detect_face(img,fd=fd):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    faces = fd.detectMultiScale(gray, 
                    scaleFactor=1.1, minNeighbors=5);
    return faces  
def draw_on_face(img,faces):
    for (x, y, w, h) in faces:     
         cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return img
    
def find_finger(frame):
    contours=find_contours(frame)
    max_contour=max(contours,key=cv2.contourArea)
    centre=centroid(max_contour)
    cv2.circle(frame,centre, 5, [255, 0, 255], -1)
    
    if max_contour is not None:
        hull = cv2.convexHull(max_contour, returnPoints=False)
        defects = cv2.convexityDefects(max_contour, hull)
        far = farthest_point(defects,max_contour, centre)
        cv2.circle(frame, far, 5, [0, 0, 255], -1)
    return frame
