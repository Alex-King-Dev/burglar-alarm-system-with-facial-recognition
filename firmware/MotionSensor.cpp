#include "MotionSensor.h"

MotionSensor::MotionSensor(String sensorId, int pin)
    : Sensor(sensorId, pin) {
    pinMode(pin, INPUT);
}

// overrides sensor parent class readState() as that inverts for INPUT_PULLUP
bool MotionSensor::readState() {
    state = (digitalRead(pin) == HIGH);
    return state;
}

bool MotionSensor::isTriggered() {
    return (digitalRead(pin) == HIGH);
}