import board, busio, displayio, time
import adafruit_displayio_ssd1306
import adafruit_imageload

import board,busio
import digitalio
from time import sleep
from adafruit_st7735 import ST7735R
import displayio

import neopixel
import adafruit_ds3231
import gifio
import os, sys
import gc

import time


import terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import rotaryio

import microcontroller

from microcontroller import watchdog
from watchdog import WatchDogMode
from time import sleep
from adafruit_htu21d import HTU21D

import gc
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.line import Line


free_memory = gc.mem_free()
print("Free memory: {} bytes".format(free_memory))

CYello=0xFFFF00

font_file = "IcleNor.bdf"
fontsek = bitmap_font.load_font(font_file)

font_file = "CordiaUPC-32.bdf"
fontsek2 = bitmap_font.load_font(font_file)


Buzz = digitalio.DigitalInOut(board.GP26)
Buzz.direction = digitalio.Direction.OUTPUT
Buzz.value = False
#-----------------------------------------------------
#
#-----------------------------------------------------
btn_H1 = digitalio.DigitalInOut(board.GP27)
btn_H1.direction = digitalio.Direction.INPUT
btn_H1.pull = digitalio.Pull.DOWN

btn_M1 = digitalio.DigitalInOut(board.GP22)
btn_M1.direction = digitalio.Direction.INPUT
btn_M1.pull = digitalio.Pull.DOWN


btn_Mode = digitalio.DigitalInOut(board.GP18)
btn_Mode.direction = digitalio.Direction.INPUT
btn_Mode.pull = digitalio.Pull.DOWN

#----ds3231
SDA = board.GP20
SCL = board.GP21
i2c = busio.I2C(SCL, SDA)
rtc = adafruit_ds3231.DS3231(i2c)

days = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
month = (" ","Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec")


SDA = board.GP14
SCL = board.GP15
i2c = busio.I2C(SCL, SDA)

htu210 = HTU21D(i2c)

temperature = htu210.temperature
humidity = htu210.relative_humidity

#----WS2812B
# Update this to match the number of NeoPixel LEDs connected to your board.
fbright=0.3
num_pixels = 9 #17
pixels = neopixel.NeoPixel(board.GP0, num_pixels)
pixels.brightness = fbright

GreenB = 0x00CC00

COLOR = (0, 0, 0) 
RR = (250, 0, 0)  # color to blink
GG = (0, 250, 0)
BB = (0, 0, 250)
WHITE = (255, 255, 255)

pixels[0] = RR

pixels[1] = RR
pixels[2] = COLOR
pixels[3] = COLOR
pixels[4] = COLOR
pixels[5] = COLOR
pixels[6] = COLOR
pixels[7] = COLOR
pixels[8] = COLOR

pixels.show()

while True:
   sleep(3)
def invert_colors():
    temp = icon_pal[0]
    icon_pal[0] = icon_pal[1]
    icon_pal[1] = temp

#-------------------------------
#
#-------------------------------

displayio.release_displays()

#----ST7735
mosi_pin = board.GP11
clk_pin = board.GP10
reset_pin = board.GP17
cs_pin_FAKE = board.GP19
cs1 = digitalio.DigitalInOut(board.GP1)
cs1.direction = digitalio.Direction.OUTPUT

dc_pin = board.GP16

displayio.release_displays()
spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)
 
display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin_FAKE, reset=reset_pin,baudrate=31250000)
display = ST7735R(display_bus, width=160, height=128, bgr = True,rotation=270)#,colstart = 26,rowstart = 0)

#=======================================
info = os.uname()[4] + "\n" + \
    sys.implementation[0] + " " + os.uname()[3] + "\n" 

print("=======================================")
print(info)
print("=======================================")
print("CircuitPython play GIF")
print()

frame_count = 0
odg = None

splash = displayio.Group()
display.root_group = splash

#=============================================================================
#
#=============================================================================
def logo():
    splash = displayio.Group()
    text = "Yakroo108"
    label_text = label.Label(terminalio.FONT, text=text, color=0xFFFFFF,x=10, y=1)
    label_text.anchor_point = (1.0, 0.0)
    label_text.anchored_position = (130, 50)
    label_text.scale = 2
    splash.append(label_text)
    display.show(splash)
   
    sleep(3)
    splash.remove(label_text)
#=============================================================================
#
#=============================================================================
def Title_gif():
    splash = displayio.Group()
    text = "GIF"
    label_text = label.Label(terminalio.FONT, text=text, color=0xFFFFFF,x=10, y=1)
    label_text.anchor_point = (1.0, 0.0)
    label_text.anchored_position = (100, 20)
    label_text.scale = 3
    
    text = "animation"
    label_text2 = label.Label(terminalio.FONT, text=text, color=0xFFFFFF,x=10, y=1)
    label_text2.anchor_point = (1.0, 0.0)
    label_text2.anchored_position = (130, 70)
    label_text2.scale = 2    
    
    splash.append(label_text)
    splash.append(label_text2)
    display.show(splash)
   
    sleep(1)

order=0
    

Color_orang = 0x00FF00
#=============================================================================
#
#=============================================================================
# Create a list of .gif files in the /pic directory
gif_folder = "/gif"
gif_files = [f for f in os.listdir(gif_folder) if f.endswith(".gif")]
print(gif_files)

num_files = len(gif_files)
print("Number of .gif files:", num_files)
print(gif_files[1])
numgif=0
#sleep(30)
def gif(gif):
    splash = displayio.Group()

    t = rtc.datetime
    text = "{}:{:02}".format(t.tm_hour, t.tm_min)

    label_text = label.Label(fontsek, text=text, color=Color_orang,x=10, y=1)
    label_text.anchor_point = (1.0, 0.0)
    label_text.anchored_position = (124, 2)
    label_text.scale = 1

    text2 = "{} {}/{}/{}".format(days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year)

    label_text2 = label.Label(terminalio.FONT, text=text2, color=0xFFFFFF,x=10, y=1)
    label_text2.anchor_point = (1.0, 0.0)
    label_text2.anchored_position = (116, 35)
    label_text2.scale = 1
    
    x = 150
    y = 120
    temperature = htu210.temperature
    humidity = htu210.relative_humidity
    text = "{:02}°C {:02}%".format(int(temperature), int(humidity))
    #text = "37C 58%"
    label_temp = label.Label(terminalio.FONT, text=text, color=0xFFFFFF,x=10, y=10)
    label_temp.anchor_point = (1.0, 0.0)
    label_temp.anchored_position = (100, y)
    label_temp.scale = (2)


    odg = gifio.OnDiskGif(gif)
    frame_count = odg.frame_count

    # Create a TileGrid to display the GIF frames
    face = displayio.TileGrid(
        odg.bitmap,
        pixel_shader=displayio.ColorConverter(
            input_colorspace=displayio.Colorspace.RGB565_SWAPPED
        ),
        x=int((display.width - odg.width) / 2),
        y=int((display.height - odg.height) / 2),
    )

    # Add the face TileGrid and labels to the splash Group
    splash.append(face)
    splash.append(label_text)
    splash.append(label_text2)
    splash.append(label_temp)
    # Create a new displayio Group to show the splash screen
    display.show(splash)
    #time.sleep(3)
    gifOK = False
    # Loop through all the frames of the GIF
    while True:
        

            for _ in range(frame_count):
                odg.next_frame()
                x -= 1  # Adjust the speed of movement by changing the value
                if x < -label_temp.width:
                    x = display.width
                label_temp.x = x
                label_temp.y = y  
                display.refresh()
                if btn_Mode.value:  # Check if the button is released (active-high)
                    gifOK = True
                    break
                #w.feed()
            t = rtc.datetime
            text = "{}:{:02}".format(t.tm_hour, t.tm_min)
            text2 = "{} {}/{}/{}".format(days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year)
            #temperature = htu210.temperature
            #humidity = htu210.relative_humidity
            text3="{:02}°C {:02}%".format(int(temperature), int(humidity))
            label_temp.text = text3    
            # Update the time and date labels
            label_text.text = text
            label_text2.text = text2
            #w.feed()
            if gifOK == True:  # Check if the button is released (active-high)
   
                    Buzz.value = True
                    time.sleep(0.5)
                    Buzz.value = False
                    if len(splash) > 0:
            # Clear the group to remove the previous image and text
                        splash.pop()
                        splash.pop()
                        splash.pop()
                    gc.collect()
                    print("mem: ", gc.mem_free())
                    break
#=============================================================================
#
#=============================================================================
def menu():
    Inx = [22, 42, 62, 82,102,122]
    splash = displayio.Group()

    t = rtc.datetime
    Hint=int(t.tm_hour)
    text = "{:02}".format(Hint) #"{:02}".format(t.tm_hour)

    label_text1 = label.Label(terminalio.FONT, text=text, color=CYello,x=10, y=1)
    label_text1.anchor_point = (1.0, 0.0)
    label_text1.anchored_position = (110, 8)
    label_text1.scale = 2

    Mint=int(t.tm_min)
    text2 = "{:02}".format(Mint)#t.tm_min)

    label_text2 = label.Label(terminalio.FONT, text=text2, color=CYello,x=10, y=1)
    label_text2.anchor_point = (1.0, 0.0)
    label_text2.anchored_position = (110, 28)
    label_text2.scale = 2

    Day=int(t.tm_wday)
    text2 = "{:02}".format(Day)#t.tm_min)
    label_Day = label.Label(terminalio.FONT, text=text2, color=CYello,x=10, y=1)
    label_Day.anchor_point = (1.0, 0.0)
    label_Day.anchored_position = (110, 48)
    label_Day.scale = 2

    Date=int(t.tm_mday)
    text2 = "{:02}".format(Date)#t.tm_min)
    label_Date = label.Label(terminalio.FONT, text=text2, color=CYello,x=10, y=1)
    label_Date.anchor_point = (1.0, 0.0)
    label_Date.anchored_position = (110, 68)
    label_Date.scale = 2
    
    Mont=int(t.tm_mon)
    text2 = "{:02}".format(Mont)#t.tm_min)
    label_Mont = label.Label(terminalio.FONT, text=text2, color=CYello,x=10, y=1)
    label_Mont.anchor_point = (1.0, 0.0)
    label_Mont.anchored_position = (110, 88)
    label_Mont.scale = 2

    Yeart=int(t.tm_year)
    text2 = "{:02}".format(Yeart)#t.tm_min)
    label_Yeart = label.Label(terminalio.FONT, text=text2, color=CYello,x=10, y=1)
    label_Yeart.anchor_point = (1.0, 0.0)
    label_Yeart.anchored_position = (110, 108)
    label_Yeart.scale = 2

    Hstr= "Hour"
    label_H = label.Label(terminalio.FONT, text=Hstr, color=0xFFFFFF,x=10, y=1)
    label_H.anchor_point = (1.0, 0.0)
    label_H.anchored_position = (50, 8)
    label_H.scale = 2

    Mstr= "Minute"
    label_M = label.Label(terminalio.FONT, text=Mstr, color=0xFFFFFF,x=10, y=1)
    label_M.anchor_point = (1.0, 0.0)
    label_M.anchored_position = (75, 28)
    label_M.scale = 2

    Mstr= "Day"
    label_strDay = label.Label(terminalio.FONT, text=Mstr, color=0xFFFFFF,x=10, y=1)
    label_strDay.anchor_point = (1.0, 0.0)
    label_strDay.anchored_position = (38, 48)
    label_strDay.scale = 2

    Mstr= "Date"
    label_strDate = label.Label(terminalio.FONT, text=Mstr, color=0xFFFFFF,x=10, y=1)
    label_strDate.anchor_point = (1.0, 0.0)
    label_strDate.anchored_position = (50, 68)
    label_strDate.scale = 2
    
    Mstr= "Month"
    label_strMont = label.Label(terminalio.FONT, text=Mstr, color=0xFFFFFF,x=10, y=1)
    label_strMont.anchor_point = (1.0, 0.0)
    label_strMont.anchored_position = (62, 88)
    label_strMont.scale = 2

    Mstr= "Year"
    label_strYear = label.Label(terminalio.FONT, text=Mstr, color=0xFFFFFF,x=10, y=1)
    label_strYear.anchor_point = (1.0, 0.0)
    label_strYear.anchored_position = (50, 108)
    label_strYear.scale = 2
    
    Mstr= "<-"
    label_strSlect = label.Label(terminalio.FONT, text=Mstr, color=0x00FF00,x=10, y=1)
    label_strSlect.anchor_point = (1.0, 0.0)
    label_strSlect.anchored_position = (154, 12)
    label_strSlect.scale = 2

    color_bitmap = displayio.Bitmap(160, 10, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x0000CC  # Bright Green

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
           
# Text
    text = "Setting TIME"
    text_setting = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
    text_setting.anchor_point = (1.0, 0.0)
    text_setting.anchored_position = (122, 1)#45)
    text_setting.scale = (1)
 
    splash.append(bg_sprite)
    splash.append(text_setting)
    splash.append(label_text1)
    splash.append(label_text2)
    splash.append(label_H)
    splash.append(label_M)
    splash.append(label_strDay)
    splash.append(label_Day)
    splash.append(label_strDate)
    splash.append(label_Date)
    splash.append(label_strMont)
    splash.append(label_Mont)
    splash.append(label_strSlect)
    splash.append(label_strYear)
    splash.append(label_Yeart)
    # Create a new displayio Group to show the splash screen
    display.show(splash)
    cntINX=0
    SetOK=False
    TimeOK = False
:
    while True:
  
        if btn_H1.value:
            time.sleep(0.02)
            if btn_H1.value:
                print ("Set") 
                SetOK=True
                if cntINX == 0:
                    if Hint < 23:
                        Hint=Hint+1
                    else :
                        Hint=0
                    text = "{:02}".format(Hint)
                    label_text1.text = text
            
                elif cntINX == 1: #min
                    if Mint < 59:
                        Mint=Mint+1
                    else :
                        Mint=0
                    text2 = "{:02}".format(Mint)
                    label_text2.text = text2

                elif cntINX == 2: #min
                    if Day < 7:
                        Day=Day+1
                    else :
                        Day=0
                    text2 = "{:02}".format(Day)
                    label_Day.text = text2

                elif cntINX == 3: #min
                    if Date < 31:
                        Date=Date+1
                    else :
                        Date=0
                    text2 = "{:02}".format(Date)
                    label_Date.text = text2
                    
                elif cntINX == 4: #min
                    if Mont < 12:
                        Mont=Mont+1
                    else :
                        Mont=0
                    text2 = "{:02}".format(Mont)
                    label_Mont.text = text2
                    
                elif cntINX == 5: #year
                    if Yeart < 2099:
                        Yeart=Yeart+1
                    else :
                        Yeart=2000
                    text2 = "{:04}".format(Yeart)
                    label_Yeart.text = text2
                    
                display.refresh()
            time.sleep(0.2)
            
        if btn_M1.value:
            time.sleep(0.02)
            if btn_M1.value:
                print ("Next")
                #SetOK=True
                if cntINX < 5 :
                     cntINX=cntINX+1
                else :
                     cntINX=0;
                label_strSlect.y = Inx[cntINX]
                display.refresh()     
                time.sleep(0.5)
           
        if btn_Mode.value:  # Check if the button is released (active-high)
            time.sleep(0.05)
            if btn_Mode.value:
                print ("Mode")
 
                Buzz.value = True
                time.sleep(0.2)
                Buzz.value = False

                if SetOK==True :
                    t = time.struct_time((Yeart,Mont, Date , Hint  , Mint ,1, Day  , -1  , -1))
                    print("Setting time to:", t)  # uncomment for debugging
                    rtc.datetime = t
                

                gc.collect()
                print("mem: ", gc.mem_free())
                TimeOK = True
                time.sleep(2)
                break
#=============================================================================
#
#=============================================================================
def pic():
    pic_folder = "/pic"
    pic_files = [f for f in os.listdir(pic_folder) if f.endswith(".bmp")]
    print(pic_files)

    numpic_files = len(pic_files)
    print("Number of .bmp files:", numpic_files)

    group = displayio.Group()
    display.show(group)

    x = 11
    y = 45

    t = rtc.datetime
    text = "{}:{:02}".format(t.tm_hour, t.tm_min)

    label_text = label.Label(fontsek, text=text, color=Color_orang, x=10, y=1)
    label_text.anchor_point = (1.0, 0.0)
    label_text.anchored_position = (124, 2)
    label_text.scale = 1

    text2 = "{} {}/{}/{}".format(days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year)

    label_text2 = label.Label(terminalio.FONT, text=text2, color=0xFFFFFF, x=10, y=1)
    label_text2.anchor_point = (1.0, 0.0)
    label_text2.anchored_position = (116, 35)
    label_text2.scale = 1

    # Use a counter to track the current image
    image_counter = 0

    picOK = False
    while True:
        t = rtc.datetime
        text = "{}:{:02}".format(t.tm_hour, t.tm_min)
        text2 = "{} {}/{}/{}".format(days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year)        
        label_text.text =text
        label_text2.text =text2
        if len(group) > 0:
            # Clear the group to remove the previous image and text
            group.pop()
            group.pop()
            group.pop()

        # Get the current image
        current_image = displayio.OnDiskBitmap("/pic/"+pic_files[image_counter])
        tile_grid = displayio.TileGrid(current_image, pixel_shader=current_image.pixel_shader)
        group.append(tile_grid)
        # Show the group on the display
        
        display.show(group)
        
        group.append(label_text)
        group.append(label_text2)
        # Increment the image counter and wrap around to the first image
        image_counter = (image_counter + 1) % len(pic_files)

        for _ in range(50):
            if btn_Mode.value:  # Check if the button is released (active-high)
                time.sleep(0.05)
                if btn_Mode.value:
                    print("Mode")
                    picOK = True
                    break
            time.sleep(0.1)
        if btn_H1.value:
            time.sleep(0.02)
            if btn_H1.value:
                Buzz.value = True
                time.sleep(0.2)
                Buzz.value = False
            #pixels.fill((255, 255, 255))
                pixels[0] = COLOR
                pixels[1] = WHITE
                pixels[2] = WHITE
                pixels[3] = WHITE
                pixels[4] = WHITE
                pixels[5] = WHITE
                pixels[6] = WHITE
                pixels[7] = WHITE
                pixels[8] = WHITE

                pixels.show()
        if btn_M1.value:
            time.sleep(0.02)
            if btn_M1.value: 
                Buzz.value = True
                time.sleep(0.2)
                Buzz.value = False
                pixels[1] = COLOR
                pixels[2] = COLOR
                pixels[3] = COLOR
                pixels[4] = COLOR
                pixels[5] = COLOR
                pixels[6] = COLOR
                pixels[7] = COLOR
                pixels[8] = COLOR            
            
                pixels.show() 
        if picOK:  # Check if the button is released (active-high)
            Buzz.value = True
            time.sleep(0.5)
            Buzz.value = False
            if len(group) > 0:
                # Clear the group to remove the previous image and text
                group.pop()
                group.pop()
                group.pop()
                
            gc.collect()
            print("mem: ", gc.mem_free())
            break

        # Wait for 5 seconds before switching to the next image
        time.sleep(2)#5)
#=============================================================================
#
#=============================================================================

def clock2():


    group = displayio.Group()
    #display.show(group)
    outline_color = 0x66FF66 #0000CC  # Initial outline color
    rounded_rect = RoundRect(2, 2, 158, 26, 8, outline=outline_color, fill=0x000000)

    outline_color2 = 0x0033FF
    rounded_rect2 = RoundRect(22,92, 114, 100, 8, outline=outline_color2, fill=0x0066FF)

    separator = displayio.Group()
    line = Rect(80, 94, 1, 50, fill=0xFFFFFF)  # 1-pixel wide vertical line, blue color
    separator.append(line)
    #group.append(separator)   
    
    x = 11
    y = 45

    t = rtc.datetime
    text = "{}:{:02}".format(t.tm_hour, t.tm_min)

    label_text = label.Label(fontsek, text=text, color=0xFFFF33, x=10, y=1)
    label_text.anchor_point = (1.0, 0.0)
    label_text.anchored_position = (124, 52)
    label_text.scale = 1

    text2 = "{} {}/{}/{}".format(days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year)

    label_text2 = label.Label(terminalio.FONT, text=text2, color=0xFFFFFF, x=10, y=1)
    label_text2.anchor_point = (1.0, 0.0)
    label_text2.anchored_position = (116, 10)
    label_text2.scale = 1

    temperature = htu210.temperature
    humidity = htu210.relative_humidity
    text = "{:02}°C {:02}%".format(int(temperature), int(humidity))
 
    label_temp = label.Label(terminalio.FONT, text=text, color=0xFFFFFF,x=10, y=10)
    label_temp.anchor_point = (1.0, 0.0)
    label_temp.anchored_position = (124, 100)
    label_temp.scale = (2)   
  

    # Use a counter to track the current image
    image_counter = 0
    temp_cnt=0
    picOK = False
    while True:
        t = rtc.datetime
        text = "{}:{:02}".format(t.tm_hour, t.tm_min)
        text2 = "{} {}/{}/{}".format(days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year)
        #temperature = htu210.temperature
        #humidity = htu210.relative_humidity
        #text3 = "{:02}°C {:02}%".format(int(temperature), int(humidity))
        label_text.text =text
        label_text2.text =text2
        #label_temp.text =text3
        if len(group) > 0:
            # Clear the group to remove the previous image and text
            group.pop()
            group.pop()
            group.pop()
            group.pop()
            group.pop()
            group.pop()
            
        display.show(group)
        group.append(rounded_rect)
        group.append(rounded_rect2) 
        group.append(label_text)
        group.append(label_text2)
        group.append(label_temp)
        group.append(separator) 

        if btn_H1.value:
            time.sleep(0.02)
            if btn_H1.value:
                Buzz.value = True
                time.sleep(0.2)
                Buzz.value = False
            #pixels.fill((255, 255, 255))
                pixels[0] = COLOR
                pixels[1] = WHITE
                pixels[2] = WHITE
                pixels[3] = WHITE
                pixels[4] = WHITE
                pixels[5] = WHITE
                pixels[6] = WHITE
                pixels[7] = WHITE
                pixels[8] = WHITE

                pixels.show()
        if btn_M1.value:
            time.sleep(0.02)
            if btn_M1.value: 
                Buzz.value = True
                time.sleep(0.2)
                Buzz.value = False
                pixels[1] = COLOR
                pixels[2] = COLOR
                pixels[3] = COLOR
                pixels[4] = COLOR
                pixels[5] = COLOR
                pixels[6] = COLOR
                pixels[7] = COLOR
                pixels[8] = COLOR            
            
                pixels.show()    
        if btn_Mode.value:  # Check if the button is released (active-high)
            time.sleep(0.02)
            if btn_Mode.value:
                Buzz.value = True
                time.sleep(0.5)
                Buzz.value = False
                if len(group) > 0:
                # Clear the group to remove the previous image and text
                    group.pop()
                    group.pop()
                    group.pop()
                    group.pop()
                    group.pop()
                    
                gc.collect()
                print("mem: ", gc.mem_free())
                break
        temp_cnt=temp_cnt+1
        if(temp_cnt>=180):
            temp_cnt=0
            gc.collect()

        # Wait for 5 seconds before switching to the next image
        time.sleep(1)
def clock():


    group = displayio.Group()
    
    outline_color = 0x66FF66 #0000CC  # Initial outline color
    rounded_rect = RoundRect(2, 2, 158, 26, 8, outline=outline_color, fill=0x000000)
    group.append(rounded_rect) 


    t = rtc.datetime
    text = "{}:{:02}".format(t.tm_hour, t.tm_min)

    label_text = label.Label(fontsek, text=text, color=0xFFFF33, x=10, y=1)
    label_text.anchor_point = (1.0, 0.0)
    label_text.anchored_position = (134, 52)
    label_text.scale = 1

    separator = displayio.Group()
    line = Rect(82, 44, 1, 50, fill=0xFFFFFF)  # 1-pixel wide vertical line, blue color
    separator.append(line)
    group.append(separator)

    Gray = 0x99FFCC #0x999999

    t = rtc.datetime
    text2 = "{}    {:02d}     {}".format(days[int(t.tm_wday)], t.tm_mday, month[int(t.tm_mon)])

    label_DATE = label.Label(fontsek2, text=text2, color=Gray,x=10, y=1)
    label_DATE.anchor_point = (1.0, 0.0)
    label_DATE.anchored_position = (155, 8)
    label_DATE.scale = 1
    
    group.append(label_text)
    #group.append(icon_grid)
    #group.append(icon_grid2)
    #group.append(icon_grid3)
    #group.append(icon_grid4)

    group.append(label_DATE)
    #group.append(label_txtmove)
    display.show(group)

    timer = 0
    pointer = 0


    cnt=0
    secH=0
    secL=0
    cbar=0

    mint=34
    mH=0
    mL=0
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    #t = time.struct_time((2023, 7 , 9  ,23  , 38 , 24 , 7   , -1  , -1))
    #print("Setting time to:", t)  
    #rtc.datetime = t
    MenuOK=False
    delay =0
    txtdelay=0
    while(MenuOK == False):#while True:
    
      t = rtc.datetime
      

      print("The date is {} {}/{}/{}".format(
                days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
               )
      )
      print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))
      
#--------------------------------
      Hmax = t.tm_hour / 10
      Hmin = t.tm_hour % 10
      MinH = t.tm_min / 10
      MinL = t.tm_min % 10       
      dateH = t.tm_mday /10
      dateL = t.tm_mday %10    

      t = rtc.datetime
      text = "{}:{:02}".format(t.tm_hour, t.tm_min)
      
      label_text.text =text

      if btn_H1.value:
            Buzz.value = True
            time.sleep(0.2)
            Buzz.value = False
            #pixels.fill((255, 255, 255))
            
            pixels[1] = WHITE
            pixels[2] = WHITE
            pixels[3] = WHITE
            pixels[4] = WHITE
            pixels[5] = WHITE
            pixels[6] = WHITE
            pixels[7] = WHITE
            pixels[8] = WHITE

            pixels.show()

      if btn_Mode.value:  # Check if the button is released (active-high)
            time.sleep(0.02)
            if btn_Mode.value:
                MenuOK = True
                Buzz.value = True
                time.sleep(0.5)
                Buzz.value = False
                if len(group) > 0:
                # Clear the group to remove the previous image and text
                    group.pop()
                    group.pop()
                    group.pop()
                label_DATE = None
                gc.collect()
                print("mem:", gc.mem_free())
                break
      sleep(1)         

#=============================================================================
#  MAIN
#=============================================================================                
while True:
    try:
        clock2()
        pic()
        Title_gif()
        #menu()
        gif("/gif/"+gif_files[numgif])
        numgif=numgif+1
        if(numgif>=num_files):
            numgif=0
        print("num: ", numgif)    
        menu()


    except Exception as e:
        # Handle the exception
        print("An error occurred:", str(e))

        









