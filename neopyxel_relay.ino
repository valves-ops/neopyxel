/*
 Protocol Structure
  BYTE0 - LED Stripe Number
  BYTE1 - Command 
  BYTE2 - Command Argument 1
  BYTEN - Command Argument N 

  Commands List
  SETPIXELCOLOR - 0x1
  PIXELSHOW - 0x2
 */
#include <Adafruit_NeoPixel.h>
bool debug = false;
const int SETPIXELCOLOR = 0x1;
const int PIXELSHOW = 0x2;
#define PIN            6

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS      30

Adafruit_NeoPixel stripe[] = {Adafruit_NeoPixel(NUMPIXELS, 4, NEO_GRB + NEO_KHZ800), 
                              Adafruit_NeoPixel(NUMPIXELS, 5, NEO_GRB + NEO_KHZ800), 
                              Adafruit_NeoPixel(NUMPIXELS, 6, NEO_GRB + NEO_KHZ800)};
//Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
byte cmd_buffer[2]; 
byte arg_buffer[4];
void setup(){
  Serial.begin(28800);
  stripe[0].begin();
  stripe[1].begin();
  stripe[2].begin();
}

void loop(){
  if (Serial.available() > 0){
   int bava = Serial.available();
   Serial.readBytes(cmd_buffer, 2);
   byte LED_STRIPE = cmd_buffer[0];
   byte cmd = cmd_buffer[1];
   if (cmd == SETPIXELCOLOR) {
     Serial.readBytes(arg_buffer, 4);
     byte p = arg_buffer[0];
     byte r = arg_buffer[1];
     byte g = arg_buffer[2];
     byte b = arg_buffer[3];
     stripe[LED_STRIPE].setPixelColor(p, stripe[LED_STRIPE].Color(r,g,b));
     if (debug) {
       Serial.print("\nBytes Available: ");
       Serial.println(bava);
       Serial.print("Stripe: ");
       Serial.println(LED_STRIPE, HEX);
       Serial.print("CMD: ");
       Serial.println(cmd, HEX);
       Serial.print("Pixel: ");
       Serial.println(p, HEX);
       Serial.print("Red: ");
       Serial.println(r);
       Serial.print("Green: ");
       Serial.println(g, HEX);
       Serial.print("Blue: ");
       Serial.println(b, HEX);
     }
   } else if (cmd == PIXELSHOW) {
      stripe[LED_STRIPE].show();
   }
  }
}
