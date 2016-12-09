from time import sleep, strftime
from datetime import datetime
import Adafruit_CharLCD as LCD
import Adafruit_MCP9808.MCP9808 as MCP9808
import CHIP_IO.GPIO as GPIO

#intialise LCD
lcd = LCD.Adafruit_CharLCDPlate()

#set initial background colour
lcd.set_color(1.0,0.0,1.0) # blue LCD only
lcd.set_backlight(0)

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
        temp = str('%.0f' % temp) # convert to string of 0 decimal places
        return temp
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Get_Temperature')
    except:
        print ('Error in Function Get_Temperature')
    finally:
        GPIO.cleanup()

#fucntion to get system time
def Get_ActualTime():
    ActualTimeDisplay = datetime.now().strftime('%H:%M')
    Hour = int(datetime.now().strftime('%H'))
    Min = int(datetime.now().strftime('%M'))
    Sec = int(datetime.now().strftime('%S'))
    ActualTime = {'H':Hour, 'M':Min, 'S':Sec}
    return ActualTime, ActualTimeDisplay

def Get_Date():
    Date = datetime.now().strftime('%a %d %b')
    return Date

def F_BackLightON():
    lcd.set_backlight(1)
    sleep(10)
    lcd.set_backlight(0)

#main
while True:
    if lcd.is_pressed(LCD.SELECT):
        F_BackLightON()

    ActualTime, ActualTimeDisplay = Get_ActualTime()
    ActualTime_in_seconds = ((ActualTime['H']*60*60) + (ActualTime['M']*60) + ActualTime['S'])
    date = Get_Date()
    temp = Get_Temperature()
    lcd.set_cursor(0,0)
    lcd.message(ActualTimeDisplay)
    lcd.set_cursor(12,0)
    lcd.message(temp + chr(223) + 'C') #chr(223) is degree sign
    lcd.set_cursor(3,1)
    lcd.message(date)
    sleep(0.5)
