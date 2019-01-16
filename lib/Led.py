import board
import neopixel
import time
from . import Database
from models import Color


class Strip(Database.LEDDriverDB, Color.LEDColor):
    def __init__(this, dbFile, dbTable):
        this.DB_FILE = dbFile
        this.DB_LED_TABLE = dbTable
        Database.LEDDriverDB.__init__(this)
        Color.LEDColor.__init__(this)
        this.NUM_LEDS = 30
        this.LED_PIN = board.D18
        this.LED_ORDER = neopixel.RGB
        this.pixels = neopixel.NeoPixel(this.LED_PIN, this.NUM_LEDS)
        this.RED = (255, 0, 0)
        this.YELLOW = (255, 150, 0)
        this.GREEN = (0, 255, 0)
        this.CYAN = (0, 255, 255)
        this.BLUE = (0, 0, 255)
        this.PURPLE = (180, 0, 255)


    def changeColor(this, red, green, blue ):
        """ Change the LED strip color ex. (66,38,176) """
        this.pixels.fill((red, green, blue))

    def alertColor(this, lastRecord, red, green, blue):
        """ Flash a color and return to the previously set color """
        try:
            print(red, green, blue)
            this.changeColor(red, green, blue)
            time.sleep(2)
            this.changeColor(lastRecord.red, lastRecord.green, lastRecord.blue)
        except AttributeError:
            this.changeColor(*this.CYAN)
            time.sleep(2)
            this.changeColor(*this.YELLOW)

    def startup(this, wait):        
        for j in range(255):
            for i in range(this.NUM_LEDS):
                pixel_index = (i * 256 // this.NUM_LEDS) + j
                this.pixels[i] = this.wheel(pixel_index & 255)
            this.pixels.show()
            time.sleep(wait)

    def shutdown(this, delay, wait):
        def chase(color, wait):
            for i in range(this.NUM_LEDS):
                this.pixels[i] = color
                time.sleep(wait)
                this.pixels.show()
            time.sleep(0.5)
        
        chase(this.RED, delay)  # Increase the number to slow down the color chase
        chase(this.YELLOW, delay)
        chase(this.GREEN, delay)
        chase(this.CYAN, delay)
        chase(this.BLUE, delay)
        chase(this.PURPLE, delay)
        time.sleep(wait)
        this.turnoff()
    
    def turnoff(this):
        this.changeColor(0,0,0)

    def wheel(this, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255 - pos*3)
        return (r, g, b) if this.LED_ORDER == neopixel.RGB or this.LED_ORDER == neopixel.GRB else (r, g, b, 0)