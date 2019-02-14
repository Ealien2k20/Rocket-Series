#############################################################################Import essential Libraries
import math                                                             #For math operations.


mass_hun=list(range(1,100))                                             #This is all the possible values of mass ejected multiplied by a factor of hundred.
                                                                        #This is because range cannot generate a range of floating point values and we have to convert
                                                                        #integer to float by dividing by hundred.

ac=1500                                                                    #Fuel acceleration for the current stage.
max_velx=0                                                              #Maximum horizontal velocity achieved by a combination of theta and ejected mass in one loop.
max_dy=0                                                                #Corresponding altitude when the Horizontal velocity is maximum.
max_vely=0                                                              #Corresponding Vertical velocity when the Horizontal velocity is maximum.
best_m=0                                                                #Best value of ejected mass for a stage calculated so far.
best_t=0                                                                #Best value of theta calculated so far.

    #Here we will be doing the same thing we did in control.py except that the rocket wont run here and we are just brute forcing all
    #possible combination of thrust and orientation to find the optimum value.
    #To do:
    #Loop through all posible values of theta (Outer loop).
    #Loop through all possible values of ejected mass (Inner loop) al values in mass_hun.
    #For each ejected mass(inner loop) do the following things.
    #Convert the mass multiplied by hundred back to value between 0-1 by division by 100.
    #Find the burn time t, for that ejected mass (Fuel mass of that stage/ejected mass).
    #Initialise the horizontal and vertical velocities and distances based on the stage.
    #For first stage they are 0 but for 2nd and 3rd stage they will be the values while the previous stage got over.
    #Initialise the total rocket mass for that stage.
    #A third inner loop inside 2nd loop is created to simulate the flight for the calculated burn time from 0 to t.
    #Instead of loop through t seconds we loop through them in step size of 20 milliseconds so we have a total of t*50 values (loop should be from 1 to t*50).
    #If you find this confusing it is just like we multiplied mass by 100, but we multiply it by 50.
    #Inside the time loop, find the correct time, current time value divided by 50.
    #Find the current orientation of the rocket in radian.
    #Store the current mass of the rocket in another variable. This will be used when calculating change in velocities.
    #Decrease the rocket mass by multiplying mass ejected in 1 second and 20 milliseconds and subtracting it from current mass
    #as mass is ejected and hence decreases.
    #Find the acceleration of the rocket (Thrust of gas divided by current rocket mass).
    #Find acceleration in x and y direction.
    #Subtract gravitational acceleration from y.
    #Find velocity variation in x and y direction using the formula we derived which uses initial and final mass for that time frame of 20 milliseconds.
    #Find distance travelled in 20 milliseconds and add it with total distance travelled until now.
    #Outside the time loop check if the altitude is greater than your specified value and the horizontal velocity calculated
    #is greater than the best value achived till now.
    #If so update the best values of theta, ejected mass, best horizontal velocity and corresponding vertical velocity.
    #Outside the mass loop print the optimum values for that particular theta.


for w in range(20,1,-1):
    for hun in mass_hun:
        m=hun/100
        t=60/m
        vx=5618.471990126066
        vy=650.3441172087391
        sy=181537.95019572318
        rocket_mass=70
        for i in range(int(t*50)):
            rad=math.pi/180*w
            initial_mass=rocket_mass
            rocket_mass-=m*1/50
            acc=ac*m/initial_mass
            ax=acc*math.cos(rad)
            ay=acc*math.sin(rad)-9.8
            vx+=ac*math.cos(rad)*math.log(initial_mass/rocket_mass)
            vy+=ac*math.sin(rad)*math.log(initial_mass/rocket_mass)-9.8*(1/50)
            sy+=vy*1/50-0.5*ay*(1/50)**2
        if sy>200000 and vx>max_velx:
            best_t=w
            best_m=m
            max_velx=vx
            max_vely=vy
            max_dy=sy
    print("The best values are(theta,m,sy,vx,vy,):",best_t,best_m,max_dy,max_velx,max_vely)
            
            
    
            
            
            
            
            


#################################################################A space to store your best values:

#The best values are(theta,m,sy,vx,vy,): 57 0.8 40653.53050629741 1210.0467116566954 1005.8085358591898
#The best values are(theta,m,sy,vx,vy,): 20 0.7 181537.95019572318 5618.471990126066 650.3441172087391
#The best values are(theta,m,sy,vx,vy,): 6 0.75 210680.8365574374 8521.347364608668 171.44861351529758

#################################################################
