#!/bin/env python3

## AUTHOR: Marcus Collins
## EMAIL:  mkcollins4350@gmail.com
## DATE:   05-Nov-2021

import sys

## number of bits per ASCII character (if padded to UTF-8 width/length)
CHAR_BITLEN = int(8)


## preamble to search for in STDIN data and its length in bits
PREAMBLE_S = "CAPTIVATION"
PREAMBLE_LEN = len(PREAMBLE_S)
PREAMBLE_BITLEN = PREAMBLE_LEN*CHAR_BITLEN


## number of bits to print to STDOUT after the preamble is found
POSTAMBLE_BITLEN = int(100)


## function to pack list of bits in characters
def packBitsToStr(bit_list):
    ### not strictly necessary to declare these global 
    global PREAMBLE_LEN
    global CHAR_BITLEN

    ### list to hold characters from transformed bits
    char_list = ['']*(PREAMBLE_LEN)

    ### integer to hold bit-to-char transformation
    curr_char = int(0)

    ### loop to transform bits
    for n,b in enumerate(bit_list):
        ### convert character b to integer-value and subtract integer-value of '0' (zero) character,
        ###    then multiple by 2 to the power of its position in the ASCII character 7 through 0
        curr_char += (ord(b) - ord('0'))*pow(2, (CHAR_BITLEN - 1 - (n%CHAR_BITLEN)))

        char_list[(n//CHAR_BITLEN)] = chr(curr_char)

        ### reset the character/integer to zero every CHAR_BITLEN bits
        if (n != 0) and ((n%CHAR_BITLEN) == 0):
            curr_char = int(0)

    ### use str.join to create output string
    out_str = "".join(char_list)

    return( out_str )


## function to find preamble and return True/False
def preambleFound(bit_list):
    global PREAMBLE_S

    pack_str = packBitsToStr(bit_list)

    if pack_str == PREAMBLE_S:
        return( True )
    else:
        return( False )


## "main" driver that reads "bits" from STDIN & writes Postamble "bits" to STDOUT
def CapSwDriver():
    global PREAMBLE_BITLEN
    global POSTAMBLE_BITLEN

    with sys.stdin as f_in, sys.stdout as f_out:
        ### the "bit" read from STDIN should have a newline stripped to 
        ###     properly check for stream end
        n_bit = int(0)
        bit_char = f_in.read(1).rstrip()

        ### storage for location(s) {zero-based} that preamble was found
        preamble_locs = []

        ### input buffer to pack into a string while checking for the preamble
        ibuffer = ['']*PREAMBLE_BITLEN
        ibuffer_pos = int(0)
        fill_ibuffer = bool(True)

        ### output string to hold the postamble "bits"
        postamble_s = ""
        postamble_pos = int(0)
        fill_postamble = bool(False)

        ### continue to read STDIN stream until an "Empty" character is found
        while bit_char != '':
            ### while a preamble is searched for fill a storage buffer
            if( fill_ibuffer ):
                ibuffer[ibuffer_pos] = bit_char
                ibuffer_pos += 1

                if( ibuffer_pos == PREAMBLE_BITLEN ):
                    fill_ibuffer = bool(False)
                    ibuffer_pos = int(0)
            else:
                ### once the preamble is found stop filling the buffer and
                ###     fill the postamble string. otherwise...
                if( preambleFound(ibuffer) ) and (not fill_postamble):
                    fill_postamble = bool(True)
                    preamble_locs.append(n_bit - PREAMBLE_BITLEN)
                else:
                    ### ...remove the "bit" from the front of the buffer and
                    ###    append the next "bit" to the end
                    ibuffer.pop(0)
                    ibuffer.append(bit_char)

                ### fill the postamble string to output to STDOUT
                if(fill_postamble) and (postamble_pos < POSTAMBLE_BITLEN):
                    postamble_s += bit_char
                    postamble_pos += 1
                
                ### reset flags, positions and strings once the postamble has
                ###     been stored and written
                if( postamble_pos == POSTAMBLE_BITLEN ):
                    f_out.write(postamble_s)

                    fill_ibuffer = bool(True)
                    fill_postamble = bool(False)
                    postamble_pos = int(0)
                    postamble_s = ""

            n_bit += 1
            bit_char = f_in.read(1).rstrip()

    ### moderate cleanup before exiting driver
    del preamble_locs

    return( None )


## call "main" driver
CapSwDriver()
