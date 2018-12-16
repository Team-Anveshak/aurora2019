/* rosserial Subscriber For Locomotion Control */
#include <ros.h>
#include <man_ctrl/Wheel_rpm.h>

#include <Wire.h>
#include "variables.h"
#include "Task.h"


ros::NodeHandle nh;

man_ctrl::Wheel_rpm RoverRpm;




void roverMotionCallback(const man_ctrl::Wheel_rpm& RoverRpm)
{
  rpm = RoverRpm.rpm;
  dir = RoverRpm.dir;
  mod = RoverRpm.mod;
}

ros::Subscriber<man_ctrl::Wheel_rpm> locomotion_sub("loco/wheel_rpm", &roverMotionCallback);


void setup()

{
  // put your setup code here, to run once:
  nh.initNode();
  nh.subscribe(locomotion_sub);
  Wire.begin(21, 22, 100000);

  xTaskCreatePinnedToCore(
    coreZeroTask,
    "i2cTask",
    10000,
    NULL,
    2,
    NULL,
    TaskcoreZero);
}

void loop()
{
  // put your main code here, to run repeatedly:
  nh.spinOnce();
  delay(10);
}
