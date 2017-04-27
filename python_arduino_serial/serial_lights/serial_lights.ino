#include "LPD8806.h"
#include "SPI.h"

int nLEDs = 48;
int dataPin  = 9;
int clockPin = 10;

int refresh_delay = 100;

LPD8806 strip = LPD8806(nLEDs, dataPin, clockPin);

void setup() {
    Serial.begin(9600);
    strip.begin();
    strip.show();
}

void loop() {
  int inByte;
  int numBytes = strip.numPixels()*3; //r,g,b for each pixe
  byte byteSequence [numBytes];
  
  // wait to get all bytes needed to fill strip
  int i = 0;
  while (i < numBytes) {
    if (Serial.available()) {
      inByte = Serial.read();
//      Serial.println(inByte, DEC);
      byteSequence[i] = inByte;
      i++;}
  }
    
  int j = 0;
  for (int i=0; i<numBytes ; i+=3) {
    byte r = byteSequence[i];
    byte g = byteSequence[i+1];
    byte b = byteSequence[i+2];
    uint32_t color = strip.Color(r, g, b);
    strip.setPixelColor(j, color);
    j++;
  }

  strip.show();
}
