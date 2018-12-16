HardwareTimer timer(3);

#include <Wire_slave.h>

/////

int address = 15;   //change address here 15,16,17

/////


#define CSr PA2
#define CSl PA3
#define slpr PA4
#define slpl PA5
#define DIRr PA6
#define DIRl PA7
#define PWMr PB0
#define PWMl PB1

volatile int rpm = 0, dir = 0, mode = 0;
int pwm = 0;

void receiveEvent(int howMany)
{
  if ( Wire.available())
  {
    rpm = Wire.read();
    dir  = Wire.read();
    mode = Wire.read();

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
  pwm = int(constrain(1.438 * abs(rpm), -255, 255));
  if (mode == 0)
  {

    switch (dir)
    { case 0:
        {
          digitalWrite(DIRr, HIGH);
          digitalWrite(DIRl, LOW);
          pwmWrite(PWMr, pwm);
          pwmWrite(PWMl, pwm);
          break;;
        }

      case 1:
        {
          digitalWrite(DIRr, LOW);
          digitalWrite(DIRl, HIGH);
          pwmWrite(PWMr, pwm);
          pwmWrite(PWMl, pwm);
          break;
        }

      default:
        {
          pwmWrite(PWMr, 0);
          pwmWrite(PWMl, 0);
          break;
        }
    }
  }


  else if (mode == 1)
  {

    switch (dir)
    { case 0:
        {
          digitalWrite(DIRr, HIGH);
          digitalWrite(DIRl, HIGH);
          pwmWrite(PWMr, pwm);
          pwmWrite(PWMl, pwm);
          break;;
        }

      case 1:
        {
          digitalWrite(DIRr, LOW);
          digitalWrite(DIRl, LOW);
          pwmWrite(PWMr, pwm);
          pwmWrite(PWMl, pwm);
          break;
        }

      default:
        {
          pwmWrite(PWMr, 0);
          pwmWrite(PWMl, 0);
          break;
        }
    }
  }

  else
  {
    pwmWrite(PWMr, 0);
    pwmWrite(PWMl, 0);
  }
}
