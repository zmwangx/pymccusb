/***************************************************************************
 Copyright (C) 2003-2008  Warren J. Jasper <wjasper@tx.ncsu.edu>
 All rights reserved.

 This program, PCI-CTR10, is free software; you can redistribute it
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

/***************************************************************************
 *
 *  test-ctr20HD.c
 *
 *  This program is used to test the PCI-CTR20HD Counter Board
 *  Linux loadable module.
 *
 ***************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include "pci-ctr20HD.h"

#define CTR2_BIT    0x2
#define CTR3_BIT    0x4
#define CTR5_BIT    0x10

/***************************************************************************
 *
 *  Global Data
 *
 ***************************************************************************/

char *DevName = "/dev/ctr20HD/ctr0_01";
int  Mode     = CTR20HD_COUNTER;
int  Print    = 1;
int  Status;

int fdctr_1;
int fdctr_2;
int fdctr_3;
int fdctr_4;
int fdctr_5;
int fdctr_6;
int fdctr_7;
int fdctr_8;
int fdctr_9;
int fdctr_a;

void DoOpenDevices()
{
  char str[80];

  strcpy(str, "/dev/ctr20HD/ctr0_01");
  if ((fdctr_1 = open(str, CTR20HD_COUNTER)) < 0) {
    perror(str);
    printf("error opening device %s\n",str);
    exit(2);
  }
  strcpy(str,"/dev/ctr20HD/ctr0_02");
  if ((fdctr_2 = open(str, CTR20HD_COUNTER)) < 0) {
    perror(str);
    printf("error opening device %s\n",str);
    exit(2);
  }

  strcpy(str, "/dev/ctr20HD/ctr0_03");
  if ((fdctr_3 = open(str, CTR20HD_FREQUENCY)) < 0) {
    perror(str);
    printf("error opening device %s\n",str);
    exit(2);
  }

  strcpy(str,"/dev/ctr20HD/ctr0_11");
  if ((fdctr_6 = open(str, CTR20HD_COUNTER)) < 0) {
    perror(str);
    printf("error opening device %s\n",str);
    exit(2);
  }

  strcpy(str,"/dev/ctr20HD/ctr0_12");
  if ((fdctr_7 = open(str, CTR20HD_COUNTER)) < 0) {
    perror(str);
    printf("error opening device %s\n",str);
    exit(2);
  }

  strcpy(str, "/dev/ctr20HD/ctr0_13");
  if ((fdctr_8 = open(str, CTR20HD_FREQUENCY)) < 0) {
    perror(str);
    printf("error opening device %s\n",str);
    exit(2);
  }
} 

void testCounter()
{
  unsigned short value_A, value_B;
  char str[80];
  int i;
  unsigned short source;

  printf("*********************************************************\n");
  printf("*     Connect the terminal blocks as follows:           *\n");
  printf("*          square wave  <-------> pin 1                 *\n");
  printf("*********************************************************\n\n");

  source = SRC1;
  while (1) {
    for (i = 0; i < 10; i++)  {
      write(fdctr_1, &source, 2);
      write(fdctr_6, &source, 2);
      // input pulses to 
      sleep(1);
      read(fdctr_1, &value_A, 2);
      read(fdctr_6, &value_B, 2);
      printf("Count_A = %d\tCount_B = %d\n", value_A, value_B);
    }
    printf("\nContinue? ");
    scanf("%s",str);
    if (str[0]=='N' || str[0]=='n') return;
  }
}

void testFreq()
{
  unsigned short value;
  char str[80];
  int source = SRC3;
  int freq;

  printf("*********************************************************\n");
  printf("*     Connect the terminal blocks as follows:           *\n");
  printf("*          pin 18  <-------> pin 11                     *\n");
  printf("*          pin  6  <-------> pin  9                     *\n");
  printf("*********************************************************\n\n");

  ioctl(fdctr_3, SET_GATE_INTERVAL, 5000);  // 5000 = 1 second */
  write(fdctr_3, &source, 2);
  ioctl(fdctr_8, SET_GATE_INTERVAL, 5000);  // 5000 = 1 second */
  write(fdctr_8, &source, 2);

  while (1) {
    printf("Input desired frequency [Hz]: ");
    scanf("%d", &freq);
    ioctl(fdctr_2, SET_SQUARE_FREQ, freq);    
    sleep(2);
    read(fdctr_3, &value, 1);
    printf("Frequency Counter 3 is %d  ",value);
    read(fdctr_8, &value, 1);
    printf("Frequency Counter 8 is %d\n",value);
    printf("\nContinue? ");
    scanf("%s",str);
    if (str[0]=='N' || str[0]=='n') {
      ioctl(fdctr_5, LOAD_CMD_REG, DISARM | CTR5_BIT | CTR3_BIT | CTR2_BIT);
      return;
    }
  }
}

void testSquare()
{
  char str[80];
  int freq;

  printf("*********************************************************\n");
  printf("*     Connect the terminal blocks as follows:           *\n");
  printf("*          pin 6  <------->  scope                     *\n");
  printf("*********************************************************\n\n");

  while (1) {
    printf("Input desired frequency [Hz]: ");
    scanf("%d", &freq);
    ioctl(fdctr_2, SET_CLOCK_INPUT, C_5MHZ);    
    ioctl(fdctr_2, SET_SQUARE_FREQ, freq);    
    printf("\nContinue? ");
    scanf("%s",str);
    if (str[0]=='N' || str[0]=='n') {
      ioctl(fdctr_2, LOAD_CMD_REG, DISARM | CTR2_BIT);
      return;
    }
  }
}

void Domenu()
{
  int choice;

  while (1) {
    system("/usr/bin/clear");
    printf("Select from the following choices:\n");
    printf("\t1. Test Counter.\n");
    printf("\t2. Measure Frequency.\n");
    printf("\t3. Generate Square Wave.\n");
    printf("\t4. Exit.\n");
    printf("\nOption: ");

    scanf("%d", &choice);
    switch (choice) {
    case 1: 
      testCounter();
      break;
    case 2:
      testFreq();
      break;
    case 3:
      testSquare();
      break;
    case 4:
      return;
      break;
    default:
      break;
    }
  }
}

int main(int argc, char **argv)
{
  DoOpenDevices();
  Domenu();
  close(fdctr_1);
  close(fdctr_2);
  close(fdctr_3);
  close(fdctr_4);
  close(fdctr_6);
  close(fdctr_7);
  close(fdctr_8);
  close(fdctr_9);
  return(0);
}
























































































































































































































































































































































































































































































