#include <Wire.h>
#include <SPI.h>
#include <SdFat.h>
#include <Adafruit_SPIFlash.h>
#include "flash_config.h"
#include "wiring_private.h"

#define SLAVE_ADDRESS 0x08
#define SDA_PIN 13
#define SCL_PIN 12

TwoWire myWire(&sercom1, SDA_PIN, SCL_PIN);

Adafruit_SPIFlash flash(&flashTransport);
FatVolume fatfs;

#define BUFFER_SIZE 32
File32 file;
char buffer[BUFFER_SIZE];
bool eofSent = false;

//NEED THIS FOR SERCOM I2C TO FUNCTION PROPERLY!!!
void SERCOM1_0_Handler() { myWire.onService(); }
void SERCOM1_1_Handler() { myWire.onService(); }
void SERCOM1_2_Handler() { myWire.onService(); }
void SERCOM1_3_Handler() { myWire.onService(); }

void setup() {
  Serial.begin(115200);
  pinPeripheral(SDA_PIN, PIO_SERCOM);
  pinPeripheral(SCL_PIN, PIO_SERCOM);

  myWire.begin(SLAVE_ADDRESS);  // I2C slave address
  myWire.onRequest(requestEvent);

  if (!flash.begin() || !fatfs.begin(&flash)) {
    Serial.println("Flash init failed!");
    while (1);
  }

  file = fatfs.open("drop_data_1.csv", FILE_READ);  // Replace with desired file
  if (!file) {
    Serial.println("File open failed");
  }
  
}

void loop() {
  delay(100);  // Wait for requests
}

void requestEvent() {
  if (!file || eofSent) {
    myWire.write("EOF");
    return;
  }

  int bytesRead = file.read(buffer, BUFFER_SIZE);
  if (bytesRead > 0) {
    myWire.write((const uint8_t*)buffer, bytesRead);
  } else {
    eofSent = true;
    file.close();
  }
}
