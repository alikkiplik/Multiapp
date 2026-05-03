# Multiapp
With this utility, you can edit text, draw, watch videos, and listen to music. To watch videos, install ffmpeg. 
Windows
```
winget install Gyan.FFmpeg
```
MacOS
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install ffmpeg
```
Linux
```
#Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

#Fedora
sudo dnf install ffmpeg

#Arch / Manjaro
sudo pacman -S ffmpeg

#openSUSE
sudo zypper install ffmpeg
```
The programm uses pygame opencv-python Pillow python-docx. Install it before using, if it wasn't installed.
```
pip install pygame opencv-python Pillow python-docx
```
