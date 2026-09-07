#ifndef STAFF_H
#define STAFF_H

#include "UserProfile.h"

class Staff : public UserProfile {
public:
    // Constructor method
    Staff(String userId, String name, int pin, String faceId);

    // Arm the alarm system if authenticated
    void armSystem(bool isAuthenticated);

    // Disarm the alarm system if authenticated
    void disarmSystem(bool isAuthenticated);
};

#endif