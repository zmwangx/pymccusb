#!/usr/bin/env python3

# A stripped down version of rxcntl based on the original C version by
# Dan Marlow and Norm Jarosik. Their work was in turn based on that of
# Warren Jasper <wjasper@tx.ncsu.edu>
#
# Currently only the read-only mode is implemented.

from __future__ import print_function
import logging
import os
import sys

import mccusb


logging.basicConfig(format='[%(levelname)s] %(message)s')
logger = logging.getLogger('rxcntl')
logger.setLevel(logging.INFO)

# Bit definitions for port A
POWER = 0x01
NOISE = 0x02
FILTER = 0x04
SPARE = 0x08

# Bit definitions for port B
POWER_ON = 0x01
NOISE_ON = 0x02
YIG_ON = 0x04
SPARE_ON = 0x08

# YIG analog definitions
ADC_CAL = 0.001221  # volts per count
YIG_AOUT_CHAN = 0
R_SENSE = 33.0
YIG_m = 0.063
YIG_b = -1.5


def value2current(value):
    return 1000. * ADC_CAL * value / R_SENSE


def current2frequency(current):
    return (current - YIG_b) / YIG_m


def get_yig_current(udev):
    return value2current(udev.aOutR(YIG_AOUT_CHAN))


def print_status(porta_init, portb_init, yig_current):
    logger.debug('porta_init = {0:02X} portb_init = {1:02X}'.format(porta_init, portb_init))
    power_state = 'ON' if portb_init & POWER_ON else 'OFF'
    filter_state = 'YIG' if portb_init & YIG_ON else '21cm'
    noise_state = 'ON' if portb_init & NOISE_ON else 'OFF'
    yig_frequency = current2frequency(yig_current)
    print('Power: {0}   Filter: {1}'.format(power_state, filter_state))
    print('Noise: {0}   '.format(noise_state))
    print(' YIG: I={0:5.1f} mA f={1:5.1f} MHz'.format(yig_current, yig_frequency))


def main():
    if os.getenv('DEBUG'):
        logger.setLevel(logging.DEBUG)

    try:
        udev = mccusb.MCCUSB1208FSPlusDevice()
        logger.debug('Success, found a USB 1208FS-Plus!')
    except mccusb.DeviceNotFoundError:
        try:
            udev = mccusb.MCCUSB1408FSPlusDevice()
            logger.debug('Success, found a USB 1408FS-Plus!')
        except mccusb.DeviceNotFoundError:
            logger.error('Failure, did not find a USB 1208FS-Plus / USB 1408FS-Plus!')
            sys.exit(1)

    udev.dTristateW(udev.PORTA, 0x00)  # Make Port A output
    udev.dTristateW(udev.PORTB, 0x01)  # Make Port B input

    porta_init = udev.dLatchR(udev.PORTA)
    yig_current = get_yig_current(udev)
    # The duplicate calls are required due to a firmware bug in the MCC device.
    udev.dPort(udev.PORTB)
    udev.dPort(udev.PORTB)
    portb_init = udev.dPort(udev.PORTB)
    porta_out = 0

    print_status(porta_init, portb_init, yig_current)


if __name__ == '__main__':
    main()
