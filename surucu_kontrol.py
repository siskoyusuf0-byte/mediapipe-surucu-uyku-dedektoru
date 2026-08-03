import cv2
import mediapipe as mp
import math
import serial
import time


arduino_portu = "COM5" 
try:
    arduino = serial.Serial(port=arduino_portu, baudrate=9600, timeout=1, write_timeout=1)
    print(f"Arduino {arduino_portu} portundan başarıyla bağlandı!")
    time.sleep(2)
except:
    arduino = None
    print("Arduino bulunamadı.")


mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

def goz_aciklik_orani(yuz_noktalari, goz_indeksleri, genislik, yukseklik):
    # Bilimsel EAR Formülü: EAR = (|P2-P6| + |P3-P5|) / (2 * |P1-P4|) 
    p2_p6 = math.dist([yuz_noktalari[goz_indeksleri[1]].x * genislik, yuz_noktalari[goz_indeksleri[1]].y * yukseklik], [yuz_noktalari[goz_indeksleri[5]].x * genislik, yuz_noktalari[goz_indeksleri[5]].y * yukseklik])
    p3_p5 = math.dist([yuz_noktalari[goz_indeksleri[2]].x * genislik, yuz_noktalari[goz_indeksleri[2]].y * yukseklik], [yuz_noktalari[goz_indeksleri[4]].x * genislik, yuz_noktalari[goz_indeksleri[4]].y * yukseklik])
    p1_p4 = math.dist([yuz_noktalari[goz_indeksleri[0]].x * genislik, yuz_noktalari[goz_indeksleri[0]].y * yukseklik], [yuz_noktalari[goz_indeksleri[3]].x * genislik, yuz_noktalari[goz_indeksleri[3]].y * yukseklik])
    return (p2_p6 + p3_p5) / (2.0 * p1_p4)


SOL_GOZ = [362, 385, 387, 263, 373, 380]
SAG_GOZ = [33, 160, 158, 133, 153, 144]


UYKU_SURE_ESIGI = 1.5 
goz_kapama_baslangic_zamani, yuz_kayip_baslangic_zamani, referans_yuz_boyutu = None, None, None


kalibrasyon_tamamlandi = False
kalibrasyon_sure_siniri = 5.0 
kalibrasyon_baslangic_zamani = None
ear_kayitlari = []
EAR_ESIK = 0.15 


pencere_adi = "Dinamik Goz Takibi"


cap = cv2.VideoCapture("test_videosu.mp4")


cv2.namedWindow(pencere_adi, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(pencere_adi, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


son_gonderilen_durum = ""

print("Sistem başlatılıyor...")

while cap.isOpened():
    success, frame = cap.read()
    if not success: 
        print("Video bitti veya okunamadı.")
        break
    
    
    h, w, _ = frame.shape
    results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    durum_metni, renk, su_anki_durum = "GOZLER ACIK", (0, 255, 0), "0"

    if results.multi_face_landmarks:
        yuz_kayip_baslangic_zamani = None
        for face_landmarks in results.multi_face_landmarks:
            
            sol_ear = goz_aciklik_orani(face_landmarks.landmark, SOL_GOZ, w, h)
            sag_ear = goz_aciklik_orani(face_landmarks.landmark, SAG_GOZ, w, h)
            ortalama_ear = (sol_ear + sag_ear) / 2.0
            
            
            alin_y, cene_y = face_landmarks.landmark[10].y * h, face_landmarks.landmark[152].y * h
            su_anki_yuz_boyutu = abs(cene_y - alin_y)
            if referans_yuz_boyutu is None: referans_yuz_boyutu = su_anki_yuz_boyutu
            kafa_orani = su_anki_yuz_boyutu / referans_yuz_boyutu

            
            if not kalibrasyon_tamamlandi:
                if kalibrasyon_baslangic_zamani is None:
                    kalibrasyon_baslangic_zamani = time.time()
                
                gecen_kalibrasyon_suresi = time.time() - kalibrasyon_baslangic_zamani
                
                
                ear_kayitlari.append(ortalama_ear)
                
                durum_metni = f"TARANIYOR... {int(kalibrasyon_sure_siniri - gecen_kalibrasyon_suresi) + 1}s"
                renk = (255, 191, 0) 
                
                if gecen_kalibrasyon_suresi >= kalibrasyon_sure_siniri:
                    
                    ortalama_acik_ear = sum(ear_kayitlari) / len(ear_kayitlari)
                    
                    EAR_ESIK = ortalama_acik_ear * 0.45
                    kalibrasyon_tamamlandi = True
                    print(f"Kalibrasyon Tamamlandı! Göz yapınız için dinamik sınır: {EAR_ESIK:.2f}")

            
            else:
                
                if (ortalama_ear < EAR_ESIK) or (kafa_orani < 0.85):
                    if goz_kapama_baslangic_zamani is None: 
                        goz_kapama_baslangic_zamani = time.time()
                    gecen_sure = time.time() - goz_kapama_baslangic_zamani
                    if gecen_sure >= UYKU_SURE_ESIGI:
                        
                        durum_metni, renk, su_anki_durum = "UYKU TEHLIKESI!", (0, 0, 255), "1"
                    else:
                        durum_metni, renk = "GOZLER KAPALI", (0, 255, 255)
                else:
                    
                    goz_kapama_baslangic_zamani = None

    else:
        
        if kalibrasyon_tamamlandi:
            if yuz_kayip_baslangic_zamani is None: yuz_kayip_baslangic_zamani = time.time()
            gecen_kayip_sure = time.time() - yuz_kayip_baslangic_zamani
            if gecen_kayip_sure >= UYKU_SURE_ESIGI:
                durum_metni, renk, su_anki_durum = "YUZ KAYIP! ALARM!", (0, 0, 255), "1"
            else:
                durum_metni, renk = "YUZ ARANIYOR", (0, 255, 255)
        else:
            durum_metni, renk = "YUZ BEKLENIYOR", (0, 165, 255)

    
    if kalibrasyon_tamamlandi:
        cv2.putText(frame, f"Esik Degeriniz: {EAR_ESIK:.2f}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 100), 2)
    
    cv2.putText(frame, durum_metni, (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, renk, 3)
    
    
    cv2.imshow(pencere_adi, frame)
    
    
    
    if arduino and su_anki_durum != son_gonderilen_durum:
        arduino.write(su_anki_durum.encode())
        son_gonderilen_durum = su_anki_durum
    
    
    if cv2.waitKey(30) & 0xFF == ord('q'): break

if arduino: arduino.close()
cap.release()
cv2.destroyAllWindows()
