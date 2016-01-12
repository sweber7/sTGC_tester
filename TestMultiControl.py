import visa
import time

def ErrorMessage(errormsg):
    print('ERROR: ' + errormsg)
    exit(0)

class Instrument:
    #Resource number the index of instruments in the list of resources (sorted by id)
    def __init__(self, ResNum):
        self.rm = visa.ResourceManager()
        resources = self.rm.list_resources()
        if len(resources) > ResNum:
            self.instrument = self.rm.open_resource(resources[ResNum]) #Currently only setting to first resource
        else:
            ErrorMessage('Resource number exceeds number of instruments')

        self.instrument.query_delay = 0.001 #Set query delay in seconds, without delay query's may not work

    def testPhysics(self):
        import antigravity


class SignalGenerator (Instrument):
    def __init__(self, ResNum):
        super(SignalGenerator, self).__init__(ResNum)

    def TestPulse(self):
        #Channel 1
        self.instrument.write('VOLT:UNIT:CH1 VPP') #Set unit/magnitude of amplitude
        self.instrument.write('APPL:PULS:CH1 1000,2.0,1.5') #apply pulse - Frequency, amplitude, offset
        self.instrument.write('TRIG:SOUR:CH1 IMM') #Signal is internally generated
        self.instrument.write('PHAS:CH1 10') #Write phase

        #Channel 2
        self.instrument.write('VOLT:UNIT:CH2 VPP') #Set unit/magnitude of amplitude
        self.instrument.write('APPL:PULS:CH2 2000,1.5,2') #apply pulse - Frequency, amplitude, offset
        self.instrument.write('TRIG:SOUR:CH2 IMM') #Signal is internally generated
        self.instrument.write('PHAS:CH1 100') #Write phase

        #Can align phase of both channels
        #PHAS:ALIGN
        for i in range (5):
            time.sleep(1)
            if i % 2:
                self.instrument.write('OUTP ON') #Can turn output on and off with this
            else:
                self.instrument.write('OUTP OFF')



class Digitizer (Instrument):
    def __init__(self, ResNum):
        super(Digitizer, self).__init__(ResNum)

    def TestGather(self):
        self.instrument.write( ":SYSTEM:HEADER OFF") #Controls whether response contains command header

        self.instrument.write( ":ACQUIRE:MODE RTIME") #Acquire in real time
        self.instrument.write( ":ACQUIRE:COMPLETE 100") #Must acquire 100% of count
        self.instrument.write( ":ACQUIRE:COUNT 16")  #Number of Averages for each waveform
        self.instrument.write( ":ACQUIRE:POINTS 100") #Analog memory depth for acquisition, ie

        self.instrument.write( ":WAVEFORM:SOURCE CHANNEL1") #Output data channel
        self.instrument.write( ":WAVEFORM:FORMAT ASCII") #Output data Format

        self.instrument.write( ":DIGITIZE CHANNEL1") #Collect data
        self.instrument.write( ":WAVEFORM:DATA?")
        self.instrument.write(':MEASURE:RESULTS?')

        time.sleep(.1)
        data = self.instrument.read()
        print(data)
        self.printData(data)

    def printData(self, data):
        import os
        import datetime
        folder = 'Data'
        dirpath = folder + '/' + datetime.datetime.now().strftime("%b %d %Hh%Mm%Ss %Y")

        #Make General data directory if it does not exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        #Make Directory for this time slot if it does not exist
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        output = open(dirpath + "/TestData.csv", 'w') #Can later put channel specific files, or aggregate
        data = str.replace(data,',', '\n') #switch to columns
        output.write(data)
        output.close()


s = SignalGenerator(0)
d = Digitizer(1)

s.TestPulse()
d.TestGather()
