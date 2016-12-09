from time import sleep
import Adafruit_CharLCD as LCD
import Adafruit_MCP9808.MCP9808 as MCP9808
import CHIP_IO.GPIO as GPIO

#intialise LCD
lcd = LCD.Adafruit_CharLCDPlate()

#set initial background colour
lcd.set_color(1.0,0.0,1.0) # blue LCD only

#intialise temp sensor
sensor = MCP9808.MCP9808()
sensor.begin()

#Function to get temperature
def Get_Temperature():
    """
    Get_Tepearture Function:
    Function to get the temperature in degrees C from the attached sensor

    Args: None

    Return: Temperature (as string)
    """
    try:
        temp = sensor.readTempC()
        temp = str('%.2f' % temp) # convert to string of 2 decimal places
        return temp
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Get_Temperature')
    except:
        print ('Error in Function Get_Temperature')
    finally:
        GPIO.cleanup()

#main
while True:
    temp = Get_Temperature()
    lcd.clear()
    lcd.message(temp + chr(223) + 'C') #chr(223) is degree sign
    sleep(5.0)
