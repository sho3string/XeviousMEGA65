----------------------------------------------------------------------------------
-- Company: 
-- Engineer: Muse ( Samuel P )
-- 
-- Create Date: 09/24/2023 11:43:13 AM
-- Design Name: Bombtrigger
-- Module Name: BombTrigger
-- Project Name: Xevious
-- Target Devices: Mega65 r3a
-- Tool Versions: 
-- Description: Commodore / Atari joysticks typically lacked a second button, the second button here is a programmable input mechanism designed to replicate the functionality of a 
-- physical second button in scenarios where only one physical button is available. It provides users with a convenient and intuitive way to trigger secondary actions 
-- or commands, such as launching special abilities or performing specific functions, without the need for additional physical button or reaching for the space bar.
-- 
-- This mimics Who Dares Wins I/II's control system where a player can effortlessly lob grenades by simply holding down the fire button for short period of time.
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity bombtrigger is
port (
 clk_i           : in std_logic;
 enable_n_i      : in std_logic;
 reset_i         : in std_logic;
 -- player 1
 fire1_n_i       : in std_logic;
 bomb1_o         : out std_logic;
 -- player 2
 fire2_n_i       : in std_logic;
 bomb2_o         : out std_logic;
 -- trigger select switch
 trigger_sel_i   : in std_logic_vector(3 downto 0)
);

end entity bombtrigger;

architecture synthesis of bombtrigger is

-- based on 18mhz * 0.25s = 4,500,000 - default setting.    
signal bomb1_trigger_count : integer range 0 to 9000000; -- Counter for a maximum of 0.50 seconds at 18mhz
signal bomb2_trigger_count : integer range 0 to 9000000;
signal bomb_delay          : integer range 0 to 9000000; -- Delay setting from OSM

begin
process (clk_i,fire1_n_i,fire2_n_i)
begin
    if rising_edge(clk_i) then
    
       if enable_n_i = '0' then
       
           -- check the delay setting from the OSM.
           bomb_delay <= 0 when trigger_sel_i = "0000" else     -- no delay 
                   2700000 when trigger_sel_i = "0001" else     -- 0.15s
                   3600000 when trigger_sel_i = "0010" else     -- 0.20s
                   4500000 when trigger_sel_i = "0011" else     -- 0.25s
                   5400000 when trigger_sel_i = "0100" else     -- 0.30s
                   6300000 when trigger_sel_i = "0101" else     -- 0.35s
                   7200000 when trigger_sel_i = "0110" else     -- 0.40s
                   8100000 when trigger_sel_i = "0111" else     -- 0.45s
                   9000000 when trigger_sel_i = "1000";         -- 0.50s
           
           if reset_i = '1' then
              bomb1_trigger_count <= bomb_delay;
              bomb1_o <= '1';
              bomb2_trigger_count <= bomb_delay;
              bomb2_o <= '1';
           else
                -- handle player 1
                if fire1_n_i = '0' then            -- fire button is active low
                    if  bomb1_trigger_count = 0 then    
                        bomb1_o <= '0';
                    else
                        bomb1_trigger_count <= bomb1_trigger_count - 1;
                        bomb1_o <= '1';
                    end if;
                else
                   bomb1_trigger_count <= bomb_delay; -- use a constant instead of a magic number
                   bomb1_o <= '1';
                end if;
                
                -- handle player 2 ( cocktail mode only )
                if fire2_n_i = '0' then            -- fire button is active low
                    if  bomb2_trigger_count = 0 then
                        bomb2_o <= '0';
                    else
                        bomb2_trigger_count <= bomb2_trigger_count - 1;
                        bomb2_o <= '1';
                    end if;
                else
                   bomb2_trigger_count <= bomb_delay; -- use a constant instead of a magic number
                   bomb2_o <= '1';
                end if;
           end if;
        end if;
  end if;
end process;

 
end architecture synthesis;