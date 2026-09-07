#ifndef USERPROFILE_H
#define USERPROFILE_H

#include <Arduino.h>

class UserProfile {
protected:
    String userId;
    String name;
    int pin;
    String faceId;

public:
    // Constructor
    UserProfile(String id, String n, int p, String face);

    // Getters
    String getUserId();
};

#endif