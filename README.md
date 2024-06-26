# Endless-Chaos

### No longer under maintenance, thank you for the support throughout the year, good luck have fun.

A Lost Ark chaos dungeon(PvE) farming bot.\
Based on the repo by any-other-guy and the fork by kotooh. \
Fully automatic mob/elite/boss detecting and clearing, based on image recognition.\
Recommended to use with GeForce Now. 

What it does:
* Infinite Chaos Dungeon clears for any selected character
* Daily x2 Chaos Dungeon FULL runs. Able to rotate through UP to 15 characters, then switch back to your main character for more infinite run cycles.
* Daily Lopang unas on selected characters
* Daily leapstone unas (Bleak Night Fog, Mokomoko Night Market, Hestera Garden, Sage Tower) on selected characters
* Daily Guild Donations/Support on selected characters
* Weekly sailing guild quests on selected characters (currently only level 3 supported)
* Daily Rapport Tasks on selected/all characters
* Auto game restart on EAC offline or crash for Steam players
* Auto restart on session timeout/connection lost for GeForce Now players


## Getting started (Please read)

### 0. Prerequisites:
- Install/Open a Command Line/Terminal app in your operating system.
- Install Python3 (if you dont have)
- Install pip (if you dont have) from your terminal:
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
python3 -m pip install --upgrade pip
```

### 1. Please change game settings to EXACTLY these numbers:

desktop resolution: 1920x1080\
In-game Video settings:
- Resolution: 1920x1080
- Screen: Borderless
- Force 21:9 Aspect Ratio checked

In-game Gameplay -> Controls and Display -> HUD size: 110%\
minimap transparency (at top right corner): 100%\
minimap zoom-in (at top right corner): 65%\
\
Please change game settings to EXACTLY these ^^ numbers

### 2a. Configure roster settings.
IMPORTANT: \
use the characters_template.py to set up a characters.py with your roster details. \
Examples are given in the template.

### 2b. Configure character ability settings.
IMPORTANT: \
please carefully setup paramters in ./config.py and ./abilities.py
refering to the comments for now.\
lots of things can be customized for your best experience.

### 3. Start running script:

```
git clone https://github.com/zachjhuang/chaos-script.git
cd chaos-script
pip install -r requirements.txt
python3 .\bot.py --chaos --endless --unas --guild --sailing
```

\
Open a Github Issue if you need any assistance or have any feedback, appreciated!

## DISCLAIMER (VERY IMPORTANT): 
This script was created solely for fulfilling my personal learning purposes. I do not commercialize it in any way. If anything is against ToS, I would take it down from the public domain.
By running the script, you agree to accept any consequence at your own risk!
