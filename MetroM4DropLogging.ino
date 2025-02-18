// Adafruit SPI Flash FatFs Simple Datalogging Example
// Author: Tony DiCola
//
// This is a simple dataloging example using the SPI Flash
// FatFs library.  The example will open a file on the SPI
// flash and append new lines of data every minute. Note that
// you MUST have a flash chip that's formatted with a flash
// filesystem before running.  See the fatfs_format example
// to perform this formatting.
//
// Usage:
// - Modify the pins and type of fatfs object in the config
//   section below if necessary (usually not necessary).
// - Upload this sketch to your M0 express board.
// - Open the serial monitor at 115200 baud.  You should see the
//   example print a message every minute when it writes a new
//   value to the data logging file.
//Above is Usage Instructions


//NOTICE: You need to format the storage for a brand new m4 that hasn't been setup. Run the format example in the Adafruit SPIFlash Library


#include <SPI.h>
#include <SdFat.h>


#include <Adafruit_SPIFlash.h>


// for flashTransport definition
#include "flash_config.h"
Adafruit_SPIFlash flash(&flashTransport);


//for Adafruit Accel/Gyro
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
Adafruit_MPU6050 mpu;




// file system object from SdFat
FatVolume fatfs;


// Configuration for the datalogging file:
#define FILE_NAME "drop_data.csv"


float dropAccelThresh = 30.0;
float freeFallThresh = 2.0;
float restingAccel = 9.0;
float peakAccel = 0.0;
unsigned long impactDuration = 0;
int fileNum = 1;


void setup() {
  // Initialize serial port and wait for it to open before continuing.
  Serial.begin(115200);
  while (!Serial) {
    delay(100);
  }
  Serial.println("Adafruit SPI Flash FatFs Data Logging Hardware Info:");


  // Initialize flash library and check its chip ID.
  if (!flash.begin()) {
    Serial.println("Error, failed to initialize flash chip!");
    while (1) {
      delay(1);
    }
  }
  Serial.print("Flash chip JEDEC ID: 0x");
  Serial.println(flash.getJEDECID(), HEX);


  // First call begin to mount the filesystem.  Check that it returns true
  // to make sure the filesystem was mounted.
  if (!fatfs.begin(&flash)) {
    Serial.println("Error, failed to mount newly formatted filesystem!");
    Serial.println(
      "Was the flash chip formatted with the fatfs_format example?");
    while (1) {
      delay(1);
    }
  }
  Serial.println("Mounted filesystem!");
  //Serial.println("Logging data every 60 seconds...");
  Serial.println("---------------------------------------");
  Serial.println();


    //Accelerometer Sensor
    Serial.println("Setting up Accelerometer/Gyro");
    if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");


  mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
    case MPU6050_RANGE_2_G:
      Serial.println("+-2G");
      break;
    case MPU6050_RANGE_4_G:
      Serial.println("+-4G");
      break;
    case MPU6050_RANGE_8_G:
      Serial.println("+-8G");
      break;
    case MPU6050_RANGE_16_G:
      Serial.println("+-16G");
      break;
  }
  mpu.setGyroRange(MPU6050_RANGE_2000_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
    case MPU6050_RANGE_250_DEG:
      Serial.println("+- 250 deg/s");
      break;
    case MPU6050_RANGE_500_DEG:
      Serial.println("+- 500 deg/s");
      break;
    case MPU6050_RANGE_1000_DEG:
      Serial.println("+- 1000 deg/s");
      break;
    case MPU6050_RANGE_2000_DEG:
      Serial.println("+- 2000 deg/s");
      break;
  }


  mpu.setFilterBandwidth(MPU6050_BAND_260_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
    case MPU6050_BAND_260_HZ:
      Serial.println("260 Hz");
      break;
    case MPU6050_BAND_184_HZ:
      Serial.println("184 Hz");
      break;
    case MPU6050_BAND_94_HZ:
      Serial.println("94 Hz");
      break;
    case MPU6050_BAND_44_HZ:
      Serial.println("44 Hz");
      break;
    case MPU6050_BAND_21_HZ:
      Serial.println("21 Hz");
      break;
    case MPU6050_BAND_10_HZ:
      Serial.println("10 Hz");
      break;
    case MPU6050_BAND_5_HZ:
      Serial.println("5 Hz");
      break;
  }


  Serial.println("Accelerometer Setup Complete");
  Serial.println("--------------------------------------");
  Serial.println();


  delay(100);
}


void logSensorData() {
  Serial.println("Collecting and Storing Accelerometer/Gyro Data...");
  // Open the datalogging file for writing.  The FILE_WRITE mode will open
    // the file for appending, i.e. it will add new data to the end of the file.
    File32 dataFile = fatfs.open(FILE_NAME, FILE_WRITE);
    // Check that the file opened successfully and write a line to it.
    if (dataFile) {
      // Take a new data reading from a Accel
      /* Get new sensor events with the readings */
      sensors_event_t a, g, temp;
      mpu.getEvent(&a, &g, &temp);
     
      float xAcel = a.acceleration.x;
      float yAcel = a.acceleration.y;
      float zAcel = a.acceleration.z;


      float totalAccel = sqrt((xAcel*xAcel) + (yAcel*yAcel) + (zAcel*zAcel));


      // Get timestamp
      unsigned long timestamp = millis();


      // Write header if file is empty
      if (dataFile.size() == 0) {
        dataFile.println("Timestamp (ms),Total Accel (m/s^2),Accel_X (m/s^2),Accel_Y (m/s^2),Accel_Z (m/s^2)");
      }


      // Write CSV data
      dataFile.print(timestamp);
      dataFile.print(",");
      dataFile.print(totalAccel);
      dataFile.print(",");
      dataFile.print(a.acceleration.x, 6); // 6 decimal places for precision
      dataFile.print(",");
      dataFile.print(a.acceleration.y, 6);
      dataFile.print(",");
      dataFile.println(a.acceleration.z, 6);


      // Close the file
      dataFile.close();
      Serial.println("Data written to file.");
    } else {
      Serial.println("Failed to open data file for writing!");
    }


  Serial.println("---------------------------------");
}


void readMetroData() {
  Serial.println("Reading from SPI Flash Storage...");
 
  //Read data from SPI Flash
  Serial.println("data stored in SPI Flash:");
  File32 myFile = fatfs.open(FILE_NAME);
  if (myFile) {
    // read from the file until there's nothing else in it:
    while (myFile.available()) {
      Serial.write(myFile.read());
    }
    // close the file:
    myFile.close();
  } else {
    // if the file didn't open, print an error:
    Serial.println("error opening ");
    Serial.print(FILE_NAME);
    Serial.print(".txt");
  }


  delay(1000);
  Serial.println("Read Complete");
  Serial.println("--------------------------");
  Serial.println();
}


void drop(float &accel, unsigned long &time) {
  float totalAccel1;
  float totalAccel;
  totalAccel1 = getAccelValue();


  bool steadyState = false;
  int impact = 0;
 
  unsigned long impactStart = 0;
  unsigned long impactEnd = 0;
 
  //if reach free fall start logging
  if (totalAccel1 < freeFallThresh) {
    while (!steadyState) {
      //once reach free fall log until reach equilibrium, to reach equilibrium must wait for spike
      logSensorData();
      totalAccel = getAccelValue();
     
      float temp1 = 0.0;


      if (totalAccel > dropAccelThresh) {
        temp1 = totalAccel; //this prevents wrong peak accel
        if (temp1 >= peakAccel) {
          peakAccel = temp1; //return peak accel
          impactStart = millis();
          impact +=1;
        }  
      }


      if ((impact > 0) && (totalAccel < 8.9)) {
        impactEnd = millis();
        impactDuration = impactEnd - impactStart; //return impact duration
        steadyState = true;
      }


    }
  }


}


float getAccelValue() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);


  float xAcel = a.acceleration.x;
  float yAcel = a.acceleration.y;
  float zAcel = a.acceleration.z;


  float totalAccel = sqrt((xAcel*xAcel) + (yAcel*yAcel) + (zAcel*zAcel));


  return totalAccel;
}


void loop() {


  unsigned long startTime = millis();
 
  // Wait for Serial to be available for up to 5 seconds
  while (!Serial && millis() - startTime < 5000) {
    delay(100);
  }


  if (Serial) {
    Serial.println("Board Detected");
  } else {
    Serial.println("Running standalone mode (No Serial)");
  }


  //Serial.setTimeout(20000);


  Serial.println();
  Serial.println("Please choose an action:");
  Serial.println("1 - Drop the Sensor and Log Data");
  Serial.println("2 - Read stored data");
  Serial.println("Enter choice:");


  while (!Serial.available()) {
    delay(100);
  }


  char action = Serial.read();
 
  // Clear buffer
  while (Serial.available()) {
    Serial.read();
  }


  if (action == '1') {
    Serial.println("Device will begin logging once it has detected being dropped, Please Unplug Metro and drop device");
    drop(peakAccel, impactDuration);
  }
  else if (action == '2') {
    readMetroData();
  }
  else {
    Serial.println("Invalid action, please try again.");
  }


  //delay(5000);
}



