#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "";
const char* password = "";

WebServer server(80);
const int relePin = 13;

void setup() {
  Serial.begin(115200);
  pinMode(relePin, OUTPUT);
  digitalWrite(relePin, HIGH);
  Serial.println("Connecting to wifi");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/on", []() {
    digitalWrite(relePin, LOW);
    server.send(200, "text/plain", "Relay ON");
    delay(2000);
    digitalWrite(relePin, HIGH);
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
