import cv2

camara = cv2.VideoCapture(0)

if not camara.isOpened():
    print("No se pudo abrir la camara")
    exit()

print("Presiona 's' para tomar una foto o 'q' para salir.")

while True:
    ret, frame = camara.read()
    if not ret:
        break

    cv2.imshow("Camara - Presiona S para capturar", frame)
    
    key = cv2.waitKey(1) & 0xFF
    
    # SI PRESIONAS 's' GUARDA LA IMAGEN
    if key == ord('s'):
        cv2.imwrite("foto_capturada.jpg", frame)
        print("¡Foto guardada como foto_capturada.jpg!")
        
    # SI PRESIONAS 'q' CIERRA EL PROGRAMA
    if key == ord('q'):
        break

camara.release()
cv2.destroyAllWindows()

# video referencia: https://www.youtube.com/watch?v=iyUuf1cLblA
