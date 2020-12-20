# Hack-Manager
A ups patch manager for the FEGBA hacking community.

## How to Download:

### Windows Users:
Download HackManager.exe

### Mac Users:
Download HackManager.dmg


## How to Use:
Put HackManager.exe or HackManager.app in a folder. Put your base roms in the same folder, name them **FE6_clean.gba**, **FE7_clean.gba**, **FE8_clean.gba**. Opening the program will create two folders: **patch** and **rom**. Put you patches in the **patch** folder, and click the **Apply Patches** button, the application will automatically find the correct patch and put the patched roms in the **rom** folder.


## How to Use with Command Line:
```python3 hack_manager.py```


## Other Features
This program will perform checksums on your roms and update your roms if the checksum doesn't match. If the patches are named with version numbers, currently only supports . and - seprarted numbers, (i.e. 1.3, 2-46-232). The program will try to inherit a save file from a previous version.
