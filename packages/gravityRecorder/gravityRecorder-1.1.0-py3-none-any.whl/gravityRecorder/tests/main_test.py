import unittest
from gravityRecorder.main import Recorder
import datetime
import uuid


class MainTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recorder = Recorder('wdb', 'watchman', 'hect0r1337', '192.168.100.118')

    def test_fix_weight_general(self):
        carrier = 1
        weight = 10000
        auto_id = 1022
        operator = 5
        trash_cat = 1
        trash_type = 1
        notes = "SOME NOTES"
        timenow = datetime.datetime.now()
        if self.recorder.check_car_has_gross(auto_id):
            # Если авто взвешивала брутто, функция должна взвесить тару, и check_car_has_gross после этого вернет False
            response = self.recorder.fix_weight_general(weight, trash_cat, trash_type, notes, operator, auto_id, carrier,
                                                        timenow)
            self.assertTrue(response['weight_stage'] == 'tare')
            self.assertTrue(self.recorder.check_car_has_gross(auto_id) is not True)
            # Проверить на правильность заполнения полей
            command = "SELECT * FROM records WHERE id={}".format(response['info'][0][0])
            response = self.recorder.get_table_dict(command)
            result = response['info'][0]
            self.assertTrue(result['brutto'] == weight)
            self.assertTrue(result['tara'] == weight)
            self.assertTrue(result['cargo'] == 0)
            self.assertTrue(result['carrier'] == carrier)
            self.assertTrue(result['trash_type'] == trash_type)
            self.assertTrue(result['trash_cat'] == trash_cat)
            self.assertTrue(result['operator'] == operator)
            self.assertTrue(result['auto'] == auto_id)
        else:
            # Если же брутто нет, то функция должна всесить брутто, и check_car_has_gross после этого вернет True
            response = self.recorder.fix_weight_general(weight, trash_cat, trash_type, notes, operator, auto_id, carrier,
                                                        timenow)
            self.assertTrue(response['weight_stage'] == 'gross')
            self.assertTrue(self.recorder.check_car_has_gross(auto_id) is True)
            # Проверить на правильность заполнения полей
            command = "SELECT * FROM records WHERE auto={} and time_out is null".format(auto_id)
            response = self.recorder.get_table_dict(command)
            result = response['info'][0]
            self.assertTrue(result['brutto'] == weight)
            self.assertTrue(result['tara'] == None)
            self.assertTrue(result['cargo'] == None)
            self.assertTrue(result['time_out'] == None)
            self.assertTrue(result['carrier'] == carrier)
            self.assertTrue(result['trash_type'] == trash_type)
            self.assertTrue(result['trash_cat'] == trash_cat)
            self.assertTrue(result['operator'] == operator)
            self.assertTrue(result['auto'] == auto_id)
        self.recorder.delete_record(result['id'])

    def test_get_protocol_settings(self):
        auto_id = 1022
        response = self.recorder.get_auto_protocol_info(auto_id)
        response_must = {'name': 'rfid', 'first_open_gate': 'near',
                         'second_open_gate': 'far', 'weighting': True,
                         'auto_id': auto_id}
        self.assertTrue(response == response_must)

    def test_register_car(self):
        car_number_uuid = uuid.uuid1()
        car_number_str = str(car_number_uuid)[0:10]
        auto_id_after_register = self.recorder.register_car(car_number_str)
        auto_id_without_register = self.recorder.register_car(car_number_str)
        self.assertTrue(auto_id_without_register == auto_id_after_register)
        self.recorder.delete_record(record_id=auto_id_without_register, table_name='auto')

    def test_init_round(self):
        response = self.recorder.init_round(5000, 'В060ХА702', operator=5)
        print("RECORD INIT RESULT:", response)
        self.recorder.delete_record(record_id=response['info'][0][0],
                                    table_name='records')

if __name__ == '__main__':
    unittest.main()
