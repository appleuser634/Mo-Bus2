import framebuf
import network
import os
import time

import gc
gc.enable()

class animation():

    def __init__(self,oled):
        self.oled = oled

    def load_image(self,filename):
        with open(filename, 'rb') as f:
            f.readline()
            f.readline()
            f.readline()
            data = bytearray(f.read())
        return framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)

    def animation_start(self,name,times):
        self.oled.fill(0)
        self.oled.show()
        
        path_name = '../images/' + name
        image_name_list = os.listdir(path_name)
        
        for _ in range(times):
            
            for image_name in image_name_list:
                self.oled.fill(0)
                
                image_path = path_name + "/" + image_name
                image = self.load_image(image_path)
            
                self.oled.blit(image, 0, 0)
                self.oled.show()

                time.sleep(0.5)
            
        self.oled.fill(0)
        self.oled.show()

            

