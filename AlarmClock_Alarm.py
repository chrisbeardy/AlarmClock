# encoding: utf-8
"""
AlarmClock_Alarm.py

Script 2 of 2 from AlarmClock Project:
Script for comparing alarm time to actual time, triggering the alarm and disabling the alarm

Created by Christopher Beard on 16-07-2016.
Copyright (c) 2016 notice:
This code is shared under the Creative Commons Attribution-ShareAlike
4.0 International Public License
It is also shared under the GNU GENERAL PUBLIC LICENSE Version 3
"""

from time import sleep, strftime
from datetime import datetime
import pickle
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT, initial = 0)
GPIO.setup(20, GPIO.OUT, initial = 0)
GPIO.setup(8, GPIO.IN, pull_up_down = GPIO.PUD_DOWN )
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_DOWN )


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
        GPIO.cleanup()
        quit()

def Get_ActualTime_in_Seconds():
    """
    Get_ActualTime_in_Seconds Function:
    Function gets actual time from AlarmClock_Screen Script and then converts to seconds

    Args: None

    Returns: ActualTime_in_seconds
    """
    try:
        ActualTime, ActualTimeDisplay = Get_ActualTime()  # get as dictionary object Hour,Mins,Secs
        ActualTime_in_seconds = ((ActualTime['H']*60*60) + (ActualTime['M']*60) + ActualTime['S'])
        return ActualTime_in_seconds
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Get_ActualTime_in_Seconds')
        GPIO.cleanup()
        quit()

def Get_AlarmTime_in_Seconds(AlarmTime, Alarm_Number):
    """
    Get_AlarmTime_in_Seconds Function:
    Function gets alarm time from AlarmClock_Screen Script and then converts to seconds

    Args: Alarm_Number

    Returns: AlarmTime_in_seconds
    """
    try:
        #use pickle to get data from other script
        if Alarm_Number == 1:
            try:
                with open('AlarmTime1.pickle', 'rb') as f:
                #get as dictionary object
                    AlarmTime = pickle.load(f)
            except EOFError:
                AlarmTime_in_seconds = AlarmTime
                return AlarmTime_in_seconds
        elif Alarm_Number == 2:
            try:
                with open('AlarmTime2.pickle', 'rb') as f2:
                    AlarmTime = pickle.load(f2)
            except Exception as e:
                AlarmTime_in_seconds = AlarmTime
                return AlarmTime_in_seconds
        else:
            print ('AlarmNumber passed to Function Get_AlarmTime_in_Seconds not valid ')

        AlarmTime_in_seconds = ((AlarmTime['H']*60*60) + (AlarmTime['M']*60) + AlarmTime['S'])
        return AlarmTime_in_seconds
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Get_AlarmTime_in_Seconds')
        GPIO.cleanup()
        quit()

def GPIO_Call(Buzzer, LEDFlash):
    """
    GPIO_Call Function:
    Take in Booleans and sets corresponding GPIO Outputs

    Args:Buzzer, LEDFlash

    Returns: None
    """
    try:
        if Buzzer:
            GPIO.output(21, 1)
        else:
            GPIO.output(21, 0)

        if LEDFlash:
            GPIO.output(20, 1)
        else:
            GPIO.output(20, 0)
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function GPIO_Call')
        GPIO.cleanup()
        quit()


def F_Alarm_Active(AlarmTime, ActualTime, AlarmButtonPressed, LEDFlash, Buzzer, AlarmHappened):
    """
    F_Alarm_Active Function:
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
            AlarmButtonPressed = False
            Buzzer = False
            LEDFlash = False
            GPIO_Call(Buzzer, LEDFlash)
            sleep(0.25)
        # Set condition for if alarm has gone off and user hasnt deactivated after 10 secs of beeping and 2 min silence
        elif (ActualTime >= (AlarmTime + (2*60))) and (ActualTime < (AlarmTime + (10*60))):
            if Buzzer:
                Buzzer = False
                LEDFlash = False
            elif not Buzzer:
                Buzzer = True
                LEDFlash = True
            GPIO_Call(Buzzer, LEDFlash)
            sleep(0.25)
        # set condition for 30 secs before alarm time
        elif (ActualTime >= (AlarmTime - 30)) and (ActualTime < (AlarmTime - 10)):
            AlarmHappened = True
            if LEDFlash:
                LEDFlash = False
            elif not LEDFlash:
                LEDFlash = True
            Buzzer = False
            GPIO_Call(Buzzer, LEDFlash)
            sleep(0.5)
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
            sleep(0.25)
        # set condition for 2 min slience period of alarm
        elif (ActualTime >= AlarmTime) and (ActualTime < (AlarmTime + (2*60))):
            AlarmHappened = True
            Buzzer = False
            LEDFlash = False
            GPIO_Call(Buzzer, LEDFlash)
            sleep(0.5)
        # set condition for sleeping alarm if over 10 mins to go
        elif (ActualTime < (AlarmTime - (10*60))):
            AlarmButtonPressed = False
            sleep(1) # preserve processor
        else:
            AlarmButtonPressed = False
            sleep(0.5)# preserve processor

        return [AlarmHappened, AlarmButtonPressed, LEDFlash, Buzzer]

    except KeyboardInterrupt:
        print ("Keyboard Interruption in F_Alarm_Active")
        GPIO.cleanup()
        quit()

def F_AlarmButtonPressed():
    AlarmButtonPressed = True
    Buzzer = False
    LEDFlash = True
    GPIO_Call(Buzzer, LEDFlash)
    sleep(0.5)
    Buzzer = False
    LEDFlash = False
    GPIO_Call(Buzzer, LEDFlash)
    return AlarmButtonPressed

# #trigger event for alarm deactivation
GPIO.add_event_detect(8, GPIO.RISING, bouncetime=300)

#trigger event for alarm deactivation
GPIO.add_event_detect(7, GPIO.RISING, bouncetime=300)

def main():
    """
    Main Funtion:
    Runs in constant while loop checking status of alarm (on/off),
    If alarm on it calls F_Alarm_Active function
    """
    #set up initial variables
    Alarm1_Happened = False
    Alarm2_Happened = False
    Alarm1ButtonPressed = False # IR Button Input for deactivating alarm
    Alarm2ButtonPressed = False
    Alarm1Time = 1
    Alarm2Time = 1
    LEDFlash = False
    Buzzer = False
    Alarm_Number = None

    try:
        while True:
            try:
                with open('Alarm1Active.pickle' , 'rb') as A1:
                    Alarm1Active = pickle.load(A1)
            except EOFError:
                Alarm1Active = Alarm1Active

            if Alarm1Active or Alarm1_Happened:
                Alarm_Number = 1
                Alarm1Time = Get_AlarmTime_in_Seconds(Alarm1Time, Alarm_Number)
                ActualTime = Get_ActualTime_in_Seconds()
                if GPIO.event_detected(8):
                    Alarm1ButtonPressed = F_AlarmButtonPressed()
                [Alarm1_Happened, Alarm1ButtonPressed, LEDFlash, Buzzer] = F_Alarm_Active(Alarm1Time, ActualTime, \
                    Alarm1ButtonPressed, LEDFlash, Buzzer, Alarm1_Happened)
            else:
                sleep(0.5) #preserve processor

            try:
                with open('Alarm2Active.pickle' , 'rb') as A2:
                    Alarm2Active = pickle.load(A2)
            except EOFError:
                Alarm2Active = Alarm2Active

            if Alarm2Active or Alarm2_Happened:
                Alarm_Number = 2
                Alarm2Time = Get_AlarmTime_in_Seconds(Alarm2Time, Alarm_Number)
                ActualTime = Get_ActualTime_in_Seconds()
                if GPIO.event_detected(7):
                    Alarm2ButtonPressed = F_AlarmButtonPressed()
                [Alarm2_Happened, Alarm2ButtonPressed, LEDFlash, Buzzer] = F_Alarm_Active(Alarm2Time, ActualTime, \
                    Alarm2ButtonPressed, LEDFlash, Buzzer, Alarm2_Happened)
            else:
                sleep(0.5) #preserve processor

    except KeyboardInterrupt:
        print ("Keyboard Interuption in main")
        GPIO.cleanup()
        quit()

if __name__ == '__main__':
    main()
