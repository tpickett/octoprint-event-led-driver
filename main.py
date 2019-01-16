import argparse
from lib import Led

DB_FILE = "./print-o-matic.sqlite"
DB_LED_TABLE = "led_state"

##
# Help config
##
parser = argparse.ArgumentParser(description='Change 3d Printer LED color.')
parser.add_argument("-t", "--type",
                    default="client-connected",
                    help="type of action that is changing the LED color")
parser.add_argument("-c", "--color",
                    nargs='+',       # one or more parameters to this switch
                    type=int,        # /parameters/ are ints
                    dest='color',     # store in 'list'.
                    default=[66,38,176],
                    help="color to change LED strip to")


if __name__ == '__main__':
    args = parser.parse_args()
    red, green, blue = args.color

    LedStrip = Led.Strip(DB_FILE, DB_LED_TABLE)
    lastRecord = LedStrip.getLastColor()


    if args.type in ['client-connected']:
        LedStrip.alertColor(lastRecord, red, green, blue)
    elif args.type in ['client-disconnected']:
        LedStrip.changeColor(red, green, blue)
    elif args.type in ['startup']:
        LedStrip.startup(0.001)
    elif args.type in ['shutdown']:
        LedStrip.shutdown(0.1, 2)
    elif args.type in ["print-started","print-failed","print-complete"]:
        LedStrip.changeColor(red, green, blue)
        LedStrip.persistColor(red, green, blue)

    LedStrip.close()