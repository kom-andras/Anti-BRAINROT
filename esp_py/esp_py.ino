const int relePin = 13;

void setup() {
  pinMode(relePin, OUTPUT);
  digitalWrite(relePin, HIGH);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "ON") {
      digitalWrite(relePin, LOW);
      delay(2000);
      digitalWrite(relePin, HIGH);
    }
  }
}
