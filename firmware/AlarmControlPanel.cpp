#include "AlarmControlPanel.h"

AlarmControlPanel::AlarmControlPanel(String id, int delaySeconds) {
    systemId = id;
    state = false;
    armTime = 0;
    sensorDelaySeconds = delaySeconds;
    sensorCount = 0;
    actuatorCount = 0;
    displayActuatorCount = 0;
    panicButton = nullptr; //c++ version of NULL essentually
}

bool AlarmControlPanel::sensorsReady() {
    if (!state) return false;
    unsigned long delay = sensorDelaySeconds * 1000;
    //count updates down in serial handling method (starting at zero)
    return (millis() - armTime) >= delay;
}

void AlarmControlPanel::triggerAlarmActuators() {
    for (int i = 0; i < actuatorCount; i++) {
        actuators[i]->activate();
    }
}

void AlarmControlPanel::alarmCutOff() {
    for (int i = 0; i < actuatorCount; i++) {
        actuators[i]->deactivate();
    }
    if (panicButton != nullptr) {
        panicButton->reset();
    }
    Serial.println("ALARM_CUTOFF");
}

void AlarmControlPanel::addActuator(Actuator* actuator) {
    if (actuatorCount < MAX_ACTUATORS) {
        actuators[actuatorCount++] = actuator;
    }
}

void AlarmControlPanel::addDisplayActuator(Actuator* actuator) {
    if (displayActuatorCount < MAX_DISPLAY_ACTUATORS) {
        displayActuators[displayActuatorCount++] = actuator;
    }
}

void AlarmControlPanel::addSensor(Sensor* sensor) {
    if (sensorCount < MAX_SENSORS) {
        sensors[sensorCount++] = sensor;
    }
}

void AlarmControlPanel::setPanicButton(PanicButton* button) {
    panicButton = button;
}


//MAIN SERIAL CONNECTION CODE!
void AlarmControlPanel::handleSerialCommand(String command) {

    if (command == "ARM") {
        state = true;
        armTime = millis();
        Serial.println("ARM_OK");

    } else if (command == "DISARM") {
        state = false;
        alarmCutOff();
        Serial.println("DISARM_OK");

    } else if (command == "GET_STATUS") {
        if (state == true) {
            Serial.println("STATUS:ARMED");
        } else {
            Serial.println("STATUS:DISARMED");
        }

    } else if (command == "GET_SENSORS") {
        String response = "SENSORS:";
        for (int i = 0; i < sensorCount; i++) {
            String sensorState;
            if (sensors[i]->getState()) {
                sensorState = "1";
            } else {
                sensorState = "0";
            }
            response += sensors[i]->getSensorId() + ":" + sensorState;
            if (i < sensorCount - 1) {
                response += ",";
            }
        }
        if (panicButton != nullptr) {
            if (sensorCount > 0) {
                response += ",";
            }
            String panicState;
            if (panicButton->getPressed()) {
                panicState = "1";
            } else {
                panicState = "0";
            }
            response += "PANIC_BUTTON:" + panicState;
        }
        Serial.println(response);

    } else if (command == "GET_ACTUATORS") {
        String response = "ACTUATORS:";
        for (int i = 0; i < actuatorCount; i++) {
            String actuatorState;
            if (actuators[i]->getState()) {
                actuatorState = "1";
            } else {
                actuatorState = "0";
            }
            response += actuators[i]->getActuatorId() + ":" + actuatorState;
            if (i < actuatorCount - 1 || displayActuatorCount > 0) {
                response += ",";
            }
        }
        for (int i = 0; i < displayActuatorCount; i++) {
            String displayState;
            if (displayActuators[i]->getState()) {
                displayState = "1";
            } else {
                displayState = "0";
            }
            response += displayActuators[i]->getActuatorId() + ":" + displayState;
            if (i < displayActuatorCount - 1) {
                response += ",";
            }
        }
        Serial.println(response);

    } else if (command == "ALARM_CUTOFF") {
        alarmCutOff();

    } else {
        Serial.println("ERROR:UNKNOWN_CMD");
    }
}

bool AlarmControlPanel::getState() { return state; }
String AlarmControlPanel::getSystemId() { return systemId; }