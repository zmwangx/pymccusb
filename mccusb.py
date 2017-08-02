import os
from ctypes import *


# Do not load shared library when building docs.
# This allows building docs in any pure Python environment.
if not os.getenv('SPHINX_BUILD'):
    libmccusb = cdll.LoadLibrary('libmccusb.so')
    # libusb_init is essential; without it usb_device_find_USB_MCC would segfault.
    libmccusb.libusb_init(None)


def getfunc(name, argtypes, restype):
    func = getattr(libmccusb, name)
    func.argtypes = argtypes
    func.restype = restype
    return func


def sequence_to_array(seq, member_type, length=None):
    # Convert any sequence or iterator type to a ctypes array. Iterator
    # is apparently consumed. member_type should be a ctypes type. The
    # length of the array is the length of the sequence unless
    # specified.
    flat = list(seq)
    if length is None:
        length = len(flat)
    return (member_type * length)(*flat)


class DeviceNotFoundError(Exception):
    pass


class MCCUSBDevice(object):

    def __init__(self, part_number, product_id):
        self.part_number = part_number
        # libusb_device_handle* usb_device_find_USB_MCC(int productId, char *serialID);
        usb_device_find = getfunc('usb_device_find_USB_MCC', [c_int, c_char_p], c_void_p)
        device_handle = usb_device_find(product_id, None)
        if device_handle is None:
            raise DeviceNotFoundError()
        else:
            self._device_handle = device_handle


class MCCUSB1208FSPlusDevice(MCCUSBDevice):

    # Constants from <libusb/usb-1208FS-Plus.h>

    PRODUCT_ID = 0x00e8

    # Digial I/O commands
    DTRISTATE       = 0x00  # Read/Write Tristate register
    DPORT           = 0x01  # Read digital port pins
    DLATCH          = 0x02  # Read/Write Digital port output latch register

    # Analog input commands
    AIN             = 0x10  # Read analog input channel
    AIN_SCAN_START  = 0x11  # Start analog input scan
    AIN_SCAN_STOP   = 0x12  # Stop analog input scan
    AIN_CONFIG      = 0x14  # Analog input channel configuration
    AIN_CLR_FIFO    = 0x15  # Clear the analog input scan FIFO
    AIN_BULK_FLUSH  = 0x16  # Flush the bulk IN endpoint with empty packets

    # Analog output commands
    AOUT            = 0x18  # Read/Write analog output channel
    AOUT_SCAN_START = 0x1A  # Start analog output scan
    AOUT_SCAN_STOP  = 0x1B  # Stop analog output scan
    AOUT_CLR_FIFO   = 0x1C  # Clear the analog output scan FIFO

    # Counter/Timer commands
    COUNTER         = 0x20  # Read/reset event counter

    # Memory commands
    CAL_MEMORY      = 0x30  # Read/Write Calibration Memory
    USER_MEMORY     = 0x31  # Read/Write User Memory
    MBD_MEMORY      = 0x32  # Read/Write MBD Memory

    # Miscellaneous commands
    BLINK_LED       = 0x41  # Causes LED to blink
    RESET           = 0x42  # Reset device
    STATUS          = 0x44  # Read device status
    SERIAL          = 0x48  # Read/Write serial number
    DFU             = 0x50  # Enter device firmware upgrade mode

    # MBD
    MBD_COMMAND     = 0x80  # Text-based MBD command / response
    MBD_RAW         = 0x81  # Raw MBD response

    # Analog input scan options
    IMMEDIATE_TRANSFER_MODE = 0x1
    BLOCK_TRANSFER_MODE     = 0x0
    DIFFERENTIAL_MODE       = 0x2
    SINGLE_ENDED_MODE       = 0x0
    NO_TRIGGER              = 0x0
    TRIG_EDGE_RISING        = 0x1 << 2
    TRIG_EDGE_FALLING       = 0x2 << 2
    TRIG_LEVEL_HIGH         = 0x3 << 2
    TRIG_LEVEL_LOW          = 0x4 << 2
    RETRIGGER_MODE          = 0x1 << 5
    STALL_ON_OVERRUN        = 0x0
    CONTINUOUS              = 0x1 << 6
    INHIBIT_STALL           = 0x1 << 7

    # Analog input
    SINGLE_ENDED   = 0
    DIFFERENTIAL   = 1
    CALIBRATION    = 3
    LAST_CHANNEL   = 0x80
    PACKET_SIZE    = 64       # max bulk transfer size in bytes

    # Ranges
    BP_20V   = 0x0      # +/- 20 V
    BP_10V   = 0x1      # +/- 10V
    BP_5V    = 0x2      # +/- 5V
    BP_4V    = 0x3      # +/- 4V
    BP_2_5V  = 0x4      # +/- 2.5V
    BP_2V    = 0x5      # +/- 2V
    BP_1_25V = 0x6      # +/- 1.25V
    BP_1V    = 0x7      # +/- 1V
    UP_5V    = 0x8      # 0-5 V analog output

    # Status bit values
    AIN_SCAN_RUNNING   = 0x1 << 1
    AIN_SCAN_OVERRUN   = 0x1 << 2
    AOUT_SCAN_RUNNING  = 0x1 << 3
    AOUT_SCAN_OVERRUN  = 0x1 << 4

    NCHAN_DE                =  4  # max number of A/D differential channels
    NCHAN_SE                =  8  # max number of A/D single-ended channels
    NCHAN_AOUT              =  2  # max number of D/A 12 bit 0-5V output channels
    NGAINS_USB1208FS_PLUS   =  8  # max number of input gain levels (differential mode only)
    MAX_PACKET_SIZE         = 64  # max packet size for FS device

    PORTA     = 0  # DIO Port A
    PORTB     = 1  # DIO Port B

    def __init__(self):
        MCCUSBDevice.__init__(self, 'USB-1208FS-Plus', self.PRODUCT_ID)

    def dTristateR(self, port):
        # uint8_t usbDTristateR_USB1208FS_Plus(libusb_device_handle *udev, uint8_t port);
        f = getfunc('usbDTristateR_USB1208FS_Plus', [c_void_p, c_uint8], c_uint8)
        return f(self._device_handle, port)

    def dTristateW(self, port, value):
        # void usbDTristateW_USB1208FS_Plus(libusb_device_handle *udev, uint8_t port, uint8_t value);
        f = getfunc('usbDTristateW_USB1208FS_Plus', [c_void_p, c_uint8, c_uint8], None)
        f(self._device_handle, port, value)

    def dPort(self, port):
        # uint8_t usbDPort_USB1208FS_Plus(libusb_device_handle *udev, uint8_t port);
        f = getfunc('usbDPort_USB1208FS_Plus', [c_void_p, c_uint8], c_uint8)
        return f(self._device_handle, port)

    def dLatchR(self, port):
        # uint8_t usbDLatchR_USB1208FS_Plus(libusb_device_handle *udev, uint8_t port);
        f = getfunc('usbDLatchR_USB1208FS_Plus', [c_void_p, c_uint8], c_uint8)
        return f(self._device_handle, port)

    def dLatchW(self, port, value):
        # void usbDLatchW_USB1208FS_Plus(libusb_device_handle *udev, uint8_t port, uint8_t value);
        f = getfunc('usbDLatchW_USB1208FS_Plus', [c_void_p, c_uint8, c_uint8], None)
        f(self._device_handle, port, value)

    def aIn(self, channel, mode, range_):
        # uint16_t usbAIn_USB1208FS_Plus(libusb_device_handle *udev, uint8_t channel, uint8_t mode, uint8_t range);
        f = getfunc('usbAIn_USB1208FS_Plus', [c_void_p, c_uint8, c_uint8, c_uint8], c_uint16)
        return f(self._device_handle, channel, mode, range_)

    def aInScanStart(self, count, retrig_count, frequency, channels, options):
        # void usbAInScanStart_USB1208FS_Plus(libusb_device_handle *udev, uint32_t count, uint32_t retrig_count, double frequency, uint8_t channels, uint8_t options);
        f = getfunc('usbAInScanStart_USB1208FS_Plus', [c_void_p, c_uint32, c_uint32, c_double, c_uint8, c_uint8], None)
        f(self._device_handle, count, retrig_count, frequency, channels, options)

    def aInScanConfig(self, ranges):
        # void usbAInScanConfig_USB1208FS_Plus(libusb_device_handle *udev, uint8_t ranges[8]);
        f = getfunc('usbAInScanConfig_USB1208FS_Plus', [c_void_p, c_uint8 * 8], None)
        f(self._device_handle, sequence_to_array(ranges, c_uint8, 8))

    def aInScanConfigR(self, ranges):
        # void usbAInScanConfigR_USB1208FS_Plus(libusb_device_handle *udev, uint8_t *ranges);
        f = getfunc('usbAInScanConfigR_USB1208FS_Plus', [c_void_p, POINTER(c_uint8)], None)
        f(self._device_handle, sequence_to_array(ranges, c_uint8))

    def aInScanRead(self, nscan, nchan, options, timeout, buffersize):
        # int usbAInScanRead_USB1208FS_Plus(libusb_device_handle *udev, int nScan, int nChan, uint16_t *data, uint8_t options, int timeout);
        f = getfunc('usbAInScanRead_USB1208FS_Plus', [c_void_p, c_int, c_int, POINTER(c_uint16), c_uint8, c_int], c_int)
        buf = (c_uint16 * buffersize)()
        ret = f(self._device_handle, nscan, nchan, buf, options, timeout)
        return ret, [val for val in buf]

    def aInScanStop(self):
        # void usbAInScanStop_USB1208FS_Plus(libusb_device_handle *udev);
        f = getfunc('usbAInScanStop_USB1208FS_Plus', [c_void_p], None)
        f(self._device_handle)

    def aInScanClearFIFO(self):
        # void usbAInScanClearFIFO_USB1208FS_Plus(libusb_device_handle *udev);
        f = getfunc('usbAInScanClearFIFO_USB1208FS_Plus', [c_void_p], None)
        f(self._device_handle)

    def aOut(self, channel, value):
        # void usbAOut_USB1208FS_Plus(libusb_device_handle *udev, uint8_t channel, uint16_t value);
        f = getfunc('usbAOut_USB1208FS_Plus', [c_void_p, c_uint8, c_uint16], None)
        f(self._device_handle, channel, value)

    def aOutR(self, channel):
        # uint16_t usbAOutR_USB1208FS_Plus(libusb_device_handle *udev, uint8_t channel);
        f = getfunc('usbAOutR_USB1208FS_Plus', [c_void_p, c_uint8], c_uint16)
        return f(self._device_handle, channel)

    def aOutScanStop(self):
        # void usbAOutScanStop_USB1208FS_Plus(libusb_device_handle *udev);
        f = getfunc('usbAOutScanStop_USB1208FS_Plus', [c_void_p], None)
        f(self._device_handle)

    def aOutScanClearFIFO(self):
        # void usbAOutScanClearFIFO_USB1208FS_Plus(libusb_device_handle *udev);
        f = getfunc('usbAOutScanClearFIFO_USB1208FS_Plus', [c_void_p], None)
        f(self._device_handle)

    def aInBulkFlush(self, count):
        # void usbAInBulkFlush_USB1208FS_Plus(libusb_device_handle *udev, uint8_t count);
        f = getfunc('usbAInBulkFlush_USB1208FS_Plus', [c_void_p, c_uint8], None)
        f(self._device_handle, count)

    def aOutScanStart(self, count, frequency, options):
        # void usbAOutScanStart_USB1208FS_Plus(libusb_device_handle *udev, uint32_t count, double frequency, uint8_t options);
        f = getfunc('usbAOutScanStart_USB1208FS_Plus', [c_void_p, c_uint32, c_double, c_uint8], None)
        f(self._device_handle, count, frequency, options)

    def counter(self):
        # uint32_t usbCounter_USB1208FS_Plus(libusb_device_handle *udev);
        f = getfunc('usbCounter_USB1208FS_Plus', [c_void_p], c_uint32)
        return f(self._device_handle)

    def counterInit(self):
        # void usbCounterInit_USB1208FS_Plus(libusb_device_handle *udev);
        f = getfunc('usbCounterInit_USB1208FS_Plus', [c_void_p], None)
        f(self._device_handle)

    def readCalMemory(self, address, count, buffersize):
        # void usbReadCalMemory_USB1208FS_Plus(libusb_device_handle *udev, uint16_t address, uint16_t count, uint8_t memory[]);
        f = getfunc('usbReadCalMemory_USB1208FS_Plus', [c_void_p, c_uint16, c_uint16, POINTER(c_uint8)], None)
        buf = (c_uint8 * buffersize)()
        f(self._device_handle, address, count, buf)
        return [val for val in buf]

    def writeCalMemory(self, address, count, data):
        # void usbWriteCalMemory_USB1208FS_Plus(libusb_device_handle *udev, uint16_t address,  uint16_t count, uint8_t data[]);
        f = getfunc('usbWriteCalMemory_USB1208FS_Plus', [c_void_p, c_uint16, c_uint16, POINTER(c_uint8)], None)
        f(self._device_handle, address, count, sequence_to_array(data, c_uint8))

    def readUserMemory(self, address, count, buffersize):
        # void usbReadUserMemory_USB1208FS_Plus(libusb_device_handle *udev, uint16_t address, uint16_t count, uint8_t memory[]);
        f = getfunc('usbReadUserMemory_USB1208FS_Plus', [c_void_p, c_uint16, c_uint16, POINTER(c_uint8)], None)
        buf = (c_uint8 * buffersize)()
        f(self._device_handle, address, count, buf)
        return [val for val in buf]

    def writeUserMemory(self, address, count, data):
        # void usbWriteUserMemory_USB1208FS_Plus(libusb_device_handle *udev, uint16_t address,  uint16_t count, uint8_t data[]);
        f = getfunc('usbWriteUserMemory_USB1208FS_Plus', [c_void_p, c_uint16, c_uint16, POINTER(c_uint8)], None)
        f(self._device_handle, address, count, sequence_to_array(data, c_uint8))

    def readMBDMemory(self, address, count, buffersize):
        # void usbReadMBDMemory_USB1208FS_Plus(libusb_device_handle *udev, uint16_t address, uint16_t count, uint8_t memory[]);
        f = getfunc('usbReadMBDMemory_USB1208FS_Plus', [c_void_p, c_uint16, c_uint16, POINTER(c_uint8)], None)
        buf = (c_uint8 * buffersize)()
        f(self._device_handle, address, count, buf)
        return [val for val in buf]

    def writeMBDMemory(self, address, count, data):
        # void usbWriteMBDMemory_USB1208FS_Plus(libusb_device_handle *udev, uint16_t address,  uint16_t count, uint8_t data[]);
        f = getfunc('usbWriteMBDMemory_USB1208FS_Plus', [c_void_p, c_uint16, c_uint16, POINTER(c_uint8)], None)
        f(self._device_handle, address, count, sequence_to_array(data, c_uint8))

    def blink(self, count):
        # void usbBlink_USB1208FS_Plus(libusb_device_handle *udev, uint8_t count);
        f = getfunc('usbBlink_USB1208FS_Plus', [c_void_p, c_uint8], None)
        f(self._device_handle, count)

    def reset(self):
        # void usbReset_USB1208FS_Plus(libusb_device_handle *udev);
        f = getfunc('usbReset_USB1208FS_Plus', [c_void_p], None)
        f(self._device_handle)

    def status(self):
        # uint16_t usbStatus_USB1208FS_Plus(libusb_device_handle *udev);
        f = getfunc('usbStatus_USB1208FS_Plus', [c_void_p], c_uint16)
        return f(self._device_handle)

    def getSerialNumber(self):
        # void usbGetSerialNumber_USB1208FS_Plus(libusb_device_handle *udev, char serial[9]);
        f = getfunc('usbGetSerialNumber_USB1208FS_Plus', [c_void_p, c_char * 9], None)
        buf = create_string_buffer(9)
        f(self._device_handle, buf)
        return b''.join(ch for ch in buf if ch != b'\x00')

    def dfu(self):
        # void usbDFU_USB1208FS_Plus(libusb_device_handle *udev);
        f = getfunc('usbDFU_USB1208FS_Plus', [c_void_p], None)
        f(self._device_handle)

    def mbdCommand(self, str_):
        # void usbMBDCommand_USB1208FS_Plus(libusb_device_handle *udev, uint8_t str[]);
        f = getfunc('usbMBDCommand_USB1208FS_Plus', [c_void_p, POINTER(c_uint8)], None)
        f(self._device_handle, sequence_to_array(str_, c_uint8))

    def mbdRaw(self, cmd, size):
        # void usbMBDRaw_USB1208FS_Plus(libusb_device_handle *udev, uint8_t cmd[], uint16_t size);
        f = getfunc('usbMBDRaw_USB1208FS_Plus', [c_void_p, POINTER(c_uint8), c_uint16], None)
        f(self._device_handle, sequence_to_array(cmd, c_uint8))

    def cleanup(self):
        # void cleanup_USB1208FS_Plus(libusb_device_handle *udev);
        f = getfunc('cleanup_USB1208FS_Plus', [c_void_p], None)
        f(self._device_handle)

    def buildGainTableDE(self, table_DE):
        # void usbBuildGainTable_DE_USB1208FS_Plus(libusb_device_handle *udev, float table_DE[NGAINS_USB1208FS_PLUS][NCHAN_DE][2]);
        table_type = c_float * 2 * self.NCHAN_DE * self.NGAINS_USB1208FS_PLUS
        f = getfunc('usbBuildGainTable_DE_USB1208FS_Plus', [c_void_p, table_type], None)
        table = table_type()
        for i in range(self.NGAINS_USB1208FS_PLUS):
            for j in range(self.NCHAN_DE):
                for k in range(2):
                    table[i][j][k] = table_DE[i][j][k]
        f(self._device_handle, table)

    def buildGainTableSE(self, table_SE):
        # void usbBuildGainTable_SE_USB1208FS_Plus(libusb_device_handle *udev, float table_SE[NCHAN_SE][2]);
        table_type = c_float * 2 * self.NCHAN_SE
        f = getfunc('usbBuildGainTable_SE_USB1208FS_Plus', [c_void_p, table_type], None)
        table = table_type()
        for i in range(self.NCHAN_SE):
            for j in range(2):
                table[i][j] = table_SE[i][j]
        f(self._device_handle, table)

    def volts(self, value, range_):
        # double volts_USB1208FS_Plus(uint16_t value, uint8_t range);
        f = getfunc('volts_USB1208FS_Plus', [c_uint16, c_uint8], c_double)
        return f(value, range_)

    # TODO: Construt struct tm in Python
    # void usbCalDate_USB1208FS_Plus(libusb_device_handle *udev, struct tm *date);


class MCCUSB1408FSPlusDevice(MCCUSB1208FSPlusDevice):

    PRODUCT_ID = 0x00e9

    def __init__(self):
        MCCUSBDevice.__init__(self, 'USB-1408FS-Plus', self.PRODUCT_ID)

    def volts(self, value, range_):
        # double volts_USB1408FS_Plus(uint16_t value, uint8_t range);
        f = getfunc('volts_USB1408FS_Plus', [c_uint16, c_uint8], c_double)
        return f(value, range_)
