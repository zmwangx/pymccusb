/***************************************************************************
 Copyright (C) 1997 - 2004  Warren J. Jasper
 All rights reserved.

 This program, PCI-DAS1602-16, is free software; you can redistribute it
 and/or modify it under the terms of the GNU General Public License as
 published by the Free Software Foundation; either version 2 of the
 License, or (at your option) any later version, provided that this
 copyright notice is preserved on all copies.

 ANY RIGHTS GRANTED HEREUNDER ARE GRANTED WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES
 OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, AND FURTHER,
 THERE SHALL BE NO WARRANTY AS TO CONFORMITY WITH ANY USER MANUALS OR
 OTHER LITERATURE PROVIDED WITH SOFTWARE OR THAM MY BE ISSUED FROM TIME
 TO TIME. IT IS PROVIDED SOLELY "AS IS".

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
***************************************************************************/

/*
 * pci-das1602.h
 */


#ifndef PCI_DAS1602_H
#define PCI_DAS1602_H

#include <linux/ioctl.h>
#define IOCTL_MAGIC 'w'

/*  ioctl() values */

#define ADC_SET_GAINS        _IO(IOCTL_MAGIC,   1)
#define ADC_GET_GAINS        _IOR(IOCTL_MAGIC,  2, long)
#define ADC_SET_PACER_FREQ   _IO(IOCTL_MAGIC,   3)
#define ADC_GET_PACER_FREQ   _IOR(IOCTL_MAGIC,  4, long)
#define ADC_START_PACER      _IO(IOCTL_MAGIC,   5)
#define ADC_STOP_PACER       _IO(IOCTL_MAGIC,   6)
#define ADC_COUNTER0         _IO(IOCTL_MAGIC,   7)
#define ADC_DIO_PRESET       _IOR(IOCTL_MAGIC,  8, long)
#define ADC_SET_TRIGGER      _IO(IOCTL_MAGIC,   9)
#define ADC_SET_MUX_LOW      _IO(IOCTL_MAGIC,  10)
#define ADC_SET_MUX_HIGH     _IO(IOCTL_MAGIC,  11)
#define ADC_GET_CHAN_MUX_REG _IOR(IOCTL_MAGIC, 12, long)
#define ADC_SET_FRONT_END    _IO(IOCTL_MAGIC,  13)
#define ADC_BURST_MODE       _IO(IOCTL_MAGIC,  14)
#define ADC_PRETRIG          _IO(IOCTL_MAGIC,  15)

#define DIO_SET_MODE         _IO(IOCTL_MAGIC,  16)
#define DIO_SET_DIRECTION    _IO(IOCTL_MAGIC,  17)

#define DAC_SET_GAINS        _IO(IOCTL_MAGIC,  18)
#define DAC_GET_GAINS        _IOR(IOCTL_MAGIC, 19, long)
#define DAC_SET_PACER_FREQ   _IO(IOCTL_MAGIC,  20)
#define DAC_GET_PACER_FREQ   _IOR(IOCTL_MAGIC, 21, long)
#define DAC_STOP_PACER       _IO(IOCTL_MAGIC,  22)
#define DAC_RECYCLE          _IO(IOCTL_MAGIC,  23)
#define DAC_SET_CLO          _IO(IOCTL_MAGIC,  24)
#define DAC_SET_CHI          _IO(IOCTL_MAGIC,  25)
#define DAC_SET_SIMULTANEOUS _IO(IOCTL_MAGIC,  26)

#define GET_BUF_SIZE         _IOR(IOCTL_MAGIC, 27, long)

#define IOCTL_MAXNR 27         /* maxinum ordinal number */

/* open mode values (pacer source) */

#define ADC_SOFT_CONVERT           (0x0)
#define ADC_EXTERNAL_PACER_FALLING (0x2)
#define ADC_EXTERNAL_PACER_RISING  (0x4)
#define ADC_PACER_CLOCK            (0x6)

#define DAC_SOFT_CONVERT           (0x1)
#define DAC_PACER_CLOCK            (0x5)
#define DAC_FALLING_EDGE           (0x3)
#define DAC_RISING_EDGE            (0x7)

/* Digital I/O Modes */
#define MODE_IO            0
#define MODE_STROBE_IO     1
#define MODE_BIDIRECTIONAL 2

/* Digital I/O Direction Settings */
#define PORT_OUTPUT        0
#define PORT_INPUT         1
#define HIGH_PORT_INPUT    2
#define HIGH_PORT_OUTPUT   3
#define LOW_PORT_INPUT     4
#define LOW_PORT_OUTPUT    5

/* ioctl(COUNTER0) mode values */
#define CTR0_MODE0 (0x0 << 17)
#define CTR0_MODE1 (0x1 << 17)
#define CTR0_MODE2 (0x2 << 17)
#define CTR0_MODE3 (0x3 << 17)
#define CTR0_MODE4 (0x4 << 17)
#define CTR0_MODE5 (0x5 << 17)
#define CTR0_NOLOAD (0xff000000)

/*  General definitions */

#define MAX_AD_FREQ 200000
#define MAX_DA_FREQ 100000
#define BYTE unsigned char
#define WORD unsigned short
#define LONG unsigned long

/* Programmable Range and Gain Settings */

#define BP_10_00V  (0x00 << 8)    /* +/- 10V      */
#define BP_5_00V   (0x01 << 8)    /* +/-  5V      */
#define BP_2_50V   (0x02 << 8)    /* +/-  2.5V    */
#define BP_1_25V   (0x03 << 8)    /* +/-  1.25V   */
#define UP_10_00V  (0x08 << 8)    /* 0 - 10V      */
#define UP_5_00V   (0x09 << 8)    /* 0 - 5V       */
#define UP_2_50V   (0x0a << 8)    /* 0 - 2.5V     */
#define UP_1_25V   (0x0b << 8)    /* 0 - 1.25V    */

/* DAC MODES */
#define ONE_SHOT    0x0
#define CONTINUOUS  0x1

/* digital output */
#define DIO_0 0x1
#define DIO_1 0x2
#define DIO_2 0x4
#define DIO_3 0x8

/* Set Trigger Values  */
#define GATE_NEG_HYS    1
#define GATE_POS_HYS    2
#define GATE_ABOVE      3
#define GATE_BELOW      4
#define TRIG_ABOVE      5
#define TRIG_BELOW      6
#define GATE_OUT_WINDOW 7
#define GATE_IN_WINDOW  8
#define GATE_HIGH       9
#define GATE_LOW        10
#define TRIG_POS_EDGE   11
#define TRIG_NEG_EDGE   12

#endif
