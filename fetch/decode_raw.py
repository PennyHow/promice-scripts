#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 12:32:54 2024

@author: pho
"""

import time, calendar

def getDataLine(payload, bin_val, bin_format, bin_len, payload_type):
    '''Get data line from transmission message
    
    Returns
    -------
    str or None
        Dataline string if found'''
        
    # Retrieve payload and prime object if valid binary message        
    bin_msg = payload[1:]
 
    dataline = ''
    bytecounter = 0
    
    # Iterate over binary message formatting string
    for i in range(0, bin_val):

        type_letter = bin_format[i]
        num_bytes = payload_type[type_letter.lower()]
        
        # Check if 2-bit NaN is present
        if check2BitNAN(bin_msg, type_letter, bytecounter):
            dataline = dataline + writeEntry('NAN', i)
            updateByteCounter(bytecounter, 2)
            bin_len -= 2
        
        # Get byte value
        else:                      
            ValueBytes = getByteValue(num_bytes, bin_msg, bytecounter)
            updateByteCounter(bytecounter, num_bytes)
            
            if len(ValueBytes) == 2:
                Value = GFP2toDEC(ValueBytes)
            elif len(ValueBytes) == 4:
                Value = GLI4toDEC(ValueBytes)
            else:
                entry = '?'
            
            # Decode based on formatting string                  
            if type_letter.lower()=='g':
                entry = str(Value/100.0)
                
            elif type_letter.lower()=='n':
                entry = str(Value/100000.0)
                
            elif type_letter.lower() =='e':
                entry = str(Value/100000.0)  
                
            elif type_letter.lower()=='f':
                if Value == 8191:
                    entry = 'NAN'
                elif Value == 8190:
                    entry = 'INF'
                elif Value == -8190 or Value == -8191:               
                    entry = '-INF'
                else:
                    entry = str(Value)    
                    
            elif type_letter.lower()=='l':
                if Value in (-2147483648, 2147450879):
                    entry = 'NAN'
                else:
                    entry = str(Value)
            
            elif type_letter.lower()=='t':
                entry = time.strftime('%Y-%m-%d %H:%M:%S', 
                                      time.gmtime(Value + EpochOffset())) + ',' + str(Value)  
            else:
                entry = '?'
                                
            # Append value outputted dataline
            if type_letter.isupper():
                dataline = dataline + RAWtoSTR(ValueBytes)
            else:
                dataline = dataline + writeEntry(entry, i, bin_val) 
            
    return dataline


def EpochOffset():
    UnixEpochOffset=calendar.timegm((1970,1,1,0,0,0,0,1,0)) 
    CRbasicEpochOffset=calendar.timegm((1990,1,1,0,0,0,0,1,0))
    EpochOffset = UnixEpochOffset + CRbasicEpochOffset
    return EpochOffset

def GFP2toDEC(Bytes):
    '''Two-bit decoder
    
    Parameters
    ----------
    Bytes : list
        List of two values
    
    Returns
    -------
    float
        Decoded value
    '''
    # print('ValueBytes received ' + str(Bytes))
    msb = Bytes[0]
    lsb = Bytes[1]    
    Csign = -2*(msb & 128)/128 + 1
    CexpM = (msb & 64)/64
    CexpL = (msb & 32)/32
    Cexp = 2*CexpM + CexpL - 3
    Cuppmant = 4096*(msb & 16)/16 + 2048*(msb & 8)/8 + 1024*(msb & 4)/4 + 512*(msb & 2)/2 + 256*(msb & 1)
    Cnum = Csign * (Cuppmant + lsb)*10**Cexp
    return round(Cnum, 3)

def GLI4toDEC(Bytes):
    '''Four-bit decoder
    
    Parameters
    ----------
    Bytes : list
        List of four values
    
    Returns
    -------
    float
        Decoded value
    '''
    Csign = int(-2 * (Bytes[0] & 0x80) / 0x80 + 1)
    byte1 = Bytes[0] & 127
    byte2 = Bytes[1]
    byte3 = Bytes[2]
    byte4 = Bytes[3]    
    return Csign * byte1 * 0x01000000 + byte2 * 0x010000 + byte3 * 0x0100 + byte4

def RAWtoSTR(Bytes):
    '''Byte-to-string decoder
    
    Parameters
    ----------
    Bytes : list
        List of values
    
    Returns
    -------
        Decoded string characters
    '''
    us = [chr(byte) for byte in Bytes] #the unicode strings
    hs = ['0x{0:02X}'.format(byte) for byte in Bytes] #the hex strings
    bs = ['0b{0:08b}'.format(byte) for byte in Bytes] #the bit strings
    return '(%s = %s = %s)' %(' '.join(us), ' '.join(hs), ' '.join(bs))

def check2BitNAN(msg, type_letter, bytecounter, letter_flag=['g','n','e'], 
                 nan_value=8191):
    '''Check if byte is a 2-bit NAN. This occurs when the GPS data is not 
    available and the logger sends a 2-bytes NAN instead of a 4-bytes value
    '''
    if type_letter.lower() in letter_flag:
        ValueBytes = getByteValue(2, msg, bytecounter)
        try:
            if GFP2toDEC(ValueBytes) == nan_value:
                return True
            else:                                
                return False
        except:
            return False
    else:
        return False   

def getByteValue(ValueBytesCount, BinaryMessage, idx):
    '''Get values from byte range in binary message'''
    ValueBytes=[]
    for i in range(0,ValueBytesCount):
        try:
            ValueBytes.append(ord(BinaryMessage[idx+i: idx+i+1]))
        except:
            print('No byte found')
    return ValueBytes

def writeEntry(entry, i, bin_val):
    '''Write out comma-formatted data entry from message'''
    if i == bin_val-1:
        return entry
    else:
        return entry + ',' 

def updateByteCounter(bytecounter, value):
    '''Update byte counter for decoding message'''
    bytecounter += value
    return bytecounter

def getTypes():
    return {'f': 2, 'l': 4, 't': 4, 'g': 4, 'n': 4, 'e': 4}

def _addCount(format_string, expected_length):
    '''Add counter to payload formatter'''
    payload_type = getTypes()
    
    assert len(format_string) == expected_length
    bytes_count = 0
    for var in format_string:
        bytes_count += payload_type[var.lower()]
    return bytes_count

if __name__ == "__main__":  
    
    f2 = '/home/pho/Desktop/data/NUK_K/E7588.TableMem.dat'
    
    with open(f2, 'rb') as file:
    
        # Step 2: Read line by line and decode
        lines = [line for line in file]

    # format_string = 'tfffffffffffffffffffffffffgneffffffffff'
    format_string = 'llffffffffffffffffffffffffffgneffffffffff'
    expected_values = 41
    bytes_count = _addCount(format_string, expected_values)
    payload_types = getTypes()
    
    test = lines[6]
    
    decoded = getDataLine(test, expected_values, format_string, bytes_count, payload_types)
    