/*
 *  This file is part of A7105-uart, a UART interface to the A7105 wireless
 *  tranceiver.
 *  Copyright (C) 2015 J.Deitmerg <mowfask@gmail.com>
 *
 *  A7105-uart is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  A7105-uart is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with A7105-uart.  If not, see <http://www.gnu.org/licenses/>.
 */


/*
 *                     Wired diagram
 *           `UNIT                 ARDUINO (Mega)
 *        -------------           --------------
 *        Pin  2  (GIO1)    -     Pin  50 (MISO)
 *        Pin  7  (GND )    -     Pin  _  (GND )
 *        Pin  9  (VDD )    -     Pin  _  (3.3V)
 *        Pin  12 (SCS )    -     Pin  10 (CS  )
 *        Pin  13 (SCK )    -     Pin  52 (SCK )
 *        Pin  14 (SDIO)    -     Pin  51 (MOSI)
 *        -------------           --------------
 */
         
// include library 
#include <Arduino.h>
#include <main.h>



// Setup hardware
void setup(){
  //      UART
  //Serial.begin(115200);
  //Serial.flush();
  //Serial.print ("Start initialize");
  //Serial.print ("     [ UART  ]        - complete ");

  ///*     SPI
   initialise the cs lock pi  */
  //pinMode(CS_PIN, OUTPUT);
  //CS_HI();
  
  ///* initialise SPI, set mode and byte order */
  //SPI.begin();
  //SPI.setDataMode(SPI_MODE0);
  //SPI.setBitOrder(MSBFIRST);
  //Serial.print ("     [ SPI   ]        - complete ");


  ///* init other hardware */
  //Serial.print ("     [ UNIT1 ]        - complete ");

  ///* init hardware is completed */
  //delay(500);
  //Serial.println("Start program");

}

// MAIN Loop of program
void loop() {
    //Variables
    uint8_t RSSI;
    uint8_t _chan;
    uint8_t _len;
    _chan = 0;

    // Main program


}



// Function   Fun1
void Fun_1 (void)
{
  // Code of Function
  return;
}


// Function   Fun2
uint8_t Fun_2 (uint8_t  variable_1, uint8_t  variable_2)
{
  // Code of Function with variable #1 and #2
  return variable_1 ;  // return   uint8_t variable
}










