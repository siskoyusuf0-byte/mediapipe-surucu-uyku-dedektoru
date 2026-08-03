<h1 align="center">Sürücü Yorgunluk ve Uyku Tespit Sistemi </h1>



Bu proje, sürücülerin direksiyon başında uyuyakalması veya dikkatinin dağılması gibi tehlikeli durumları önlemek amacıyla geliştirilmiş gerçek zamanlı bir Sürücü İzleme Sistemidir. Kamera üzerinden alınan görüntüler işlenerek sürücünün yüz ve göz durumu analiz edilir, tehlike anında Arduino üzerinden gecikmesiz olarak sesli ve görsel uyarı verilir.

---

## Proje Demosu

![Sürücü Yorgunluk Sistemi Demosu]<img width="800" height="447" alt="surucu_test_demo" src="https://github.com/user-attachments/assets/102a0afe-eb8b-434c-8c49-2992f247af24" />


**Detaylı Test ve Çalışma Videosu:**

https://github.com/user-attachments/assets/6fc1839f-0e46-4461-84a4-92d00451a150



---

## Öne Çıkan Özellikler

* **Dinamik Göz Kalibrasyonu:** Sistem ilk açıldığında 5 saniye boyunca sürücünün normal bakışını tarar. Her insanın göz yapısı farklı olduğu için sabit bir eşik değeri kullanmak yerine kişiye özel bir sınır belirler.
* **Matematiksel Analiz:** MediaPipe Face Mesh kullanılarak yüzdeki 468 nokta tespit edilir. Göz kapağı açıklığı bilimsel algoritmalarla gerçek zamanlı olarak hesaplanır.
* **Kafa Eğikliği Tespiti:** Sadece gözlerin kapanması değil, yorgunluktan kafanın öne düşmesi durumu da kafa oranlaması yapılarak tespit edilir ve alarm tetiklenir.
* **Gecikmesiz Donanım Uyarısı:** Tehlike algılandığı an Python, Arduino ile seri haberleşerek anında donanımsal ikaz (LED ve Buzzer) sistemini çalıştırır.

---

## Sistem Nasıl Çalışır?

Sistem temel olarak Göz Açıklık Oranı (Eye Aspect Ratio - EAR) algoritmasına dayanır. Yüz üzerindeki alt ve üst göz kapağı noktaları arasındaki dikey mesafe, gözün yatay genişliğine oranlanır:

$$EAR = \frac{||P_2 - P_6|| + ||P_3 - P_5||}{2 ||P_1 - P_4||}$$

Gözler kapandığında bu oran hızla düşer. Sistem, başlangıçta kişiye özel belirlediği dinamik eşik değerinin altına düşüldüğünde ve bu durum 1.5 saniyeden uzun sürdüğünde otomatik olarak uyku tehlikesi alarmı üretir.

---

## Devre Kurulumu

Arduino bağlantılarını aşağıdaki şemaya göre yapabilirsiniz:

| Bileşen | Arduino Pini | Açıklama |
| :--- | :--- | :--- |
| **Kırmızı LED (+)** | Pin 8 | 220 Ohm direnç ile bağlanmalıdır. |
| **Buzzer (+)** | Pin 9 | Tehlike anında devreye giren sesli ikaz modülü. |
| **GND (Toprak)** | GND | Ortak eksi (-) hat. |

---

## Kurulum ve Çalıştırma Adımları

**1. Gerekli kütüphaneleri yükleyin:**
```bash
pip install opencv-python mediapipe pyserial
```
**2. Arduino kodunu yükleyin:**
Depoda bulunan arduino_uyari_sistemi.ino dosyasını Arduino IDE üzerinden geliştirme kartınıza yükleyin.

**3. Sistemi başlatın:**
Kodu çalıştırmadan önce Arduino'nun bağlı olduğu portu (örneğin COM5) Python kodunda doğrulayın ve ardından programı çalıştırın:
```bash
python surucu_yorgunluk_tespiti.py
```
## Gelecek Geliştirmeler
Bu proje temel bir konsept kanıtı niteliğindedir. İlerleyen aşamalarda sisteme entegre edilebilecek özellikler:

* Esneme tespiti için ağız açıklık analizinin eklenmesi.

* Sistemin masaüstü bilgisayar yerine Raspberry Pi gibi taşınabilir bir gömülü sistem üzerinde (araç içi kamera formatında) bağımsız çalıştırılması.

* Gece sürüşleri için kızılötesi kamera desteği sağlanması.
