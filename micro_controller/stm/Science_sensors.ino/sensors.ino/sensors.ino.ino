
#include <SparkFunTSL2561.h>
#include <Wire.h>
#include <ros.h>
#include <science/Science.h>
#include <SFE_BMP180.h>

ros::NodeHandle nh;
// Create an SFE_TSL2561 object, here called "light":

SFE_TSL2561 light;

// Global variables:

boolean gain;     // Gain setting, 0 = X1, 1 = X16;
unsigned int ms;  // Integration ("shutter") time in milliseconds

// You will need to create an SFE_BMP180 object, here called "pressure":

SFE_BMP180 pressure;

#define ALTITUDE 1655.0 // Altitude of SparkFun's HQ in Boulder, CO. in meters
int UVOUT = PA0; //Output from the sensor
int REF_3V3 = PA1; //3.3V power on the Arduino board

science::Science science_task;

ros::Publisher p1("Science_data",&science_task);

void setup()
{
  // Initialize the Serial port:
  
 
  light.begin();
  unsigned char ID;
  gain = 0;
  unsigned char time = 2;
  light.setTiming(gain,time,ms);
  light.setPowerUp();
  
  nh.initNode();
  nh.advertise(p1);
}

void loop()
{
  char status;
  double T,P,p0,a;
  
  unsigned int data0, data1;
  
  if (light.getData(data0,data1))
  {
    
    double lux;    // Resulting lux value
    boolean good;  // True if neither sensor is saturated
    
    // Perform lux calculation:

    good = light.getLux(gain,ms,data0,data1,lux);
    science_task.luminosity=lux;

  }
 status = pressure.startTemperature();
  if (status != 0)
  {
    status = pressure.getTemperature(T);
    if (status != 0)
    {
      status = pressure.startPressure(3);
      if (status != 0)
      {
        status = pressure.getPressure(P,T);
        if (status != 0)
        {
          p0 = pressure.sealevel(P,ALTITUDE); // we're at 1655 meters (Boulder, CO)
          a = pressure.altitude(P,p0);
        }
      }
    }
  }
  science_task.pressure=P;
  science_task.Temp=T;

  int uvLevel = averageAnalogRead(UVOUT);
  int refLevel = averageAnalogRead(REF_3V3);

  //Use the 3.3V power pin as a reference to get a very accurate output value from sensor
  float outputVoltage = 3.3 / refLevel * uvLevel;

  float uvIntensity = mapfloat(outputVoltage, 0.99, 2.8, 0.0, 15.0); //Convert the voltage to a UV intensity level
  science_task.UVintensity=uvIntensity;
   
  p1.publish(&science_task);
  nh.spinOnce();
}

int averageAnalogRead(int pinToRead)
{
  byte numberOfReadings = 8;
  unsigned int runningValue = 0; 

  for(int x = 0 ; x < numberOfReadings ; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= numberOfReadings;

  return(runningValue);  
}

//The Arduino Map function but for floats
//From: http://forum.arduino.cc/index.php?topic=3922.0
float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
