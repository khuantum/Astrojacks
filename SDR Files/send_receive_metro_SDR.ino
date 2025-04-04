// For Arduino MEGA or Leonardo with Serial1 connected to XBee
// XBee TX → Pin 19 (RX1)
// XBee RX → Pin 18 (TX1)
// GND → GND, 3.3V → 3.3V

void setup() {
  Serial.begin(9600);    // USB to PC
  Serial1.begin(9600);   // XBee
}

void loop() {
  // Pass bytes from Serial → XBee
  if (Serial.available() > 0) {
    Serial1.write(Serial.read());
  }
  // Pass bytes from XBee → Serial
  if (Serial1.available() > 0) {
    Serial.write(Serial1.read());
  }
}

