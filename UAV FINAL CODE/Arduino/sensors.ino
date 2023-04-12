#include <I2Cdev.h>
#include <MPU6050.h>
#include <Adafruit_BMP085.h>
#include <HMC5883L_Simple.h>
#include <SoftwareSerial.h>

SoftwareSerial gpsSerial(2, 3);  // RX, TX

MPU6050 accelgyro;
Adafruit_BMP085 bmp;
HMC5883L_Simple Compass;


int16_t ax, ay, az;
int16_t gx, gy, gz;

#define LED_PIN 13
bool blinkState = false;

void setup() {
  Serial.begin(9600);
  gpsSerial.begin(9600);
  Wire.begin();

  // initialize devices
  Serial.println("Initializing I2C devices...");

  // initialize bmp085
  if (!bmp.begin()) {
    Serial.println("Could not find a valid BMP085 sensor, check wiring!");
    while (1) {}
  }

  // initialize mpu6050
  accelgyro.initialize();
  Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
  accelgyro.setI2CBypassEnabled(true); // set bypass mode for gateway to hmc5883L
  
  
  // initialize hmc5883l
  Compass.SetDeclination(23, 35, 'E');
  Compass.SetSamplingMode(COMPASS_SINGLE);
  Compass.SetScale(COMPASS_SCALE_130);
  Compass.SetOrientation(COMPASS_HORIZONTAL_X_NORTH);


  // configure Arduino LED for checking activity
  pinMode(LED_PIN, OUTPUT);
}

void loop() {

  Serial.print(bmp.readTemperature());
  Serial.print(",");

  Serial.print(bmp.readPressure());
  Serial.print(",");
  
  // Calculate altitude assuming 'standard' barometric
  // pressure of 1013.25 millibar = 101325 Pascal
  Serial.print(bmp.readAltitude());
  Serial.print(",");
  Serial.print(bmp.readSealevelPressure());
  Serial.print(",");
  Serial.print(bmp.readAltitude(101500));
  Serial.print(",");

  
  // read raw accel/gyro measurements from device
  accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  
  // display tab-separated accel/gyro x/y/z values

  Serial.print(ax); Serial.print(",");
  Serial.print(ay); Serial.print(",");
  Serial.print(az); Serial.print(",");
  Serial.print(gx); Serial.print(",");
  Serial.print(gy); Serial.print(",");
  Serial.print(gz); Serial.print(",");


  float heading = Compass.GetHeadingDegrees();
  Serial.print( heading );
    String data = gpsSerial.readStringUntil('\n');

  if (data.startsWith("$GNRMC") || data.startsWith("$GPRMC")) {
     Serial.print(",");
    // Extract time, date, latitude, longitude, speed, and course from RMC sentence
    int comma1 = data.indexOf(",");
    int comma2 = data.indexOf(",", comma1 + 1);
    int comma3 = data.indexOf(",", comma2 + 1);
    int comma4 = data.indexOf(",", comma3 + 1);
    int comma5 = data.indexOf(",", comma4 + 1);
    int comma6 = data.indexOf(",", comma5 + 1);
    int comma7 = data.indexOf(",", comma6 + 1);
    int comma8 = data.indexOf(",", comma7 + 1);

    String time = data.substring(comma1 + 1, comma2);
    float latitude = data.substring(comma3 + 1, comma4).toFloat();
    float longitude = data.substring(comma5 + 1, comma6).toFloat();
    float speed = data.substring(comma7 + 1, comma8).toFloat();
    float course = data.substring(comma8 + 1).toFloat();

    // Extract date from RMC sentence
    int dateStart = data.indexOf(",", comma8 + 1) + 1;
    int dateEnd = data.indexOf(",", dateStart);
    String date = data.substring(dateStart, dateEnd);

    // Concatenate the data into a comma-separated list
    String output = time + "," + date + "," + String(latitude, 6) + "," + String(longitude, 6) + "," + String(speed, 2) + "," + String(course, 2) ;
    Serial.print(output);
  }
  Serial.println();
}
