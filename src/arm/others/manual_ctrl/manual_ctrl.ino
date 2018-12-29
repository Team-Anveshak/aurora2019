#include<ros.h>
#include<arm/Pwm.h>

//2-ch Polulu on PCB
#define EN1 43
#define EN2 25
#define EN3 37
#define EN4 27
#define INA1 45
#define INA2 23
#define INA3 39
#define INA4 29
#define INB1 47
#define INB2 35
#define INB3 41
#define INB4 31
#define PWM1 8
#define PWM2 5
#define PWM3 7
#define PWM4 4

//2-ch Pololu on GCB
#define INA5 6  	//PWM_G
#define INA6 21 	//SCL
#define INB5 42		//DIR
#define INB6 20 	//SDA
#define PWM6 2 	//ENCA2
#define PWM5 3		//ENCA1



/*
// L293D
#define ENABLE 46
#define INPUT1 48
#define INPUT2 50

// RHINO Encoders
#define ENCA1 3
#define ENCA2 2

// 2-ch POLULO
#define PWM3 7
#define EN3 37
#define INA3 39
#define INB3 41
*/

bool dir[6] ={ false};
int pwm[6] ={0};
  
//----------|| 1-4 : grip , elbow , pitch , roll  ||------------
//----------|| 5,6 : base , shoulder ||----------

ros::NodeHandle nh;

void Set(const arm::Pwm& data)
{
 
  
  pwm[0] = data.grip;
  pwm[5] = data.shoulder;
  pwm[1] = data.elbow;
  pwm[2] = data.pitch;
  pwm[3] = data.roll;
  pwm[4] = data.base;
}

ros::Subscriber<arm::Pwm> sub1("set", Set );

void setup(){
  //Initialize pins
  pinMode(EN1, OUTPUT);
  pinMode(EN2, OUTPUT);
  pinMode(EN3, OUTPUT);
  pinMode(EN4, OUTPUT);
  
  pinMode(INA1, OUTPUT);
  pinMode(INA2, OUTPUT);
  pinMode(INA3, OUTPUT);
  pinMode(INA4, OUTPUT);
  pinMode(INA5, OUTPUT);
  pinMode(INA6, OUTPUT);
  
  pinMode(INB1, OUTPUT);
  pinMode(INB2, OUTPUT);
  pinMode(INB3, OUTPUT);
  pinMode(INB4, OUTPUT);
  pinMode(INB5, OUTPUT);
  pinMode(INB6, OUTPUT);
  
  pinMode(PWM1, OUTPUT);
  pinMode(PWM2, OUTPUT);
  pinMode(PWM3, OUTPUT);
  pinMode(PWM4, OUTPUT);
  pinMode(PWM5, OUTPUT);
  pinMode(PWM6, OUTPUT);
  
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);
  digitalWrite(EN3, HIGH);
  digitalWrite(EN4, HIGH);


  nh.initNode();
  nh.subscribe(sub1);
}


void loop(){
  nh.spinOnce();
  
  if (pwm[0] >0){
    digitalWrite(INA1,HIGH);
  digitalWrite(INB1,LOW);
  }else{
    digitalWrite(INB1,HIGH);
  digitalWrite(INA1,LOW);
  }
  analogWrite(PWM1,pwm[0]);
  
 if (pwm[1] >0){
    digitalWrite(INA2,HIGH);
  digitalWrite(INB2,LOW);
  }else{
    digitalWrite(INB2,HIGH);
  digitalWrite(INA2,LOW);
  }
  analogWrite(PWM2,pwm[1]);
  
  if (pwm[2] >0){
    digitalWrite(INA3,HIGH);
  digitalWrite(INB3,LOW);
  }else{
    digitalWrite(INB3,HIGH);
  digitalWrite(INA3,LOW);
  }
  analogWrite(PWM3,pwm[2]);
  
  if (pwm[3] >0){
    digitalWrite(INA4,HIGH);
  digitalWrite(INB4,LOW);
  }else{
    digitalWrite(INB4,HIGH);
  digitalWrite(INA4,LOW);
  }
  analogWrite(PWM4,pwm[3]);
  
 if (pwm[4] >0){
    digitalWrite(INA5,HIGH);
  digitalWrite(INB5,LOW);
  }else{
    digitalWrite(INB5,HIGH);
  digitalWrite(INA5,LOW);
  }
  analogWrite(PWM5,pwm[4]);
  
  if (pwm[5] >0){
    digitalWrite(INA6,HIGH);
  digitalWrite(INB6,LOW);
  }else{
    digitalWrite(INB6,HIGH);
  digitalWrite(INA6,LOW);
  }
  analogWrite(PWM6,pwm[5]);
}
