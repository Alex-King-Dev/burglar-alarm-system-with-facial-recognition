#ifndef ALARMCONTROLPANEL_H
#define ALARMCONTROLPANEL_H

#include <Arduino.h>
#include "Sensor.h"
#include "Actuator.h"
#include "PanicButton.h"

//array size values
#define MAX_SENSORS 10
#define MAX_ACTUATORS 10
#define MAX_DISPLAY_ACTUATORS 10

class AlarmControlPanel {
private:
    String systemId;
    bool state;
    unsigned long armTime;
    int sensorDelaySeconds;
    int sensorCount;
    int actuatorCount;
    int displayActuatorCount;
    
    //arrays
    Sensor* sensors[MAX_SENSORS];
    Actuator* actuators[MAX_ACTUATORS];
    Actuator* displayActuators[MAX_DISPLAY_ACTUATORS];
    PanicButton* panicButton;

public:
    // Constructor method
    AlarmControlPanel(String id, int delaySeconds);

    // Check sensor are ready after 10 second arming delay
    bool sensorsReady();

    // Trigger alarm actuators only (buzzer, solenoid) except LEDs
    void triggerAlarmActuators();

    // Cut off all alarm actuators and reset panic button state after 20 mins
    void alarmCutOff();

    // Add alarm actuator (buzzer, solenoid) to actuator array during ssetup
    void addActuator(Actuator* actuator);

    // Add  display actuator (LEDs) to array during setup
    void addDisplayActuator(Actuator* actuator);

    // Add sensors to the sensor array during setup
    void addSensor(Sensor* sensor);

    // Set panic button so alarmCutOff can reset it
    void setPanicButton(PanicButton* button);

    // Handle serial commands from Python
    void handleSerialCommand(String command);

    // Getters
    bool getState();
    String getSystemId();
};

#endif