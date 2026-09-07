#include "Admin.h"

Admin::Admin(String userId, String name, int pin, String faceId)
    : Staff(userId, name, pin, faceId) {
}

void Admin::changeUserPin(int newUserPin) {
    Serial.println("CHANGE_OK");
}

void Admin::addUser(String userId, String name, int pin, String faceId) {
    Serial.println("ADD_OK:" + userId + ":" + name);
}

void Admin::deleteUser(String userId) {
    Serial.println("DELETE_OK:" + userId);
}

void Admin::armSystem(bool isAuthenticated) {
    if (isAuthenticated) {
        Serial.println("ARM_OK");
        Serial.println("LOG:ADMIN_ARM:" + userId);
    } else {
        Serial.println("ARM_FAIL");
    }
}

void Admin::disarmSystem(bool isAuthenticated) {
    if (isAuthenticated) {
        Serial.println("DISARM_OK");
        Serial.println("LOG:ADMIN_DISARM:" + userId);
    } else {
        Serial.println("DISARM_FAIL");
    }
}