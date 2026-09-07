#include "AlarmControlPanel.h"
#include "Buzzer.h"
#include "SolenoidLock.h"
#include "StatusLED.h"
#include "SwitchSensor.h"
#include "MotionSensor.h"
#include "PanicButton.h"

AlarmControlPanel panel("PANEL_01", 10);

Buzzer buzzer("BUZZER_01", 5, 1, 1000);
SolenoidLock solenoid("LOCK_01", 7, 0);

StatusLED ledGreen1("LED_GREEN_1", 53, 0);
StatusLED ledGreen2("LED_GREEN_2", 49, 0);
StatusLED ledYellow1("LED_YELLOW_1", 47, 0);
StatusLED ledYellow2("LED_YELLOW_2", 51, 0);
StatusLED ledRed1("LED_RED_1", 43, 0);
StatusLED ledRed2("LED_RED_2", 45, 0);
StatusLED ledRed3("LED_RED_3", 41, 0);

SwitchSensor doorSensor("DOOR_01", 17);
MotionSensor motionSensor("MOTION_01", 6);
PanicButton panicButton(10);

bool systemReady = false;
bool armingDelayDone = false;
bool alarmActive = false;

void allLedsOff() {
    ledGreen1.turnOff(); ledGreen2.turnOff();
    ledYellow1.turnOff(); ledYellow2.turnOff();
    ledRed1.turnOff(); ledRed2.turnOff(); ledRed3.turnOff();
}

void setDisarmed() {
    allLedsOff();
    ledGreen1.setDisarmedColour();
    ledGreen2.setDisarmedColour();
}

void setArmed() {
    allLedsOff();
    ledYellow1.setArmedColour();
    ledYellow2.setArmedColour();
}

void setAlarmTriggered() {
    allLedsOff();
    ledRed1.setAlarmColour();
    ledRed2.setAlarmColour();
}

void setPanicTriggered() {
    allLedsOff();
    ledRed1.setAlarmColour();
    ledRed2.setAlarmColour();
    ledRed3.setAlarmColour();
}

void setup() {
    Serial.begin(9600);
    delay(1000);

    //oobjects in as pointer parameters so that they can be added to
    panel.addActuator(&buzzer);
    panel.addActuator(&solenoid);

    panel.addDisplayActuator(&ledGreen1);
    panel.addDisplayActuator(&ledGreen2);
    panel.addDisplayActuator(&ledYellow1);
    panel.addDisplayActuator(&ledYellow2);
    panel.addDisplayActuator(&ledRed1);
    panel.addDisplayActuator(&ledRed2);
    panel.addDisplayActuator(&ledRed3);

    panel.addSensor(&doorSensor);
    panel.addSensor(&motionSensor);
    
    panel.setPanicButton(&panicButton);

    setDisarmed();
    Serial.println("ARDUINO_READY");
    delay(1000);
}

void loop() {
    ledYellow1.update();
    ledYellow2.update();
    ledRed1.update();
    ledRed2.update();
    ledRed3.update();

    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        if (command.length() > 0) {
            if (command == "READY_ACK") {
                systemReady = true;
                Serial.println("SYSTEM_READY");
            } else if (command == "ARM") {
                panel.handleSerialCommand(command);
                armingDelayDone = false;
                alarmActive = false;
                setArmed();
            } else if (command == "DISARM") {
                panel.handleSerialCommand(command);
                armingDelayDone = false;
                alarmActive = false;
                setDisarmed();
            } else {
                panel.handleSerialCommand(command);
            }
        }
    }

    if (!systemReady) return;

    if (panel.getState() && !armingDelayDone && panel.sensorsReady()) {
        armingDelayDone = true;
        setArmed();
    }

    if (panel.getState() && armingDelayDone && !alarmActive) {
        bool doorTriggered = doorSensor.isTriggered();
        bool motionTriggered = motionSensor.isTriggered();

        if (doorTriggered || motionTriggered) {
            alarmActive = true;
            if (doorTriggered) Serial.println("TRIGGER:SWITCH:DOOR_01");
            if (motionTriggered) Serial.println("TRIGGER:MOTION:MOTION_01");
            panel.triggerAlarmActuators();
            setAlarmTriggered();
        }
    }

    if (!alarmActive && panicButton.isTriggered(digitalRead(panicButton.getPin()) == LOW)) {
        alarmActive = true;
        Serial.println("TRIGGER:PANIC:PANIC_BTN");
        panel.triggerAlarmActuators();
        setPanicTriggered();
    }

}