/******************************************************************************
  SparkFun Easy Driver Basic Demo
  Toni Klopfenstein @ SparkFun Electronics
  March 2015
  https://github.com/sparkfun/Easy_Driver

  Simple demo sketch to demonstrate how 5 digital pins can drive a bipolar stepper motor,
  using the Easy Driver (https://www.sparkfun.com/products/12779). Also shows the ability to change
  microstep size, and direction of motor movement.

  Development environment specifics:
  Written in Arduino 1.6.0

  This code is beerware; if you see me (or any other SparkFun employee) at the local, and you've found our code helpful, please buy us a round!
  Distributed as-is; no warranty is given.

  Example based off of demos by Brian Schmalz (designer of the Easy Driver).
  http://www.schmalzhaus.com/EasyDriver/Examples/EasyDriverExamples.html
******************************************************************************/
//Declare pin functions on Redboard
#include <Servo.h>
#include <Wire_slave.h>
HardwareTimer timer(1);
/////

int address = 15;   //change address here 15,16,17

/////

#define stp PA7
#define dir PB10
#define MS1 PA6
#define MS2 PA3
#define EN  PA2
#define SOL1 PB5
#define SOL2 PA8
#define NWIRE PA4

//Declare variables for functions
char user_input;
int x;
int y;
int state;
Servo SciServo;

int steps = 0, period = 0;
float spd = 0;
int sol1 = 0;
int sol2 = 0;
int nwire = 0;
int servo = 0;

void receiveEvent(int howMany)
{
  if ( Wire.available())
  {
    steps = Wire.read();
    //spd = Wire.read();
    period = Wire.read();
    sol1 = Wire.read();
    sol2 = Wire.read();
    nwire = Wire.read();
    servo = Wire.read();
  }
}


void setup() {
  timer.setPrescaleFactor(6);
  timer.setOverflow(240);
  pinMode(stp, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(EN, OUTPUT);
  pinMode(SOL1, OUTPUT);
  pinMode(SOL2, OUTPUT);
  pinMode(NWIRE, OUTPUT);
  pinMode(PB4,INPUT);
  pinMode(PA10, OUTPUT);
  digitalWrite(PA10, LOW);
  SciServo.attach(PB11);
  resetEDPins(); //Set step, direction, microstep and enable pins to default states
  Wire.begin(address);

  Wire.onReceive(receiveEvent);

}

//Main loop
void loop() {
  digitalWrite(EN, LOW); //Pull enable pin low to allow motor control
  ForwardBackwardStep();
}

//Reset Easy Driver pins to default states
void resetEDPins()
{
  digitalWrite(stp, LOW);
  digitalWrite(dir, LOW);
  digitalWrite(MS1, LOW);
  digitalWrite(MS2, LOW);
  digitalWrite(EN, HIGH);
}

//Forward/reverse stepping function
void ForwardBackwardStep()
{
  if (steps == 1)
  {
    digitalWrite(dir, LOW);
    if (period == 1)
    {
      digitalWrite(stp, HIGH); //Trigger one step
    }
    if (period == 0)
    {
      digitalWrite(stp, LOW); //Pull step pin low so it can be triggered again
    }
  }
  if (steps == 2)
  {
    digitalWrite(dir, HIGH);
    if (period == 1)
    {
      digitalWrite(stp, HIGH); //Trigger one step
    }
    if (period == 0)
    {
      digitalWrite(stp, LOW); //Pull step pin low so it can be triggered again
    }
  }
    if (sol1 == 1)
      digitalWrite(SOL1, HIGH);
    if (sol1 == 0)
      digitalWrite(SOL1, LOW);
    if (sol2 == 1)
      digitalWrite(SOL2, HIGH);
    if (sol2 == 0)
      digitalWrite(SOL2, LOW);
  if (nwire == 1)
      digitalWrite(NWIRE,HIGH);
  if (nwire == 0)
       digitalWrite(NWIRE,LOW);
     if(servo==1)
        SciServo.write(180);

}
