from time import sleep
import numpy as np
from qcodes import ChannelList, InstrumentChannel
from qcodes.utils.validators import Arrays, Enum
from qcodes.instrument.group_parameter import GroupParameter, Group
from qcodes.instrument.ip import IPInstrument


class SiglentSds1102xChannel(InstrumentChannel):
    """
    Contains methods and attributes specific to the Siglent
    oscilloscope channels.
    The output trace from each channel of the oscilloscope
    can be obtained using 'trace' parameter.
    """

    def __init__(self, parent, name, channel):
        super().__init__(parent, name)
        self.channel = channel

        self.add_parameter('volt_vdiv',
                           get_cmd=f':C{channel}:VDIV?',
                           set_cmd=f':C{channel}:VDIV {{}}',
                           get_parser=float)
        self.add_parameter('offset',
                           get_cmd=f'C{channel}:OFFSET?',
                           set_cmd=f':C{channel}:OFFSET {{}}',
                           get_parser=float)
        self.add_parameter('trace',
                           get_cmd=self._get_full_trace,
                           vals=Arrays(shape=(self.parent.number_of_point,)))
        self.add_parameter('trig_slope',
                           get_cmd=f'C{channel}:TRIG_SLOPE?',
                           set_cmd=f'C{channel}:TRIG_SLOPE {{}}',
                           vals=Enum('NEG', 'POS', 'WINDOW'))
        self.add_parameter('trig_level',
                           get_cmd=f'C{channel}:TRIG_LEVEL?',
                           set_cmd=f'C{channel}:TRIG_LEVEL {{}}')
        self.add_parameter('trig_coupling',
                           get_cmd=f'C{channel}:TRIG_COUPLING?',
                           set_cmd=f'C{channel}:TRIG_COUPLING {{}}',
                           vals=Enum('AC', 'DC', 'HFREJ', 'LFREJ'))
        self.add_parameter('parameter_custom',
                           set_cmd=f'PACU {{}},C{channel}',
                           vals=Enum('PKPK', 'MAX', 'MIN', 'AMPL', 'TOP', 'BASE', 'CMEAN', 'MEAN', 'STDEV', 'VSTD',
                                     'RMS', 'CRMS', 'OVSN', 'FPRE', 'OVSP', 'RPRE', 'LEVELX', 'DELAY', 'TIMEL', 'PER',
                                     'FREQ', 'PWID', 'NWID', 'RISE', 'FALL', 'WID', 'DUTY', 'NDUTY', 'ALL'))
        self.add_parameter('parameter_mean_value',
                           get_cmd=f'C{channel}:PAVA? MEAN',
                           get_parser=lambda msg: float(msg.split(',')[1]))

    def _get_full_trace(self) -> np.ndarray:
        y_vdiv = self.volt_vdiv()
        y_offset = self.offset()
        y_raw = self._get_raw_trace()
        full_data = y_raw * (y_vdiv/25) - y_offset
        return full_data

    def _get_raw_trace(self) -> np.ndarray:
        raw_trace_val = self.root_instrument.visa_handle.query_binary_values(
            f'C{self.channel}:WF? DAT2',
            datatype='h',  # h for signed short integer, https://docs.python.org/3/library/struct.html#format-characters
            is_big_endian=False,
            expect_termination=False)  # \n\n
        return np.array(raw_trace_val)


class Sds1102x(IPInstrument):
    """
    The QCoDeS drivers for Oscilloscope Siglent DS1102X.
    """
    def __init__(self, address=None, port=5025, **kwargs):
        super().__init__('Sds1102x', address, port, timeout=5, terminator='\n', persistent=False,
                         write_confirmation=False, **kwargs)
        self.add_parameter('reset',
                           set_cmd='*RST'
                           )
        self.add_parameter('comm_header',
                           set_cmd='CHDR {}'
                           )
        self.add_parameter('arm_acquisition',
                           set_cmd='ARM'  # start a new signal acquisition
                           )
        self.add_parameter('internal_state_register',
                           get_cmd='INR?'  # query reads and clears the contents of internal register
                           )
        self.add_parameter('parameter_clr',
                           set_cmd='PARAMETER_CLR'  # pass/fail clear
                           )
        self.add_parameter('pf_createm',
                           set_cmd='PFCM'  # pass/fail create mask rule
                           )
        self.add_parameter('pf_datadis',
                           get_cmd='PFDD?',  # pass/fail query pass/fail result
                           get_parser=lambda msg: {'fail': msg.split(',')[1], 'pass': msg.split(',')[3], 'total': msg.split(',')[5]}
                           )
        self.add_parameter('pf_display',
                           set_cmd='PFDS {}',
                           vals=Enum('ON', 'OFF'),
                           get_cmd='PFDS?'  # pass/fail display enable
                           )
        self.add_parameter('pf_enable',
                           set_cmd='PFEN {}',
                           vals=Enum('ON', 'OFF'),
                           get_cmd='PFEN?'  # pass/fail enable
                           )
        self.add_parameter('pf_fail_stop',
                           set_cmd='PFFS {}',
                           vals=Enum('ON', 'OFF'),
                           get_cmd='PFFS?'  # pass/fail stop upon failure enable
                           )
        self.add_parameter('pf_operation',
                           set_cmd='PFOP {}',
                           vals=Enum('ON', 'OFF'),
                           get_cmd='PFOP?'  # pass/fail operation enable
                           )
        self.add_parameter('pf_source',
                           set_cmd='PFSC {}',
                           vals=Enum('C1', 'C2', 'C3', 'C4'),
                           get_cmd='PFSC?'  # pass/fail source select
                           )
        self.add_parameter('xmask', parameter_class=GroupParameter)
        self.add_parameter('ymask', parameter_class=GroupParameter)
        self.pf_set = Group([self.xmask, self.ymask],
                            set_cmd=f'PFST XMASK,{{xmask}},YMASK,{{ymask}}',
                            get_cmd='PFST?',
                            get_parser=lambda msg: {'xmask': msg.split(',')[1],
                                                    'ymask': msg.split(',')[3]})
        self.add_parameter('sparse_point', parameter_class=GroupParameter)
        self.add_parameter('number_of_point', parameter_class=GroupParameter)
        self.add_parameter('first_point', parameter_class=GroupParameter)
        self.waveform_setup = Group([self.sparse_point, self.number_of_point, self.first_point],
                                    set_cmd=f'WFSU SP,{{sparse_point}},NP,{{number_of_point}},FP,{{first_point}}',
                                    get_cmd='WAVEFORM_SETUP?',
                                    get_parser=lambda msg: {'sparse_point': msg.split(',')[1],
                                                            'number_of_point': msg.split(',')[3],
                                                            'first_point': msg.split(',')[5]})
        self.add_parameter('trigger_mode',
                           get_cmd='TRIG_MODE?',
                           set_cmd='TRIG_MODE {}',
                           vals=Enum('AUTO', 'NORM', 'SINGLE', 'STOP'),
                           get_parser=str
                           )
        self.add_parameter('trig_type', parameter_class=GroupParameter, vals=Enum('EDGE', 'SLEW', 'GLIT',
                                                                                  'INTV', 'RUNT', 'DROP'))
        self.add_parameter('trig_source', parameter_class=GroupParameter, vals=Enum('C1', 'C2', 'C3', 'C4',
                                                                                    'LINE', 'EX', 'EX5'))
        self.add_parameter('hold_type', parameter_class=GroupParameter, vals=Enum('OFF', 'TI'))  # off or time
        self.add_parameter('hold_value1', parameter_class=GroupParameter)
        self.trig_select = Group([self.trig_type, self.trig_source, self.hold_type, self.hold_value1],
                                 set_cmd=f'TRIG_SELECT {{trig_type}},SR,{{trig_source}},HT,{{hold_type}},HV,{{hold_value1}}',
                                 get_cmd='TRIG_SELECT?',
                                 get_parser=lambda msg: {'trig_type': msg.split(',')[0],
                                                         'trig_source': msg.split(',')[2],
                                                         'hold_type': msg.split(',')[4],
                                                         'hold_value1': 'ignore'})
        self.add_parameter('cymometer',
                           get_cmd='CYMT?',
                           get_parser=float)
        self.add_parameter('measure_gate_switch',
                           set_cmd='MEGS {}',
                           vals=Enum('ON', 'OFF'))
        self.add_parameter('measure_gatea',
                           set_cmd='MEGA {}')
        self.add_parameter('measure_gateb',
                           set_cmd='MEGB {}')

        self.add_parameter('time_div',
                           get_cmd='TIME_DIV?',
                           set_cmd='TIME_DIV {}',
                           vals=Enum('1NS', '2NS', '5NS', '10NS', '20NS', '50NS', '100NS', '200NS', '500NS',
                                     '1US', '2US', '5US', '10US', '20US', '50US', '100US', '200US', '500US',
                                     '1MS', '2MS', '5MS', '10MS', '20MS', '50MS', '100MS', '200MS', '500MS',
                                     '1S', '2S', '5S', '10S', '20S', '50S', '100S'))
        self.add_parameter('trig_delay',
                           get_cmd='TRIG_DELAY?',
                           set_cmd='TRIG_DELAY {}')
        self.add_parameter('hor_magnify',
                           get_cmd='HOR_MAGNIFY?',
                           set_cmd='HOR_MAGNIFY {}',
                           vals=Enum('1NS', '2NS', '5NS', '10NS', '20NS', '50NS', '100NS', '200NS', '500NS',
                                     '1US', '2US', '5US', '10US', '20US', '50US', '100US', '200US', '500US',
                                     '1MS', '2MS', '5MS', '10MS', '20MS', '50MS', '100MS', '200MS', '500MS',
                                     '1S', '2S', '5S', '10S', '20S', '50S', '100S'))
        self.add_parameter('hor_position',
                           get_cmd='HOR_POSITION?',
                           set_cmd='HOR_POSITION {}')
        self.add_parameter('edu_mode',
                           set_cmd='EMOD Cursors,{}',
                           vals=Enum('ON', 'OFF'),
                           get_cmd='EMOD?'  # education mode (locks of autosetup, measure and cursors)
                           )
        self.add_parameter('buzzer',
                           set_cmd='BUZZ {}',
                           vals=Enum('ON', 'OFF'),
                           get_cmd='BUZZ?'  # education mode (locks of autosetup, measure and cursors)
                           )
        channels = ChannelList(self,
                               "channels",
                               SiglentSds1102xChannel,
                               snapshotable=False
                               )

        for channel_number in range(1, 3):
            channel = SiglentSds1102xChannel(self, f"ch{channel_number}", channel_number)
            channels.append(channel)

        channels.lock()
        self.add_submodule('channels', channels)


if __name__ == '__main__':
    siglent = Sds1102x(address='192.168.153.191')
    siglent.reset('')
    sleep(5)
    siglent.comm_header('OFF')  # header and unit are omitted in response string.
    siglent.waveform_setup.set_parameters({'sparse_point': 1, 'number_of_point': 10, 'first_point': 100})
    siglent.trigger_mode('NORM')
    siglent.trig_select.set_parameters({'trig_type': 'EDGE', 'trig_source': 'C1', 'hold_type': 'TI', 'hold_value1': '1mS'})
    siglent.channels.ch1.trig_slope('POS')
    siglent.channels.ch1.trig_level('500mV')
    siglent.channels.ch1.trig_coupling('DC')
    siglent.channels.ch1.volt_vdiv('500mV')
    siglent.channels.ch1.offset('-1V')
    siglent.time_div('1US')
    siglent.trig_delay('-2uS')
    siglent.hor_magnify('100NS')
    siglent.hor_position('-2uS')
    siglent.measure_gatea('-0.7uS')
    siglent.measure_gateb('0.7uS')
    siglent.measure_gate_switch('ON')
    siglent.edu_mode('ON')
    siglent.buzzer('ON')
    print(f'The edu_mode readout value is::::: {siglent.edu_mode()}')
    # print(f'The cymometer readout value is::::: {siglent.cymometer()}')
    # siglent.channels.ch1.parameter_custom('MEAN')
    # print(f"The measurement mean readout value is::::: {siglent.channels.ch1.parameter_mean_value()}")
    #
    # # siglent.pf_enable('ON')
    # # siglent.pf_fail_stop('OFF')
    # # siglent.pf_display('ON')
    # # siglent.pf_source('C1')
    # # siglent.pf_set.set_parameters({'xmask': 0.5, 'ymask': 0.5})
    # # siglent.pf_createm()
    # # siglent.parameter_clr()
    # # siglent.pf_operation('ON')
    # # print(f'The pass/fail test result readout value is::::: {siglent.pf_datadis()}')
    # siglent.trigger_mode('SINGLE')
    # sleep(0.5)
    # print(f'The internal state register readout value is::::: {siglent.internal_state_register()}')
    # print(f'The internal state register readout value is::::: {siglent.internal_state_register()}')
    #
    # siglent.arm_acquisition('')
    # print(f'The internal state register readout value is::::: {siglent.internal_state_register()}')
    # print(f'The internal state register readout value is::::: {siglent.internal_state_register()}')
    #
    # siglent.arm_acquisition('')
    # print(f'The internal state register readout value is::::: {siglent.internal_state_register()}')
    # x = siglent.channels.ch1.trace()
    # print(x)
    # print(f'The internal state register readout value is::::: {siglent.internal_state_register()}')
    # x = siglent.channels.ch1.trace()
    # print(x)
    # siglent.trigger_mode('NORM')
