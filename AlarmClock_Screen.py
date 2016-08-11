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
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


def Get_Temperature():
    """
    Get_Tepearture Function:
    Function to get the temperature in degrees C from the attached sensor

    Args: None

    Return: Temperature
    """
    try:
        suite
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Get_Temperature')
    except:
        print ('Error in Function Get_Temperature')
    finally:
        GPIO.cleanup()

def Get_ActualTime():
    pass

def Get_AlarmTime(Alarm_Number):
    pass

