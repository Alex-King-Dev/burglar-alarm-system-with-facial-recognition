#ifndef SWITCHSENSOR_H
#define SWITCHSENSOR_H

#include "Sensor.h"

class SwitchSensor : public Sensor {
public:
    // Constructor
    SwitchSensor(String sensorId, int pin);

    // Check if door or window is triggered
    bool isTriggered();
};

#endif