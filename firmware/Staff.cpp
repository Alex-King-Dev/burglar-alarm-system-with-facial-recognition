#include "Staff.h"

Staff::Staff(String userId, String name, int pin, String faceId)
    : UserProfile(userId, name, pin, faceId) {
}

void Staff::armSystem(bool isAuthenticated) {
    if (isAuthenticated) {
        Serial.println("ARM_OK");
    } else {
        Serial.println("ARM_FAIL");
    }
}

void Staff::disarmSystem(bool isAuthenticated) {
    if (isAuthenticated) {
        Serial.println("DISARM_OK");
    } else {
        Serial.println("DISARM_FAIL");
    }
}