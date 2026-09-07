#ifndef PANICBUTTON_H
#define PANICBUTTON_H

#include <Arduino.h>

class PanicButton {
private:
    bool pressed;
    int pin;

public:
    // Constructor method
    PanicButton(int p);

    // Check if the panic button has been pressed
    bool isTriggered(bool buttonPressed);

    // Reset the panic button state
    void reset();

    // Getters
    bool getPressed();
    int getPin();
};

#endif