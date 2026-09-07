#ifndef SOLENOIDLOCK_H
#define SOLENOIDLOCK_H

#include "Actuator.h"

class SolenoidLock : public Actuator {
private:
    bool locked;

public:
    // Constructor method
    SolenoidLock(String actuatorId, int pin, int cutOffMinutes);

    // Lock the solenoid
    void lock();

    // Unlock the solenoid
    void unlock();

    // Getter
    bool isLocked();
};

#endif