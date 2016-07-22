# encoding: utf-8
"""
AlarmClock_Alarm.py

Script 2 of 2 from AlarmClock Project:
Script for comparing alarm time to actual time, triggering the alarm and disabling the alarm

Created by Christopher Beard on 16-07-2016.
Copyright (c) 2016 notice: 
This code is shared under the Creative Commons Attribution-ShareAlike
4.0 International Public License 
"""

from time import sleep
import AlarmClock_Screen
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

def GPIO_Call(Buzzer, LEDFlash):
    """
    GPIO_Call Fucntion:
    Take in Booleans and sets corresponding GPIO Outputs

    Args:Buzzer, LEDFlash
 
    Returns: None 
    """
    # set up GPIO
    try:
        if Buzzer:
            pass # set GPIO true 
        else:
            pass # set GPIO false

        if LEDFlash:
            pass # set GPIO True
        else:
            pass # set GPIO False
    except KeyboardInterrupt:
        print 'KeyboardInterrupt in Function GPIO_Call'
    except:
        print 'Error in Function GPIO_Call'
    finally:
        GPIO.cleanup() 
    

def Alarm_Active(AlarmTime, ActualTime, AlarmButtonPressed, LEDFlash, Buzzer, AlarmHappened):
    """
    Alarm_Active Function:
    Takes in Alarm parameters the triggers alarm at correct time

    Args: AlarmTime, ActualTime, AlarmButtonPressed, LEDFlash, Buzzer, AlarmHappened

    Returns: AlarmHappened, AlarmButtonPressed, LEDFlash, Buzzer
    """
    
    try:
        # if the alarm has gone off and then the user deactivates it sleep for 20 mins 
        if AlarmButtonPressed and AlarmHappened:
            Buzzer = False
            LEDFlash = False
            AlarmHappened = False
            AlarmButtonPressed = False   
            GPIO_Call(Buzzer, LEDFlash)                     
            sleep(20*60) #20 mins in seconds
        # If actual time is greater than the alarm time + 10 mins from above e.g. 03:00 > 02:40 then 
        # the alarm can never go off as 24hr clock so actual time will cycle round at midnight 
        elif ActualTime >= (AlarmTime + (10*60)):
            AlarmHappened = False
            Buzzer = False
            LEDFlash = False
            GPIO_Call(Buzzer, LEDFlash)            
            sleep(0.25) # preserve processor
        # Set condition for if alarm has gone off and user hasnt deactivated after 10 secs of beeping and 2 min silence
        elif (ActualTime >= (AlarmTime + (2*60))) and (ActualTime < (AlarmTime + (10*60))):
            if Buzzer:
                Buzzer = False
                LEDFlash = False
            elif not Buzzer:
                Buzzer = True
                LEDFlash = True
            GPIO_Call(Buzzer, LEDFlash)
            sleep(1)            
        # set condition for 30 secs before alarm time
        elif (ActualTime >= (AlarmTime - 30)) and (ActualTime < (AlarmTime - 10)):
            AlarmHappened = True
            if LEDFlash:
                LEDFlash = False
            elif not LEDFlash:
                LEDFlash = True
            Buzzer = False
            GPIO_Call(Buzzer, LEDFlash)
            sleep(1)
        #set condition for 10 secs before alarm time (beeping)
        elif (ActualTime >= (AlarmTime - 10)) and (ActualTime < AlarmTime):
            AlarmHappened = True
            if Buzzer:
                Buzzer = False
                LEDFlash = False
            elif not Buzzer:
                Buzzer = True
                LEDFlash = True                
            GPIO_Call(Buzzer, LEDFlash)
            sleep(1)            
        # set condition for 2 min slience period of alarm
        elif (ActualTime >= AlarmTime) and (ActualTime < (AlarmTime + (2*60))):
            AlarmHappened = True
            Buzzer = False
            LEDFlash = False
            GPIO_Call(Buzzer, LEDFlash)
            sleep(0.25) # preserve processor
        # set condition for sleeping alarm if over 10 mins to go
        elif (ActualTime < (AlarmTime - (10*60))):
            sleep(0.25) # preserve processor

        return [AlarmHappened, AlarmButtonPressed, LEDFlash, Buzzer]

    except KeyboardInterrupt:
        print "Keyboard Interruption in Alarm_Active"
    except:
        print "Error in Alarm_Active Function on AlarmClock_Alarm"
    finally:
        GPIO.cleanup()


def main():
    """
    Main Funtion:
    Runs in constant while loop checking status of alarm (on/off), 
    If alarm on it calls Alarm_Active function
    """
    #set up initial variables
    Alarm1_Happened = False  # Can you do arrays python or does list work?
    Alarm2_Happened = False
    Alarm1ButtonPressed = False # IR Button Input for deactivating alarm
    Alarm2ButtonPressed = False 
    LEDFlash = False
    Buzzer = False
    Alarm_Number = None

    try:
        while True:
            if AlarmClock_Screen.Alarm1Active:
                Alarm_Number = 1
                Alarm1Time = AlarmClock_Screen.Get_AlarmTime(Alarm_Number)
                ActualTime = AlarmClock_Screen.Get_ActualTime()
                AlarmButtonGPIO = None # Assign Later
                #set up input GPIO as interupt if high then set Alarm1ButtonPressed = True
                #call function
                [Alarm1_Happened, Alarm1ButtonPressed, LEDFlash, Buzzer] = Alarm_Active(Alarm1Time, ActualTime, \
                    Alarm1ButtonPressed, LEDFlash, Buzzer, Alarm1_Happened) # check syntax
            else:
                sleep(0.25) #preserve processor
                
            if AlarmClock_Screen.Alarm2Active:
                Alarm_Number = 2
                Alarm2Time = AlarmClock_Screen.Get_AlarmTime(Alarm_Number)
                ActualTime = AlarmClock_Screen.Get_ActualTime()
                AlarmButtonGPIO = None # Assign Later
                #set up input GPIO as interupt if high then set Alarm1ButtonPressed = True
                #call function
                [Alarm2_Happened, Alarm2ButtonPressed, LEDFlash, Buzzer] = Alarm_Active(Alarm2Time, ActualTime, \
                    Alarm2ButtonPressed, LEDFlash, Buzzer, Alarm2_Happened) # check syntax
            else:
                sleep(0.25) #preserve processor

    except KeyboardInterrupt:
        print "Keyboard Interuption in main"
    except:
        print "Error in Main of AlarmClock_Alarm"
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()