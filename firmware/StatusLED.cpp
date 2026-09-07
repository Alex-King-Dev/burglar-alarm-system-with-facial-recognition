#include "StatusLED.h"

StatusLED::StatusLED(String actuatorId, int pin, int cutOffMinutes)
    : Actuator(actuatorId, pin, cutOffMinutes) {
    flashing = false;
    lastFlashTime = 0;
    flashInterval = 500;
}

void StatusLED::setDisarmedColour() {
    flashing = false;
    activate();
}

void StatusLED::setArmedColour() {
    flashing = false;
    activate();
}

void StatusLED::setAlarmColour() {
    flashing = true;
}

void StatusLED::turnOff() {
    flashing = false;
    deactivate();
}

void StatusLED::update() {
    if (!flashing) return;
    unsigned long now = millis();
    if (now - lastFlashTime >= flashInterval) {
        lastFlashTime = now;
        state = !state;
        if (state) {
            digitalWrite(pin, HIGH);
        } else {
            digitalWrite(pin, LOW);
        }
    }
}