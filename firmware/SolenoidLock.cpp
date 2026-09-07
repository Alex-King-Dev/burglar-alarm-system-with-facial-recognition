#include "SolenoidLock.h"

SolenoidLock::SolenoidLock(String actuatorId, int pin, int cutOffMinutes)
    : Actuator(actuatorId, pin, cutOffMinutes) {
    locked = true;
}

void SolenoidLock::lock() {
    locked = true;
    activate();
    Serial.println("LOCK_LOCKED:" + actuatorId);
}

void SolenoidLock::unlock() {
    locked = false;
    deactivate();
    Serial.println("LOCK_UNLOCKED:" + actuatorId);
}

bool SolenoidLock::isLocked() { return locked; }