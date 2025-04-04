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
#define FILE_NAME "data.csv"

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
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
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
  for (int i = 0; i <= 300; i++) {
    // Open the datalogging file for writing.  The FILE_WRITE mode will open
    // the file for appending, i.e. it will add new data to the end of the file.
    File32 dataFile = fatfs.open(FILE_NAME, FILE_WRITE);
    // Check that the file opened successfully and write a line to it.
    if (dataFile) {
      // Take a new data reading from a Accel
      /* Get new sensor events with the readings */
      sensors_event_t a, g, temp;
      mpu.getEvent(&a, &g, &temp);

      // Write a line to the file.  You can use all the same print functions
      // as if you're writing to the serial monitor.  For example to write
      // two CSV (commas separated) values:

      dataFile.print("Data Log #");
      dataFile.print(i);
      dataFile.println("Sensor #1:");
      dataFile.println("Acceleration X: ");
      dataFile.print(a.acceleration.x);
      dataFile.print(", Y: ");
      dataFile.print(a.acceleration.y);
      dataFile.print(", Z: ");
      dataFile.print(a.acceleration.z);
      dataFile.println(" m/s^2");

      dataFile.print("Rotation X: ");
      dataFile.print(g.gyro.x);
      dataFile.print(", Y: ");
      dataFile.print(g.gyro.y);
      dataFile.print(", Z: ");
      dataFile.print(g.gyro.z);
      dataFile.println(" rad/s");

      dataFile.print("Temperature: ");
      dataFile.print(temp.temperature);
      dataFile.println(" degC");

      dataFile.println("");
      // Finally close the file when done writing.  This is smart to do to make
      // sure all the data is written to the file.
      dataFile.close();
    } else {
      Serial.println("Failed to open data file for writing!");
    }
    delay(1);
  }
  
  Serial.println("Wrote measurements to data file!");
  Serial.println("Collection and Storage Complete");
  Serial.println("---------------------------------");
  Serial.println();
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
  Serial.println("1 - Start logging sensor data");
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
    Serial.println("Do you wish to begin logging sensor data on-device or onboard (battery powered)?");
    Serial.println("Enter [0] for on device(Will log and report), [1] for onboard Metro M4 (Will log unplugged, but to read new logs use action 2)");

    while (!Serial.available()) {
      delay(100);
    }

    char onOrOffBoard = Serial.read();
    
    // Clear buffer
    while (Serial.available()) {
      Serial.read();
    }

    if (onOrOffBoard == '0') {
      logSensorData();
    } else if (onOrOffBoard == '1') {
      Serial.println("Onboard Selected. Please unplug Metro M4 and wait at least 5 seconds before reconnecting.");
      delay(10000);
      Serial.println("Looks like you didn't unplug, logging anyways, be faster next time...");
      logSensorData();
    } else {
      Serial.println("Invalid input, please try again.");
    }
  } 
  else if (action == '2') {
    readMetroData();
  } 
  else {
    Serial.println("Invalid action, please try again.");
  }

  //delay(5000);
}
