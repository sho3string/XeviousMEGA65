Xevious for MEGA65
==================

Xevious (1982):

Xevious is considered one of the pioneering titles in the vertical-scrolling shooter genre. The game features a unique blend of both air and ground combat, distinguishing it from many other shooters of its time. Players control the Solvalou, a futuristic aircraft, and must navigate through hostile airspace, destroying both aerial and ground-based enemies.

Key features and elements of Xevious include:

Dual Attack: The Solvalou can fire both a forward-firing blaster for air targets and bombs for ground targets, allowing players to engage enemies from multiple directions.

Varied Enemy Types: The game features a wide range of enemy aircraft, ground-based installations, and bosses, each with its own attack patterns and behaviors.

Terrain Interaction: Players must pay attention to both the aerial and ground elements of the game, as enemy installations on the ground can pose threats, and the landscape can be used for cover.

Super Xevious (1984):

Super Xevious is an enhanced version of the original Xevious, featuring improved gameplay elements. It retains the core gameplay of its predecessor but adds new features and challenges.
Power-Ups: Power-ups can be collected to enhance the Solvalou's capabilities and firepower.

Both games are known for their engaging and fast-paced gameplay, as well as their contribution to the shoot 'em up genre. Porting these classics to an FPGA platform would provide nostalgic gaming experiences for enthusiasts and preserve the legacy of these iconic titles.

This core is based on the
[MiSTer](https://github.com/MiSTer-devel/Arcade-Xevious_MiSTer)
Xevious core which
itself is based on the work of [many others](AUTHORS).

[Muse aka sho3string](https://github.com/sho3string)
ported the core to the MEGA65 in 2023.

The core uses the [MiSTer2MEGA65](https://github.com/sy2002/MiSTer2MEGA65)
framework and [QNICE-FPGA](https://github.com/sy2002/QNICE-FPGA) for
FAT32 support (loading ROMs, mounting disks) and for the
on-screen-menu.

How to install the Xevious core on your MEGA65
----------------------------------------------

1.Download ROM: Download the Xevious MAME ROM ZIP file (do not unzip!) from the internet. Search for xevious.zip or sxeviousj.zip for Super Xevious.

2.Download the Python script: Download the provided Python script that prepares the ROMs such that the Xevious core is able to use it from https://github.com/sho3string/XeviousMEGA65/blob/master/xevious_rom_installer.py

3.Run the Python script: Execute the Python script to create a folder with the ROMs. Use the command python xevious_rom_installer.py <path to the zip file> <output_folder>.

4.ROM files within the zip arhive are automatically evaluated for the correct SHA1 checksums.

Copy the ROMs to your MEGA65 SD card: Copy the generated folder with the ROMs to your MEGA65 SD card. You can use either the bottom SD card tray of the MEGA65 or the tray at the backside of the computer (the latter has precedence over the first). The ROMs need to be in the folder arcade/xevious.  

The script will also generate the xevcfg file and supports the following versions of Xevious.  

xevious    - Xevious (Namco)  
xeviousa   - Xevious (Atari, harder)  
xeviousc   - Xevious (Atari, Namco PCB)  
sxeviousj  - Super Xevious (Japan)  

IMPORTANT! Super Xevious has an inverted freeze dip, which means you will need to enable/select it in the Namco dip switch configuration or the game will freeze at the crosshatch.  
5. Check the MAME driver for setting dip switch positions or search for 'xevious dip switch settings'.  You really won't need to do this if you accept the defaults after a fresh install.  
6. **Download and run the Xevious core**: Follow the instructions on [this site](https://sy2002.github.io/m65cores/) to download and run the Xevious core on your MEGA65.  
7. **Common problems [WIP]**  


    
