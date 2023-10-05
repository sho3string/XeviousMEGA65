----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 09/24/2023 11:43:13 AM
-- Design Name: 
-- Module Name: BombTrigger - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
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
 enable_i        : in std_logic;
 reset_i         : in std_logic;
 fire_i          : in std_logic;
 bomb_o          : out std_logic
);

end entity bombtrigger;

architecture synthesis of bombtrigger is

-- based on 18mhz * 0.25s = 4,500,500       
signal debounce_count : integer range 0 to 4500000; -- Counter for 0.25 seconds debounce (adjust based on clock frequency)
signal bomb           : std_logic;

begin
process (clk_i)
begin
    if rising_edge(clk_i) then
        if fire_i = '1' then
            if debounce_count < 4500000 then
                debounce_count <= debounce_count + 1;
                bomb_o <= '0';
            else
                debounce_count <= 0; --reset the count for another 0.25s
                bomb_o <= '1'; -- Trigger bomb
            end if;
         else
            debounce_count <= 0;
         end if;
    end if;
end process;
 bomb_o <= bomb;
 
end architecture synthesis;