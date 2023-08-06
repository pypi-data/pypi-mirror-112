from traceback import format_exc
import datetime
from gravityRecorder import functions
from gravityRecorder.alerts import alert_funcs
from wsqluse.wsqluse import Wsqluse


class Recorder(Wsqluse):
    """ Класс, генерирующий факты взвешивания """
    def __init__(self, dbname, user, password, host, debug=False,
                 auto_table_name='auto',
                 records_table_name='records',
                 disputs_table_name='disputs'):
        Wsqluse.__init__(self, dbname, user, password, host, debug=debug)
        self.auto_table_name = auto_table_name
        self.records_table_name = records_table_name
        self.disputs_table_name = disputs_table_name

    def get_auto_protocol_info(self, auto_id):
        """ Вернуть информацию о протоколе авто по его id """
        protocol_name = functions.get_auto_protocol(self, auto_id)
        protocol_settings = functions.get_auto_protocol_settings(self,
                                                                 protocol_name,
                                                                 auto_id)
        return protocol_settings

    def register_car(self, car_number):
        """ Проверить, есть ли в таблице auto машина с таким гос.номером,
        если нет - зарегистрировать """
        auto_id = functions.check_car_registered(self, car_number)
        if not auto_id:
            auto_id = functions.register_new_car(self, car_number)
        return auto_id

    def init_round(self, weight, car_number, carrier=None, operator=None,
                   trash_cat=None, trash_type=None, notes=None,
                   *args, **kwargs):
        """
        Обработать взвешивание
        :param trash_cat:
        :param car_number:
        :param carrier:
        :param operator:
        :param trash_type:
        :param notes:
        :param args:
        :param kwargs:
        :return:
        """
        # Извлечь auto_id (уже зареганного или зарегать, если не зареган)
        auto_id = self.register_car(car_number)
        response = self.fix_weight_general(weight, trash_cat, trash_type, notes, operator,
                                auto_id, carrier,
                                datetime=datetime.datetime.now())
        return response

    def get_rfid_by_carnum(self, carnum):
        """ Вернуть RFID-номер машины по его гос.номеру """
        command = "SELECT rfid FROM auto WHERE car_number='{}'".format(carnum)
        response = self.try_execute_get(command)
        return response

    def check_car_choose_mode(self, alerts, choose_mode, car_number, course):
        # Проверить, как была выбрана машина (вручную/автоматоически)
        rfid = self.get_rfid_by_carnum(car_number)[0][0]
        alerts = alert_funcs.check_car_choose_mode(rfid, alerts, choose_mode,
                                                   car_number, course)
        return alerts

    def get_rfid_by_id(self, auto_id):
        """ Вернуть RFID-номер машины по его ID """
        command = "SELECT rfid FROM auto WHERE id={}".format(auto_id)
        response = self.try_execute_get(command)
        return response

    def check_car(self, cargo, alerts):
        alerts = alert_funcs.cargo_null(cargo, alerts)
        return alerts

    def fast_car(self, carnum, alerts):
        # Проверить, не слишком ли быстро вернулась машина,
        # если да - дополнить алерт кодом из wsettings и вернуть
        print('\nИнициирована проверка на FastCar')
        timenow = datetime.datetime.now()
        command = "SELECT le.date from last_events le " \
                  "INNER JOIN auto a ON (le.car_id=a.id) " \
                  "where a.car_number='{}'".format(carnum)
        try:
            last_visit_date = self.try_execute_get(command)[0][0]
            alerts = alert_funcs.check_fast_car(last_visit_date, timenow,
                                                alerts)
        except:
            print('\tОшибка при проверке заезда')
            print(format_exc())
        return alerts

    def check_car_inside(self, carnum, tablename):
        '''Проверяет находится ли машина на территории предприятия'''
        # self.check_presence(carnum, tablename, column)
        response = self.try_execute_get(
            "select * from {} "
            "where car_number='{}' and time_out is null".format(tablename,
                                                                carnum))
        if len(response) > 0:
            return True

    def check_car_has_gross(self, auto_id):
        """
        :param auto_id:
        :return:
        Проверить взвешивала ли машина брутто
        """
        command = "select * from {} where auto='{}' and time_out is " \
                  "null".format(self.records_table_name, auto_id)
        response = self.try_execute_get(command)
        if len(response) > 0:
            return True


    def get_last_id(self, tablename):
        # Вернуть максимальный ID из таблицы tablename
        command = "select max(id) from {}".format(tablename)
        max_id = self.try_execute_get(command)
        return max_id

    def get_last_visit(self, tablename, ident, value):
        # Вернуть строку с последней записью из таблицы tablename,
        # где выполняется условие ident, сортируется по value
        command = 'SELECT * FROM {} where {} ORDER BY {} DESC LIMIT 1'.format(
            tablename, ident, value)
        record = self.try_execute_get(command)
        return record

    def add_alerts(self, alerts, rec_id):
        '''Добавляет строку в таблицу disputs, где указываются данные об инциденте'''
        self.show_print('\n###Добавляем новые алерты к записи###')
        self.show_print('\talerts -', alerts)
        if len(alerts) > 0:
            timenow = datetime.now()
            command = "insert into {} ".format(s.disputs_table)
            command += "(date, records_id, alerts) "
            command += "values ('{}', {}, '{}') ".format(timenow, rec_id, alerts)
            command += "on conflict (records_id) do update "
            command += "set alerts = disputs.alerts || '{}'".format(alerts)
            self.try_execute(command)

    def updLastEvents(self, carnum, carrier, trash_type, trash_cat, timenow):
        self.show_print('\nОбновление таблицы lastEvents')
        carId = "select id from auto where car_number='{}' LIMIT 1".format(carnum)
        comm = 'insert into {} '.format(s.last_events_table)
        comm += '(car_id, carrier, trash_type, trash_cat, date) '
        comm += "values (({}),{},{},{},'{}') ".format(carId, carrier, trash_type,
                                                      trash_cat, timenow)
        comm += 'on conflict (car_id) do update '
        comm += "set carrier={}, trash_cat={}, trash_type={}, date='{}'"
        comm = comm.format(carrier, trash_cat, trash_type, timenow)
        self.try_execute(comm)

    def upd_old_num(self, old_carnum, new_carnum):
        # Обновляет старый номер на новый
        command = "UPDATE {} SET car_number='{}' WHERE car_number='{}'"
        command = command.format('auto', new_carnum, old_carnum)
        self.try_execute(command)

    def check_access(self, rfid):
        ''' Проверяет, разрешается ли машине въезд '''
        command = "SELECT rfid FROM {} WHERE rfid='{}'".format(s.auto, rfid)
        response = self.try_execute_get(command)
        if len(response) > 0:
            return True

    def fix_weight_general(self, weight, trash_cat, trash_type, notes,
                           operator, auto_id, carrier=None,
                           datetime=datetime.datetime.now()):
        have_gross = self.check_car_has_gross(auto_id)
        if have_gross:
            response = self.fix_weight_tare(auto_id, weight, notes, datetime)
            response['weight_stage'] = 'tare'
        else:
            response = self.fix_weight_gross(auto_id, weight, carrier,
                                             trash_cat, trash_type, notes,
                                             operator, datetime)
            response['weight_stage'] = 'gross'
        return response

    def fix_weight_tare(self, auto_id, weight_tare, notes, datetime=datetime.datetime.now()):
        """ Зафиксировать вес ТАРА """
        gross = self.get_gross(auto_id, self.records_table_name)        # Извлечь вес БРУТТО
        cargo = functions.get_cargo(gross, weight_tare)                 # Вычислить вес НЕТТО
        # Сформировать команду на обновление записи по auto_id
        sql_command = "UPDATE {} SET tara={}, cargo={}, time_out='{}', " \
                      "notes =  notes || 'Выезд: {}| ' " \
                      "WHERE auto={} and time_out is null"
        sql_command = sql_command.format(self.records_table_name, weight_tare,
                                         cargo, datetime, notes, auto_id)
        response = self.try_execute(sql_command)                        # Выполнить команду
        return response

    def get_gross(self, auto_id, records_table_name: str):
        command = "SELECT brutto FROM {} " \
                  "WHERE auto={} and time_out is null"
        command = command.format(records_table_name, auto_id)
        gross = self.try_execute_get(command)
        return gross[0][0]

    def fix_weight_gross(self, auto_id, weight, carrier, trash_cat, trash_type,
                         notes, operator, timenow=datetime.datetime.now()):
        """ Создать новую запись с брутто """
        command = """ INSERT INTO records (auto, brutto, time_in, carrier, 
                    trash_cat, trash_type, notes, operator) 
                    values (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"""
        cursor, conn = self.get_cursor_conn()
        values = (auto_id, weight, timenow, carrier, trash_cat, trash_type,
                  'Въезд: {}| '.format(notes), operator)
        cursor.execute(command, values)
        response = cursor.fetchall()
        conn.commit()
        return {'status': 'success', 'info': response}

    def delete_record(self, record_id, table_name=None):
        """ Удалить запись с id=record_id"""
        if not table_name:
            table_name = self.records_table_name
        command = "DELETE FROM {} WHERE id={}".format(table_name, record_id)
        response = self.try_execute(command)
        return response
