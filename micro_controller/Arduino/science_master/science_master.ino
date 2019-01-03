#include <ros.h>
#include <science/Science.h>

#include <Wire.h>
#include <Servo.h>

#define b1 15

int steps = 0, period = 0;
float spd = 0;
int sol1 = 0;
int sol2 = 0;
int nwire = 0;
int servo = 0;

ros::NodeHandle nh;

science::Science RoverSci;

void loco(int address)
{

  Wire.beginTransmission(address);
  Wire.write(steps);
//  Wire.write(spd);
  Wire.write(period);
  Wire.write(sol1);
  Wire.write(sol2);
  Wire.write(nwire);
  Wire.write(servo);
  Wire.endTransmission();
}

void roverMotionCallback(const science::Science& RoverSci)
{
  steps = RoverSci.steps;
  //spd = RoverSci.spd;
  period = RoverSci.period;
  sol1 = RoverSci.sol1;
  sol2 = RoverSci.sol2;
  nwire = RoverSci.nwire;
  servo = RoverSci.servo;
  loco(b1);
}

ros::Subscriber<science::Science> locomotion_sub("Science_data", &roverMotionCallback);

void setup() {
  nh.initNode();
  nh.subscribe(locomotion_sub);
  Wire.begin();

}

void loop() {

  nh.spinOnce();
  //delay(10);
}
