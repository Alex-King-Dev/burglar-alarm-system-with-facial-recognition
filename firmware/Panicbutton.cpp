#include "PanicButton.h"

PanicButton::PanicButton(int p) {
    pin = p;
    pressed = false;
    pinMode(p, INPUT_PULLUP);
}

bool PanicButton::isTriggered(bool buttonPressed) {
    pressed = buttonPressed;
    return buttonPressed;
}

void PanicButton::reset() {
    pressed = false;
}

bool PanicButton::getPressed() { return pressed; }
int PanicButton::getPin() { return pin; }