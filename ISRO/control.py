#############################################Import Essentials Libraries
import math                                 #For math operations


def get_rocket(payload):                    #To select rocket based on payload (return ("GSLV",2)or ("PSLV",6))
    if float(payload)>1.2:
        return("GSLV",2)
    else:
        return("PSLV",6)

def launch_permission(count_down):          #To launch rocket at T minus 0 seconds (When count_down is 0 return True)

    if count_down==0:
        return(True)
    else:
        return(False)
        

def rocket_control(rocket_horizontal,rocket_altitude,rocket_mass,rocket_velx,rocket_vely,l_time,rocket_ang=90): #Main function

    #rocket_horizontal is the horizontal distance travelled since launch time
    #rocket_altitude is the rocket's altitude at that moment from the sea level
    #rocket_mass is the mass of the rocket at that moment
    #rocket_velx is the velocity of the rocket in x(horizontal) direction at that moment
    #rokcet_vely is the velocity of the rocket in y(vertical) direction at that moment
    #l_time is the time difference between previous function call and current function call (can sometimes be multiplied by 2,4,8,etc to speed up the game)
    #rocket_angle is the orientation of the rocket with respect to the horizontal

    #To do:
    #Write a script to calculate the optimum mass to be ejected per second and the optimum orientation of the rocket to achieve good horizontal velocity and altitude
    #In each loop we have to have two types of mass initial mass and final mass(rocket_mass-ejected_mass) and the log of the ration of both will be used
    #Store the initial mass in another variable
    #to calculate the change in velocity in that loop
    #We have to calculate the thrust of the rocket based on the formula we derived (Fuel acceleration*ejected_mass)
    #We have to calculate the acceleration of the rocket (Thrust/mass)
    #Calculate the final mass for that loop
    #If the rocket is not oriented to the optimum angle, bring it towards that angle by decreasing the orientation everytime towards the optimum value and if
    #it exceed optimum value,bring it back to optimum value
    #If rocket mass is lesser than the mass required to eject the stage, bring it back to the correct value
    #Create boolean values b_seperate,c_seperate and u_seperate to indicate whether boosters,core and upper stages can be seperated or not based on that stage
    #When u_seperate is True this program will terminate although upper stage will still be attached to the rocket
    #Calculate the orientation of the rocket in radian
    #Calculate the acceleration of the rocket in x and y direction (subtract gravity from y acceleration)
    #Calculate the change in velocity in x and y direction and add it to previous velocities
    #Calculate the change in altitude and horizontal direction(in km divide meter value by 1000)
    #Return the values
    #The final task left you you will be seen in control2.py
    
    
    if rocket_mass>250:                     #For Initial stage with booster (no stage is sperated from the rocket)
        fuel_acc=9000                       #Fuel acceleration for first stage (Change this if you want to solve the final task left to you)
        initial_mass=rocket_mass
        ejected_mass=.8
        rocket_orient=57
        rocket_thrust=fuel_acc*ejected_mass
        rocket_acc=rocket_thrust/rocket_mass
        rocket_mass-=ejected_mass*l_time
        if rocket_mass<250:
            rocket_mass=250
        b_seperate=c_seperate=u_seperate=False
        
    elif rocket_mass>90:                    #For second stage, i.e core stage. Boosters are seperated
        if rocket_mass==250:
            rocket_mass-=20
        fuel_acc=5000                       #Fuel acceleration for second stage (Change this if you want to solve the final task left to you)
        ejected_mass=.7
        rocket_orient=20        
        initial_mass=rocket_mass
        rocket_thrust=fuel_acc*ejected_mass
        rocket_acc=rocket_thrust/rocket_mass
        rocket_mass-=ejected_mass*l_time
        if rocket_mass<90:
            rocket_mass=90
        b_seperate=True
        c_seperate=u_seperate=False
            

    elif rocket_mass>10:                    #For third stage, i.e upper stage. Core is seperated
        fuel_acc=1500                       #Fuel acceleration for upperstage (Change this if you want to solve the final task left to you)
        if rocket_mass==90:
            rocket_mass-=20
        ejected_mass=.75        
        rocket_orient=6
        initial_mass=rocket_mass
        rocket_thrust=fuel_acc*ejected_mass
        rocket_acc=rocket_thrust/rocket_mass
        rocket_mass-=ejected_mass*l_time
        if rocket_mass<10:
            rocket_mass=10
        b_seperate=c_seperate=True
        u_seperate=False
            
        
    else:                                   #Upper stage has burnt its fuel
        fuel_acc=0                          #No more acceleration rocket is free falling
        ejected_mass=0        
        rocket_orient=0
        initial_mass=rocket_mass
        rocket_thrust=fuel_acc*ejected_mass
        rocket_acc=rocket_thrust/rocket_mass
        rocket_mass-=ejected_mass*l_time
        b_seperate=c_seperate=u_seperate=True
        

    if rocket_ang>rocket_orient:
        rocket_ang-=10*l_time
        if rocket_ang<rocket_orient:
            rocket_ang=rocket_orient
    rad=rocket_ang/180*math.pi
    rocket_accx=rocket_acc*math.cos(rad)
    rocket_accy=rocket_acc*math.sin(rad)-9.8
    rocket_velx+=fuel_acc*math.cos(rad)*math.log(initial_mass/rocket_mass)
    rocket_vely+=fuel_acc*math.sin(rad)*math.log(initial_mass/rocket_mass)-9.8*l_time
    rocket_altitude+=(rocket_vely*l_time-0.5*rocket_accy*l_time**2)/1000
    rocket_horizontal+=(rocket_velx*l_time-0.5*rocket_accx*l_time**2)/1000

    
        

    deployed=False                          #Satellite will be deployed only when rocket is orbiting the earth dont change this


    return(rocket_accx,rocket_accy,rocket_velx,rocket_vely,rocket_ang,rocket_altitude,rocket_horizontal,rocket_mass,b_seperate,c_seperate,u_seperate,l_time,deployed)
    










