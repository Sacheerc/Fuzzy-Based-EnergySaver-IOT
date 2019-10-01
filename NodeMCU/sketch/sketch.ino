#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

#define USE_SERIAL Serial

ESP8266WiFiMulti WiFiMulti;

void setup() {
   USE_SERIAL.begin(9600);
   // USE_SERIAL.setDebugOutput(true);

    USE_SERIAL.println();
    USE_SERIAL.println();
    USE_SERIAL.println();

    for(uint8_t t = 4; t > 0; t--) {
        USE_SERIAL.printf("[SETUP] WAIT %d...\n", t);
        USE_SERIAL.flush();
        delay(1000);
    }

    WiFiMulti.addAP("PROLINK_H5004NK_7C0FF", "0112293636slt");

}

void loop() {
  float temp=24.5;
  float light=45.4;
  
  if((WiFiMulti.run() == WL_CONNECTED)) {
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
        String payload = http.getString();                                        //Get the response payload
 
        Serial.println(httpCode);   //Print HTTP return code
        Serial.println(payload);    //Print request response payload

        http.end();
  }else{
    Serial.println("Error in WiFi connection");
  }
    delay(10000);

}
