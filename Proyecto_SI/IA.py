import cv2
camera=cv2.VideoCapture(1)

def getContours(img):
    contours , Hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        print(area)
        if area>500:
            cv2.drawContours(frame, cnt, -1, (255,0,0), 3)
            perimetro=cv2.arcLength(cnt, True)
            #Encontrar bordes o esquinas de cada figura
            aprrox=cv2.approxPolyDP(cnt, 0.02*perimetro, True)
            #Una vez encontrado la cantidad, la contamos
            objCorner=len(aprrox)
            x, y, w, h = cv2.boundingRect(aprrox)
            
            #Con ese numero determinamos que figuea es
            objectType = "Desconocido"
            
            if objCorner ==3:
                objectType="Triangulo"
            elif objCorner==4:
                aspecto=w/float(h)
                if aspecto > 0.95 and aspecto < 1.05:
                    objectType="Cuadrado"
                else:
                    objCorner="Rectangulo"
            elif objCorner>10:
                objectType="Circulo"
            else:
                objectType="Figura compleja"
                
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, objectType ,(x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7, (0,0,255),2,cv2.LINE_AA)    
            
while True:
    ret, frame= camera.read()
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgBlur= cv2.GaussianBlur(imgGray, (7,7), 1)
    imgCanny = cv2.Canny(imgBlur, 50,50)
    getContours(imgCanny)
    cv2.imshow("Figuras Geometricas", frame)
    
    if cv2.waitKey(1) == 27:
        break
    
                