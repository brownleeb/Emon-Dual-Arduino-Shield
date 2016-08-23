/*

  EmonTx CT123 Voltage Serial Only example

  Part of the openenergymonitor.org project
  Licence: GNU GPL V3

  Author: Trystan Lea
*/

#include "EmonLib.h"
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 4
#define TEMPERATURE_PRECISION 9

EnergyMonitor ct1;
const int LEDpin = 9;

OneWire oneWire(4);
DallasTemperature sensors(&oneWire);
//DeviceAddress address_T1 = { 0x28, 0xFF, 0xC9, 0x64, 0x15, 0x00, 0x03, 0x4E };
DeviceAddress address_T1;
int numberOfDevices;

void setup()
{
  Serial.begin(9600);
  // Calibration factor = CT ratio / burden resistance = (80A / 0.1A) / 33 Ohms = 24.24
  ct1.current(1, 23.695);

  // (ADC input, calibration, phase_shift)
  // ct1.voltage(0, 127.2, 1.7);  L2 - Furnace Outlet
  ct1.voltage(0, 127.3, 1.7);  //L1 - Panel Outlet
  // Setup indicator LED
  pinMode(LEDpin, OUTPUT);
  digitalWrite(LEDpin, HIGH);
  sensors.begin();
  
  numberOfDevices = sensors.getDeviceCount();
  for (int i = 0; i < numberOfDevices; i++)
  {
    if (sensors.getAddress(address_T1, i))
    {
      sensors.setResolution(address_T1, TEMPERATURE_PRECISION);
    }
  }
  while (millis() < 30000) {}
}

void loop()
{
  unsigned long start = millis();
  unsigned long finish = (((start + 30000) / 1000) * 1000);
  float myPower1 = 0.0;
  float myAPower1 = 0.0;
  float myPowerFactor1 = 0.0;
  float myVrms1 = 0.0;
  float myIrms1 = 0.0;
  float avgDenom = 0.0;
  int ct = 0;

  while (millis() < finish)
  {
    // Calculate all. No.of crossings, time-out
    ct1.calcVI(20, 2000);

    myPower1 += ct1.realPower;
    myAPower1 += ct1.apparentPower;
    myPowerFactor1 += ct1.powerFactor;
    myVrms1 += ct1.Vrms;
    myIrms1 += ct1.Irms;
    //Serial.println(ct1.Irms);

    ct++;
  }
  finish = millis();

  avgDenom = 0.004 * (finish - start);
  myPower1 = (myPower1 / ct) / avgDenom;
  myAPower1 = (myAPower1 / ct) / avgDenom;
  myPowerFactor1 = myPowerFactor1 / ct;
  myVrms1 = myVrms1 / ct;
  myIrms1 = myIrms1 / ct;
  sensors.requestTemperatures();
  double temperature = sensors.getTempC(address_T1);
  Serial.print(myPower1, 3);
  Serial.print(",");
  Serial.print(myAPower1, 3);
  Serial.print(",");
  Serial.print(myPowerFactor1, 5);
  Serial.print(",");
  Serial.print(myVrms1, 5);
  Serial.print(",");
  Serial.print(myIrms1, 5);
  Serial.print(",");
  Serial.print(ct);
  Serial.print(",");
  Serial.println(DallasTemperature::toFahrenheit(temperature),1);
}
