#include "UserProfile.h"

UserProfile::UserProfile(String id, String n, int p, String face) {
    userId = id;
    name = n;
    pin = p;
    faceId = face;
}

String UserProfile::getUserId() { return userId; }