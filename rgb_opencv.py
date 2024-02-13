import cv2
import numpy as np
import pandas as pd
from datetime import datetime

# now = datetime.now()
# now = now.strftime("%Y-%m-%d %H:%M:%S:%f")


time_points = []
red_points = []
blue_points = []
green_points = []

# Video dosyasını aç
video = cv2.VideoCapture('./daha_iyi_deneme.mp4')

# Renk aralıklarını tanımla
lower_blue = np.array([120, 0, 0])
upper_blue = np.array([255, 100, 100])

lower_red = np.array([0, 0, 100])
upper_red = np.array([100, 100, 255])

lower_green = np.array([0, 100, 0])
upper_green = np.array([100, 255, 100])



while True:
    # Video'dan bir kare al
    ret, frame = video.read()
    
    if not ret:
        break
    
    # Mavi rengi tespit etmek için bir maske oluştur
    blue_mask = cv2.inRange(frame, lower_blue, upper_blue)
    
    # Kırmızı rengi tespit etmek için bir maske oluştur
    red_mask = cv2.inRange(frame, lower_red, upper_red)

    # Yeşil rengi tespit etmek için bir maske oluştur
    green_mask = cv2.inRange(frame, lower_green, upper_green)

    
    # Mavi nesneleri etiketle
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for blue_contour in blue_contours:
        area = cv2.contourArea(blue_contour)
        if area > 100:  # minimum alan kontrolü
            M = cv2.moments(blue_contour)
            if M["m00"] != 0:
                cx_b = int(M["m10"] / M["m00"])
                cy_b = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cx_b, cy_b), 5, (255, 0, 0), -1)
                cv2.putText(frame, "Blue Object", (cx_b - 20, cy_b - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                blue_points.append((cx_b,cy_b))
    
    # Kırmızı nesneleri etiketle
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for red_contour in red_contours:
        area = cv2.contourArea(red_contour)
        if area > 100:  # minimum alan kontrolü
            M = cv2.moments(red_contour)
            if M["m00"] != 0:
                cx_r = int(M["m10"] / M["m00"])
                cy_r = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cx_r, cy_r), 5, (0, 0, 255), -1)
                cv2.putText(frame, "Red Object", (cx_r - 20, cy_r - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                now = datetime.now()
                now = now.strftime("%Y-%m-%d %H:%M:%S:%f")
                time_points.append(now)
                red_points.append((cx_r,cy_r))
    
     # Yeşil nesneleri etiketle
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for green_contour in green_contours:
        area = cv2.contourArea(green_contour)
        if area > 100:  # minimum alan kontrolü
            M = cv2.moments(green_contour)
            if M["m00"] != 0:
                cx_g = int(M["m10"] / M["m00"])
                cy_g = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cx_g, cy_g), 5, (0, 255, 0), -1)
                cv2.putText(frame, "Green Object", (cx_g - 20, cy_g - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                green_points.append((cx_g,cy_g))



    # Etiketlenmiş kareyi göster
    cv2.imshow('Frame', frame)
    
    # Çıkış için 'q' tuşuna basıldığını kontrol et
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break


# Veri çerçevelerini oluştur
df_time = pd.DataFrame(time_points, columns=['date'])
df_red = pd.DataFrame(red_points, columns=['x_Red', 'y_Red'])
df_green = pd.DataFrame(green_points, columns=['x_Green', 'y_Green'])
df_blue = pd.DataFrame(blue_points, columns=['x_Blue', 'y_Blue'])

# Veri çerçevelerini birleştir
df_combined = pd.concat([df_time,df_red, df_blue, df_green], axis=1)

# Excel dosyasına yaz
df_combined.to_excel(f'renk_koordinatları_{now}.xlsx', index=False)

# Temizlik
video.release()
cv2.destroyAllWindows()
