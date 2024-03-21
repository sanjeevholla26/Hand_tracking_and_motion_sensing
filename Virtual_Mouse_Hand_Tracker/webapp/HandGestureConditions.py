# Here conditions for all the Hand gestures have been defined

def OnlyIndexFingerUp(fingers):
    if fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
        return True
    else:
        return False

def IndexAndThumbFinger(fingers):
    if fingers[0] and fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
        return True
    else:
        return False

def RingFingerUp(fingers):
    if not fingers[1] and not fingers[2] and fingers[3] and not fingers[4]:
        return True
    else:
        return False

def IndexAndMiddleFingersUp(fingers):
    if fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
        return True
    else:
        return False

def IndexAndLastFingerUp(fingers):
    if fingers[1] and not fingers[2] and not fingers[3] and fingers[4]:
        return True
    else:
        return False

def AllFingersUp(fingers):
    if fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4]:
        return True
    else:
        return False

def OnlyThumbFingerUp(fingers):
    if fingers[0] and not fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
        return True
    else:
        return False

def AllFingersClosed(fingers):
    if not fingers[0] and not fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
        return True
    else:
        return False

category_id_for_conditions = {
    1: OnlyIndexFingerUp,
    2: IndexAndMiddleFingersUp,
    3: IndexAndThumbFinger,
    4: RingFingerUp,
    5: IndexAndLastFingerUp,
    6: AllFingersUp,
    7: AllFingersClosed
}
