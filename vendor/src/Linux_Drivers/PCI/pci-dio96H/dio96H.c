/***************************************************************************
 Copyright (C) 2013  Warren J. Jasper
 All rights reserved.

 This program, PCI-DIO96H, is free software; you can redistribute it
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

#if defined(CONFIG_MODVERSIONS) && !defined(MODVERSIONS)
#define MODVERSIONS
#endif

#ifndef LINUX_VERSION_CODE
#include <linux/version.h>
#endif

#ifndef VERSION_CODE
#define VERSION_CODE(vers,rel,seq) ( ((vers)<<16) | ((rel)<<8) | (seq) )
#endif

#if LINUX_VERSION_CODE < VERSION_CODE(2,4,0) /*  < 2.0 */
#error "This kernel is too old: not supported by this file"
#endif

#if LINUX_VERSION_CODE >= VERSION_CODE(2,4,0) && LINUX_VERSION_CODE < VERSION_CODE(2,4,0xff)
#include "dio96H_2_4.c"
#endif

#if LINUX_VERSION_CODE >= VERSION_CODE(2,6,0) && LINUX_VERSION_CODE < VERSION_CODE(2,6,22)
#include "dio96H_2_6_20.c"
#endif

#if LINUX_VERSION_CODE >= VERSION_CODE(2,6,22) && LINUX_VERSION_CODE < VERSION_CODE(2,6,27)
#include "dio96H_2_6_26.c"
#endif

#if LINUX_VERSION_CODE >= VERSION_CODE(2,6,29) && LINUX_VERSION_CODE < VERSION_CODE(2,6,35)
#include "dio96H_2_6_29.c"
#endif

#if LINUX_VERSION_CODE >= VERSION_CODE(3,0,0) && LINUX_VERSION_CODE < VERSION_CODE(3,7,0)
#include "dio96H_3_3_7.c"
#endif

#if LINUX_VERSION_CODE >= VERSION_CODE(3,7,0) && LINUX_VERSION_CODE < VERSION_CODE(3,20,0)
#include "dio96H_3_10_11.c"
#endif

#if LINUX_VERSION_CODE >= VERSION_CODE(4,0,0) && LINUX_VERSION_CODE < VERSION_CODE(4,20,0)
#include "dio96H_4_0_8.c"
#endif

#if LINUX_VERSION_CODE >= VERSION_CODE(4,20,0)
#error "Your kernel is too new for the current driver.  It may work but is untested."
#endif

