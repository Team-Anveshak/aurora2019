HardwareTimer timer(3);

#include <Wire_slave.h>

/////

int address = 16;   //change address here 15,16,17

/////


#define CSr PA2
#define CSl PA3
#define slpr PA4
#define slpl PA5
#define DIRr PA6
#define DIRl PA7
#define PWMr PB0
#define PWMl PB1

volatile int forward = 0, rotate = 0, f = 0, r = 0;
volatile int max_rpm = 30;
int pwmr = 0, pwml = 0;

void receiveEvent(int howMany)
{
  if ( Wire.available())
  {
    f = Wire.read();
    r = Wire.read();
    max_rpm = Wire.read();
    forward = map(f, 0, max_rpm, -max_rpm, max_rpm);
    rotate = map(r, 0, max_rpm, -max_rpm, max_rpm);
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

  pwmr = int(constrain(1.438 * (forward + rotate), -255, 255));
  pwml = int(constrain(1.438 * (forward - rotate), -255, 255));
  if (pwmr >= 0)
  {
    digitalWrite(DIRr, HIGH);
    pwmWrite(PWMr, abs(pwmr));

  }

  else
  {
    digitalWrite(DIRr, LOW);
    pwmWrite(PWMr, abs(pwmr));

  }

  if (pwml >= 0)
  {
    digitalWrite(DIRl, LOW);
    pwmWrite(PWMl, abs(pwml));
  }

  else
  {
    digitalWrite(DIRl, HIGH);

    pwmWrite(PWMl, abs(pwml));
  }
}

