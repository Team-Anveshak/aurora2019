void loco(int address)
{

  Wire.beginTransmission(address);
  Wire.write(rpm);
  Wire.write(dir);
  Wire.write(mod);
  Wire.endTransmission();
  delay(50);

}

void coreZeroTask(void * pvParameters)
{
  loco(b1);
  loco(b2);
  loco(b3);
}

