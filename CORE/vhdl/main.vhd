----------------------------------------------------------------------------------
-- MiSTer2MEGA65 Framework
--
-- Wrapper for the MiSTer core that runs exclusively in the core's clock domanin
--
-- MiSTer2MEGA65 done by sy2002 and MJoergen in 2022 and licensed under GPL v3
----------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.video_modes_pkg.all;

entity main is
   generic (
      G_VDNUM                 : natural                     -- amount of virtual drives
   );
   port (
      clk_main_i              : in  std_logic;
      reset_soft_i            : in  std_logic;
      reset_hard_i            : in  std_logic;
      pause_i                 : in  std_logic;
      dim_video_o             : out std_logic;

      -- MiSTer core main clock speed:
      -- Make sure you pass very exact numbers here, because they are used for avoiding clock drift at derived clocks
      clk_main_speed_i        : in  natural;

      -- Video output
      video_ce_o              : out std_logic;
      video_ce_ovl_o          : out std_logic;
      video_red_o             : out std_logic_vector(3 downto 0);
      video_green_o           : out std_logic_vector(3 downto 0);
      video_blue_o            : out std_logic_vector(3 downto 0);
      video_vs_o              : out std_logic;
      video_hs_o              : out std_logic;
      video_hblank_o          : out std_logic;
      video_vblank_o          : out std_logic;

      -- Audio output (Signed PCM)
      audio_left_o            : out signed(15 downto 0);
      audio_right_o           : out signed(15 downto 0);

      -- M2M Keyboard interface
      kb_key_num_i            : in  integer range 0 to 79;    -- cycles through all MEGA65 keys
      kb_key_pressed_n_i      : in  std_logic;                -- low active: debounced feedback: is kb_key_num_i pressed right now?

      -- MEGA65 joysticks and paddles/mouse/potentiometers
      joy_1_up_n_i            : in  std_logic;
      joy_1_down_n_i          : in  std_logic;
      joy_1_left_n_i          : in  std_logic;
      joy_1_right_n_i         : in  std_logic;
      joy_1_fire_n_i          : in  std_logic;

      joy_2_up_n_i            : in  std_logic;
      joy_2_down_n_i          : in  std_logic;
      joy_2_left_n_i          : in  std_logic;
      joy_2_right_n_i         : in  std_logic;
      joy_2_fire_n_i          : in  std_logic;

      pot1_x_i                : in  std_logic_vector(7 downto 0);
      pot1_y_i                : in  std_logic_vector(7 downto 0);
      pot2_x_i                : in  std_logic_vector(7 downto 0);
      pot2_y_i                : in  std_logic_vector(7 downto 0);
      
       -- Dipswitches
      dsw_a_i                 : in  std_logic_vector(7 downto 0);
      dsw_b_i                 : in  std_logic_vector(7 downto 0);

      dn_clk_i                : in  std_logic;
      dn_addr_i               : in  std_logic_vector(16 downto 0);
      dn_data_i               : in  std_logic_vector(7 downto 0);
      dn_wr_i                 : in  std_logic;

      sp_grphx_addr           : out std_logic_vector(14 downto 0);
      
      osm_control_i      : in  std_logic_vector(255 downto 0)
      
   );
end entity main;

architecture synthesis of main is

signal keyboard_n        : std_logic_vector(79 downto 0);
signal pause_cpu         : std_logic;
signal status            : signed(31 downto 0);
signal flip_screen       : std_logic;
signal flip              : std_logic := '0';
signal video_rotated     : std_logic;
signal rotate_ccw        : std_logic := flip_screen;
signal direct_video      : std_logic;
signal forced_scandoubler: std_logic;
--signal no_rotate         : std_logic := status(2) OR direct_video;
signal gamma_bus         : std_logic_vector(21 downto 0);
signal audio             : std_logic_vector(15 downto 0);


-- I/O board button press simulation ( active high )
-- b[1]: user button
-- b[0]: osd button

signal buttons           : std_logic_vector(1 downto 0);
signal reset             : std_logic  := reset_hard_i or reset_soft_i;


-- highscore system
signal hs_address       : std_logic_vector(10 downto 0);
signal hs_data_in       : std_logic_vector(7 downto 0);
signal hs_data_out      : std_logic_vector(7 downto 0);
signal hs_write_enable  : std_logic;

signal hs_pause         : std_logic;
signal options          : std_logic_vector(1 downto 0);
signal self_test        : std_logic;

constant C_MENU_OSMPAUSE     : natural := 2;
constant C_MENU_OSMDIM       : natural := 3;
constant C_MENU_FLIP         : natural := 9;

-- Game player inputs
constant m65_1             : integer := 56; --Player 1 Start
constant m65_2             : integer := 59; --Player 2 Start
constant m65_5             : integer := 16; --Insert coin 1
constant m65_6             : integer := 19; --Insert coin 2

-- Offer some keyboard controls in addition to Joy 1 Controls
constant m65_up_crsr       : integer := 73; --Player up
constant m65_vert_crsr     : integer := 7;  --Player down
constant m65_left_crsr     : integer := 74; --Player left
constant m65_horz_crsr     : integer := 2;  --Player right
constant m65_left_shift    : integer := 15; --Fire
constant m65_right_shift   : integer := 52; --Fire 2
constant m65_space         : integer := 60; --Bomb


-- Pause, credit button & test mode
constant m65_p             : integer := 41; --Pause button
constant m65_s             : integer := 13; --Service 1
constant m65_capslock      : integer := 72; --Service Mode
constant m65_help          : integer := 67; --Help key



signal ps2_key : std_logic_vector(10 downto 0 );
signal pressed : std_logic;
signal old_state : std_logic;
signal key_start1, key_start2 : std_logic;
signal key_coin1, key_coin2, key_coin3, key_coin4 : std_logic;
signal key_reset, key_service : std_logic;

signal key_p1_up, key_p1_left, key_p1_down, key_p1_right, key_p1_fire, key_p1_bomb : std_logic;
signal key_p2_up, key_p2_left, key_p2_down, key_p2_right, key_p2_fire, key_p2_bomb : std_logic;

signal bomb_auto : std_logic;

begin
   
    audio_left_o(15) <= not audio(15);
    audio_left_o(14 downto 0) <= signed(audio(14 downto 0));
    audio_right_o(15) <= not audio(15);
    audio_right_o(14 downto 0) <= signed(audio(14 downto 0));
   
    options(0) <= osm_control_i(C_MENU_OSMPAUSE);
    options(1) <= osm_control_i(C_MENU_OSMDIM);
    flip_screen <= osm_control_i(C_MENU_FLIP);
    
    
    i_bombtrigger : entity work.bombtrigger
    port map (
    
    clk_i           => clk_main_i, -- use the core's 18mhz clock
                    --reset the time when the fire button is not depressed
    reset_i         => reset,
    enable_i        => '1',                                        
    fire_i          => joy_1_fire_n_i or keyboard_n(m65_right_shift) or joy_2_fire_n_i,
    bomb_o          => bomb_auto           -- c
    );
    
    process (clk_main_i)
        begin
        if rising_edge(clk_main_i) then
            if  not pause_cpu then 
                    self_test <= '1' when not keyboard_n(m65_capslock) else '0';
            end if;
  
        end if;
    end process;
    
    pressed <= ps2_key(9);
    process (clk_main_i)
        begin
        if rising_edge(clk_main_i) then
            old_state <= ps2_key(10);
            if old_state /= ps2_key(10) then
                case ps2_key(8 downto 0) is
                    when x"16" =>
                        key_start1  <= pressed; -- 1
                    when x"1E" =>
                        key_start2  <= pressed; -- 2
                    when x"2E" =>
                        key_coin1   <= pressed; -- 5
                    when x"36" =>
                        key_coin2   <= pressed; -- 6
                    when x"04" =>
                        key_reset   <= pressed; -- F3
                    when x"46" =>
                        key_service <= pressed; -- 9
                        
                    when x"75" => 
                        key_p1_up   <= pressed; -- up
			        when x"6b" =>
			            key_p1_left <= pressed; -- left
			        when x"72" =>
			            key_p1_down <= pressed; -- down
			        when x"74" =>
			            key_p1_right<= pressed; -- right
			        when x"014"=>
			            key_p1_fire <= pressed; -- lctrl    
			        when x"011"=>
			            key_p1_bomb <= pressed; -- lalt
			            
			        when x"02d" =>
			            key_p2_up   <= pressed; -- r
			        when x"023" => 
			            key_p2_left <= pressed; -- d
			        when x"02b" =>
			             key_p2_down <= pressed; -- f
			        when x"034" =>
			             key_p2_right<= pressed; -- g
			        when x"01c" =>
			             key_p2_fire <= pressed; -- a
			        when x"01b" =>
			             key_p2_bomb <= pressed; -- s  
                    when others =>
                        null; -- Do nothing for other cases
                end case;
            end if;
        end if;
    end process;


    i_xevious : entity work.xevious
    port map (
    
    clock_18   => clk_main_i,
    reset      => reset,
    
    video_r    => video_red_o,
    video_g    => video_green_o,
    video_b    => video_blue_o,
    
    --video_csync => open,
    video_hs    => video_hs_o,
    video_vs    => video_vs_o,
    blank_h     => video_hblank_o,
    blank_v     => video_vblank_o,
    
    audio       => audio,
    
    self_test  => self_test,
    service    => not keyboard_n(m65_s),
    coin1      => not keyboard_n(m65_5),
    coin2      => not keyboard_n(m65_6),
    start1     => not keyboard_n(m65_1),
    start2     => not keyboard_n(m65_2),
    up1        => not joy_1_up_n_i, --or not keyboard_n(m65_up_crsr),
    down1      => not joy_1_down_n_i, --or not keyboard_n(m65_vert_crsr),
    left1      => not joy_1_left_n_i, --or not keyboard_n(m65_left_crsr),
    right1     => not joy_1_right_n_i, --or not keyboard_n(m65_horz_crsr),
    fire1      => not joy_1_fire_n_i, --or not keyboard_n(m65_right_shift),
    fire2      => not joy_2_fire_n_i, --or not keyboard_n(m65_space),
    -- player 2 joystick is only active in cocktail/table mode.
    up2        => not joy_2_up_n_i,
    down2      => not joy_2_down_n_i,
    left2      => not joy_2_left_n_i,
    right2     => not joy_2_right_n_i,
    flip       => flip_screen,
    
    -- dip a and b are labelled back to front in MiSTer core, hence this workaround.
    dip_switch_a    => not dsw_b_i,
    dip_switch_b    => not (dsw_a_i(7 downto 5) & (not keyboard_n(m65_space) or not bomb_auto) & dsw_a_i(3 downto 1) & (not keyboard_n(m65_space) or not bomb_auto)),
    
    h_offset   => status(27 downto 24),
    v_offset   => status(31 downto 28),
    pause      => pause_cpu or pause_i,
   
    hs_address => hs_address,
    hs_data_out=> hs_data_out,
    hs_data_in => hs_data_in,
    hs_write   => hs_write_enable,
    
    -- @TODO: ROM loading. For now we will hardcode the ROMs
    -- No dynamic ROM loading as of yet
    dn_clk     => dn_clk_i,
    dn_addr    => dn_addr_i,
    dn_data    => dn_data_i,
    dn_wr      => dn_wr_i
 );
 
    i_pause : entity work.pause
     generic map (
     
        RW  => 3,
        GW  => 3,
        BW  => 2,
        CLKSPD => 18
        
     )         
     port map (
     
         clk_sys        => clk_main_i,
         reset          => reset,
         user_button    => keyboard_n(m65_p),
         pause_request  => hs_pause,
         options        => options,  -- not status(11 downto 10), - TODO, hookup to OSD.
         OSD_STATUS     => '0',       -- disabled for now - TODO, to OSD
         r              => video_red_o,
         g              => video_green_o,
         b              => video_blue_o,
         pause_cpu      => pause_cpu,
         dim_video      => dim_video_o
         --rgb_out        TODO
         
      );
      
   -- @TODO: Keyboard mapping and keyboard behavior
   -- Each core is treating the keyboard in a different way: Some need low-active "matrices", some
   -- might need small high-active keyboard memories, etc. This is why the MiSTer2MEGA65 framework
   -- lets you define literally everything and only provides a minimal abstraction layer to the keyboard.
   -- You need to adjust keyboard.vhd to your needs
   i_keyboard : entity work.keyboard
      port map (
         clk_main_i           => clk_main_i,

         -- Interface to the MEGA65 keyboard
         key_num_i            => kb_key_num_i,
         key_pressed_n_i      => kb_key_pressed_n_i,

         keyboard_n_o          => keyboard_n
      ); -- i_keyboard

end architecture synthesis;

