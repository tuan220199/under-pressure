#include "Adafruit_Si7021.h"
unsigned long startMillis;  
unsigned long currentMillis;
bool enableHeater = false;
uint8_t loopCnt = 0;
Adafruit_Si7021 sensor = Adafruit_Si7021();

void setup() {
  //Set up the baudrate 
  Serial.begin(9600);

  // wait for serial port to open
 if (!sensor.begin()) {
    Serial.println("Did not find Si7021 sensor!");
    while (true)
      ;
  }

  //Check if the SI7021 working
  Serial.print("Found model ");
  switch(sensor.getModel()) {
    case SI_Engineering_Samples:
      Serial.print("SI engineering samples"); break;
    case SI_7013:
      Serial.print("Si7013"); break;
    case SI_7020:
      Serial.print("Si7020"); break;
    case SI_7021:
      Serial.print("Si7021"); break;
    case SI_UNKNOWN:
    default:
      Serial.print("Unknown");
  }
  Serial.print(" Rev(");
  Serial.print(sensor.getRevision());
  Serial.print(")");
  Serial.print(" Serial #"); Serial.print(sensor.sernum_a, HEX); Serial.println(sensor.sernum_b, HEX);

  //initial start time
  startMillis = millis();  
}

void loop() 
{
  //get the current "time" (actually the number of milliseconds since the program started)
  currentMillis = millis();

  //When the first minute pass for the sensors stabilize
  if (currentMillis - startMillis >= 60000)  
  {
    // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
    // Pressure sensor 1
    int sensorValue1 = analogRead(A0); 
    float voltage1 = sensorValue1 * (5.0 / 1023.0);

    // Pressure sensor 2
    int sensorValue2 = analogRead(A1);
    float voltage2 = sensorValue2 * (5.0 / 1023.0);

  
    //Calibration 
    //Diameter of sensor area 9.53mm; area of sensor
    float d = 9.53*pow(10,-3);
    float r = d/2;
    float A = 3.14*pow(r,2);

    //Convert voltage into force 
    float force1 = (voltage1 + 0.551) / (0.1665);
    float force2 = (voltage2 + 0.551) / (0.1665);

    //Convert force into pressure (unit Pa=N/m2)
    float pressure1 = force1/A;
    float pressure2 = force2/A;

    //Convert unit Pa into mmHg (unit mmHg)
    pressure1 /= 133.322;
    pressure2 /= 133.322;

    //Error measurement calibration
    pressure1 /= 12.8;
    pressure2 /= 12.8;

    // Print out the value you read / Send to processing via UART
    Serial.print(sensor.readHumidity(), 2);
    Serial.print(",");
    Serial.print(sensor.readTemperature(), 2);
    Serial.print(",");
    Serial.print(pressure1);
    Serial.print(",");
    Serial.print(pressure2);
    Serial.println();

    // Wait 15 second fro the next measurement
    delay(15000);  
  
  }
}


