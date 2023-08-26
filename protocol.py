# low-level Protocol (https://tellopilots.com/wiki/protocol/#MessageIDs)
START_OF_PACKET                     = 0xcc
SSID_MSG                            = 0x0011
SSID_CMD                            = 0x0012
SSID_PASSWORD_MSG                   = 0x0013
SSID_PASSWORD_CMD                   = 0x0014
WIFI_REGION_MSG                     = 0x0015
WIFI_REGION_CMD                     = 0x0016
WIFI_MSG                            = 0x001a
VIDEO_ENCODER_RATE_CMD              = 0x0020
VIDEO_DYN_ADJ_RATE_CMD              = 0x0021
EIS_CMD                             = 0x0024
VIDEO_START_CMD                     = 0x0025
VIDEO_RATE_QUERY                    = 0x0028
TAKE_PICTURE_COMMAND                = 0x0030
VIDEO_MODE_CMD                      = 0x0031
VIDEO_RECORD_CMD                    = 0x0032
EXPOSURE_CMD                        = 0x0034
LIGHT_MSG                           = 0x0035
JPEG_QUALITY_MSG                    = 0x0037
ERROR_1_MSG                         = 0x0043
ERROR_2_MSG                         = 0x0044
VERSION_MSG                         = 0x0045
TIME_CMD                            = 0x0046
ACTIVATION_TIME_MSG                 = 0x0047
LOADER_VERSION_MSG                  = 0x0049
STICK_CMD                           = 0x0050
TAKEOFF_CMD                         = 0x0054
LAND_CMD                            = 0x0055
FLIGHT_MSG                          = 0x0056
SET_ALT_LIMIT_CMD                   = 0x0058
FLIP_CMD                            = 0x005c
THROW_AND_GO_CMD                    = 0x005d
PALM_LAND_CMD                       = 0x005e
TELLO_CMD_FILE_SIZE                 = 0x0062  # pt50
TELLO_CMD_FILE_DATA                 = 0x0063  # pt50
TELLO_CMD_FILE_COMPLETE             = 0x0064  # pt48
SMART_VIDEO_CMD                     = 0x0080
SMART_VIDEO_STATUS_MSG              = 0x0081
LOG_HEADER_MSG                      = 0x1050
LOG_DATA_MSG                        = 0x1051
LOG_CONFIG_MSG                      = 0x1052
BOUNCE_CMD                          = 0x1053
CALIBRATE_CMD                       = 0x1054
LOW_BAT_THRESHOLD_CMD               = 0x1055
ALT_LIMIT_MSG                       = 0x1056
LOW_BAT_THRESHOLD_MSG               = 0x1057
ATT_LIMIT_CMD                       = 0x1058 # Stated incorrectly by Wiki (checked from raw packets)
ATT_LIMIT_MSG                       = 0x1059

EMERGENCY_CMD                       = 'emergency'

class Packet(object):
    def __init__(self, cmd, pkt_type=0x68, payload=b''):
        if isinstance(cmd, str):
            self.buf = bytearray()
            for c in cmd:
                self.buf.append(ord(c))
        elif isinstance(cmd, (bytearray, bytes)):
            self.buf = bytearray()
            self.buf[:] = cmd
        else:
            self.buf = bytearray([
                START_OF_PACKET,
                0, 0,
                0,
                pkt_type,
                (cmd & 0xff), ((cmd >> 8) & 0xff),
                0, 0])
            self.buf.extend(payload)