from os import path, listdir

log_types = ['conn.log', 'dce_rpc.log', 'dhcp.log', 'dnp3.log', 'dns.log', 'ftp.log', 'http.log', 'irc.log',
             'modbus.log', 'modbus_register_change.log', 'mysql.log', 'ntlm.log', 'ntp.log', 'radius.log', 'rdp.log',
             'rfb.log', 'sip.log', 'smb_cmd.log', 'smb_files.log', 'smb_mapping.log', 'smtp.log', 'snmp.log',
             'socks.log', 'ssh.log', 'ssl.log', 'syslog.log', 'tunnel.log']


def get_log_types(dir_path):
    """
    Returns types of log files present in directory.
    :param dir_path: String containing path of log directory
    :return: List of strings indicating log types present
    """
    if path.exists(dir_path):
        files = listdir(dir_path)
        logs_present = []
        for file in files:
            if file in log_types:
                logs_present.append(file)
        return logs_present
    else:
        return False


def get_log_start_time(dir_path):
    if path.exists(dir_path):
        files = listdir(dir_path)
        logs_present = get_log_types(dir_path)
        earliest_timestamp = None
        for log_file in files:
            try:
                with open(f'{dir_path}{log_file}', 'r') as file:
                    first_line_fields = file.readline().split()
                    start_time = first_line_fields[0]
                    if not earliest_timestamp:
                        earliest_timestamp = start_time
                    else:
                        if start_time < earliest_timestamp:
                            earliest_timestamp = start_time
            except:
                return None
        print(f'Earlist time: {earliest_timestamp}')
    else:
        return False
    return earliest_timestamp


def get_log_end_time(dir_path):
    if path.exists(dir_path):
        files = listdir(dir_path)
        logs_present = get_log_types(dir_path)
        latest_timestamp = None
        for log_file in files:
            try:
                with open(f'{dir_path}{log_file}', 'r') as file:
                    last_line_fields = file.readlines()[-1].split()
                    end_time = last_line_fields[0]
                    print(end_time)
                    if not latest_timestamp:
                        latest_timestamp = end_time
                    else:
                        if end_time < latest_timestamp:
                            latest_timestamp = end_time
            except:
                return None
        print(f'Latest time: {latest_timestamp}')
    else:
        return False
    return latest_timestamp


if __name__ == '__main__':
    get_log_end_time('../data/zeek/')

