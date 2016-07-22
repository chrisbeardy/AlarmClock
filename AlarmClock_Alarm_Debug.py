# encoding: utf-8
"""
AlarmClock_Alarm.py

Script 2 of 2 from AlarmClock Project:
Script for comparing alarm time to actual time, triggering the alarm and disabling the alarm

Created by Christopher Beard on 16-07-2016.
#Copyright statement, share but attribute
"""

from time import sleep #check this
#import AlarmClock_Screen
#import RPi

def GPIO_Call(Buzzer, LEDFlash):
    """
    GPIO_Call Fucntion:
    Take in Booleans and sets corresponding GPIO Outputs

    Args:Buzzer, LEDFlash
 
    Returns: None 
    """
    # set up GPIO
    if Buzzer == True:
        pass # set GPIO true 
    else:
        pass # set GPIO false

    if LEDFlash == True:
        pass # set GPIO True
    else:
        pass # set GPIO False 
    

def Alarm_Active(AlarmTime, ActualTime, AlarmButtonPressed, LEDFlash, Buzzer, AlarmHappened):
    """
    Alarm_Active Function:
    Takes in Alarm parameters the triggers alarm at correct time

    Args: AlarmTime, ActualTime, AlarmButtonPressed, LEDFlash, Buzzer, AlarmHappened

    Returns: AlarmHappened, AlarmButtonPressed, LEDFlash, Buzzer
    """
    
    try:
        # if the alarm has gone off and then the user deactivates it sleep for 20 mins 
        if (AlarmButtonPressed == True) and (AlarmHappened == True):
            print '1'
            Buzzer = False
            LEDFlash = False
            AlarmHappened = False
            AlarmButtonPressed = False   
            GPIO_Call(Buzzer, LEDFlash)                     
            #sleep(20*60) #20 mins in seconds
            sleep(10)
        # If actual time is greater than the alarm time + 10 mins from above e.g. 03:00 > 02:40 then 
        # the alarm can never go off as 24hr clock so actual time will cycle round at midnight 
        elif ActualTime >= (AlarmTime + (10*60)):
            print '2'
            AlarmHappened = False
            Buzzer = False
            LEDFlash = False
            GPIO_Call(Buzzer, LEDFlash)            
            sleep(0.25) # sleep for two hours, reduce for initial debug, maybe inly sleep for 0.25 to reduce processor
        # Set condition for if alarm has gone off and user hasnt deactivated after 10 secs of beeping and 2 min silence
        elif (ActualTime >= (AlarmTime + (2*60))) and (ActualTime < (AlarmTime + (10*60))):
            print '3'
            if Buzzer == True:
                Buzzer = False
                LEDFlash = False
            elif Buzzer == False:
                Buzzer = True
                LEDFlash = True
            GPIO_Call(Buzzer, LEDFlash)
            sleep(1)            
        # set condition for 30 secs before alarm time
        elif (ActualTime >= (AlarmTime - 30)) and (ActualTime < (AlarmTime - 10)):
            print '4'
            AlarmHappened = True
            if LEDFlash == True:
                LEDFlash = False
            elif LEDFlash == False:
                LEDFlash = True
            Buzzer = False
            GPIO_Call(Buzzer, LEDFlash)
            print Buzzer
            print LEDFlash
            sleep(1)
        #set condition for 10 secs before alarm time (beeping)
        elif (ActualTime >= (AlarmTime - 10)) and (ActualTime < AlarmTime):
            print '5'
            AlarmHappened = True
            if Buzzer == True:
                Buzzer = False
                LEDFlash = False
            elif Buzzer == False:
                Buzzer = True
                LEDFlash = True                
            GPIO_Call(Buzzer, LEDFlash)
            print Buzzer
            print LEDFlash
            sleep(1)            
        # set condition for 2 min slience period of alarm
        elif (ActualTime >= AlarmTime) and (ActualTime < (AlarmTime + (2*60))):
            print '6'
            AlarmHappened = True
            Buzzer = False
            LEDFlash = False
            GPIO_Call(Buzzer, LEDFlash)
            sleep(0.25)
        # set condition for sleeping alarm if over 30 secsto go
        elif (ActualTime < (AlarmTime - (30))):
            print '7'
            sleep(0.25) 
        else:
            print '8'

        return [AlarmHappened, AlarmButtonPressed, LEDFlash, Buzzer]

    except KeyboardInterrupt:
        #GPIO_Cleanup()
        print "Keyboard Interruption in Alarm_Active"
    except:
        #GPIO_Cleanup()
        print "Error in Alarm_Active Function on AlarmClock_Alarm"            

        
def main():
    """
    Main Funtion:
    Runs in constant while loop checking status of alarm (on/off), 
    If alarm on it calls Alarm_Active function
    """
    #set up initial variables
    ActualTime = 71999
    Alarm1Time = 20*60*60
    Alarm1Active = True
    Alarm1_Happened = False  # Can you do arrays python or does list work?
    #Alarm2_Happened = False
    Alarm1ButtonPressed = True # IR Button Input for deactivating alarm
    #Alarm2ButtonPressed = False 
    LEDFlash = False
    Buzzer = False
    #Alarm_Number = None

    try:
        while True:
            if Alarm1Active == True:
                #Alarm_Number = 1
                #Alarm1Time = AlarmClock_Screen.Get_AlarmTime(Alarm_Number)
                #ActualTime = AlarmClock_Screen.Get_ActualTime()
                #AlarmButtonGPIO = None # Assign Later
                #set up input GPIO as interupt if high then set Alarm1ButtonPressed = True
                #call function
                print 'Going into function'
                [Alarm1_Happened, Alarm1ButtonPressed, LEDFlash, Buzzer] = Alarm_Active(Alarm1Time, ActualTime, \
                    Alarm1ButtonPressed, LEDFlash, Buzzer, Alarm1_Happened) # check syntax
            else:
                sleep(3600) #sleep for 1 hour in seconds to preserve battery, take out for initial debug
                
            #if AlarmClock_Screen.Alarm2Active == True:
             #   Alarm_Number = 2
              #  Alarm2Time = AlarmClock_Screen.Get_AlarmTime(Alarm_Number)
               # ActualTime = AlarmClock_Screen.Get_ActualTime()
                #AlarmButtonGPIO = None # Assign Later
                #set up input GPIO as interupt if high then set Alarm1ButtonPressed = True
                #call function
                #Alarm2_Happened, Alarm2ButtonPressed, LEDFlash, Buzzer = Alarm_Active(Alarm2Time, ActualTime, \
               #     Alarm2ButtonPressed, LEDFlash, Buzzer, Alarm2_Happened) # check syntax
            #else:
             #   sleep(3600) #sleep for 1 hour in seconds to preserve battery, take out for initial debug and pass

    except KeyboardInterrupt:
        #GPIO_Cleanup() # check correct 
        print "Keyboard Interuption in main"
    except:
        #GPIO_Cleanup() #check
        print "Error in Main of AlarmClock_Alarm"

if __name__ == '__main__':
    main()