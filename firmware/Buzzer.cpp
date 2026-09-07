#include "Buzzer.h"

Buzzer::Buzzer(String actuatorId, int pin, int cutOffMinutes, int Frequency)
    : Actuator(actuatorId, pin, cutOffMinutes) {
    sounding = false;
    frequency = Frequency;
}

void Buzzer::activate() {
    // Use tone() instead of digitalWrite to sound the buzzer
    state = true;
    tone(pin, frequency);
    Serial.println("ACTUATOR_ON:" + actuatorId);
}

void Buzzer::deactivate() {
    // Use noTone() to turn off  buzzer
    state = false;
    noTone(pin);
    Serial.println("ACTUATOR_OFF:" + actuatorId);
}

bool Buzzer::isSounding() { return sounding; }