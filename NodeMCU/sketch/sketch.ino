#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

#define USE_SERIAL Serial

ESP8266WiFiMulti WiFiMulti;
int ledPin = D4;

void setup() {
   USE_SERIAL.begin(9600);
   // USE_SERIAL.setDebugOutput(true);

    USE_SERIAL.println();
    USE_SERIAL.println();
    USE_SERIAL.println();
    
    pinMode(ledPin, OUTPUT);
    pinMode(D5,OUTPUT);
    pinMode(D6,OUTPUT);
    pinMode(D7,OUTPUT);
    pinMode(D3,OUTPUT);
    
    for(uint8_t t = 4; t > 0; t--) {
        USE_SERIAL.printf("[SETUP] WAIT %d...\n", t);
        USE_SERIAL.flush();
        digitalWrite(ledPin, 0);
        delay(300);
        digitalWrite(ledPin, 1);
        delay(700);
    }

    WiFiMulti.addAP("PROLINK_H5004NK_7C0FF", "0112293636slt");

}

void loop() { 
  if((WiFiMulti.run() == WL_CONNECTED)) {
        float light_out=0;
        float ac_out=0;
        digitalWrite(D3,HIGH);
        delay(100);
        int temp=analogRead(A0);
        digitalWrite(D3,LOW);
        delay(100);
        digitalWrite(D7,HIGH);
        delay(100);
        int light=analogRead(A0);
        digitalWrite(D7,LOW);
        delay(100);
        digitalWrite(ledPin, 0);
        
        StaticJsonBuffer<300> JSONbuffer;   //Declaring static JSON buffer
        JsonObject& JSONencoder = JSONbuffer.createObject(); 
 
        JSONencoder["temperature"] = temp; 
        JSONencoder["light"] = light; 
        char JSONmessageBuffer[300];
        JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
        Serial.println(JSONmessageBuffer);

        HTTPClient http;
        
        http.begin("http://192.168.1.6:8000/indata/");      //Specify request destination
        http.addHeader("Content-Type", "application/json");  //Specify content-type header

        int httpCode = http.POST(JSONmessageBuffer);   //Send the request
        if((int)httpCode>0){
            const size_t bufferSize = JSON_OBJECT_SIZE(2) + JSON_OBJECT_SIZE(3) + JSON_OBJECT_SIZE(5) + JSON_OBJECT_SIZE(8) + 370;
            DynamicJsonBuffer jsonBuffer(bufferSize);
            JsonObject& root = jsonBuffer.parseObject(http.getString());
            light_out=root["output_lights"];
            ac_out=root["output_ac"];
            
        }

 
        Serial.println(httpCode);   //Print HTTP return code
        Serial.println(light_out);
        Serial.println(ac_out);//Print request response payload

        http.end();
  }else{
    Serial.println("Error in WiFi connection");
    digitalWrite(ledPin, 0);
  }
    delay(10000);

}
