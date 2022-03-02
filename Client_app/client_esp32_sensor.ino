#include <WiFi.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <string.h>

#define DHTPIN 27
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "network_name";
const char* password =  "network_password";

const uint16_t port = 5050;
const char * host = "server_IP_address";


void setup()
{

  Serial.begin(115200);
  dht.begin();
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
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  
  Serial.println("Connected to server successful!");
  String st = String(t, 2);
  String sh = String(h, 2);
  
  client.print(st);
  delay(1000);
  client.print(sh);
  delay(1000);
  client.print("!DISCONNECT");
  Serial.println("Disconnecting...");
  client.stop();

  delay(5000);
}
