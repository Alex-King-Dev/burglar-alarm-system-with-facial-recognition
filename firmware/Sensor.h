#ifndef SENSOR_H
#define SENSOR_H

#include <Arduino.h>

class Sensor {
protected:
    String sensorId;
    bool state;
    int pin;

public:
    // Constructor method
    Sensor(String id, int p);

    // Read the current state of the sensor from its pin
    virtual bool readState();

    // Getters
    String getSensorId();
    bool getState();
};

#endif