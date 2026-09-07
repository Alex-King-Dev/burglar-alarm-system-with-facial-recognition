#ifndef BUZZER_H
#define BUZZER_H

#include "Actuator.h"

class Buzzer : public Actuator {
private:
    bool sounding;
    int frequency;

public:
    // constructor method
    Buzzer(String actuatorId, int pin, int cutOffMinutes, int Frequency);

    // Override activate and deactivate to use tone/noTone
    void activate() override;
    void deactivate() override;

    // Getter
    bool isSounding();
};

#endif