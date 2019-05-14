/* rosserial Subscriber For Locomotion Control */
HardwareTimer timer(3);

#include <ros.h>
#include <man_ctrl/WheelRpm.h>
#include <sensors/PanTilt.h>

#include <Wire.h>
#include <Servo.h>

#define b1 15
#define b2 16
#define b3 17
#define b4 20

#define relay PA1
#define PAN PA6
#define TILT PA7

int vel = 0, omega = 0;
int max_rpm = 30;
int panAngle = 0;
int tiltAngle = 0;
int pan_pos = 10, tilt_pos = 10;
double panPwm, tiltPwm = 0.0;
 
ros::NodeHandle nh;

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
  loco(b4);
}

void servoCallback(const sensors::PanTilt& Control)
{
  digitalWrite(relay,Control.rel);
  
  panPwm = Control.pan;
  tiltPwm = Control.tilt;
  pwmWrite(PAN,int(panPwm));
  pwmWrite(TILT,int(tiltPwm));
}

ros::Subscriber<man_ctrl::WheelRpm> locomotion_sub("motion", &roverMotionCallback);
ros::Subscriber<sensors::PanTilt> pantilt_sub("pan_tilt_ctrl", &servoCallback);

void setup() {
  nh.initNode();
  nh.subscribe(locomotion_sub);
  nh.subscribe(pantilt_sub);
  Wire.begin();
  pinMode(relay,OUTPUT);
  timer.setPeriod(20000);
  pinMode(PAN,PWM);
  pinMode(TILT,PWM);

}

void loop() {

  nh.spinOnce();
  //delay(10);
}
