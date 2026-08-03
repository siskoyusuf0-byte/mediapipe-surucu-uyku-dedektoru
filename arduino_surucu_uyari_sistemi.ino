
const int ledPin = 8;
const int buzzerPin = 9;


char gelenKomut;

void setup() {
  
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  
  
  Serial.begin(9600);
  
  
  digitalWrite(ledPin, LOW);
  noTone(buzzerPin); 
}

void loop() {
  
  if (Serial.available() > 0) {
    gelenKomut = Serial.read(); 
    
    
    if (gelenKomut == '1') {
      digitalWrite(ledPin, HIGH); 
      tone(buzzerPin, 1000);      
    } 
    
    
    else if (gelenKomut == '0') {
      digitalWrite(ledPin, LOW);  
      noTone(buzzerPin);          
    }
  }
}
