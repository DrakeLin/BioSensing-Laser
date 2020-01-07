#!/usr/bin/python
# .py

from includes import *
import SANTEC510_v2
import SANTEC210
import Agilent8164B
import Agilent81600B
#import JasonECL
#import PowerMeter


# Main thing
def sweep_laser(file_handle, start, stop, step): #start, stop wavelength, step scan laser (20 nano, 40 nano, 5 picometers)

    wavelengths = frange(start, stop, step)
    losses = [] #output power of ring => input 100 power and getting 50 power, losses is 50 power
    #laser = JasonECL.JasonECL(com_port = 3, home = False, verbose = False)
    laser = SANTEC510_v2.SantecLaser(gpib_address=28) #define what laser using
    #laser = SANTEC210.Santec210()
    #laser.setLaserPower(3.5)

    power_meter = Agilent8164B.Agilent8164B(gpib_address=20) #type of equipment, gpab -> laser, through computer tell laser
    power_meter.set_avg_time(5, unit = 'ms')

    #new code
    minimum = float('inf')

    for wavelength in wavelengths: 
        laser.set_wavelength(wavelength) 
        time.sleep(0.01)
        power = power_meter.read_power(read_1 = False, read_2 = True) #read the power
        time.sleep(0.01)

        #new code
        if power < minimum:
            minimum = power

        losses.append(power) #put power and print it
        print ("Wavelength: %f nm, Reading:%f dBm" % (wavelength, power))
        file_handle.write(str(wavelength)+','+str(power)+'\n') #write it into a file

    file_handle.close()

    p.figure(2)
    p.plot(wavelengths,losses,'-')
    p.xlabel('Wavelength')
    p.ylabel('Loss (dB)')
    p.savefig(file_name+'.png')
    #p.show()
    p.close()

    #returning minimum
    return minimum

# Run the program
if __name__ == "__main__":

    if not len(sys.argv) == 6:
        print "USAGE: start, stop, step are in nm"
        print "    LaserSweep chip label start stop step"
        sys.exit(1)

    #Cumulative results
    date_time=str(datetime.datetime.now())
    file_cumulative_name = "%s/%s_%d_%snm-%snm_%s-%s-%s-%s-cumulative.csv" % (dir_name, sys.argv[2], i, sys.argv[3],  sys.argv[4], \
    date_time[0:10], date_time[11:13], date_time[14:16], date_time[17:19])
    file_cumulative_handle = open(file_cumulative_name, 'w+')
    p.figure(1)
    p.xlabel('Loss (dB)')
    p.ylabel("iteration, time")
    minimums = []
    iterations = []

    # Loop over 120 iterations
    for i in range(1):
        dir_name='../../data/sweeps/%s' % sys.argv[1]

        # Create directory if it does not exist
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        date_time=str(datetime.datetime.now()) #reading time
        # Create results directory
        file_name = "%s/%s_%d_%snm-%snm_%s-%s-%s-%s.csv" % (dir_name, sys.argv[2], i, sys.argv[3],  sys.argv[4], \
        date_time[0:10], date_time[11:13], date_time[14:16], date_time[17:19])
        file_handle = open(file_name, 'w+')

        #is this file_handle necessary?
        minimum = sweep_laser(file_handle, float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])) #sweep laser and return min
        time.sleep(0.5)

        #cumulative writing
        p.figure(1)
        minimums.append(minimum)
        iterations.append(i)
        p.plot(iterations, minimums, '-')
        file_cumulative_handle.write('iteration ' + str(i+1) + ' : Minimum ' + str(minimum))

        #relative shift
        if i > 0:
            shift = minimums[i] - minimums[0]
            file_cumulative_handle.write('. Shift 1->' + str(i+1) + ' = ' + str(shift) + 'dBm' + '\n')
        else:
            file_cumulative_handle.write('\n')
    
    p.figure(1)
    file_cumulative_handle.close()
    p.savefig(file_cumulative_name + '.png')
    p.close()

    #each iteration should just show minimum => curve vs. time of each iteration
    #find relative shift, iteration shift of 1 vs 2
    #create in same script a plugin that finds minimum point, save it to another matrix => graph point in real time (window pops out)
      	
    sys.exit(0)
