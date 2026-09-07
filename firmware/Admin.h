#ifndef ADMIN_H
#define ADMIN_H

#include "Staff.h"

class Admin : public Staff {
public:
    // Constructor method
    Admin(String userId, String name, int pin, String faceId);

    // Change PIN of an existing user
    void changeUserPin(int newUserPin);

    // Add new staff user to the system
    void addUser(String userId, String name, int pin, String faceId);

    // Delete user from the system
    void deleteUser(String userId);

    // Arm alarm with admin logging
    void armSystem(bool isAuthenticated);

    // Disarm alarm with admin logging
    void disarmSystem(bool isAuthenticated);
};

#endif