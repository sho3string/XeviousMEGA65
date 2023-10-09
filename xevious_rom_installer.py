#!/usr/bin/env python3
import os
import sys
import zipfile
import tempfile
import shutil
import hashlib


# Xevious Atari Namco PCB

    
ANAMCO_FILES = [
    "xvi_u_.3p", "xv_2-2.3m", "xv_2-3.2m", "xvi_u_.2l",     #cpu1 - 16kb
    "xv2_5.3f","xvi_6.3j",                                  #sub1 - 8kb
    "xvi_7.2c",                                             #sub2 - 4kb
    "xvi_12.3b",                                            #fgc  - 4kb
    "xvi_13.3c","xvi_14.3d",                                #bgc  - 8kb
    "xvi_15.4m","xvi_17.4p","xvi_16.4n", "xvi_18.4r",       #spr  - 28kb
    "xvi_9.2a","xvi_10.2b","xvi_11.2c",                     #bgtm - 4kb
    "50xx.bin","51xx.bin","54xx.bin"                        #mcu  - 4kb
    ]
    

ANAMCO_CHK = {
    # cpu
    "xvi_u_.3p": "3bafaa42bccddfaf8d9197e93416a731b7f8fb94",
    "xv_2-2.3m": "23cdf1f2c2642f9bc3f843b5c338372027032380",
    "xv_2-3.2m": "eb42393720fc1fd4a1f6cdba87ac4177fd5827fe",
    "xvi_u_.2l": "ff3a96d6f7357fb2d33cd9d77d53477b9071ffc9",
    "xv2_5.3f": "9b02c00cff6c771d46776416295f9e12a2166cc5", 
    "xvi_6.3j": "6b79efee1a9642edb9f752101737132401248aed",
    "xvi_7.2c": "f8d1f8e019d8198308443c2e7e815d0d04b23d14",
    # foreground characters
    "xvi_12.3b": "9c3b61dfca2f84673a78f7f66e363777a8f47a59",
    # background characters
    "xvi_13.3c": "32bc09be5ff8b52ee3a26e0ac3ebc2d4107badb7",
    "xvi_14.3d": "fb9ffe5fc43e0213231267e98d605d43c15f61e8",
    # sprites
    "xvi_15.4m": "19ddbd9805f77f38c9a9a1bb30dba6c720b8609f",
    "xvi_17.4p": "acff2bf5cde85a16cdc98a52cdea11f77fadf25a",
    "xvi_16.4n": "3bf380ef76c03822a042ecc73b5edd4543c268ce",
    "xvi_18.4r": "b5f830dd2cf25cf154308d2e640f0ecdcda5d8cd",
    # background tilemaps
    "xvi_9.2a": "3106d1aacff06cf78371bd19967141072b32b7d7",
    "xvi_10.2b": "49064b25667ffcd81137cd5e800df4b78b182a46",
    "xvi_11.2c": "3f7eac12863697a98e1122111801606759e44b2a",
    # mcus
    "50xx.bin": "f03c79451e73b3a93c1591cdb27fedc9f130508d",
    "51xx.bin": "50de79e0d6a76bda95ffb02fcce369a79e6abfec",
    "54xx.bin": "01bdf984a49e8d0cc8761b2cc162fd6434d5afbe",
}

# Xevious Namco version 

NAMCO_FILES = [
    "xvi_1.3p", "xvi_2.3m", "xvi_3.2m", "xvi_4.2l",         #cpu1 - 16kb
    "xvi_5.3f","xvi_6.3j",                                  #sub1 - 8kb
    "xvi_7.2c",                                             #sub2 - 4kb
    "xvi_12.3b",                                            #fgc  - 4kb
    "xvi_13.3c","xvi_14.3d",                                #bgc  - 8kb
    "xvi_15.4m","xvi_17.4p","xvi_16.4n", "xvi_18.4r",       #spr  - 28kb
    "xvi_9.2a","xvi_10.2b","xvi_11.2c",                     #bgtm - 4kb
    "50xx.bin","51xx.bin","54xx.bin"                        #mcu  - 4kb
    ]

NAMCO_CHK = {
    # cpu
    "xvi_1.3p": "4882b25b0938a903f3a367455ba788a30759b5b0", 
    "xvi_2.3m": "8adc60a5fcbca74092518dbc570ffff0f04c5b17",
    "xvi_3.2m": "c6a154858716e1f073b476824b183de20e06d093",
    "xvi_4.2l": "4b846de204d08651253d3a141677c8a31626af07",
    "xvi_5.3f": "15f1c005b9d806a384ab1f2240b9c580bfe83893",
    "xvi_6.3j": "6b79efee1a9642edb9f752101737132401248aed",
    "xvi_7.2c": "f8d1f8e019d8198308443c2e7e815d0d04b23d14",
    # foreground characters
    "xvi_12.3b": "9c3b61dfca2f84673a78f7f66e363777a8f47a59",
    # background characters
    "xvi_13.3c": "32bc09be5ff8b52ee3a26e0ac3ebc2d4107badb7",
    "xvi_14.3d": "fb9ffe5fc43e0213231267e98d605d43c15f61e8",
    # sprites
    "xvi_15.4m": "19ddbd9805f77f38c9a9a1bb30dba6c720b8609f",
    "xvi_17.4p": "acff2bf5cde85a16cdc98a52cdea11f77fadf25a",
    "xvi_16.4n": "3bf380ef76c03822a042ecc73b5edd4543c268ce",
    "xvi_18.4r": "b5f830dd2cf25cf154308d2e640f0ecdcda5d8cd",
    # background tilemaps
    "xvi_9.2a": "3106d1aacff06cf78371bd19967141072b32b7d7",
    "xvi_10.2b": "49064b25667ffcd81137cd5e800df4b78b182a46",
    "xvi_11.2c": "3f7eac12863697a98e1122111801606759e44b2a",
    # mcus
    "50xx.bin": "f03c79451e73b3a93c1591cdb27fedc9f130508d",
    "51xx.bin": "50de79e0d6a76bda95ffb02fcce369a79e6abfec",
    "54xx.bin": "01bdf984a49e8d0cc8761b2cc162fd6434d5afbe",
}

# Super Xevious JAPAN

SUPERX_FILES = [
    "xv3_1.3p", "xv3_2.3m", "xv3_3.2m", "xv3_4.2l",         #cpu1 - 16kb
    "xv3_5.3f","xv3_6.3j",                                  #sub1 - 8kb
    "xvi_7.2c",                                             #sub2 - 4kb
    "xvi_12.3b",                                            #fgc  - 4kb
    "xvi_13.3c","xvi_14.3d",                                #bgc  - 8kb
    "xvi_15.4m","xvi_17.4p","xvi_16.4n", "xvi_18.4r",       #spr  - 28kb
    "xvi_9.2a","xvi_10.2b","xvi_11.2c",                     #bgtm - 4kb
    "50xx.bin","51xx.bin","54xx.bin"                        #mcu  - 4kb
    ]

SUPERX_CHK = {
    # cpu
    "xv3_1.3p": "9001856aad0f31b40443f21b7a895e4101684307", 
    "xv3_2.3m": "2fb4034d9d757376df59378df539bf41d99ed43e",
    "xv3_3.2m": "ecc39fb2c0065a36f20541747089b4e30dfb99b1",
    "xv3_4.2l": "0ca726f7f9528789f2a718df55e59406a283cdfa",
    "xv3_5.3f": "5831bb306bd650779207936bfd00f25864733abb",
    "xv3_6.3j": "5a020822387ab8c69214db961180760fa9853e6e",
    "xvi_7.2c": "f8d1f8e019d8198308443c2e7e815d0d04b23d14",
    # foreground characters
    "xvi_12.3b": "9c3b61dfca2f84673a78f7f66e363777a8f47a59",
    # background characters
    "xvi_13.3c": "32bc09be5ff8b52ee3a26e0ac3ebc2d4107badb7",
    "xvi_14.3d": "fb9ffe5fc43e0213231267e98d605d43c15f61e8",
    # sprites
    "xvi_15.4m": "19ddbd9805f77f38c9a9a1bb30dba6c720b8609f",
    "xvi_17.4p": "acff2bf5cde85a16cdc98a52cdea11f77fadf25a",
    "xvi_16.4n": "3bf380ef76c03822a042ecc73b5edd4543c268ce",
    "xvi_18.4r": "b5f830dd2cf25cf154308d2e640f0ecdcda5d8cd",
    # background tilemaps
    "xvi_9.2a": "3106d1aacff06cf78371bd19967141072b32b7d7",
    "xvi_10.2b": "49064b25667ffcd81137cd5e800df4b78b182a46",
    "xvi_11.2c": "3f7eac12863697a98e1122111801606759e44b2a",
    # mcus
    "50xx.bin": "f03c79451e73b3a93c1591cdb27fedc9f130508d",
    "51xx.bin": "50de79e0d6a76bda95ffb02fcce369a79e6abfec",
    "54xx.bin": "01bdf984a49e8d0cc8761b2cc162fd6434d5afbe",
}


# Xevious Atari Harder PCB

ATARI2_FILES = [
    "xea-1m-a.bin", "xea-1l-a.bin",                         #cpu1 - 16kb
    "xea-4c-a.bin",                                         #sub1 - 8kb
    "xvi_7.2c",                                             #sub2 - 4kb
    "xvi_12.3b",                                            #fgc  - 4kb
    "xvi_13.3c","xvi_14.3d",                                #bgc  - 8kb
    "xvi_15.4m","xvi_17.4p","xvi_16.4n", "xvi_18.4r",       #spr  - 28kb
    "xvi_9.2a","xvi_10.2b","xvi_11.2c",                     #bgtm - 4kb
    "50xx.bin","51xx.bin","54xx.bin"                        #mcu  - 4kb
]

ATARI2_CHK = {
    # cpu
    "xea-1m-a.bin": "f770873b711d838556dde67a8aac8a7f572fcc5b", 
    "xea-1l-a.bin": "c6c322c61d0985a2ac59f5e92d4e351107afb9eb",
    "xea-4c-a.bin": "e8114141394adda86184b146f2497cfeef7fc2eb",
    "xvi_7.2c": "f8d1f8e019d8198308443c2e7e815d0d04b23d14",
    # foreground characters
    "xvi_12.3b": "9c3b61dfca2f84673a78f7f66e363777a8f47a59",
    # background characters
    "xvi_13.3c": "32bc09be5ff8b52ee3a26e0ac3ebc2d4107badb7",
    "xvi_14.3d": "fb9ffe5fc43e0213231267e98d605d43c15f61e8",
    # sprites
    "xvi_15.4m": "19ddbd9805f77f38c9a9a1bb30dba6c720b8609f",
    "xvi_17.4p": "acff2bf5cde85a16cdc98a52cdea11f77fadf25a",
    "xvi_16.4n": "3bf380ef76c03822a042ecc73b5edd4543c268ce",
    "xvi_18.4r": "b5f830dd2cf25cf154308d2e640f0ecdcda5d8cd",
    # background tilemaps
    "xvi_9.2a": "3106d1aacff06cf78371bd19967141072b32b7d7",
    "xvi_10.2b": "49064b25667ffcd81137cd5e800df4b78b182a46",
    "xvi_11.2c": "3f7eac12863697a98e1122111801606759e44b2a",
    # mcus
    "50xx.bin": "f03c79451e73b3a93c1591cdb27fedc9f130508d",
    "51xx.bin": "50de79e0d6a76bda95ffb02fcce369a79e6abfec",
    "54xx.bin": "01bdf984a49e8d0cc8761b2cc162fd6434d5afbe"
}

def calculate_sha1(file_path):
    sha1_hash = hashlib.sha1()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha1_hash.update(byte_block)
    return sha1_hash.hexdigest()

def verify_checksums(temp_path,EXPECTED_CHKSM,EXPECTED_FILES):
    for file in EXPECTED_FILES:
        file_path = os.path.join(temp_path, file)
        calculated_checksum = calculate_sha1(file_path)
        expected_checksum = EXPECTED_CHKSM[file]
        if calculated_checksum != expected_checksum:
            print(f"Error: Checksum mismatch for {file}")
            print(f"Expected: {expected_checksum}")
            print(f"Calculated: {calculated_checksum}")
            sys.exit(1)
            
               
def split_and_copy_binary_file(input_file, output_file1, output_file2, output_folder,temp_dir):
    try:
    
        fname1=output_file1
        fname2=output_file2
        fname1 = output_file1
        fname2 = output_file2
        output_file1 = os.path.join(temp_dir, fname1)
        output_file2 = os.path.join(temp_dir, fname2)
        
        # Split the binary file into two halves
        with open(input_file, 'rb') as f:
            file_contents = f.read()
            midpoint = len(file_contents) // 2
            first_half = file_contents[:midpoint]
            second_half = file_contents[midpoint:]

             # Determine the output file paths
            output_path1 = os.path.join(temp_dir, output_file1)
            output_path2 = os.path.join(temp_dir, output_file2)
       
            # Write the halves to temporary files
            with open(output_path1, 'wb') as out1:
                out1.write(first_half)
            with open(output_path2, 'wb') as out2:
                out2.write(second_half)
       
            # Copy the split files to the output folder
            print(f"Copying {fname1} to output folder")
            shutil.copy(output_path1, os.path.join(output_folder, fname1))
            print(f"Copying {fname2} to output folder")
            shutil.copy(output_path2, os.path.join(output_folder, fname2))

    except Exception as e:
        print("Error:", str(e))


def main():

    # set pointer to particular version of Bosconian.
    EXPECTED_FILES = ""
    EXPECTED_CHKSM = {}
    
    print("Xevious for MEGA65: ROM Installer")
    print("=================================\n")
    if len(sys.argv) != 3:
        print("The Xevious core expects the files generated by this script located in the folder /arcade/xevious on your SD card.")
        print("This script supports the following versions of Xevious.\n")
        print("xevious           Xevious (Namco)                           (Namco, 1982)")
        print("xeviousa          Xevious (Atari, harder)                   (Namco (Atari license), 1982)")
        print("xeviousc          Xevious (Atari, Namco PCB)                (Namco (Atari license), 1982)")
        print("sxeviousj         Super Xevious (Japan)                     (Namco, 1984)")
        print("Usage: script.py <path to the zip file> <output_folder>")
        sys.exit(1)
      
    filename=""
    if len(sys.argv) > 1:
        argument_value = sys.argv[1]
        fileName = os.path.split(argument_value)[1]
        if fileName == "xevious.zip":             # Xevious (Namco)                    (Namco, 1982)
            EXPECTED_FILES=NAMCO_FILES
            EXPECTED_CHKSM=NAMCO_CHK
        elif fileName == "xeviousc.zip":          # Xevious (Atari, Namco PCB)         (Namco (Atari license), 1982)
            EXPECTED_FILES=ANAMCO_FILES
            EXPECTED_CHKSM=ANAMCO_CHK
        elif fileName == "sxeviousj.zip":         # Super Xevious (Japan)              (Namco, 1984)
            EXPECTED_FILES=SUPERX_FILES
            EXPECTED_CHKSM=SUPERX_CHK     
        elif fileName == "xeviousa.zip":          # Xevious (Atari, harder)            (Namco (Atari license), 1982)
            EXPECTED_FILES=ATARI2_FILES
            EXPECTED_CHKSM=ATARI2_CHK     
            
        else:
            print ("No match found for",sys.argv[1],"\n")
            return
    

    rom_zip_path =  sys.argv[1]
    output_folder = sys.argv[2]

    if not os.path.exists(output_folder):
        print(f"Creating output folder: {output_folder}")
        os.makedirs(output_folder)
  
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Extracting files to temporary directory: {temp_dir}")
        try:
            with zipfile.ZipFile(rom_zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                missing_files = [f for f in EXPECTED_FILES if not os.path.isfile(os.path.join(temp_dir, f))]
                if missing_files:
                    print(f"Error: Missing files in the provided zip file: {', '.join(missing_files)}")
                    sys.exit(1)
                print("Verifying checksums...")
                verify_checksums(temp_dir,EXPECTED_CHKSM,EXPECTED_FILES)
                
                
                print("Merging files and copying to output folder...\n\n")
                # rom1
                print("Preparing ROM 1")
                print("---------------")
                if fileName != "xeviousa.zip":
                    with open(os.path.join(output_folder, "rom1.rom"), "wb") as rom1:
                        for part in [EXPECTED_FILES[0], EXPECTED_FILES[1], EXPECTED_FILES[2], EXPECTED_FILES[3]]: 
                            print(f"Appending {part} to rom1.rom")
                            with open(os.path.join(temp_dir, part), "rb") as f:
                                rom1.write(f.read())
                else:
                    with open(os.path.join(output_folder, "rom1.rom"), "wb") as rom1:
                        for part in [EXPECTED_FILES[0], EXPECTED_FILES[1]]: 
                            print(f"Appending {part} to rom1.rom")
                            with open(os.path.join(temp_dir, part), "rb") as f:
                                rom1.write(f.read())
                                
                 # rom2
                print("\nPreparing ROM 2")
                print("---------------")   
                if fileName != "xeviousa.zip": 
                    with open(os.path.join(output_folder, "rom2.rom"), "wb") as rom2:
                        for part in [EXPECTED_FILES[4],EXPECTED_FILES[5]]: 
                            print(f"Appending {part} to rom2.rom")
                            with open(os.path.join(temp_dir, part), "rb") as f:
                                rom2.write(f.read())          
                else:
                    with open(os.path.join(output_folder, "rom2.rom"), "wb") as rom2:
                        for part in [EXPECTED_FILES[2]]: 
                            print(f"Copying {part} to rom2.rom")
                            with open(os.path.join(temp_dir, part), "rb") as f:
                                rom2.write(f.read())          
                            
                # rom3
                print("\nCopying ROM 3")
                print("-------------")
                if fileName != "xeviousa.zip": 
                    for filename in [EXPECTED_FILES[6]]:
                        print(f"Copying {filename} to output folder")
                        shutil.copy(os.path.join(temp_dir, filename), output_folder)
                else:
                    for filename in [EXPECTED_FILES[3]]:
                        print(f"Copying {filename} to output folder")
                        shutil.copy(os.path.join(temp_dir, filename), output_folder)
                            
                 # foreground tiles
                print("\nCopying foreground tiles")
                print("------------------------")
                if fileName != "xeviousa.zip": 
                    for filename in [EXPECTED_FILES[7]]:
                        print(f"Copying {filename} to output folder")
                        shutil.copy(os.path.join(temp_dir, filename), output_folder)
                else:
                    for filename in [EXPECTED_FILES[4]]:
                        print(f"Copying {filename} to output folder")
                        shutil.copy(os.path.join(temp_dir, filename), output_folder)
                    
                # background tiles
                print("\nCopying background tiles")
                print("------------------------")
                if fileName != "xeviousa.zip": 
                    for filename in [EXPECTED_FILES[8], EXPECTED_FILES[9]]:
                        print(f"Copying {filename} to output folder")
                        shutil.copy(os.path.join(temp_dir, filename), output_folder)
                else:
                    for filename in [EXPECTED_FILES[5], EXPECTED_FILES[6]]:
                        print(f"Copying {filename} to output folder")
                        shutil.copy(os.path.join(temp_dir, filename), output_folder)
                    
                # preparing sprites
                print("\nPreparing sprites")
                print("------------------------")
                if fileName != "xeviousa.zip": 
                    for filename in [EXPECTED_FILES[10],EXPECTED_FILES[11],EXPECTED_FILES[12]]:
                        print(f"Copying {filename} to output folder")
                        shutil.copy(os.path.join(temp_dir, filename), output_folder)
                else:
                    for filename in [EXPECTED_FILES[7],EXPECTED_FILES[8],EXPECTED_FILES[9]]:
                        print(f"Copying {filename} to output folder")
                        shutil.copy(os.path.join(temp_dir, filename), output_folder)
                    
                # Split and copy binary files within the temporary directory
                if fileName != "xeviousa.zip": 
                    input_file = os.path.join(temp_dir, EXPECTED_FILES[13])
                else:
                    input_file = os.path.join(temp_dir, EXPECTED_FILES[10])
                split_and_copy_binary_file(input_file, 'xvi_18.4r_1', 'xvi_18.4r_2', output_folder,temp_dir)
                    
                # background tile maps
                print("\nCopying background tile maps")
                print("----------------------------")
                if fileName != "xeviousa.zip": 
                    for filename in [EXPECTED_FILES[14], EXPECTED_FILES[15],EXPECTED_FILES[16]]:
                        print(f"Copying {filename} to output folder")
                        shutil.copy(os.path.join(temp_dir, filename), output_folder)
                else:
                    for filename in [EXPECTED_FILES[11], EXPECTED_FILES[12],EXPECTED_FILES[13]]:
                        print(f"Copying {filename} to output folder")
                        shutil.copy(os.path.join(temp_dir, filename), output_folder)
                        
                print("\nFiles extracted and merged successfully.")
                print("Cleaning up temporary files...")
                
                # MCU
                print("\nCopying MCUs")
                print("------------")
                if fileName != "xeviousa.zip": 
                    for filename in [EXPECTED_FILES[17], EXPECTED_FILES[18],EXPECTED_FILES[19]]:
                        print(f"Copying {filename} to output folder")
                        shutil.copy(os.path.join(temp_dir, filename), output_folder)
                else:
                    for filename in [EXPECTED_FILES[14], EXPECTED_FILES[15],EXPECTED_FILES[16]]:
                        print(f"Copying {filename} to output folder")
                        shutil.copy(os.path.join(temp_dir, filename), output_folder)
                            
                print("\nFiles extracted and merged successfully.")
                print("Cleaning up temporary files...")
                
                #Create the xevcfg file
                print("\nCreating xevcfg file")
               
                output_file_path = os.path.join(output_folder, "xevcfg")
                with open(output_file_path, "wb") as binary_file:
                    binary_file.write(bytes([0xff]) * 99)
          

        except FileNotFoundError:
                    print(f"Error: ZIP file not found: {rom_zip_path}")
                    sys.exit(1)
        except zipfile.BadZipFile:
                    print(f"Error: Invalid or corrupted ZIP file: {rom_zip_path}")
                    sys.exit(1)

if __name__ == "__main__":
    main()
