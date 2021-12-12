from collections import OrderedDict

class menu(): 
    
    def __init__(self):
        self.mode_list = OrderedDict()
        self.mode_list["Internet"] = (5,10)
        self.mode_list["Local"] = (5,20)
        self.mode_list["Plactice"] = (5,30)
        self.menu_index = 0
    
    def select_mode(self,oled,switchs):
        while True:
            if switchs.get_switch_state("s1") == True:
                return list(self.mode_list.keys())[self.menu_index]
            elif switchs.get_switch_state("s2") == True:
                self.menu_index += 1
            elif switchs.get_switch_state("s3") == True:
                self.menu_index -= 1
            
            len_modes = len(list(self.mode_list.keys())) 
            if self.menu_index >= len_modes:
                self.menu_index = len_modes - 1
            elif self.menu_index < 0:
                self.menu_index = 0

            oled.fill(0)
            for i, mode in enumerate(self.mode_list):
                x = self.mode_list[mode][0]
                y = self.mode_list[mode][1]
                if i == self.menu_index: 
                    oled.fill_rect(0, y-1, 128, 10, 1)
                    oled.text(mode, x, y, 0) 
                else:
                    oled.text(mode,x,y)
            oled.show()
