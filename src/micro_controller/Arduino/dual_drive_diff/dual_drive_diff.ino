/* rosserial Subscriber For Locomotion Control */
#include <ros.h>
#include <rover_msgs/Wheel_rpm.h>

#include <Wire.h>

#define b1 15
#define b2 16
#define b3 17


int forward = 0, rotate = 0;
int max_rpm = 30;

ros::NodeHandle nh;

rover_msgs::Wheel_rpm RoverRpm;

void loco(int address)
{
 
  Wire.beginTransmission(address);
  Wire.write(forward);
  Wire.write(rotate);
  Wire.write(max_rpm); 
  Wire.endTransmission();
  
}

void roverMotionCallback(const rover_msgs::Wheel_rpm& RoverRpm)
{
  forward = int(constrain(RoverRpm.forward,-150,150));
  rotate = int(constrain(RoverRpm.rotate,-150,150));
  max_rpm= RoverRpm.max_rpm; 
  forward = map(forward,-max_rpm,max_rpm, 0, max_rpm);
  rotate = map(rotate,-max_rpm,max_rpm, 0, max_rpm);
}
 
ros::Subscriber<rover_msgs::Wheel_rpm> locomotion_sub("loco/wheel_rpm", &roverMotionCallback); 
 
 void setup(){
    nh.initNode();
    nh.subscribe(locomotion_sub);
    Wire.begin();
   // nh.advertise(WheelVelocity);
   
 }
 
 void loop(){
    loco(b1);
    loco(b2);
    loco(b3);
    nh.spinOnce();
    delay(10);
}
