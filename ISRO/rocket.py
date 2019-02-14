##############################Importing Libraries and programs#######################
import pygame                                                                       #For game
import control                                                                      #Your program 1
import control2                                                                     #Your program 2
import time                                                                         #For delay
import math                                                                         #For trignometric operations
pygame.init()                                                                       #Initialising pygame library
pygame.mixer.init()                                                                 #Initialise pygame mixer for audio files
pygame.font.init()                                                                  #Initialising font to write on screen 
speech=pygame.mixer.Sound('Images\speech.wav')                                      #Speech message
man_count=pygame.mixer.Sound('Images\launch.wav')                                   #Rocket count down
win=pygame.display.set_mode((750,500))                                              #Create display window
pygame.display.set_caption('Rocket Launch!!!!!!!!')                                 #Set title for game window
bg=pygame.image.load('Images\LaunchPad.jpg')                                        #Obtain image of launch pad as background
bg=pygame.transform.scale(bg,(750,500))                                             #Resize background
bg2=pygame.image.load('Images\sky.jpg')                                             #Second Background
bg3=pygame.image.load('Images\space.jpg')                                           #Third background
earth=pygame.image.load('Images\earth.png')                                         #Earth image
earth=pygame.transform.scale(earth,(300,300))                                        #Resize earth image
font = pygame.font.SysFont('Comic Sans MS', 20)                                     #For displaying fonts and object font is created
win.blit(bg,(0,0))                                                                  #Draw the background
pygame.display.update()                                                             #Update the pygame display
count=[]                                                                            #Empty list which will be stored with images of the countdown
rocket_velx=0                                                                       #Rocket's velocity in x direction
rocket_vely=0                                                                       #Rocket's velocity in y direction
rocket_altitude=0                                                                   #Rocket's altitude from sea level
rocket_horizontal=0                                                                 #Rocket's horizontal distance
rocket_accx=0                                                                       #Rocket's acceleration in x direction
rocket_accy=0                                                                       #Rocket's acceleration in y direction
rocket_mass=320                                                                     #Rocket's initial mass in tonnes assuming it is PSLV
rocket_ang=90                                                                       #Rocket's orientation
fuel_acc=4200                                                                       #Fuel acceleration rate for 1st stage
booster_count=0                                                                     #Number of booster to be in rocket
fly_time=0                                                                          #Time taken from beginning of flight
l_time=0                                                                            #Time taken for one loop
speed=1                                                                             #Fast Forward or slow motion
b_seperate=c_seperate=u_seperate=False                                              #
deployed=False                                                                      #
earth_core=[0,0]
rocket_coord=[0,0]                                                                  #
for i in range(11):                                                                 #Loop to store images
    count.append(pygame.image.load('Images\\'+str(i)+'.jpg'))                       #Append the ith image to the list as pygame surface
    count[i]=pygame.transform.scale(count[i],(100,100))                             #Scale the ith image to 100x100
def seperate_b(rocket_booster,b_horizontal,b_altitude):                             #
    for n,i in enumerate(rocket_booster):                                           #
        i,tl=rot_center(i,80)                                                       #
        win.blit(i,(int(b_horizontal+n*100//(booster_count-1)),int(b_altitude)))    #
    pygame.display.update()                                                         #
def seperate_c(rocket_core_detached,c_horizontal,c_altitude):                       #
    rot_core,tl=rot_center(rocket_core_detached,80)                                 #
    win.blit(rot_core,(int(c_horizontal),int(c_altitude)))                          #
    pygame.display.update()                                                         #
                                                                                    #
##############################Rotating image#########################################
def rot_center(rocket, rocket_ang):                                                 #Function for rotating the rocket and maintaining its position
    angle=rocket_ang-90                                                             #We have to calculate the angle by which the rocket should be rotated clockwise so we subtract 90 offset
    rect_1=list(rocket.get_rect())                                                  #Get dimensions of rocket image as a list.[0,0,widht,height]
    loc = rocket.get_rect().center                                                  #Center of rocket
    rot_sprite = pygame.transform.rotate(rocket, angle)                             #Rotating the rocket image by angle
    rect_2=list(rot_sprite.get_rect())                                              #Get dimensions of rocket image as a list.[0,0,width,height]
    rot_sprite.get_rect().center = loc                                              #Reset position of center of image
    top_left=((rect_2[2]-rect_1[2])//2,(rect_2[3]-rect_1[3])//2)                    #Position by which top left should be changed in x and y direction for center of rotation to be in same place
    return rot_sprite,top_left                                                      #
#############################Select rocket image#####################################
def rocket_select():                                                                #For choosing the appropriate rocket
    pygame.event.get()                                                              #To prevent the game from crashing pygame should regularly interact with the OS so it asks the OS about all events occuring like keypress
    speech.play()                                                                   #Play Audio file
    payload=input('Enter the payload(in Tonnes):')                                  #Get the payload capacity from the user
    rocket_type,booster_count=control.get_rocket(payload)                           #Call the control station to get rocket type(a string)
    rocket=pygame.image.load('Images\\'+rocket_type+'.png')                         #Get rocket image from computer
    return(rocket,rocket_type,booster_count)                                        #Returns the pygame surface of the required rocket
#############################From 10 to 0############################################
def count_down():                                                                   #Function for initiating count down sequence
    launch=False                                                                    #When launch is True rocket will launch
    count_down=10                                                                   #Initial count is 10
    man_count.play()                                                                #Play countdown audio file
    pygame.time.delay(1000)                                                         #Wait for 1 second  
    while(not(launch)):                                                             #Loop to count down to 0 and launch
        pygame.event.get()                                                          #To prevent the game from crashing pygame should regularly interact with the OS so it asks the OS about all events occuring like keypress
        launch=control.launch_permission(count_down)                                #Call control station giving the count and to check if rocket can launch
        win.blit(rocket,(290,125))                                                  #Draw the rocket on the screen
        win.blit(count[count_down],(600,0))                                         #Draw the count on the screen
        pygame.display.update()                                                     #Update the display to reflect the changes
        count_down-=1                                                               #Count down once
        pygame.time.delay(1000)                                                     #Wait for 1 second
###########################Initialising mass,thrust and velocities###################                                                                                    
def fly(rocket):                                                                    #Function to control rocket flight
    rocket_altitude=rocket_horizontal=rocket_velx=rocket_vely=0                     #
    rocket_mass=320                                                                 #
    fuel_acc=4200                                                                   #
    fly_time=0                                                                      #
    l_time=0                                                                        #
    speed=1                                                                         #
################################Lift-Off#############################################
    while(rocket_altitude<.0986):                                                   #When rocket altitude is below .025 km (25 meters) from sea level
        time1=time.time()                                                           #
        pygame.event.get()                                                          #To prevent the game from crashing pygame should regularly interact with the OS so it asks the OS about all events occuring like keypress
        rocket_accx,rocket_accy,rocket_velx,rocket_vely,rocket_ang,rocket_altitude,rocket_horizontal,rocket_mass,b_seperate,c_seperate,u_seperate,l_time,deployed=control.rocket_control(rocket_horizontal,rocket_altitude,rocket_mass,rocket_velx,rocket_vely,l_time)
                                                                                    #Get rocket's acceleration in y direction
        keys=pygame.key.get_pressed()                                               #
        if keys[pygame.K_LEFT]:                                                     #
            speed/=2                                                                #
        if keys[pygame.K_RIGHT]:                                                    #
            speed*=2                                                                #            
        win.blit(bg,(0,0))                                                          #
        win.blit(rocket,(290,125-rocket_altitude*5000))                             #Increase rocket altitude
        pygame.display.update()                                                     #Update the display to reflect the changes
        pygame.time.delay(12)                                                       #Wait for 12 milli seconds (a loop takes more than 12 milli seconds)
        l_time=(time.time()-time1)*speed                                            #
        fly_time+=l_time                                                            #
################################First flight#########################################
    while(not(b_seperate)):                                                         #Till stage seperation
        time1=time.time()                                                           #
        pygame.event.get()                                                          #To prevent the game from crashing pygame should regularly interact with the OS so it asks the OS about all events occuring like keypress
        rocket_accx,rocket_accy,rocket_velx,rocket_vely,rocket_ang,rocket_altitude,rocket_horizontal,rocket_mass,b_seperate,c_seperate,u_seperate,l_time,deployed=control.rocket_control(rocket_horizontal,rocket_altitude,rocket_mass,rocket_velx,rocket_vely,l_time,rocket_ang)
        keys=pygame.key.get_pressed()                                               #
        if keys[pygame.K_LEFT]:                                                     #
            speed/=2                                                                #
        if keys[pygame.K_RIGHT]:                                                    #
            speed*=2                                                                #            
        rot_rocket,top_left=rot_center(rocket,rocket_ang)                           #
        win.blit(bg2,(-1000-(rocket_horizontal*1000)//625,-2500+(rocket_altitude*1000)//370))#Draw new background
        win.blit(rot_rocket,(290-top_left[0]+(rocket_horizontal*50//300),125-top_left[1]-(rocket_altitude*30)//100))
        altitude = font.render('Rocket Altitude(km):'+str(round(rocket_altitude,3)), False, (0, 0, 0))
        horizontal=font.render('Horizontal Distance(km):'+str(round(rocket_horizontal,3)), False, (0, 0, 0))
        mass = font.render('Rocket Mass(tons):'+str(round(rocket_mass,3)), False, (0, 0, 0))
        f_time=font.render('Time(s):'+str(round(fly_time,3)), False, (0, 0, 0))     #
        h_vel=font.render('Horizontal Velocity(km/s):'+str(round(rocket_velx/1000,3)),False,(0,0,0))
        win.blit(altitude,(375,380))                                                #
        win.blit(mass,(375,400))                                                    #
        win.blit(horizontal,(375,420))                                              #
        win.blit(h_vel,(375,440))                                                   #
        win.blit(f_time,(375,460))                                                  #  
        pygame.display.update()                                                     #
        pygame.time.delay(12)                                                       #Wait for 12 milli seconds (a loop takes more than 12 milli seconds)
        l_time=(time.time()-time1)*speed                                            #
        fly_time+=l_time                                                            #
    b_altitude=125-top_left[1]-(rocket_altitude*30)//32+100                         #
    b_horizontal=290-top_left[0]+(rocket_horizontal*50//50)+7                       #
###############################Booster Separation####################################
    while(not(c_seperate)):                                                         #
        time1=time.time()                                                           #
        pygame.event.get()                                                          #
        rocket_accx,rocket_accy,rocket_velx,rocket_vely,rocket_ang,rocket_altitude,rocket_horizontal,rocket_mass,b_seperate,c_seperate,u_seperate,l_time,deployed=control.rocket_control(rocket_horizontal,rocket_altitude,rocket_mass,rocket_velx,rocket_vely,l_time,rocket_ang)
        keys=pygame.key.get_pressed()                                               #
        if keys[pygame.K_LEFT]:                                                     #
            speed/=2                                                                #
        if keys[pygame.K_RIGHT]:                                                    #
            speed*=2                                                                #            
        rot_rocket,top_left=rot_center(rocket_core,rocket_ang)                      #
        win.blit(bg2,(-1000-(rocket_horizontal*1000)//625,-2500+(rocket_altitude*1000)//370))#Draw new background
        win.blit(rot_rocket,(290-top_left[0]+(rocket_horizontal*50//300),125-top_left[1]-(rocket_altitude*30)//100))
        altitude = font.render('Rocket Altitude(km):'+str(round(rocket_altitude,3)), False, (0, 0, 0))
        horizontal=font.render('Horizontal Distance(km):'+str(round(rocket_horizontal,3)), False, (0, 0, 0))
        mass = font.render('Rocket Mass(tons):'+str(round(rocket_mass,3)), False, (0, 0, 0))
        f_time=font.render('Time(s):'+str(round(fly_time,3)), False, (0, 0, 0))     #
        h_vel=font.render('Horizontal Velocity(km/s):'+str(round(rocket_velx/1000,3)),False,(0,0,0))        
        win.blit(altitude,(375,380))                                                #
        win.blit(mass,(375,400))                                                    #
        win.blit(horizontal,(375,420))                                              #
        win.blit(h_vel,(375,440))                                                   #
        win.blit(f_time,(375,460))                                                  #  
        pygame.time.delay(12)                                                       #Wait for 12 milli seconds (a loop takes more than 12 milli seconds)
        l_time=(time.time()-time1)*speed                                            #
        fly_time+=l_time                                                            #
        b_horizontal-=4                                                             #
        b_altitude+=6                                                               #
        seperate_b(rocket_booster,b_horizontal,b_altitude)                          #
    c_altitude=125-top_left[1]-(rocket_altitude*30)//100                            #
    c_horizontal=290-top_left[0]+(rocket_horizontal*50//300)                        #
#####################################################################################
    while(not(u_seperate)):                                                         #
        time1=time.time()                                                           #
        pygame.event.get()                                                          #
        rocket_accx,rocket_accy,rocket_velx,rocket_vely,rocket_ang,rocket_altitude,rocket_horizontal,rocket_mass,b_seperate,c_seperate,u_seperate,l_time,deployed=control.rocket_control(rocket_horizontal,rocket_altitude,rocket_mass,rocket_velx,rocket_vely,l_time,rocket_ang)
        keys=pygame.key.get_pressed()                                               #
        if keys[pygame.K_LEFT]:                                                     #
            speed/=2                                                                #
        if keys[pygame.K_RIGHT]:                                                    #
            speed*=2                                                                #            
        rot_rocket,top_left=rot_center(rocket_upper,rocket_ang)                     #
        win.blit(bg2,(-1000-(rocket_horizontal*1000)//625,-2500+(rocket_altitude*1000)//370))#Draw new background
        win.blit(rot_rocket,(290-top_left[0]+(rocket_horizontal*50//300),125-top_left[1]-(rocket_altitude*30)//100))
        altitude = font.render('Rocket Altitude(km):'+str(round(rocket_altitude,3)), False, (0, 0, 0))
        horizontal=font.render('Horizontal Distance(km):'+str(round(rocket_horizontal,3)), False, (0, 0, 0))
        mass = font.render('Rocket Mass(tons):'+str(round(rocket_mass,3)), False, (0, 0, 0))
        f_time=font.render('Time(s):'+str(round(fly_time,3)), False, (0, 0, 0))     #
        h_vel=font.render('Horizontal Velocity(km/s):'+str(round(rocket_velx/1000,3)),False,(0,0,0))        
        win.blit(altitude,(375,380))                                                #
        win.blit(mass,(375,400))                                                    #
        win.blit(horizontal,(375,420))                                              #
        win.blit(h_vel,(375,440))                                                   #
        win.blit(f_time,(375,460))                                                  #  
        pygame.time.delay(12)                                                       #Wait for 12 milli seconds (a loop takes more than 12 milli seconds)
        l_time=(time.time()-time1)*speed                                            #
        fly_time+=l_time                                                            #
        c_horizontal-=4                                                             #
        c_altitude+=6                                                               #
        seperate_c(rocket_core_detached,c_horizontal,c_altitude)                    #
    rocket_coord=[0,rocket_altitude+6400]                                           #
    apogee=perigee=rocket_altitude+6400                                             #
    rect=list(rocket_upper.get_rect())                                              #Get dimensions of rocket image as a list.[0,0,widht,height]
    rocket_upper_s=pygame.transform.scale(rocket_upper,(rect[2]//5,rect[3]//5))     #
    pygame.display.quit()                                                           #
    win2=pygame.display.set_mode((1000,650))                                        #Create display window
    pygame.display.set_caption('Rocket Launch!!!!!!!!')                             #Set title for game window
    apo=peri='Calculating'
    while(not(deployed)):                                                           #
        time1=time.time()                                                           #
        pygame.event.get()                                                          #
        rocket_coord,rocket_velx,rocket_vely,apogee,perigee,rocket_altitude,rocket_ang,l_time,found=control2.orbit_control(earth_core,rocket_coord,rocket_velx,rocket_vely,l_time,apogee,perigee)
        keys=pygame.key.get_pressed()                                               #
        if keys[pygame.K_LEFT]:                                                     #
            speed/=2                                                                #
        if keys[pygame.K_RIGHT]:                                                    #
            speed*=2                                                                #
        win2.blit(bg3,(0,0))                                                        #Draw space background
        win2.blit(earth,(300,125))                                                  #Draw the earth at the center of the image
        rad=math.atan2(rocket_coord[1]-earth_core[1],rocket_coord[0]-earth_core[0]) #
        alt_x=round(rocket_altitude*math.cos(rad)/32)                               #
        alt_y=round(rocket_altitude*math.sin(rad)/32)                               #
        if found:                                                                   #
            apo=str(round(apogee))                                                  #
            peri=str(round(perigee))                                                #
        rot_rocket,top_left=rot_center(rocket_upper_s,rocket_ang)                   #
        apog=font.render('Apogee:'+apo, False, (255, 255, 255))                     #
        perig=font.render('Perigee:'+peri, False, (255, 255, 255))                  #
        win2.blit(rot_rocket,(int(500+alt_x),int(325-alt_y)))                       #
        win2.blit(apog,(775,580))                                                   #   
        win2.blit(perig,(775,605))                                                  #
        pygame.display.update()                                                     #
        pygame.time.delay(12)                                                       #Wait for 12 milli seconds (a loop takes more than 12 milli seconds)
        l_time=(time.time()-time1)*speed                                            #
        fly_time+=l_time                                                            #
#####################################################################################        
rocket,rocket_type,booster_count=rocket_select()                                    #Call function to select rocket,and rocket's mass
win.blit(rocket,(290,125))                                                          #Draw the rocket on the screen
pygame.display.update()                                                             #Reflect the changes
count_down()                                                                        #Call count down function
rocket=pygame.image.load('Images\\'+rocket_type+'_launch.png')                      #Get rocket launch image from computer
rocket_booster=[]                                                                   #We don't know how many booster the rocket has so we have an empty list to store the boosters
for i in range(booster_count):                                                      #Store boosters in a loop by appending them
    rocket_booster.append(pygame.image.load('Images\\'+rocket_type+'_booster.png')) #Get the rocket booster image
rocket_core=pygame.image.load('Images\\'+rocket_type+'_core.png')                   #Get the rocket core and upper image
rocket_core_detached=pygame.image.load('Images\\'+rocket_type+'_core_detached.png') #Get the rocket core detached image
rocket_upper=pygame.image.load('Images\\'+rocket_type+'_upper.png')                 #Get the rocket upper stage image
win.blit(bg,(0,0))                                                                  #Overwrite window with bg image
win.blit(rocket,(290,125))                                                          #Draw rocket image on window
pygame.display.update()                                                             #Update pygame display
fly(rocket)                                                                         #Call fly function
pygame.time.delay(3000)                                                             #Wait for 3 seconds
pygame.quit()                                                                       #Quit program
#####################################################################################

#   1 frame 20 milli seconds
#   Initially 1 meter equals to 5 pixels
#   (((rocket_horizontal)//0.021231149623285184)-top_left[0],(500-(rocket_altitude-0.09864302443415972)//0.1227392190799033014)-top_left[1])
