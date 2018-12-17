/* rosserial Subscriber For Locomotion Control */
#include <ros.h>
#include <man_ctrl/Wheel_rpm.h>

#include <Wire.h>

#define b1 15
#define b2 16
#define b3 17


int rpm = 0,  dir = 0;
int mod = 0;

ros::NodeHandle nh;

man_ctrl::Wheel_rpm RoverRpm;

void loco(int address)
{

  Wire.beginTransmission(address);
  Wire.write(rpm);
  Wire.write(dir);
  Wire.write(mod);
  Wire.endTransmission();
}

void roverMotionCallback(const man_ctrl::Wheel_rpm& RoverRpm)
{
  rpm = RoverRpm.rpm;
  dir = RoverRpm.dir;
  mod = RoverRpm.mod;

  loco(b1);
  loco(b2);
  loco(b3);
}

ros::Subscriber<man_ctrl::Wheel_rpm> locomotion_sub("loco/wheel_rpm", &roverMotionCallback);

void setup() {
  nh.initNode();
  nh.subscribe(locomotion_sub);
  Wire.begin();
  // nh.advertise(WheelVelocity);

}

void loop() {

  nh.spinOnce();
  //delay(10);
}
