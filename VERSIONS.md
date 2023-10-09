Version 0.5.0 - October 2, 2023
===============================

Xevious/Super Xevious for the MEGA65 version 0.5.0 is based on this version 1.0.0 of the MiSTer2MEGA65 framework.

Despite being labeled as a "beta" release, the game is entirely playable with no major issues however, users will encounter a lower framerate in rotate mode. It's important to note that this is not due to any limitations in the Mega65's hardware, but rather a constraint in the M2M framework. Presently, screen rotation is only supported at 50hz, whereas Xevious's video hardware runs at 60hz. For the best experience, it is recommended not ( despite this being the default ) to rotate the display via the OSD (On-Screen Display) but rather to physically rotate your monitor instead. This limitation will be fixed in the future.

## Features
* Screen rotation of 90° is available, although not recommended (please see above for more information)
* Supports various HDMI modes
* Compatible with VGA (standard) and Retro 15Khz modes, with separate HS/VS or CSYNC
* Supports Atari and Namco versions.
* Joystick ports can be flipped via the OSD
* Ability to save OSD/Menu settings
* Fully configurable DIP switches
* Holding down the fire button triggers bombs ( Delay time is configurable up to 1/2 a second )

## Constraints 
* Core does not support dynamic ROM loading yet
* Screen can't be flipped horizontally in rotate mode
* No Vsync/Hsync adjustment
* Aspect ratio is currently fixed
* No autosave of highscores is supported


## Bugs
* Keyboard controls are temporarily disabled until the next version, this is to prevent players from pressing the up and down keys simulatenously which causes the Salvalou to dart across the screen.
* Game may get into a reset loop during power up reset cycle, it's unknown as to what causes this.
* Ship may randomly fly off to the left of the screen on game start, this is reproduced in MAME also.
* Pressing the service mode button in the gameplay mode crashes the game.