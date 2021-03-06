# SynClock-Display-Raspberry-Pi
Display for the next alarm clock in my phone.

This code displays the time of my next alarm in my [Synchronized Alarm Clock](https://github.com/OrBin/SynClock), if it is in the next 24 hours.
This module only fetches the next alarm time from a [server](https://github.com/OrBin/SynClock-Server).


Requirements:

1. The URL to get the time from should be saved in a file named ```.raspi_clock_display_config``` in the main directory of the repository, for example: ```https://example.com/get_next_alarm.php ```.

2. The server has to return the time as two numbers in UNIX-time format (seconds since Jan 1, 1970 00:00:00 GMT). The first is the next alarm time and the second it the time when the next alarm time was last updated.


This module should be run as root:
```
sudo python main.py &
```
