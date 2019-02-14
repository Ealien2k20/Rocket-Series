#########################################################################################################Import essential Libraries
import math                                                                                     #For math operations


def orbit_control(earth_core,rocket_coord,rocket_velx,rocket_vely,l_time,apogee,perigee):

    #earth_core is the coordinates of earth [0,0] (it is a list)
    #rocket_coord is the coordinates of the rocket at that instant [x,y] (it is a list)
    #rocket_velx and rocket_vely are the velocities of the rocket in x and y direction respectively
    #l_time is the time difference between previous call and current call of this function
    #apogee and perigee and the calculated values of apogee and perigee which may have to be corrected if incorrect or left as it is if correct.

    #To do:
    #Calculate the rocket's altitude using distance formula between 2 points. Use coordinates of rocket and earth to do that.
    #Check if current altitude is greater than or lesser than the calculated apogees and perigees respectively and update them if required.
    #Find the inclination of the rocket with respect to horizontal theta1 tan inverse((y2-y1)/(x2-x2)) which has to be converted to radians
    #Find theta2 = -180+theta1 which has to be converted to radians
    #When theta1 lies between 30 degree and 33 degree, reset apogee and perigee with current rocket altitude
    #this is because apogee and perigee varies with each orbit, though this doesn't happen theoreticaly
    #due to accumulation of floating point approximation error over the time, the values change.
    #Calculate the acceleration due to gravity G*M/r^2
    #Calculate the acceleration in x and y direction
    #Calculate the velocities in x and y direction using acceleration v=u+at
    #Calculate the variation in rocket coordiantes using velocities, s=vt-(1/2)*a*t^2
    #Calculate the tilt of the rocket inverse tan(vy/vx)
    #Calculate the new altitude
    #Set boolean variable found to True if theta 1 is between 91 and 93 degree. This will be used to update perigee and apogee on screen after one orbit.
    
    rocket_altitude=math.sqrt((earth_core[0]-rocket_coord[0])**2+(earth_core[1]-rocket_coord[1])**2)

    if rocket_altitude>apogee:
        apogee=rocket_altitude
    if rocket_altitude<perigee:
        perigee=rocket_altitude

    ang=math.atan2(rocket_coord[1],rocket_coord[0])/math.pi*180

    theta=-180+ang

    rad=theta*math.pi/180

    if ang>30 and ang<33:
        apogee=perigee=rocket_altitude

    

    
    G=6.67408*10**-11                                                   #Universal gravitational constant
    M=5.972*10**24                                                      #Mass of the earth

    g=G*M/((rocket_altitude*1000)**2)
    
    accx=g*math.cos(rad)
    accy=g*math.sin(rad)

    rocket_velx+=accx*l_time
    rocket_vely+=accy*l_time

    rocket_coord[0]+=(rocket_velx*l_time-0.5*accx*l_time**2)/1000
    rocket_coord[1]+=(rocket_vely*l_time-0.5*accy*l_time**2)/1000

    rocket_ang=math.atan2(rocket_vely,rocket_velx)/math.pi*180
    rocket_altitude=math.sqrt((earth_core[0]-rocket_coord[0])**2+(earth_core[1]-rocket_coord[1])**2)

    if ang>90 and ang<93:
        found=True
    else:
        found=False

        
        
    
    return(rocket_coord,rocket_velx,rocket_vely,apogee,perigee,rocket_altitude,rocket_ang,l_time,found)
    

    #The final task left to you is to circularise the orbit. So, you need more fuel even after the upper stage so that you can burn it in apogee
    #to make the perigee move farther
    #away from the earth

    #You need to know the apogee and when rocket altitude is equal to apogee, burn the fuel. You have to include extra
    #variable to calculate change in acceleration in x and y direction.
    
