#include "SwitchSensor.h"

SwitchSensor::SwitchSensor(String sensorId, int pin)
    : Sensor(sensorId, pin) {
    pinMode(pin, INPUT_PULLUP);
}

bool SwitchSensor::isTriggered() {
    return digitalRead(pin) == 1;
}