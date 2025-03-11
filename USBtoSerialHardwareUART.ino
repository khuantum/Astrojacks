//#include &lt;Arduino.h&gt;
#include "wiring_private.h" // pinPeripheral() function

#define PIN_SERIAL2_RX 12  // PA17 Pin 12
#define PAD_SERIAL2_RX (SERCOM_RX_PAD_1)
#define PIN_SERIAL2_TX 13  // PA16 Pin 13
#define PAD_SERIAL2_TX (UART_TX_PAD_0)

Uart Serial2( &sercom1, PIN_SERIAL2_RX, PIN_SERIAL2_TX, PAD_SERIAL2_RX, PAD_SERIAL2_TX );

void SERCOM1_0_Handler()
{
  Serial2.IrqHandler();
}
void SERCOM1_1_Handler()
{
  Serial2.IrqHandler();
}
void SERCOM1_2_Handler()
{
  Serial2.IrqHandler();
}
void SERCOM1_3_Handler()
{
  Serial2.IrqHandler();
}
void setup() {
  Serial.begin(9600);

  Serial1.begin(9600);

  Serial2.begin(9600);
  
  // Assign pins 12 & 13 SERCOM functionality
  pinPeripheral(PIN_SERIAL2_RX, PIO_SERCOM);
  pinPeripheral(PIN_SERIAL2_TX, PIO_SERCOM);
}

void loop() {
  // Pass bytes from Serial → XBee
  if (Serial.available() > 0) {
    int c = Serial.read();      // Read 1 byte from USB
    Serial1.write(c);           // Send same byte to XBee1
    Serial2.write(c);           // And to XBee2
  }
  // Pass bytes from XBee → Serial
  if (Serial1.available() > 0) {
    Serial.write(Serial1.read());
  }
  //Pass bytes from Second XBee to Serial
  if (Serial2.available() > 0) {
    Serial.write(Serial2.read());
  }
}