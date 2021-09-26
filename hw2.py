import csv


def create_hierarchy(records: list) -> dict:
    """Creates a hierarchy in the following form: {department: [units]}"""
    scheme = {}
    for record in records:
        if scheme.get(record['Департамент']) is None:
            scheme[record['Департамент']] = [record['Отдел']]
        elif record['Отдел'] not in scheme[record['Департамент']]:
            scheme[record['Департамент']].append(record['Отдел'])
    return scheme


def show_hierarchy():
    """Prints hierarchy"""
    scheme = create_hierarchy(corps)
    for dep, unit in scheme.items():
        nice_unit_format = ', '.join(unit)
        print(f'Департамент {dep} содержит следующие отделы: {nice_unit_format}')


def create_report(records: list) -> dict:
    """Creates a report in the following form:
    {department: [number of employees, min_salary, max_salary, avg salary]}"""
    report = {}
    temp_salaries = {}
    for record in records:
        if report.get(record['Департамент']) is None:
            report[record['Департамент']] = [1, int(record['Оклад']), int(record['Оклад'])]
            temp_salaries[record['Департамент']] = [int(record['Оклад'])]
        else:
            temp_salaries[record['Департамент']].append(int(record['Оклад']))
            report[record['Департамент']][0] += 1
            if report[record['Департамент']][1] > int(record['Оклад']):
                report[record['Департамент']][1] = int(record['Оклад'])
            elif report[record['Департамент']][2] < int(record['Оклад']):
                report[record['Департамент']][2] = int(record['Оклад'])
    for dep, salary in temp_salaries.items():
        report[dep].append(round((sum(temp_salaries[dep]))/len(temp_salaries[dep]), 2))
    return report


def report_helper() -> list:
    """Formats the report for recording"""
    report_for_csv = []
    report = create_report(corps)
    for dep in report.keys():
        report_for_csv.append({'Департамент': dep,
                               'Число работников': report[dep][0],
                               'Минимальная зп': report[dep][1],
                               'Максимальная зп': report[dep][2],
                               'Средняя зп': report[dep][3]})
    return report_for_csv


def print_report():
    """Prints a report"""
    report = create_report(corps)
    for dep, info in report.items():
        print(f'В департаменте {dep} работают {info[0]} человек, вилка зарплат: {info[1]} - {info[2]}, '
              f'а средняя зарплата равна {info[3]}.')


def write_report():
    """Writes a report in a file 'department report.csv'"""
    writing_report = report_helper()
    with open('department report.csv', 'w') as writing_file:
        fieldnames = ['Департамент', 'Число работников', 'Минимальная зп',
                      'Максимальная зп', 'Средняя зп']
        writer = csv.DictWriter(writing_file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(writing_report)


def interface():
    """Interface for interaction"""
    print('Привет, введи 1, чтобы получить иерархию отделов \n'
          'Введи 2, чтобы получить отчет по департаментам \n'
          'Введи 3, чтобы записать отчет по департаментам \n'
          'Введи 4, чтобы выйти')
    option = input()
    while option != '4':
        if option == '1':
            print('Иерархия отделов:')
            show_hierarchy()
            print('Продолжим работу?')
            option = input()
        elif option == '2':
            print('Отчет по отделам:')
            print_report()
            print('Продолжим работу?')
            option = input()
        elif option == '3':
            write_report()
            print('Отчет записан в файл department report.csv, продолжим работу?')
            option = input()
        else:
            print('Недопустимое значение, введите 1, 2, 3 или 4')
            option = input()
    print('Пока')


if __name__ == '__main__':
    corps = []
    with open('Corp Summary.csv') as File:
        reader = csv.DictReader(File, delimiter=';')
        for row in reader:
            corps.append(row)
    interface()
