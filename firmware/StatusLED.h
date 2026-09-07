#ifndef STATUSLED_H
#define STATUSLED_H

#include "Actuator.h"

class StatusLED : public Actuator {
private:
    bool flashing;
    unsigned long lastFlashTime;
    int flashInterval;

public:
    // Constructor
    StatusLED(String actuatorId, int pin, int cutOffMinutes);

    // Set LED states
    void setDisarmedColour();    // green on steady
    void setArmedColour();       // orange steady once fully armed
    void setAlarmColour();       // red flashing on alarm trigger

    // Turn LED off
    void turnOff();

    // Call in loop() to handle flashing
    void update();
};

#endif