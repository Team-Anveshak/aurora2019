HardwareTimer timer(3);

#include <Wire_slave.h>

/////

int address = 17;   //change address here 15,16,17

/////


#define CSr PA2
#define CSl PA3
#define slpr PA4
#define slpl PA5
#define DIRr PA6
#define DIRl PA7
#define PWMr PB0
#define PWMl PB1

int vel = 0, omega = 0;
float ang_vel = 0;
int max_rpm = 30;
int pwmr = 0, pwml = 0;

void receiveEvent(int howMany)
{
  if ( Wire.available())
  {
    vel = Wire.read();
    omega = Wire.read();
    max_rpm = Wire.read();
    vel = map(vel, 0, max_rpm, -max_rpm, max_rpm);
    omega = map(omega , 0, max_rpm, -max_rpm, max_rpm);
    ang_vel = omega * 3.06;
  }
}

void setup()
{
  timer.setPrescaleFactor(6);
  timer.setOverflow(240);
  pinMode(PWMl, PWM);
  pinMode(PWMr, PWM);
  pinMode(slpl, OUTPUT);
  pinMode(slpr, OUTPUT);
  pinMode(DIRr, OUTPUT);
  pinMode(DIRl, OUTPUT);
  pinMode(CSr, INPUT);
  pinMode(CSl, INPUT);

  digitalWrite(slpl, HIGH);
  digitalWrite(slpr, HIGH);


  Wire.begin(address);

  Wire.onReceive(receiveEvent);

}

void loop()
{

  pwmr = int(constrain(1.438 * (float(vel) + ang_vel), -255, 255));
  pwml = int(constrain(1.438 * (float(vel) - ang_vel), -255, 255));
  if (pwmr > 0)
  {
    digitalWrite(slpr, HIGH);
    digitalWrite(DIRr, HIGH);
    pwmWrite(PWMr, abs(pwmr));

  }

  else if (pwmr < 0)
  {
    digitalWrite(slpr, HIGH);
    digitalWrite(DIRr, LOW);
    pwmWrite(PWMr, abs(pwmr));

  }

  else
  {
    digitalWrite(slpr, LOW);
    pwmWrite(PWMr, 0);
  }

  if (pwml > 0)
  {
    digitalWrite(slpl, HIGH);
    digitalWrite(DIRl, LOW);
    pwmWrite(PWMl, abs(pwml));
  }

  else if (pwml < 0)
  {
    digitalWrite(slpl, HIGH);
    digitalWrite(DIRl, HIGH);
    pwmWrite(PWMl, abs(pwml));
  }
  else
  {
    digitalWrite(slpl, LOW);
    pwmWrite(PWMl, 0);
  }
}


