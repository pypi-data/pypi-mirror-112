import base64

from . import utility as util


class JciHitachiCommand:
    """Sending job command.

    Parameters
    ----------
    gateway_mac_address : str
        Gateway mac address.
    """

    def __init__(self, gateway_mac_address):
        self.job_info_base = bytearray.fromhex(
                              "d0d100003c6a9dffff03e0d4ffffffff \
                               00000100000000000000002000010000 \
                               000000000000000002000d278050f0d4 \
                               469dafd3605a6ebbdb130d278052f0d4 \
                               469dafd3605a6ebbdb13060006010000 \
                               0000")
        self.job_info_base[32:40] = bytearray.fromhex(hex(int(gateway_mac_address))[2:])
    
    def get_command(self, command, value):
        raise NotImplementedError
    
    def get_b64command(self, command, value):
        return base64.b64encode(self.get_command(command, value)).decode()


class JciHitachiCommandAC(JciHitachiCommand):
    def __init__(self, gateway_mac_address):
        super().__init__(gateway_mac_address)

    def get_command(self, command, value):
        job_info = self.job_info_base.copy()
        
        # Command (eg. target_temp)
        job_info[78] = 128 + JciHitachiAC.idx[command]

        # Value (eg. 27)
        job_info[80] = value

        # Checksum 
        # Original algorithm:
        # xor job_info 76~80
        # Since byte 76, 77, and 79 are constants,
        # here is the simplified algorithm:
        # command ^ value ^ 0x07 (flip last 3 bits) 
        job_info[81] = job_info[78] ^ job_info[80] ^ 0x07

        assert len(job_info) == 82, \
            "The length of job_info should be 82 bytes."

        return job_info


class JciHitachiStatusInterpreter:
    def __init__(self, code):
        self.base64_bytes = base64.standard_b64decode(code)
        self.status_number = self._decode_status_number()

    def _decode_status_number(self):
        if 6 < self.base64_bytes[0] and (self.base64_bytes[1], self.base64_bytes[2]) == (0, 8):
            return int((self.base64_bytes[0]-4)/3)
        else:
            return 0

    def _decode_single_status(self, max_func_number, while_counter):
        output = util.bin_concat(0xff, max_func_number)
        output = (output << 16) & 0xffff0000 | max_func_number

        stat_idx = while_counter * 3 + 3

        if stat_idx + 3 <= self.base64_bytes[0] - 1:
            var1 = self.base64_bytes[stat_idx]
            var2 = util.cast_bytes(var1, 1)
            var3 = util.cast_bytes(var1 >> 8, 1)

            inner_concat = util.bin_concat(var2, (var1 & 0x80) != 0)
            mid_concat = util.bin_concat(var3, inner_concat, 1, 2)
            outer_concat = util.bin_concat(self.base64_bytes[stat_idx + 2], mid_concat, 1, 3)
            return outer_concat & 0xffff7fff
        else:
            return output

    def decode_status(self):
        table = {}
        for i in range(self.status_number):
            ret = self._decode_single_status(self.status_number, i)
            idx = util.cast_bytes(ret >> 8, 1)
            table[idx] = ret >> 0x18
        return table


class JciHitachiAC:
    idx = {
        'power': 0,
        'mode': 1,
        'air_speed': 2,
        'target_temp': 3,
        'indoor_temp': 4,
        'sleep_timer': 6,
        'mold_prev': 23,
        'fast_op': 26,
        'energy_save': 27,
        'sound_prompt': 30,
        'outdoor_temp': 33
    }

    def __init__(self, status):
        self._status = status
        
    @property
    def status(self):
        return {
            "power": self.power,
            "mode" : self.mode,
            "air_speed": self.air_speed,
            "target_temp": self.target_temp,
            "indoor_temp": self.indoor_temp,
            "sleep_timer": self.sleep_timer,
            "mold_prev": self.mold_prev,
            'fast_op': self.fast_op,
            'energy_save': self.energy_save,
            'sound_prompt': self.sound_prompt,
            "outdoor_temp": self.outdoor_temp
        }

    @property
    def power(self):
        v = self._status.get(JciHitachiAC.idx['power'], -1)
        if v == -1:
            return "unsupported"
        elif v == 0:
            return "off"
        elif v == 1:
            return "on"
        else:
            return "unknown"

    @property
    def mode(self):
        v = self._status.get(JciHitachiAC.idx['mode'], -1)
        if v == -1:
            return "unsupported"
        elif v == 0:
            return "cool"
        elif v == 1:
            return "dry"
        elif v == 2:
            return "fan"
        elif v == 3:
            return "auto"
        elif v == 4:
            return "heat"
        else:
            return "unknown"

    @property
    def air_speed(self):
        v = self._status.get(JciHitachiAC.idx['air_speed'], -1)
        if v == -1:
            return "unsupported"
        elif v == 0:
            return "auto"
        elif v == 1:
            return "silent"
        elif v == 2:
            return "low"
        elif v == 3:
            return "moderate"
        elif v == 4:
            return "high"
        else:
            return "unknown"

    @property
    def target_temp(self):
        """Target temperature"""
        v = self._status.get(JciHitachiAC.idx['target_temp'], -1)
        return v

    @property
    def indoor_temp(self):
        """Indoor temperature"""
        v = self._status.get(JciHitachiAC.idx['indoor_temp'], -1)
        return v
    
    @property
    def max_temp(self):
        """Maximum target temperature"""
        return 32
    
    @property
    def min_temp(self):
        """Minimum target temperature"""
        return 16

    @property
    def sleep_timer(self):
        """Sleep timer"""
        v = self._status.get(JciHitachiAC.idx['sleep_timer'], -1)
        return v
    
    @property
    def mold_prev(self):
        """Mold prevention"""
        v = self._status.get(JciHitachiAC.idx['mold_prev'], -1)
        if v == -1:
            return "unsupported"
        elif v == 0:
            return "disabled"
        elif v == 1:
            return "enabled"
        else:
            return "unknown"
    
    @property
    def fast_op(self):
        """Fast operation"""
        v = self._status.get(JciHitachiAC.idx['fast_op'], -1)
        if v == -1:
            return "unsupported"
        elif v == 0:
            return "disabled"
        elif v == 1:
            return "enabled"
        else:
            return "unknown"
    
    @property
    def energy_save(self):
        """Energy saving"""
        v = self._status.get(JciHitachiAC.idx['energy_save'], -1)
        if v == -1:
            return "unsupported"
        elif v == 0:
            return "disabled"
        elif v == 1:
            return "enabled"
        else:
            return "unknown"

    @property
    def sound_prompt(self):
        """Sound prompt"""
        v = self._status.get(JciHitachiAC.idx['sound_prompt'], -1)
        if v == -1:
            return "unsupported"
        elif v == 0:
            return "enabled"
        elif v == 1:
            return "disabled"
        else:
            return "unknown"

    @property
    def outdoor_temp(self):
        """Outdoor temperature"""
        v = self._status.get(JciHitachiAC.idx['outdoor_temp'], -1)
        return v
