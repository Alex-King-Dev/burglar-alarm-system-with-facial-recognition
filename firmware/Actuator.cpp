#include "Actuator.h"

Actuator::Actuator(String actuatorID, int _pin, int cutOffMins) {
    actuatorId = actuatorID;
    pin = _pin;
    cutOffMinutes = cutOffMins;
    state = false;
    pinMode(pin, OUTPUT);
}

void Actuator::activate() {
    state = true;
    digitalWrite(pin, HIGH);
}

void Actuator::deactivate() {
    state = false;
    digitalWrite(pin, LOW);
}

String Actuator::getActuatorId() { return actuatorId; }
bool Actuator::getState() { return state; }
