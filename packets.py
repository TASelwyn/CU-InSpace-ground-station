from __future__ import annotations

# Imports
from random import randrange

# Conversion tables
hex_bin_dic = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}
bin_hex_dic = {v: k for k, v in hex_bin_dic.items()}
kx134_1211_dic = {
    '0x0': 0.781,
    '0x1': 1.563,
    '0x2': 3.125,
    '0x3': 6.25,
    '0x4': 12.5,
    '0x5': 25,
    '0x6': 50,
    '0x7': 100,
    '0x8': 200,
    '0x9': 400,
    '0xA': 800,
    '0xB': 1600,
    '0xC': 3200,
    '0xD': 6400,
    '0xE': 12800,
    '0xF': 25600,
    '0xa': 800,
    '0xb': 1600,
    '0xc': 3200,
    '0xd': 6400,
    '0xe': 12800,
    '0xf': 25600,
}


# Conversion functions
def hex_str_to_int(hex_string: str) -> int:

    """Returns the integer value of a hexadecimal string."""

    return int(hex_string, 16)


def bin_to_hex(bin_string: str) -> hex:

    """Returns a hexidecimal code for a given binary string."""

    return hex(int(bin_string, 2))


def hex_to_bin(hex_string: str) -> str:

    """Returns a binary string from a hexadecimal string.

    It is better to use this method than the built-in 'bin()' method because this method will preserve the number of
    bits. For example bin(0x10) will produce 0b'10000 when we actually want 0b'00010000."""

    # Removes '0x' from start of string, if it's present
    if hex_string[0:2] == '0x':
        hex_string = hex_string[2:]

    converted_string = ""
    for char in hex_string:
        converted_string += hex_bin_dic[char]

    return converted_string


def signed_hex_str_to_int(hex_string: str) -> int:

    """Returns an integer value for a given signed hexadecimal string. Return value preservces the number of bits."""

    bin_input = hex_to_bin(hex_string)

    if bin_input[0] == '1':
        return int(bin_input[1:], 2) - (2 ** (len(bin_input) - 1))
    else:
        return int(bin_input[1:], 2)


def signed_bin_str_to_int(bin_string: str) -> int:

    """Returns an integer value for a signed binary string."""

    return signed_hex_str_to_int(hex(int(bin_string, 2)))


# Packet classes
class AltitudeData:

    def __init__(self):
        self._time: int
        self._pressure: int
        self._temperature: int
        self._altitude: int

    # Creation
    @classmethod
    def create_from_raw(cls, raw_data: str) -> AltitudeData:

        """Returns an AltitudeData packet from raw data."""

        print(f"Packet data being set from {raw_data}")

        packet = AltitudeData()

        # Set attributes from raw data
        packet.time = raw_data[:8]
        packet.pressure = raw_data[8:16]
        packet.temperature = raw_data[16:24]
        packet.altitude = raw_data[24:32]

        return packet

    # Getters
    @property
    def time(self) -> int:
        return self._time

    @property
    def pressure(self) -> int:
        return self._pressure

    @property
    def temperature(self) -> int:
        return self._temperature

    @property
    def altitude(self) -> int:
        return self._altitude

    # Setters
    @staticmethod
    def __convert_raw(raw_data: str) -> int:

        """Checks that the raw data contains 8 nybbles (hex characters) and converts it to an integer."""

        # Error if too many or too little nybbles (hex characters)
        if len(raw_data) != 8:
            raise ValueError("Hexadecimal strings must contain 8 hexadecimal characters.")

        return hex_str_to_int(raw_data)

    @time.setter
    def time(self, raw_time: str) -> None:

        """Time is received in milliseconds."""

        self._time = self.__convert_raw(raw_time)

    @pressure.setter
    def pressure(self, raw_pressure: str) -> None:

        """Pressure in kilopascals is converted to Pascals."""

        self._pressure = self.__convert_raw(raw_pressure) / 1000

    @temperature.setter
    def temperature(self, raw_temperature: str) -> None:

        """Temperature in millidegrees Celsius is converted to a degrees Celsius."""

        self._temperature = self.__convert_raw(raw_temperature) / 1000

    @altitude.setter
    def altitude(self, raw_altitude: str) -> None:

        """Altitude in millimeters is converted to meters."""

        self._altitude = self.__convert_raw(raw_altitude) / 1000

    # String representation
    def __str__(self):
        return f"time:{self.time}\n" \
               f"pressure:{self.pressure}\n" \
               f"temperature:{self.temperature}\n" \
               f"altitude:{self.altitude}\n"


class AccelerationData:

    def __init__(self, resolution):
        self.resolution = resolution  # Resolution for calculations

        self._time: int
        self._fsr: int
        self._x_axis: int
        self._y_axis: int
        self._z_axis: int

    @classmethod
    def create_from_raw(cls, raw_data: str, resolution) -> AccelerationData:

        """Returns an AccelerationData packet from raw data."""

        print(f"Packet data being set from {raw_data}")

        packet = AccelerationData(resolution)

        # Set attributes from raw data
        packet.time = raw_data[:8]
        packet.fsr = raw_data[8:12]  # Must be set before axes, as they depend on this value
        packet.x_axis = raw_data[12:16]
        packet.y_axis = raw_data[16:20]
        packet.z_axis = raw_data[20:24]

        return packet

    # Getters
    @property
    def time(self):
        return self._time

    @property
    def fsr(self):
        return self._fsr

    @property
    def x_axis(self):
        return self._x_axis

    @property
    def y_axis(self):
        return self._y_axis

    @property
    def z_axis(self):
        return self._z_axis

    # Setters
    @staticmethod
    def __convert_raw(raw_data: str, hex_length: int) -> int:

        """Converts a hexadecimal string to an integer."""

        # Value error if string is not the right length
        if len(raw_data) != hex_length:
            raise ValueError(f"Hexadecimal string must be of length {hex_length}.")

        return hex_str_to_int(raw_data)

    @time.setter
    def time(self, raw_time: str) -> None:
        self._time = self.__convert_raw(raw_time, hex_length=8)

    @fsr.setter
    def fsr(self, raw_fsr: str) -> None:

        """Adjusts the FSR based on the resolution."""

        adjustment_factor = 16 - self.resolution + 1
        unadjusted_fsr = self.__convert_raw(raw_fsr, hex_length=4)

        self._fsr = unadjusted_fsr // 2 ** adjustment_factor

    @x_axis.setter
    def x_axis(self, raw_x_axis) -> None:
        # TODO: These are signed values and so must be fixed
        self._x_axis = self.__convert_raw(raw_x_axis, hex_length=4) * self.fsr / 2 ** 15

    @y_axis.setter
    def y_axis(self, raw_y_axis) -> None:
        self._y_axis = self.__convert_raw(raw_y_axis, hex_length=4) * self.fsr / 2 ** 15

    @z_axis.setter
    def z_axis(self, raw_z_axis) -> None:
        self._z_axis = self.__convert_raw(raw_z_axis, hex_length=4) * self.fsr / 2 ** 15

    # String representation
    def __str__(self):
        return f"{self.time_stamp}\n" \
               f"{self.fsr}\n" \
               f"{self.x_axis}\n" \
               f"{self.y_axis}\n" \
               f"{self.z_axis}\n"


class AngularVelocityData:

    def __init__(self, raw, resolution):
        self.time_stamp = None
        self.fsr = None
        self.x_velocity = None
        self.y_velocity = None
        self.z_velocity = None

        self.set_time(raw)
        self.set_fsr(raw, resolution)
        self.set_x_velocity(raw, resolution)
        self.set_y_velocity(raw, resolution)
        self.set_z_velocity(raw, resolution)

    def set_time(self, raw):
        self.time_stamp = hex_str_to_int(raw[0:8])

    def set_fsr(self, raw, resolution):
        unadjusted_fsr = hex_str_to_int(raw[8:12])

        adjustment_factor = 16 - (resolution + 1)

        self.fsr = unadjusted_fsr // (2 ** adjustment_factor)

    def set_x_velocity(self, raw, resolution):
        measurement = hex_str_to_int(raw[12:16])
        self.x_velocity = measurement * (self.fsr / (2 ** 15))

    def set_y_velocity(self, raw, resolution):
        measurement = hex_str_to_int(raw[16:20])
        self.y_velocity = measurement * (self.fsr / (2 ** 15))

    def set_z_velocity(self, raw, resolution):
        measurement = hex_str_to_int(raw[20:24])
        self.z_velocity = measurement * (self.fsr / (2 ** 15))

    def __str__(self):
        return f"fsr: {self.fsr}\n" \
               f"x_velocity: {self.x_velocity}\n" \
               f"y_velocity: {self.y_velocity}\n" \
               f"z_velocity: {self.z_velocity}\n"


class GNSSMetaData:
    class Info:
        """stores metadata on satellites used in the GNSS"""

        def __init__(self, raw):

            # elevation of GNSS satellite in degrees
            self.elevation = None

            # signal to noise ratio in dB Hz
            self.SNR = None

            # the pseudo-random noise sequence for GPS satellites or the ID for GLONASS satellites
            self.ID = None

            # satellite's azimuth in degrees
            self.azimuth = None

            # the type of satellite (GPS or GLONASS)
            self.type = None

            # set up all parameters
            self.setup(raw)

        def setup(self, raw):

            self.elevation = int(raw[0:8], 2)
            self.SNR = int(raw[8:16], 2)

            self.ID = int(raw[16:21], 2)
            self.azimuth = int(raw[21:30], 2)

            # check to see if the type bit is 1 or 0
            if raw[31] == '1':
                self.type = 'GLONASS'
            else:
                self.type = 'GPS'

        def __str__(self):

            return f"elevation: {self.elevation}\n" \
                    f"SNR: {self.SNR}\n" \
                    f"ID: {self.ID}\n" \
                    f"Azimuth: {self.azimuth}\n" \
                    f"type: {self.type}\n"

    def __init__(self, raw):
        self.mission_time = None
        self.gps_sats_in_use = []
        self.glonass_sats_in_use = []
        self.sat_info = {}
        self.setup(raw)

    def setup(self, raw):
        self.mission_time = hex_str_to_int(raw[0:8])

        # convert to binary
        bin_raw = bin(int(raw, 16))

        bin_GPS_sats_in_use = bin_raw[34:66]
        bin_GLONASS_sats_in_use = bin_raw[66:98]

        # figure out which satellites are in use
        for i in range(32):

            if bin_GPS_sats_in_use[i] == '1':
                self.gps_sats_in_use.append(i + 1)

            if bin_GLONASS_sats_in_use[i] == '1':
                self.glonass_sats_in_use.append(i + 1)

        # parse information about the satellites
        sat_info = bin_raw[98:]

        num_sats = len(sat_info) // 32

        for i in range(num_sats):
            # each satellite's info is stored in 32 bits
            meta_data = self.Info(sat_info[i * 32: i * 32 + 32])
            self.sat_info[meta_data.ID] = meta_data


class GNSSLocationData:

    def __init__(self, raw):

        # mission time when fix was received
        self.fix_time = None

        # latitude in units of 100u' (100 micro arcminute) or 10^-4 arc minutes per least significant bit
        self.latitude = None

        # latitude in units of 100u' (100 micro arcminute) or 10^-4 arc minutes per least significant bit
        self.longitude = None

        # the time (in UTX) when the fix was received in seconds since the Unix apoch
        self.utc_time = None

        # millimeters above sea level
        self.altitude = None

        # speed of the rocket over the ground in units of 1/100th of a knot
        self.rocket_speed = None

        # course of rocket in units of 1/100th of a degree
        self.rocket_course = None

        # position dilution of precision * 100
        self.pdop = None

        # horizontal dilution of precision * 100
        self.hdop = None

        # veritcal dilution of precision * 100
        self.vdop = None

        # number of GNSS satellites used to get this fix
        self.num_sats = None

        # the type of fix, can be either 'unknown', 'not available', '2D fix', or '3D fix'
        self.fix_type = None

        self.setup(raw)

    def setup(self, raw):
        print(raw)

        self.fix_time = hex_str_to_int(raw[0:8])
        self.latitude = signed_hex_str_to_int(raw[8:16])
        self.longitude = signed_hex_str_to_int((raw[16:24]))
        self.utc_time = hex_str_to_int(raw[24:32])
        self.altitude = hex_str_to_int(raw[32:40])

        self.rocket_speed = signed_hex_str_to_int(raw[40:44])
        self.rocket_course = signed_hex_str_to_int(raw[44:48])
        self.pdop = hex_str_to_int(raw[48:52])
        self.hdop = hex_str_to_int(raw[52:56])

        self.vdop = hex_str_to_int(raw[56:60])
        self.num_sats = hex_str_to_int(raw[60:62])

        fix_type_temp = hex_to_bin(raw[62:])
        fix_type_temp = fix_type_temp[2:4]
        fix_type = int(fix_type_temp, 2)

        if fix_type == 0:
            self.fix_type = 'unknown'
        elif fix_type == 1:
            self.fix_type = 'not available'
        elif fix_type == 2:
            self.fix_type = '2D fix'
        elif fix_type == 3:
            self.fix_type = '3D fix'
        else:
            self.fix_type = 'error'

    def __str__(self):
        return f"fix time: {self.fix_time}\n" \
                f"latitude: {self.latitude}\n" \
                f"longitude: {self.longitude}\n" \
                f"utc_time: {self.utc_time}\n" \
                f"altitude: {self.altitude}\n" \
                f"rocket speed: {self.rocket_speed}\n" \
                f"rocket_course: {self.rocket_course}\n" \
                f"pdop: {self.pdop}\n" \
                f"hdop: {self.hdop}\n" \
                f"vdop: {self.vdop}\n" \
                f"num_sats: {self.num_sats}\n" \
                f"fix_type: {self.fix_type}\n"


class MPU9250Data:
    """data from the MPU9250 IMU"""

    class Measurement:

        def __init__(self, raw_bin):
            print(raw_bin)
            self.time_stamp = int(raw_bin[0:32], 2)
            self.accel_x = int(raw_bin[32:48], 2)
            self.accel_y = int(raw_bin[48:64], 2)
            self.accel_z = int(raw_bin[64:80], 2)
            self.temperature = int(raw_bin[80:96], 2)

            self.gyro_x = int(raw_bin[96:112], 2)
            self.gyro_y = int(raw_bin[112:128], 2)
            self.gyro_z = int(raw_bin[128:144], 2)

            self.mag_x = int(raw_bin[144:160], 2)
            self.mag_y = int(raw_bin[160:176], 2)
            self.mag_z = int(raw_bin[176:192], 2)

            self.mag_valid = int(raw_bin[195], 2)
            self.mag_resolution = int(raw_bin[196], 2)

        def __str__(self):
            return f"time: {self.time_stamp}\n" \
                   f"temperature: {self.temperature}\n" \
                   f"accel x: {self.accel_x}\n" \
                   f"accel y: {self.accel_y}\n" \
                   f"accel z: {self.accel_z}\n" \
                   f"gyro x: {self.gyro_x}\n" \
                   f"gyro y: {self.gyro_y}\n" \
                   f"gyro z: {self.gyro_z}\n" \
                   f"mag x: {self.mag_x}\n" \
                   f"mag y: {self.mag_y}\n" \
                   f"mag z: {self.mag_z}\n" \
                   f"mag valid: {self.mag_valid}\n" \
                   f"mag resolution: {self.mag_resolution}\n"

    def __init__(self, raw):
        self.time_stamp = None

        # sample rate of the accelerometer and gyroscope
        self.ag_sample_rate = None

        # accelerometer full scale range
        self.accelerometer_fsr = None

        # gyroscope full scale range
        self.gyroscope_fsr = None

        # bandwidth for the low pass filter used by the accelerometer
        self.accelerometer_bw = None

        # bandwidth for the low pass filter used by the gyroscope
        self.gyroscope_bw = None

        self.setup(raw)

    def setup(self, raw):
        self.time_stamp = hex_str_to_int(raw[0:8])

        self.ag_sample_rate = hex_str_to_int(raw[8:10])

        raw_bin = hex_to_bin(raw)

        # get the fsr of the accelerometer
        raw_a_fsr = int(raw_bin[39:41], 2)
        self.accelerometer_fsr = 2 ** (raw_a_fsr + 1)

        # TODO: this needs to be finished after we receive an input from this device


class KX1341211Data:
    class Measurement:
        def __init__(self, raw):
            self.x_accel = None
            self.y_accel = None
            self.z_accel = None

            self.setup(raw)

        def setup(self, raw):
            # if resolution of data is 8 bit (three 8 bit readings)
            if len(raw) == 24:
                self.x_accel = signed_bin_str_to_int(raw[0:8])
                self.y_accel = signed_bin_str_to_int(raw[8:16])
                self.z_accel = signed_bin_str_to_int(raw[16:24])

            # if resolution of data is 16 bit (three 16 bit readings)
            elif len(raw) == 48:
                self.x_accel = int(raw[0:16], 2)
                self.y_accel = int(raw[16:32], 2)
                self.z_accel = int(raw[32:48], 2)

        def __str__(self):
            return f"x: {self.x_accel}\n" \
                   f"y: {self.y_accel}\n" \
                   f"z: {self.z_accel}\n"

    def __init__(self, raw):

        self.time_stamp = None

        # data rate of the accelerometer in Hz
        self.data_rate = None

        # set the full scale range (in G's)
        self.full_scale_range = None

        # the corner frequency of the accelerometer's low pass filter (in Hz)
        self.corner_freq = None

        # the actual measurements taken by the accelerometer
        self.measurements = []

        self.setup(raw)

    def __str__(self):

        data_points_str = ''
        for m in self.measurements:
            data_points_str += str(m)
            data_points_str += '____\n'

        return f"time stamp: {self.time_stamp}\n" \
               f"data rate: {self.data_rate}\n" \
               f"full scale range: {self.full_scale_range}\n" \
               f"corner frequency: {self.corner_freq}\n" \
               f"measurements:\n{data_points_str}" + "-" * 20

    def setup(self, raw):

        raw_bin = hex_to_bin(raw)

        self.time_stamp = int(raw_bin[0:32], 2)

        # data rate of the accelerometer in Hz
        data_rate = hex(int(raw_bin[32:36], 2))
        self.data_rate = kx134_1211_dic[data_rate]

        # set the full scale range (in G's)
        full_scale_range = int(raw_bin[36:38], 2)

        if full_scale_range == 0:
            self.full_scale_range = 8
        elif full_scale_range == 1:
            self.full_scale_range = 16
        elif full_scale_range == 2:
            self.full_scale_range = 32
        elif full_scale_range == 3:
            self.full_scale_range = 64
        else:
            self.full_scale_range = -1

        # the corner frequency of the accelerometer's low pass filter (in Hz)
        corner_freq = raw_bin[38]

        if corner_freq == '0':
            self.corner_freq = self.data_rate / 9
        elif corner_freq == '1':
            self.corner_freq = self.data_rate / 2

        # resolution of the accelerometer reading (in bits)
        resolution = raw_bin[39]

        if resolution == '0':
            resolution = 8
        elif resolution == '1':
            resolution = 16

        print('resolution is ', resolution)

        # number of bits of padding added to the end of the data packet
        padding = int(raw_bin[46:48], 2) * 8
        print('padding is ', padding)

        accel_data = raw_bin[48:]

        chunk_size = resolution * 3

        # break the accel data into chunks that contain acceleration in the x y and z directions
        accel_data = [accel_data[i:i + chunk_size] for i in range(0, (len(accel_data) - padding), chunk_size)]

        print(accel_data)
        for data in accel_data:
            self.measurements.append(self.Measurement(data))
