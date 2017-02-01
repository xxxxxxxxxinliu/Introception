#include <Wire.h>
#include "Adafruit_MCP9808.h"

#define MCP9808_RESOLUTION          0x08

Adafruit_MCP9808 tempsensor = Adafruit_MCP9808();

void setup() {
  Serial.begin(9600);
  Serial.println("MCP9808 demo");
  
  // Make sure the sensor is found, you can also pass in a different i2c
  // address with tempsensor.begin(0x19) for example
  if (!tempsensor.begin()) {
    Serial.println("Couldn't find MCP9808!");
    while (1);
  }
  tempsensor.shutdown_wake(0); 
  Wire.beginTransmission(0x18);
  Wire.write((uint8_t)MCP9808_RESOLUTION);    
  Wire.write(0x02);
  //Wire.write(value & 0xFF);
  Wire.endTransmission();
}

void loop() {
  //Serial.println("wake up MCP9808.... "); // wake up MSP9808 - power consumption ~200 mikro Ampere 
  // Read and print out the temperature
  float c = tempsensor.readTempC();
  Serial.println(c); 
  delay(65);

}
