from portdatasplitter.main import PortDataSplitter
from weightsplitter import support_functions as sup_func
from traceback import format_exc
import weightsplitter.settings as s


class WeightSplitter(PortDataSplitter):
    def __init__(self, ip, port, port_names_list=['/dev/ttyUSB0',], terminal_name='CAS', debug=False, test_mode=False,
                 *args, **kwargs):
        super().__init__(ip, port, port_names_list, device_name=terminal_name, debug=debug, test_mode=test_mode,
                         *args, **kwargs)
        self.terminal_name = terminal_name
        if test_mode:
            self.terminal_name = 'None'
        self.terminal_funcs = sup_func.extract_terminal_func(self.terminal_name)

    def make_data_aliquot(self, data, value=10):
        # Сделать вес кратным value
        try:
           data = int(data)
           data = data - (data % value)
        except:
            self.show_print(format_exc())
        return data

    def check_data(self, data):
        # Проверить данные, вызывал функцию этого терминала
        if self.terminal_funcs.check_scale_disconnected(data):
            data = s.scale_disconnected_code
        else:
            data = self.terminal_funcs.get_parsed_input_data(data)
        return data

    def send_data(self, data, **kwargs):
        # Отправить данные
        if data is not None:
            try:
                #data = bytes(data, encoding='utf-8')
                self.show_print('Sending:', data, debug=True)
                super().send_data(data, **kwargs)
            except TypeError:
                self.show_print("Reconnecting...", debug=True)
                self.reconnect_logic()
