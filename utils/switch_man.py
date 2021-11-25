from machine import Pin, Timer


class switchs():
    def __init__(self):
        self.s1 = Pin(22, Pin.IN, Pin.PULL_UP)
        self.s2 = Pin(23, Pin.IN, Pin.PULL_UP)
        self.s3 = Pin(15, Pin.IN, Pin.PULL_UP)
        self.s4 = Pin(21, Pin.IN, Pin.PULL_UP)

        self.s1_pushing = False
        self.s2_pushing = False
        self.s3_pushing = False
        self.s4_pushing = False

        self.s1_pushed = False
        self.s2_pushed = False
        self.s3_pushed = False
        self.s4_pushed = False

        t0 = Timer(0)
        t0.init(period=10, mode=Timer.PERIODIC, callback=self.set_switch_state)

    def set_switch_state(self,timer):
        if self.s1.value() == 0:
            self.s1_pushing = True
            self.s1_pushed = False
        if self.s1_pushing == True and self.s1.value() == 1:
            self.s1_pushed = True
            self.s1_pushing = False

        if self.s2.value() == 0:
            self.s2_pushing = True
            self.s2_pushed = False
        if self.s2_pushing == True and self.s2.value() == 1:
            self.s2_pushed = True
            self.s2_pushing = False

        if self.s3.value() == 0:
            self.s3_pushing = True
            self.s3_pushed = False
        if self.s3_pushing == True and self.s3.value() == 1:
            self.s3_pushed = True
            self.s3_pushing = False

        if self.s4.value() == 0:
            self.s4_pushing = True
            self.s4_pushed = False
        if self.s4_pushing == True and self.s4.value() == 1:
            self.s4_pushed = True
            self.s4_pushing = False

    def get_switch_state(self,switch_name):
        if switch_name == "s1":
            if self.s1_pushed == True:
                self.s1_pushed = False
                return True
            else:
                return False
        if switch_name == "s2":
            if self.s2_pushed == True:
                self.s2_pushed = False
                return True
            else:
                return False
        if switch_name == "s3":
            if self.s3_pushed == True:
                self.s3_pushed = False
                return True
            else:
                return False 
        if switch_name == "s4":
            if self.s4_pushed == True:
                self.s4_pushed = False
                return True
            else:
                return False
