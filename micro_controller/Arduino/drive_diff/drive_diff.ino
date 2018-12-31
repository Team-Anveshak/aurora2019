/* rosserial Subscriber For Locomotion Control */
#include <ros.h>
#include <man_ctrl/WheelRpm.h>

#include <Wire.h>

#define b1 15
#define b2 16
#define b3 17


int vel = 0, omega = 0;
int max_rpm = 30;

ros::NodeHandle nh;

man_ctrl::WheelRpm RoverRpm;

void loco(int address)
{

  Wire.beginTransmission(address);
  Wire.write(vel);
  Wire.write(omega);
  Wire.write(max_rpm);
  Wire.endTransmission();
}

void roverMotionCallback(const man_ctrl::WheelRpm& RoverRpm)
{
  vel = int(constrain(RoverRpm.vel, -150, 150));
  omega = int(constrain(RoverRpm.omega, -150, 150));
  max_rpm = RoverRpm.max_rpm;
  vel = map(vel, -max_rpm, max_rpm, 0, max_rpm);
  omega = map(omega, -max_rpm, max_rpm, 0, max_rpm);

  loco(b1);
  loco(b2);
  loco(b3);
}

ros::Subscriber<man_ctrl::WheelRpm> locomotion_sub("motion", &roverMotionCallback);

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
