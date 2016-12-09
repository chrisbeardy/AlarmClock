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

from time import sleep
import AlarmClock_Screen
import pickle
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(port, GPIO.OUT, [initial=0]) #set ports later
GPIO.setup(port, GPIO.OUT, [initial=0])
GPIO.setup(port, GPIO.IN, [pull_up_down=GPIO.PUD_DOWN])
GPIO.setup(port, GPIO.IN, [pull_up_down=GPIO.PUD_DOWN])


def Get_ActualTime_in_Seconds():
    """
    Get_ActualTime_in_Seconds Function:
    Function gets actual time from AlarmClock_Screen Script and then converts to seconds

    Args: None

    Returns: ActualTime_in_seconds
    """
    try:
        ActualTime, ActualTimeDisplay = AlarmClock_Screen.Get_ActualTime()  # get as dictionary object Hour,Mins,Secs
        ActualTime_in_seconds = ((ActualTime['H']*60*60) + (ActualTime['M']*60) + ActualTime['S'])
        return ActualTime_in_seconds
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Get_ActualTime_in_Seconds')
    except:
        print ('Error in Function Get_ActualTime_in_Seconds')
    finally:
        GPIO.cleanup()

def Get_AlarmTime_in_Seconds(Alarm_Number):
    """
    Get_AlarmTime_in_Seconds Function:
    Function gets alarm time from AlarmClock_Screen Script and then converts to seconds

    Args: Alarm_Number

    Returns: AlarmTime_in_seconds
    """
    try:
        #use pickle to get data from other script
        if Alarm_Number == 1:
            with open('AlarmTime1.pickle', 'rb') as f:
            #get as dictionary object
            AlarmTime = pickle.load(f)
        elif Alarm_Number == 2:
            with open('AlarmTime2.pickle', 'rb') as f:
            AlarmTime = pickle.load(f)
        else:
            print ('AlarmNumber passed to Function Get_AlarmTime_in_Seconds not valid ')

        AlarmTime_in_seconds = ((AlarmTime['H']*60*60) + (AlarmTime['M']*60) + AlarmTime['S'])
        return AlarmTime_in_seconds
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function Get_AlarmTime_in_Seconds')
    except:
        print ('Error in Function Get_AlarmTime_in_Seconds')
    finally:
        GPIO.cleanup()

def GPIO_Call(Buzzer, LEDFlash):
    """
    GPIO_Call Function:
    Take in Booleans and sets corresponding GPIO Outputs

    Args:Buzzer, LEDFlash

    Returns: None
    """
    try:
        if Buzzer:
            GPIO.output(port, 1) #set port later
        else:
            GPIO.output(port, 0)

        if LEDFlash:
            GPIO.output(port, 1)
        else:
            GPIO.output(port, 0)
    except KeyboardInterrupt:
        print ('KeyboardInterrupt in Function GPIO_Call')
    except:
        print ('Error in Function GPIO_Call')
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
        print ("Keyboard Interruption in Alarm_Active")
    except:
        print ()"Error in Alarm_Active Function on AlarmClock_Alarm")
    finally:
        GPIO.cleanup()

def F_Alarm1ButtonPressed(Alarm1ButtonPressed):
    return Alarm1ButtonPressed = True

def F_Alarm2ButtonPressed(Alarm2ButtonPressed):
    return Alarm2ButtonPressed = True

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
            with open('Alarm1Active.pickle' , 'rb') as A1:
                Alarm1Active = pickle.load(A1)

            if Alarm1Active:  #possibly can't do this, would need to have function
            #can't do this, needs to be pickle get
                Alarm_Number = 1
                Alarm1Time = Get_AlarmTime_in_Seconds(Alarm_Number)
                ActualTime = Get_ActualTime_in_Seconds()
                GPIO.add_event_detect(port, GPIO.RISING, callback=F_Alarm1ButtonPressed, bouncetime=300)
                [Alarm1_Happened, Alarm1ButtonPressed, LEDFlash, Buzzer] = Alarm_Active(Alarm1Time, ActualTime, \
                    Alarm1ButtonPressed, LEDFlash, Buzzer, Alarm1_Happened)
            else:
                sleep(0.25) #preserve processor

            with open('Alarm2Active.pickle' , 'rb') as A2:
                Alarm1Active = pickle.load(A2)
            if Alarm2Active:
                Alarm_Number = 2
                Alarm2Time = Get_AlarmTime_in_Seconds(Alarm_Number)
                ActualTime = Get_ActualTime_in_Seconds()
                GPIO.add_event_detect(port, GPIO.RISING, callback=F_Alarm2ButtonPressed, bouncetime=300)
                [Alarm2_Happened, Alarm2ButtonPressed, LEDFlash, Buzzer] = Alarm_Active(Alarm2Time, ActualTime, \
                    Alarm2ButtonPressed, LEDFlash, Buzzer, Alarm2_Happened)
            else:
                sleep(0.25) #preserve processor

    except KeyboardInterrupt:
        print ("Keyboard Interuption in main")
    except:
        print ("Error in Main of AlarmClock_Alarm")
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
