#ifndef ACTUATOR_H
#define ACTUATOR_H

#include <Arduino.h>

class Actuator {
protected:
    String actuatorId;
    bool state;
    int pin;
    int cutOffMinutes;

public:
    // Constructor method
    Actuator(String actuatorID, int _pin, int cutOffMinutes);

    // Activate the actuator (virtual as buzzer overrides)
    virtual void activate();

    // Deactivate the actuator (virtual as buzzer overrides)
    virtual void deactivate();

    // Getters
    String getActuatorId();
    bool getState();
};

#endif
