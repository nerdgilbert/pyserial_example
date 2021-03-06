#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    __author__="Gilbert Montague"
    Super simple example of using the PySerial module to send characters over the serial line
"""
import serial
import argparse
import glob
import sys
import time

# My own library for pretty print debug statements
import debug_status as ds

default_port = '/dev/ttyUSB0'
default_baud_rate = 115200


def get_serial_ports():
    """ Lists available serial ports

        :returns:
            A list of serial ports available
    """
    ports = glob.glob('/dev/tty[A-Za-z]*')

    available_ports = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            available_ports.append(port)
        except(OSError, serial.SerialException):
            pass
    return available_ports


if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="Set the port to listen to")
    parser.add_argument("--baud", help="Set the baud rate")
    args = parser.parse_args()

    # Setup serial port
    port = default_port
    if args.port == None:
        ds.print_status(
            ds.WARNING, "No port specified, defaulting to: %s" % default_port)
    else:
        ds.print_status(ds.INFO, "Using provided port: %s" % args.port)
        port = args.port

        # Check if this port actually exists
        try:
            s = serial.Serial(port)
            s.close()
        except(OSError, serial.SerialException):
            ds.print_status(
                ds.WARNING, "User provided port does not exist. Using default port: %s" % default_port)

    # Setup baud rate
    baud_rate = default_baud_rate
    if args.baud == None:
        ds.print_status(
            ds.WARNING, "No baud rate specified, defaulting to: %d" % default_baud_rate)
    else:
        ds.print_status(ds.INFO, "Using provided baud rate: %s" % args.baud)
        baud_rate = args.baud

    # Try and open the port
    ds.print_status(ds.INFO, "Opening port: %s with baud rate: %s" %
                    (port, baud_rate))
    try:
        ser = serial.Serial(port, baud_rate)
    except(OSError, serial.SerialException):
        ds.print_status(
            ds.FATAL_ERROR, "UNABLE TO OPEN PORT: %s WITH BAUD RATE: %s" % (port, baud_rate))
        exit()
    ds.print_status(ds.INFO, "Successfully opened serial port")

    # Write stuff
    while True:
        write_string = raw_input(
            "Type stuff. Press enter to send. Type 'close' to close the port. ")

        if write_string == 'close':
            ds.print_status(ds.INFO, "Closing connection. Goodbye")
            ser.flush()
            ser.close()
            exit()
        else:
            # Send the string
            try:
                ser.write(str(write_string))
                ser.write('\r\n')
                ser.flush()
                ds.print_status(ds.INFO, "Sent: %s" % str(write_string))
            except:
                ds.print_status(ds.WARNING, "Unable to send string")

            # Read what we just wrote
            try:
                time.sleep(0.1)
                line = ser.readline()
                ds.print_status(ds.INFO, "Recieved: %s" % str(line))
            except Exception, e:
                ds.print_status(ds.WARNING, str(e))
