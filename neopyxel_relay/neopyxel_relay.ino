/*
 Protocol Structure
  BYTE0 - LED Stripe Number
  BYTE1 - Command 
  BYTE2 - Command Argument 1
  BYTEN - Command Argument N 

  Commands List
  SETPIXELCOLOR - 0x1
  PIXELSHOW - 0x2
  ADDSTRIPE - 0x3
  CLEARSTRIPES - 0x4
 */
#include <Adafruit_NeoPixel.h>
bool debug = false;
const int SETPIXELCOLOR = 0x1;
const int PIXELSHOW = 0x2;
const int ADDSTRIPE = 0x3;
const int CLEARSTRIPES = 0x4;

Adafruit_NeoPixel stripes[14];
byte cmd_buffer[2]; 
byte arg_buffer[4];
byte stripes_array_size = 0;
//Adafruit_NeoPixel stripes[0];


void setup(){
  Serial.begin(12800);
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
     
     stripes[LED_STRIPE].setPixelColor(p, stripes[LED_STRIPE].Color(r,g,b));
   } 
   else if (cmd == PIXELSHOW) {
      stripes[LED_STRIPE].show();
   } 
   else if (cmd == ADDSTRIPE) {
     Serial.readBytes(arg_buffer, 2);
     byte num_pixels = arg_buffer[0];
     byte pin = arg_buffer[1];
     
     stripes[stripes_array_size] = Adafruit_NeoPixel(num_pixels, pin, NEO_GRB + NEO_KHZ800);
     stripes[stripes_array_size].begin();
     stripes_array_size++;
   } 
   else if (cmd == CLEARSTRIPES) {
     stripes_array_size = 0;
   }

  }
}
