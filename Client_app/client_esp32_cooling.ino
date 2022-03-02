#include <WiFi.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <string.h>
#define RELAY_PIN 27

const char* ssid = "network_name";
const char* password =  "network_password";

const uint16_t port = 5050;
const char * host = "server_IP_address";


void setup()
{
  pinMode(RELAY_PIN, OUTPUT);

  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }

  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

}

void loop()
{
  WiFiClient client;

  if (!client.connect(host, port)) {

    Serial.println("Connection to host failed");

    delay(1000);
    return;
  }

  Serial.println("Connected to server successful!");

  client.print("ok");
  delay(1000);
  int i = client.read();
  Serial.println(i);
  client.print("!DISCONNECT");
  Serial.println("Disconnecting...");
  client.stop();
     
  if (i == 49) {
    digitalWrite(RELAY_PIN, HIGH);
    delay(600000);
    } else {
      digitalWrite(RELAY_PIN, LOW);

      }
  delay(5000);
}
