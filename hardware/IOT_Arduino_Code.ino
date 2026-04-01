#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); 

// Pins
const int trigPin = 9;
const int echoPin = 8;
const int pirPin = 2;
const int buzzer = 3; 

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(pirPin, INPUT);
  pinMode(buzzer, OUTPUT);

  lcd.print("SYSTEM READY");
  lcd.setCursor(0, 1); lcd.print("Asish Project");
  delay(2000);
  lcd.clear();
  lcd.print("Loading States...");
  delay(2000);
}

bool alarmActive = false;

void loop() {
  // 1. Measure Distance (Ultrasonic)
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH); 
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH, 30000);
  int distance = (duration * 0.034) / 2;

  // 2. Check Motion (PIR)
  int motion = digitalRead(pirPin);

  // 3. Simple Alarm Logic
  // If motion is detected AND distance is between 1cm and 100cm
  if (motion == HIGH && distance > 0 && distance < 100) {
    alarmActive = true;
  }

  if(alarmActive && distance > 0 && distance < 100){
    tone(buzzer, 500); // Sound ON
    
    lcd.setCursor(0, 0); lcd.print("ANIMAL DETECTED ");
    lcd.setCursor(0, 1); lcd.print("Dist: "); lcd.print(distance); lcd.print("cm    ");
    
    Serial.print("ALARM! Animal Detected --> Distance: "); Serial.println(distance);
  } 
  else {
    noTone(buzzer); // Sound OFF
    digitalWrite(buzzer, LOW);
    
    alarmActive = false;
    lcd.setCursor(0, 0); lcd.print("STATUS: SECURE  ");
    lcd.setCursor(0, 1); lcd.print("Scanning...    ");
  }
  
  delay(500); // Wait a bit before checking again
}