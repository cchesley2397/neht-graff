import os


def slice_logs(start, end, log_dir):
    """
    Given a directory containing zeek log files and a start and end time,
    create a new directory named after the time constrains and generate corresponding log files excluding entries
    outside of the specified times.
    :param start: Float containing start time as epoch
    :param end: Float containing end time as epoch
    :param log_dir: Directory containing zeek log files
    :return:
    """
    log_file_list = os.listdir(log_dir)
    slice_dir = f'{str(start)}-{str(end)}'
    try:
        os.mkdir(f'{log_dir}/{slice_dir}')
        for log_name in log_file_list:
            print(f'Slicing {log_name}')
            with open(f'./{log_dir}/{slice_dir}/{log_name}', 'w', encoding='utf-8') as slice_file:
                with open(f'{log_dir}/{log_name}', 'r', encoding='utf-8') as zeek_file:
                    lines = zeek_file.read().split('\n')
                    for line in lines:
                        time = line.split('\t')[0]
                        if time:
                            epoch_timestamp = float(time)
                            if epoch_timestamp >= end:
                                break
                            elif epoch_timestamp >= start:
                                slice_file.writelines(f'{line}\n')
    except FileExistsError as err:
        print('Directory already exists for these time constraints')


if __name__ == '__main__':
    slice_logs(1331922852.390000, 1331999738.860000, './data/zeek')