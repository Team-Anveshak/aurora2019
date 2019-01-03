/* rosserial Subscriber For Locomotion Control */
#include <ros.h>
#include <man_ctrl/WheelRpm.h>
#include <sensors/PanTilt.h>

#include <Wire.h>
#include <Servo.h>

#define b1 15
#define b2 16
#define b3 17

Servo pan;
Servo tilt;

int vel = 0, omega = 0;
int max_rpm = 30;
int panAngle = 0;
int tiltAngle = 0;
int pan_pos = 10, tilt_pos = 10;
int servo_then;

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

void servoCallback(const sensors::PanTilt& Control)
{
  panAngle = Control.pan;
  tiltAngle = Control.tilt;
  pan.write(panAngle);
  tilt.write(tiltAngle);

  if (panAngle == 1) {
    if (abs(millis() - servo_then) > 100) {
      pan.write(pan_pos);
      if (pan_pos < 179) pan_pos++;
      servo_then = millis();
    }
  }
  else if (panAngle == -1) {
    if (abs(millis() - servo_then) > 100) {
      pan.write(pan_pos);
      if (pan_pos > 1) pan_pos--;
      servo_then = millis();
    }
  }
  if (tiltAngle == 1) {
    if (abs(millis() - servo_then) > 100) {
      tilt.write(tilt_pos);
      if (tilt_pos < 179) tilt_pos++;
      servo_then = millis();
    }
  }
  else if (tiltAngle == -1) {
    if (abs(millis() - servo_then) > 100) {
      tilt.write(tilt_pos);
      if (tilt_pos > 1) tilt_pos--;
      servo_then = millis();
    }
  }
}

ros::Subscriber<man_ctrl::WheelRpm> locomotion_sub("motion", &roverMotionCallback);
ros::Subscriber<sensors::PanTilt> pantilt_sub("pan_tilt_ctrl", &servoCallback);

void setup() {
  nh.initNode();
  nh.subscribe(locomotion_sub);
  nh.subscribe(pantilt_sub);
  Wire.begin();
  // nh.advertise(WheelVelocity);
  pan.attach(2);
  tilt.attach(3);

}

void loop() {

  nh.spinOnce();
  //delay(10);
}
