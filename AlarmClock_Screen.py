# encoding: utf-8
"""
AlarmClock_screen.py

Script 1 of 2 from AlarmClock Project:
Script for controlling the LCD Screen on the alarm clock, displaying time and date,
reading the set alarm time etc.

Created by Christopher Beard on 16-07-2016.
Copyright (c) 2016 notice:
This code is shared under the Creative Commons Attribution-ShareAlike
4.0 International Public License
It is also shared under the GNU GENERAL PUBLIC LICENSE Version 3
"""
from time import sleep, strftime
from datetime import datetime
import pickle
import Adafruit_CharLCD as LCD
import Adafruit_MCP9808.MCP9808 as MCP9808
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(port, GPIO.IN, [pull_up_down=GPIO.PUD_DOWN])
#intialise LCD
lcd = LCD.Adafruit_CharLCDPlate()
#set initial background colour
lcd.set_color(1.0,0.0,1.0) # blue LCD only
#set background off intially, need GPIO event to set high
lcd.set_backlight(0)
#intialise temp sensor
sensor = MCP9808.MCP9808()
sensor.begin()

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
    finally:
        GPIO.cleanup()

def Get_ActualTime():
    """
    Get_ActualTime Function:
    Function to get the actual time from the system, then seperate into
    a time for the display and a dictionary item for the time in
    individual hours, minutes and seconds

    Args: None

    Return: ActualTime,  ActualTimeDisplay
    """
    try:
        ActualTimeDisplay = datetime.now().strftime('%H:%M')
        Hour = int(datetime.now().strftime('%H'))
        Min = int(datetime.now().strftime('%M'))
        Sec = int(datetime.now().strftime('%S'))
        ActualTime = {'H':Hour, 'M':Min, 'S':Sec}
        return ActualTime, ActualTimeDisplay
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Get_ActualTime')
    finally:
        GPIO.cleanup()

def Get_Date():
    """
    Get_Date fucntion:
    Fucntion to get date from the system

    Args: None

    Return: Date
    """
    try:
        Date = datetime.now().strftime('%a %d %b')
        return Date
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Get_Date')
    finally:
        GPIO.cleanup()

def Set_AlarmTime(Hour, Min, Sec, Alarm_Number):
    """
    Set_AlarmTime Function:
    Function to alter the set alarm time using the LCD touchbuttons changing
    hour and minute seperately

    Args: Hour, Min, Sec, Alarm_Number

    Return: Hour, Min, Sec
    """
    lcd.set_backlight(1)
    lcd.clear()
    lcd.message('Alarm ' + str(Alarm_Number) + ' Time:\n' )
    lcd.message(str(Hour)+':'+str(Min))
    Cycle = True
    while Cycle:
        if lcd.is_pressed(LCD.UP):
            Hour += 1
            lcd.clear()
            lcd.message('Alarm ' + str(Alarm_Number) + ' Time:\n' )
            lcd.message(str(Hour)+':'+str(Min))
        elif lcd.is_pressed(LCD.DOWN):
            Hour -= 1
            lcd.clear()
            lcd.message('Alarm ' + str(Alarm_Number) + ' Time:\n' )
            lcd.message(str(Hour)+':'+str(Min))
        elif lcd.is_pressed(LCD.SELECT):
            Cycle = False
            sleep(0.5)

    Cycle = True
    while Cycle:
        if lcd.is_pressed(LCD.UP):
            Min += 1
            lcd.clear()
            lcd.message('Alarm ' + str(Alarm_Number) + ' Time:\n' )
            lcd.message(str(Hour)+':'+str(Min))
        elif lcd.is_pressed(LCD.DOWN):
            Min -= 1
            lcd.clear()
            lcd.message('Alarm ' + str(Alarm_Number) + ' Time:\n' )
            lcd.message(str(Hour)+':'+str(Min))
        elif lcd.is_pressed(LCD.SELECT):
            Cycle = False
            sleep(0.5)

    lcd.clear()
    lcd.set_backlight(0)
    return Hour, Min, Sec

def Get_AlarmTime(Hour, Min, Sec, Alarm_Number):
    """
    Get_AlarmTime function:
    Function to get the individual times of the alarm in Hous, mins and secs
    and convert to dictionary item

    Args: Hour, Min, Sec, Alarm_Number

    Return: AlarmTime
    """
    try:
        #convert to dictionary
        AlarmTime = {'H':Hour, 'M':Min, 'S':Sec}
        return AlarmTime
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Get_AlarmTime')
    finally:
        GPIO.cleanup()


def F_BackLightON():
    """
    F_BackLightON function:
    Function to turn LCD backlight on for a duration of time

    Args: None

    Return: None
    """
    try:
        lcd.set_backlight(1)
        sleep(8)
        lcd.set_backlight(0)
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function F_BackLightON')
    finally:
        GPIO.cleanup()


def F_AlarmOnOff(AlarmActive):
    """
    AlarmActive function:
    Function to enable and disable alarm when button is pressed as well as
    display status on screen

    Args: AlarmActive

    Return: AlarmActive
    """
    try:
        if AlarmActive:
            AlarmActive = False
            lcd.set_backlight(1)
            lcd.clear()
            lcd.message('Alarm ' + str(Alarm_Number) + ' Disabled')
            sleep(2)
            lcd.clear()
            lcd.set_backlight(0)
            return AlarmActive
        else:
            AlarmActive = True
            lcd.set_backlight(1)
            lcd.clear()
            lcd.message('Alarm ' + str(Alarm_Number) + ' Enabled')
            sleep(2)
            lcd.clear()
            lcd.set_backlight(0)
            return AlarmActive
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function F_AlarmOnOff')
    finally:
        GPIO.cleanup()

def main():
    """
    Main Function:
    Runs continously calling appropriate functions to set screens depending on buttons pressed
    """
    try:
        #Intialise variables
        Alarm1Active = False
        Alarm2Active = False
        Hour1 = 1
        Min1 = 1
        Sec1 = 0
        Hour2 = 1
        Min2 = 1
        Sec2 = 0

        while True:
            if lcd.is_pressed(LCD.UP):
                Alarm1Active = F_AlarmOnOff(Alarm1Active, 1)
            elif lcd.is_pressed(LCD.DOWN):
                Alarm2Active = F_AlarmOnOff(Alarm2Active, 2)
            elif lcd.is_pressed(LCD.LEFT):
                Hour1, Min1, Sec1 = Set_AlarmTime(Hour1, Min1, Sec1, 1)
            elif lcd.is_pressed(LCD.RIGHT):
                Hour2, Min2, Sec2 = Set_AlarmTime(Hour2, Min2, Sec2, 2)
            else:
                #Main Screen
                ActualTime, ActualTimeDisplay = Get_ActualTime()
                date = Get_Date()
                temp = Get_Temperature()
                lcd.set_cursor(0,0)
                lcd.message(ActualTimeDisplay)
                lcd.set_cursor(12,0)
                lcd.message(temp + chr(223) + 'C') #chr(223) is degree sign
                lcd.set_cursor(3,1)
                lcd.message(date)
                sleep(0.25)
                #trigger event for backlight
                GPIO.add_event_detect(port, GPIO.RISING, callback=F_BackLightON(), bouncetime=300)
                #tigger event for enabling/disabling first alarm
                GPIO.add_event_detect(port, GPIO.RISING, callback=F_AlarmOnOff(Alarm1Active), bouncetime=300)
                #tigger event for enabling/disabling second alarm
                GPIO.add_event_detect(port, GPIO.RISING, callback=F_AlarmOnOff(Alarm2Active), bouncetime=300)
                #setup pickles here
                with open('Alarm1Active.pickle', 'wb') as f:
                    # Pickle the 'data' using the highest protocol available.
                    pickle.dump(Alarm1Active, f, pickle.HIGHEST_PROTOCOL)
                with open('Alarm2Active.pickle', 'wb') as f2:
                    # Pickle the 'data' using the highest protocol available.
                    pickle.dump(Alarm2Active, f2, pickle.HIGHEST_PROTOCOL)
                with open('AlarmTime1.pickle.', 'wb') as f3:
                    AlarmTime1 = Get_AlarmTime(Hour1, Min1, Sec1, 1)
                    # Pickle the 'data' using the highest protocol available.
                    pickle.dump(AlarmTime1, f3, pickle.HIGHEST_PROTOCOL)
                with open('AlarmTime2.pickle.', 'wb') as f4:
                    AlarmTime2 = Get_AlarmTime(Hour2, Min2, Sec2, 2)
                    # Pickle the 'data' using the highest protocol available.
                    pickle.dump(AlarmTime2, f4, pickle.HIGHEST_PROTOCOL)

    except KeyboardInterrupt:
        print('KeyboardInterrupt in Main')
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
