# Ground station software for communication with the CU-InSpace rocket via an
# RN2483 LoRa radio module.
# Authors: 
# 


import serial

class GroundStation:
    
    def __init__(self, com_port='COM4'):
        
        #USB serial connection 
        self.ser = serial.Serial(port = com_port,
                                  timeout=1,
                                  baudrate=57600,
                                  # number of bits per message
                                  bytesize=serial.EIGHTBITS,
                                  # set parity check: no parity
                                  parity=serial.PARITY_NONE,
                                  # number of stop bits
                                  stopbits = 1,
                                  # disable hardware (RTS/CTS) flow control
                                  rtscts=False)           
    

    def init_serial(port):
        
            
        return 0
        


    def init_GPIO(self):
        self.write_to_ground_station("sys set pinmode GPIO0 digin")
        self.write_to_ground_station("sys set pinmode GPIO1 digin")
        self.write_to_ground_station("sys set pinmode GPIO2 digin")
        self.write_to_ground_station("sys set pinmode GPIO3 digin")
        self.write_to_ground_station("sys set pinmode GPIO4 digin")
        self.write_to_ground_station("sys set pinmode GPIO5 digin")
        self.write_to_ground_station("sys set pinmode GPIO6 digin")
        self.write_to_ground_station("sys set pinmode GPIO5 digin")
        self.write_to_ground_station("sys set pinmode GPIO6 digin")
        self.write_to_ground_station("sys set pinmode GPIO7 digin")
        self.write_to_ground_station("sys set pinmode GPIO8 digin")
        self.write_to_ground_station("sys set pinmode GPIO9 digin")
        self.write_to_ground_station("sys set pinmode GPIO10 digin")
        self.write_to_ground_station("sys set pinmode GPIO11 digin")
        self.write_to_ground_station("sys set pinmode GPIO12 digin")
        self.write_to_ground_station("sys set pinmode GPIO13 digin")    

    def init_ground_station(self):

        # initlize all the pins to be inputs
        self.init_GPIO()

        #set the frequency of the radio
        self.radio_set_freq(433050000)
        
        # set the power to -14 db
        self.radio_set_pwr(14)
        
        # set the spreading factor
        self.radio_set_sf("sf9")
        
        # set the coding rate
        self.radio_set_cr("4/7")
        
        # set bandwdith
        self.radio_set_rxbw(500)
        
        # set prlen preamble length
        self.radio_set_prlen(6)
        
        # set crc
        self.radio_set_crc("on")
        
        # set iqi
        self.radio_set_iqi("on")
        
        # set sync word to be 0x43
        self.radio_set_sync("43")
        
        print("sucessfully configured lora radio")


        
    def write_to_ground_station(self, command_string):
        """writes data to the ground station via UART
        author: Tarik
        @param command_string: full command to be send to the ground station
        @param COM_PORT: the COM port to be used for the UART transmission
        
        Ex.
        >>write_to_ground_station("radio set pwr 7", COM1)
        >>"ok"
        
        //above example sets the radio tramission power to 7 using COM1
        
        """

        data = str(command_string)
        
        #must include carriage return for valid commands (see DS40001784B pg XX)
        data = data + "\r\n"
        
        # encode command_string as bytes and then transmit over serial port
        self.ser.write(data.encode('utf-8'))  
        
        
    

    def process_response(self, response:str) -> str:
        """
        Removes the carriage return from the output received 
        from the radio.
        Author: Fahim
        @param  response: contains response from radio
        @return: the response received from radio in a clean format. 
        will return -1 if error is found.
        >>>strip_output("b'21313123321\r\n'")
        21313123321
        """
        #if we don't get a response
        if len(response) == 0:
            return -1
        if response == '\r\n':
            return -1 
        
        #remove carriage return value 
        return response.decode('UTF-8')[:-2]
    
    
    #radio commands
    def read_frequency(self):
        freq = int(self.read_from_ground_station("freq"))
        UPPER_1 = 434800000
        LOWER_1 = 433000000
        UPPER_2 = 870000000
        LOWER_2 = 863000000
    
        if (freq > LOWER_1 and freq < UPPER_1):
            return freq
        elif (freq > LOWER_2 and freq < UPPER_2):
            return freq
        else:
            return -1
    
    def read_bitrate():
        bitrate = int(strip_output(read_from_ground_station("bitrate")))
        UPPER_1 = 65535
        LOWER_1 = 0
        if (bitrate > LOWER_1 and bitrate < UPPER_1):
            return bitrate
        else:
            return -1
    
    def read_bw():
        bw = int(strip_output(read_from_ground_station("bw")))
        possibilities = [125,250,500] #the three possible values
        if (bw in possibilities):
            return bw
        else:
            return -1
    
    def read_cr(self):
        cr = self.read_from_ground_station("cr")
        possibilities = ['4/5','4/6','4/7','4/8'] #the four possible strings
        if (cr in possibilities):
            return cr
        else:
            return -1
    
    def read_bt():
        bt = strip_output(read_from_ground_station("bt"))
        possibilities = ['none','1.0','0.5','0.3'] #the four possible strings
        if (bt in possibilities):
            return bt
        else:
            return -1
    
    def read_crc(self):
        return read_from_ground_station("crc")
    
    def read_fdev():
        return read_from_ground_station("fdev")
    
    def read_afcbw():
        return read_from_ground_station("afcbw")
    
    def read_iqi():
        return read_from_ground_station("iqi")
    
    def read_mod():
        return read_from_ground_station("mod")
    
    def read_prlen():
        return read_from_ground_station("prlen")
    
    def read_pwr():
        return read_from_ground_station("pwr")
    
    def read_rssi():
        return read_from_ground_station("rssi")
    
    def read_rxbw():
        return read_from_ground_station("rxbw")
    
    def read_sf():
        return read_from_ground_station("sf")
    
    def read_snr():
        return read_from_ground_station("snr")
    
    def read_sync():
        return read_from_ground_station("sync")
    
    def read_wdt():
        return read_from_ground_station("wdt")
    
    #sys commands
    
    def read_ver():
        return read_from_ground_station("ver")
    
    def read_vdd():
        return read_from_ground_station("vdd")
    
    def read_hweui(): #remove?
        return read_from_ground_station("hweui")
    
    def read_nvm(address: str):
        """
        Accepts hexadecimal address from 300 to 3FF.
        """
        return read_from_ground_station("nvm " + address)
    
    def read_pindig(pinName: str): #remove
        """
        Accepts GPIO0 - 13, UART_CTS, UART_RTS, TEST0-1.
        """
        return read_from_ground_station("pindig " + pinName)
    
    def read_pinana(pinName: str): #remove
        """
        Accepts GPIO0 - 3, and GPIO5 - 13
        Enter only the pin #, as GPIO is already accounted for
        """
        return read_from_ground_station("pinana GPIO" + pinName)    
    
    def read_from_ground_station(self, command: str):
        """reads data from the ground station via UART
       author: Fahim

       @param  command: contains commmand that will be written to ground station
       @return: the message received from station
                will return -1 if error is found
        """
        command = str(command)
        
        #split command into individual words if command is more than one word
        #long. Example:  'nvm 300'
        cmds = command.split()
        
        #these are parameters that require a 'sys' call. Ex. 'sys get vdd'
        sys_commands = ['vdd', 'nvm','ver','hweui','pindig','pinana']
        
        if(cmds[0] in sys_commands): 
            self.write_to_ground_station("sys get " + command)
        
        #if parameter to be read is not covered by 'sys', it requires 'radio'
        else:
            self.write_to_ground_station("radio get " + command)
    
        #if command was recieved and valid:
        return self.process_response(self.ser.readline())

        
           


    def load_map(self):
        """load in a map that can be used offline
            author: """

    # wait for serial response we have set a timeout value so it will wait for a response and checks if it's not ok
    def wait_for_ok(self):
        
        
        # flush the serial port
        self.ser.flush()
        
        #read 'ok' from the terminal, if it's there.
        rv = str(self.ser.readline())
        
        if ('ok' in rv):  # check for ok and report if param invalid
            return True
        
        elif rv != 'ok':
            print("ERROR: wait for ok(): " + rv)
            print(len(rv))
            return False



    def radio_set_freq(self, freq):
        """set the frequency of transmitted signals"""
        
        self.write_to_ground_station("radio set freq " + str(freq))
        
        success = self.wait_for_ok()
        
        if(success):
            print("frequency sucessfully set")
            return True
        else:
            print("error: frequency not set")
            return False
                

    
    def radio_set_pwr(self, pwr):
        """ set power possible values between -3 and 14 db"""
        
        if pwr in range(-3, 15):
            
            sucess=  self.write_to_ground_station("radio set pwr " + str(pwr))
            
            if sucess:
                print("value power sucessfully set")
                return
            
            else:
                print("power error:radio unable to set")
                return
                
        print("invalid power param")
        return
    

    # spreading factor can only be set to  sf7", "sf8", "sf9", "sf10", "sf11", "sf12"]
    def radio_set_sf(self, sf):
        
        if sf in ["sf7", "sf8", "sf9", "sf10", "sf11", "sf12"]:
            sucess= self.write_to_ground_station("radio set sf " + sf)
            if sucess:
                print("value spreading factor sucessfully set")
                return
            else:
                print("spreading factor  error:radio unable to set")
                return
                
        print("invalid spreading factor error")
        return
    
    # set coding rate which can only be "4/5", "4/6", "4/7", "4/8"


    def radio_set_cr(self, cr):
        if cr in ["4/5", "4/6", "4/7", "4/8"]:
            sucess=self.write_to_ground_station("radio set cr " + str(cr))
            if sucess:
                print("value cr sucessfully set")
                return
            else:
                print("cr error:radio unable to set")
                return
        print("invalid cycling rate ")
        return

    # set the bandwidth which can only  be 125 250 or 500 hz


    def radio_set_rxbw(self, bw):
        if bw in [125, 250, 500]:
            sucess= self.write_to_ground_station("radio set bw " + str(bw))
            if sucess:
                print("value rxbw sucessfully set")
                return
            else:
                print("rxbw error:radio unable to set")
                return
            
        print("invalid recieving bandwidth  ")
        return
    

    # set IQI to be on or off


    def radio_set_iqi(self, iqi):
        if iqi in ["on", "off"]:
            sucess= self.write_to_ground_station("radio set iqi " + str(iqi))
            if sucess:
                print("value sucessfully set")
            else:
                print("iqi error:radio unable to set")
        print("invalid iqi setting ")
    # set sync word it's a 2 bytes no error checking is done because it's confusing to change between types


    def radio_set_sync(self, sync):
        sucess= self.write_to_ground_station("radio set sync" + str(sync))
        if sucess:
            print("value sync word sucessfully set")
        else:
            print("sync param error:radio unable to set ")


    # set the preamble length between 0 and  65535
    def radio_set_prlen(self, pr):
        if pr in range(0, 65535):
            sucess=self.write_to_ground_station("radio set pr" + str(pr))
            if sucess:
                print("value prlen sucessfully set")
            else:
                print("prlen error:radio unable to set ")
        print("invalid preamble length")

    # crc can only be set to True or false to enable error checking


    def radio_set_crc(self, crc):
        if crc in ["on", "off"]:
            sucess= self.write_to_ground_station("radio set crc" + str(crc))
            if sucess:
                print("value crc sucessfully set")
            else:
                print("crc error:radio unable to set")
        print("invalid crc param ")


    def radio_set_rxmode(self):
        # set the timeout to 65535 the maximum amount
        # we will set this value to be the transmission
        #The mac pause command must be called before any radio transmission
        #or reception, even if no MAC operations have been initiated before.

        self.write_to_ground_station(str("mac pause", "utf-8"))

        # set rx amount to the amount of bytes we need
        #suggestion is to keep it to 0 since we know the packet lenght and anoumt of blocks is varible
        self.write_to_ground_station(str("radio rx 0", "utf-8"))
        
    def test_radio(self):
        #send a valid command which get's frequency

        while(1):
            self.write_to_ground_station(str("radio get freq "+ "\r\n", "utf-8"))
            rv = ser.readline()
            print(rv)
    def radio_set_txmode(self, data):
        self.write_to_ground_station(str("radio tx "+data+"\r\n", utf8)) 
        

rad = GroundStation()
rad.init_ground_station()
#rad.init_ground_station()
print('_____________________________________')
print(rad.read_cr())

#rad.read_from_ground_station('pwr')
#rad.read_from_ground_station('bw')
#rad.read_from_ground_station('bt')
#rad.read_from_ground_station('cr')
#rad.read_from_ground_station('crc')
#rad.read_from_ground_station('fdev')
#rad.read_from_ground_station('freq')
#rad.read_from_ground_station('iqi')
#rad.read_from_ground_station('mod')
#rad.read_from_ground_station('prlen')
#rad.read_from_ground_station('rssi')
#rad.read_from_ground_station('rxbw')
#rad.read_from_ground_station('sf')
#rad.read_from_ground_station('snr')
#rad.read_from_ground_station('sync')
#rad.read_from_ground_station('wdt')