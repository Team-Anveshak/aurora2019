HardwareTimer timer(1);


//Declare pin functions on Redboard
#include <ros.h>
#include <science/Science.h>
//HardwareTimer timer(1);

#define stp1 PA7
#define stp2 PB9
#define dir1 PB10
#define dir2 PB15
#define MS1 PA1
#define MS2 PA3
#define EN  PA2
/*
  #define SOL1 PB5
  #define SOL2 PA8
  #define NWIRE PA4
*/

#define SER1 PA10
#define SER2 PA8

//Declare variables for functions
char user_input;
int x;
int y;
int state;

int steps1 = 0, steps2 = 0, period1 = 0, period2 = 0;
float sol1 = 80;
float sol2 = 0;

ros::NodeHandle nh;

science::Science RoverSci;

void roverMotionCallback(const science::Science& RoverSci)
{
  steps1 = RoverSci.steps1;
  steps2 = RoverSci.steps2;
  period1 = RoverSci.period1;
  period2 = RoverSci.period2;
  sol1 = RoverSci.sol1;
  sol2 = RoverSci.sol2;

}

ros::Subscriber<science::Science> locomotion_sub("Science_data", &roverMotionCallback);

void setup() {
  timer.setPeriod(20000);
  pinMode(stp1, OUTPUT);
  pinMode(stp2, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(EN, OUTPUT);

  pinMode(SER1, PWM);
  pinMode(SER2, PWM);

  

  resetEDPins(); //Set step, direction, microstep and enable pins to default states
  nh.initNode();
  nh.subscribe(locomotion_sub);
}

//Main loop
void loop() {
  digitalWrite(EN, LOW); //Pull enable pin low to allow motor control
  ForwardBackwardStep();
  nh.spinOnce();
}

//Reset Easy Driver pins to default states
void resetEDPins()
{
  digitalWrite(stp1, LOW);
    digitalWrite(stp2, LOW);
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, LOW);
  digitalWrite(MS1, LOW);
  digitalWrite(MS2, LOW);
  digitalWrite(EN, HIGH);
}

//Forward/reverse stepping function
void ForwardBackwardStep()
{
  if (steps1 == 1)
  {
    digitalWrite(dir1, LOW);
    if (period1 == 1)
    {
      digitalWrite(stp1, HIGH); //Trigger one step
    }
    if (period1 == 0)
    {
      digitalWrite(stp1, LOW); //Pull step pin low so it can be triggered again
    }
  }
  if (steps1 == -1)
  {
    digitalWrite(dir1, HIGH);
    if (period1 == 1)
    {
      digitalWrite(stp1, HIGH); //Trigger one step
    }
    if (period1 == 0)
    {
      digitalWrite(stp1, LOW); //Pull step pin low so it can be triggered again
    }
  }
  if (steps2 == 1)
  {
    digitalWrite(dir2, LOW);
    if (period2 == 1)
    {
      digitalWrite(stp2, HIGH); //Trigger one step
    }
    if (period2 == 0)
    {
      digitalWrite(stp2, LOW); //Pull step pin low so it can be triggered again
    }
  }
  if (steps2 == -1)
  {
    digitalWrite(dir2, HIGH);
    if (period2 == 1)
    {
      digitalWrite(stp2, HIGH); //Trigger one step
    }
    if (period2 == 0)
    {
      digitalWrite(stp2, LOW); //Pull step pin low so it can be triggered again
    }
  }
  pwmWrite(SER1, sol1);
  pwmWrite(SER2, sol2);

}
