"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def generateCAcode(self, prn):
        
        return CAcode
        
        
    def __init__(self, sampleRate=6e6,centreFreq=0,prn=1,acqThreshold=2,vectorSize=6000):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='GPS Signal Acquisition',   # will show up in GRC
            in_sig=[(np.complex64,vectorSize)],
            out_sig=[(np.complex64,vectorSize)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.sampleRate = sampleRate
        self.centreFreq=centreFreq
        self.prn=prn-1
        prn=self.prn
        self.CAcode=[]
        self.acqThreshold=acqThreshold
        self.lastAcquiredFreq=0
        self.acquiredFreq=0
        self.lastCodePhase=0
        self.codePhase=0
        self.samplesPerCode=int(sampleRate/1e3)
        self.portName='msg out'
        self.message_port_register_out(pmt.intern(self.portName))
        # CAcode = generateCAcode(PRN)

        #   Inputs:
        #       PRN         - PRN number of the sequence.

        #   Outputs:
        #       CAcode      - a vector containing the desired C/A code sequence
        #                   (chips).

        # --- Make the code shift array. The shift depends on the PRN number -------
        # The g2s vector holds the appropriate shift of the g2 code to generate
        # the C/A code (ex. for SV#19 - use a G2 shift of g2s(19) = 471)

        assert prn in range(0, 32)
        g2s = [5, 6, 7, 8, 17, 18, 139, 140, 141, 251,
               252, 254, 255, 256, 257, 258, 469, 470, 471, 472,
               473, 474, 509, 512, 513, 514, 515, 516, 859, 860,
               861, 862,
               145, 175, 52, 21, 237, 235, 886, 657, 634, 762, 355, 1012, 176, 603, 130, 359, 595, 68, 386]

        # --- Pick right shift for the given PRN number ----------------------------
        g2shift = g2s[prn]

        # --- Generate G1 code -----------------------------------------------------

        # --- Initialize g1 output to speed up the function ---
        g1 = np.zeros(1023)

        # --- Load shift register ---
        reg = -1 * np.ones(10)

        # --- Generate all G1 signal chips based on the G1 feedback polynomial -----
        for i in range(1023):
            g1[i] = reg[-1]
            saveBit = reg[2] * reg[9]
            reg[1:] = reg[:-1]
            reg[0] = saveBit

        # --- Generate G2 code -----------------------------------------------------

        # --- Initialize g2 output to speed up the function ---
        g2 = np.zeros(1023)

        # --- Load shift register ---
        reg = -1 * np.ones(10)

        # --- Generate all G2 signal chips based on the G2 feedback polynomial -----
        for i in range(1023):
            g2[i] = reg[-1]
            saveBit = reg[1] * reg[2] * reg[5] * reg[7] * reg[8] * reg[9]
            reg[1:] = reg[:-1]
            reg[0] = saveBit

        # --- Shift G2 code --------------------------------------------------------
        # The idea: g2 = concatenate[ g2_right_part, g2_left_part ];
        g2 = np.r_[g2[1023 - g2shift:], g2[:1023 - g2shift]]

        # --- Form single sample C/A code by multiplying G1 and G2 -----------------
        self.CAcode = -g1 * g2
        CAcode=self.CAcode
        CAcode=np.array(CAcode)
        codeIndex=np.floor(np.linspace(0,1023,num=int(self.samplesPerCode),endpoint=False))
        codeIndex=np.longlong(codeIndex)
        self.codeSequence=CAcode[codeIndex]
        # get frequency domin of the codeSequence
        self.codeFreqDomin=np.fft.fft(self.codeSequence[:]).conj()
    

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        
        sig=np.array(input_items[0][0])
        shapeSig=sig.shape
        #print(sig.shape)
       
        
        ##generate code sequence
        
        samplesPerCode=self.samplesPerCode
        
        
        ## get the frequency-codePhase mat
        searchBand=20 #kHz
        freqBins=searchBand*2+1 # 500Hz per bin
        #initialize the space for frequency-codePhase mat
        freqCodeMat=np.zeros((freqBins,samplesPerCode))
        # generate time sequence 
        t=np.linspace(0,1e-3,num=int(samplesPerCode),endpoint=False)
        
        for freqBin in range(freqBins):
            #the frequency
            frequency=self.centreFreq-searchBand*1e3+freqBin*500
            
            #generate the carrier signal
            carrier=np.exp(1j*frequency*2*np.pi*t)
            #print(carrier.shape)
            
            #get the sig in frequency Domin
            sigFreq=np.fft.fft(carrier*sig)
            
            #get the acquisition result of this frequency bin
            acqRes=abs(np.fft.ifft(sigFreq*self.codeFreqDomin))
            
            freqCodeMat[freqBin,:]=acqRes[:]
            
            #print(acqRes.shape)
        
        #print(freqCodeMat.shape)
        peakValue=freqCodeMat.max(0).max(0)
        
        maxFreqIndex=freqCodeMat.max(1).argmax()
        
        maxCodePhaseIndex=freqCodeMat.max(0).argmax()
        
        tempFreq=self.centreFreq-searchBand*1e3+maxFreqIndex*500
        
        ##find more accurate frequency
        
        #rotate the code sequence
        codeSequence=np.roll(self.codeSequence,maxCodePhaseIndex)
        
        #remove the CA code
        sig=sig*codeSequence
        
        #get fft result
        fftNum=32*2**np.ceil(np.log2(samplesPerCode))
        sigFreqDom=np.fft.fft(sig,np.long(fftNum))
        sigFreqDom=abs(sigFreqDom)
        
        maxFreqIndex=sigFreqDom.argmax()
        if(maxFreqIndex<(fftNum/2)):
            tempFreq=(maxFreqIndex/fftNum)*self.sampleRate
        else:
            tempFreq=(maxFreqIndex/fftNum)*self.sampleRate-self.sampleRate
        
        
        
        
        
        print(peakValue,"   " ,np.median(freqCodeMat),"   ",tempFreq,"  ",maxCodePhaseIndex)
            
        PMT_msg=pmt.from_float(tempFreq)
        self.message_port_pub(pmt.intern(self.portName),PMT_msg)
        
        
        
        output_items[0][:]=input_items[0]
        return len(output_items[0])
