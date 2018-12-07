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

int forward = 0,rotate = 0;
int max_rpm = 30;
int pwm = 0;

void receiveEvent(int howMany)
{
  if( Wire.available())
  {
    forward = Wire.read();
    rotate  = Wire.read();
    max_rpm = Wire.read();
    forward = map(forward,0, max_rpm, -max_rpm, max_rpm);
    rotate = map(rotate,0, max_rpm, -max_rpm, max_rpm);
  }
}

void setup() 
{
  timer.setPrescaleFactor(6);
  timer.setOverflow(240);
  pinMode(PWMl,PWM);
  pinMode(PWMr,PWM); 
  pinMode(slpl,OUTPUT);
  pinMode(slpr,OUTPUT);
  pinMode(DIRr,OUTPUT);
  pinMode(DIRl,OUTPUT);
  pinMode(CSr,INPUT);
  pinMode(CSl,INPUT);
  
  digitalWrite(slpl,HIGH);
  digitalWrite(slpr,HIGH);

 
  Wire.begin(address);  

  Wire.onReceive(receiveEvent); 
     
}

void loop() 
{  

  if (abs(forward)>5)
  {
    pwm = int(constrain(1.438*abs(forward),-255,255));
    
    if(forward>0)
    {
      digitalWrite(DIRr,HIGH);
      digitalWrite(DIRl,HIGH);
      pwmWrite(PWMr,pwm);
      pwmWrite(PWMl,pwm);
    }

    else
    {
      digitalWrite(DIRr,LOW);
      digitalWrite(DIRl,LOW);
      pwmWrite(PWMr,pwm);
      pwmWrite(PWMl,pwm);

    }
  }
  if (abs(rotate)>5)
  {
    pwm = int(constrain(1.438*abs(rotate),-255,255));
    
    if(rotate>0)
    {
      digitalWrite(DIRr,LOW);
      digitalWrite(DIRl,HIGH);
      pwmWrite(PWMr,pwm);
      pwmWrite(PWMl,pwm);
    }

    else
    {
      digitalWrite(DIRr,HIGH);
      digitalWrite(DIRl,LOW);
      pwmWrite(PWMr,pwm);
      pwmWrite(PWMl,pwm);
    }
  }
}
