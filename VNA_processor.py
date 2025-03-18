#Class to remote control the VNA 
import RsInstrument, time
import numpy as np
import pickle, datetime
from RsInstrument import *

class VNA:
    def __init__(self, LAN = 'TCPIP::10.42.1.55::5025::SOCKET'):
        self.instr = RsInstrument(LAN)
        #Set the timeout time to avoid annoying freezes for the default 10 s
        self.instr.visa_timeout = 3000

        #This timeout time is the max time for the VNA subsystems to 
            #finish carrying out operations
        self.instr.opc_timeout = 30000

    def set_trace_averaging(self, navg=10, channel=1):
        '''
        Parameters: Channel (default is 1) and navg (default is 10)
        Sets the trace averaging feature, usually not necessary
        '''
        self.instr.write('SENS'+str(channel)+':AVER:COUN '+str(navg)+'; :AVER ON')
        
        #self.instr.write('SENS<'+channel+'>:AVER:COUN 10; :AVER ON')

    def get_trace_measurement(self, navg=10,channel=1, tracename='Trc1'):
        '''
        Parameters: Number of points to average over (default is 10),
        Channel (default is 1), Trace name (passed in as a string),
        Note: To disable averaging, set navg=1
        Returns: numpy array containing trace values
        '''
        
        #First clear the averaged data and initiate measurement
        self.instr.write('AVER:COUN '+str(navg)+'; CLE')
        #Wait for the average to fill out again (building in a slight margin)
        sweeptime = float(self.instr.query('SWE:TIME?'))
        buffertime = (navg+1) * sweeptime  

        #Now wait until 10 sweeps are done before saving the trace
        time.sleep(buffertime)
        
        
        #Measure trace and save as numpy array
        trace = self.instr.query('CALC:DATA:TRAC? \''+tracename+'\', FDAT')
        tracearr = np.array(trace.split(',')).astype('float')
        return(tracearr)

    def get_freq_values(self, nsweep=4001):
        '''
        Parameters: Trace name (optional, default is Trc1)
        Returns a numpy array containing the frequency points used in the sweep
        '''
        #Todo: find how to read off the number of sweep points
        nsweep = int(self.instr.query('SWE:POIN?'))
        start = float(self.instr.query('FREQ:STAR?'))/1000  #In MHz
        stop = float(self.instr.query('FREQ:STOP?'))/1000  #In MHz
        freq = np.linspace(start,stop, num=nsweep)
        return(freq)
        

    def close_instrument(self):
        '''
        Parameters: none
        Purpose: Closes the remote access to the instrument
        '''
        self.instr.close()

if __name__ == "__main__":

    while True:

        #example code.
        vna = VNA()
        vna.set_trace_averaging(navg=10)
        trace = vna.get_trace_measurement(tracename='Trc1')
        freqs = vna.get_freq_values()
        vna.close_instrument()

        data = {"freqs": freqs, "trace": trace}

        timestamp = datetime.datetime.now().isoformat()
        file_suffix = "pkl"
        path = f"testrun/measurement_at_{timestamp}.{file_suffix}"
        with open(path, 'wb') as outfile:
            pickle.dump(data, outfile)

        print(f"Wrote measurement to '{path}'.")
            
        time.sleep(300)
        
        



#with open("<filepath>", 'rb') as infile:
#    data = pickle.load(infile)