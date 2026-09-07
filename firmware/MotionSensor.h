#ifndef MOTIONSENSOR_H
#define MOTIONSENSOR_H

#include "Sensor.h"

class MotionSensor : public Sensor {
public:
    // Constructor method
    MotionSensor(String sensorId, int pin);

    // Override readState to avoid INPUT_PULLUP
    bool readState();

    // Check if motion is detected
    bool isTriggered();
};

#endif