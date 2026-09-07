#include "Sensor.h"

Sensor::Sensor(String id, int p) {
    sensorId = id;
    pin = p;
    state = false;
    pinMode(p, INPUT_PULLUP);
}

bool Sensor::readState() {
    // invert the low reading on the most part (for door and window etc, motion overrides)
    state = !digitalRead(pin);
    return state;
}

String Sensor::getSensorId() { return sensorId; }
bool Sensor::getState() { return state; }