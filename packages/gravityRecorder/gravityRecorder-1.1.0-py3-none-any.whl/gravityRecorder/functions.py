def get_weighting_stage(sqlshell, car_number: str):
    sqlshell


def get_cargo(gross, tare):
    """ Получает cargo (cargo), как разницу между gross и tare """
    cargo = int(gross) - int(tare)
    return cargo


def get_auto_protocol_settings(sql_shell, auto_protocol, auto_id,
                               *args, **kwargs):
    command = "SELECT p.name, ps.first_open_gate, ps.second_open_gate, ps.weighting " \
              "FROM round_protocols p INNER JOIN round_protocols_settings ps ON (p.id = ps.protocol) " \
              "WHERE p.name = '{}'".format(auto_protocol)
    response = sql_shell.get_table_dict(command)
    if response['status'] == 'success':
        response['info'][0]['auto_id'] = auto_id
        return response['info'][0]


def get_auto_protocol(sql_shell, auto_id):
    """ Возвращает протокол авто по его ID"""
    command = "SELECT id_type FROM auto WHERE id={}".format(auto_id)
    response = sql_shell.try_execute_get(command)
    return response[0][0]


def check_car_registered(sqlshell, car_number):
    """ Проверить регистрирована ли машина в таблице auto """
    command = "select id from auto where car_number='{}'".format(car_number)
    response = sqlshell.try_execute_get(command)
    response = response
    if response:
        # Если транзакция удалась
        return response[0][0]


def register_new_car(sqlshell, car_number):
    """ Зарегистрировать новую машину"""
    command = "insert into auto (car_number, id_type) values ('{}', 'tails')".format(car_number)
    response = sqlshell.try_execute(command)
    if response['status'] == 'success':
        return response['info'][0][0]
