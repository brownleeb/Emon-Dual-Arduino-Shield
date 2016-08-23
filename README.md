# Emon-Dual-Arduino-Shield
Open Energy Monitor to monitor each leg of US residential power, send results via USB to Raspberry Pi

This project is for monitoring residential power usage when data from the meter is not available via pulse sensing or RF.  Since I have metered usage with different rates based on demand times, I want to be able to see accurate usage info by hour so avoid usage during peak times.
I was not able to get the accuracy I wanted with a single EmonTX Arduino Shield.  Even though it uses a voltage sensor for 'real power', I felt the two mains were different enough that I would try adding a second Shield with voltage monitor.
Each EmonTX sends several values back to a Raspberry Pi vi USB for post-processing.  I am actually running 3 Arduinos (1 Leonardo, 2 Unos) off of the USB on a RPi-2 (without powered hub) without any problems (so far).
Each EmonTX was calibrated separately.  The RPi is running Arch Linux, so all Arduinos are referenced by USB ID to preserve configuration across reboots.
This sketch samples as many times as possible in a 30 second period and returns average values for Real Power Watts, Apparent Power Watts, Power Factor, RMS Voltage and RMS Current along with the number of samples in the period.  
This is not to be confused with running in Continuous Mode (CM).  My method needs tuning for most accuracy, but I am working on that.

Arduino sketch is slightly modified from https://github.com/openenergymonitor/emonTxFirmware/tree/master/emonTxShield
EmonTX Shield and Voltage Sensor purchased from Open Energy Monitor (https://shop.openenergymonitor.com/)
