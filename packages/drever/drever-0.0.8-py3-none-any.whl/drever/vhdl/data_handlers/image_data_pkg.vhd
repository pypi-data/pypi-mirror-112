library ieee;
use ieee.math_real.all;

use std.textio.all;

library vunit_lib;
use vunit_lib.logger_pkg.all;

package image_data_pkg is

    type t_params is record
        width    : natural;
        height   : natural;
        bitdepth : natural;
        channels : natural;
    end record;

    constant DEFAULT_PARAMS : t_params := (
        width    => 0,
        height   => 0,
        bitdepth => 8,
        channels => 3
    );

    constant MAX_BITDEPTH : natural := 16;
    constant MAX_CHANNELS : natural :=  3;

    subtype t_pixel_range is natural range 0 to 2**MAX_BITDEPTH-1;

    type t_coordinate is record
        x  : natural;
        y  : natural;
        ch : natural;
    end record;

    type t_image is protected
        procedure init(constant name : in string);
        procedure set_params(width, height, bitdepth, channels : natural);
        procedure set_params(image_params : t_params);
        impure function get_params return t_params;
        procedure set_name(name : string);
        procedure set_logger(name : string);
        impure function get_logger_handler return logger_t;
        procedure load(filename : string; use_bitdepth : natural := 0; verbose : boolean := true);
        procedure report_info(prepend : string := "");
        impure function get_entry(x, y, channel : natural := 0) return t_pixel_range;
        procedure set_entry(data : t_pixel_range; x, y, channel : natural := 0);
    end protected;

    impure function compare_image_params(a, b : t_params) return boolean;
    procedure compare_image(
        variable a, b        : inout t_image;
        variable result      : out   integer;
        variable first_error : out   t_coordinate
    );

    procedure assert_image_equal(
        variable a, b   : inout t_image;
        constant msg    : in    string   := "No Message";
        variable logger : in    logger_t := null_logger
    );

end package image_data_pkg;

package body image_data_pkg is

    type t_image is protected body

        variable logger : logger_t := null_logger;

        variable params : t_params := DEFAULT_PARAMS;

        type t_p_string is access string;
        variable p_filename : t_p_string;
        variable p_name     : t_p_string;

        type t_pixel is array (0 to MAX_CHANNELS-1) of t_pixel_range;
        type t_image_data is array (natural range <>, natural range <>) of t_pixel;

        type t_p_image_data is access t_image_data;
        variable p_image_data : t_p_image_data;

        procedure init(constant name : in string) is
        begin
            set_name(name);
            set_logger(name);
        end procedure;

        procedure set_filename(filename : string) is
        begin
            deallocate(p_filename);
            p_filename     := new string(filename'range);
            p_filename.all := filename;
        end procedure;

        procedure set_params(width, height, bitdepth, channels : natural) is
        begin

            if (params.width /= width or params.height /= height) then
                deallocate(p_image_data);
                p_image_data := new t_image_data(
                    0 to width-1,
                    0 to height-1
                );
            end if;

            params.width    := width;
            params.height   := height;
            params.bitdepth := bitdepth;
            params.channels := channels;

        end procedure set_params;

        procedure set_params(image_params : t_params) is
        begin
            set_params(
                image_params.width,
                image_params.height,
                image_params.bitdepth,
                image_params.channels
            );
        end procedure set_params;

        impure function get_params return t_params is
        begin
            return params;
        end function get_params;

        procedure set_name(name : string) is
        begin
            deallocate(p_name);
            p_name     := new string(name'range);
            p_name.all := name;
        end procedure;

        procedure set_logger(name : string) is
        begin
            logger := get_logger(name);
        end procedure;

        impure function get_logger_handler return logger_t is
        begin
            return logger;
        end function;

        procedure load(filename : string; use_bitdepth : natural := 0; verbose : boolean := true) is

            file     ppm_file       : text open read_mode is filename;
            variable ppm_line       : line;
            variable readout_val    : integer;
            variable read_ok        : boolean;

            variable magic_number   : string(1 to 2) := "PX";
            variable file_params    : t_params       := DEFAULT_PARAMS;
            variable max_value      : natural        := 0;
            variable coords         : t_coordinate   := (others => 0);

        begin

            -- Read Magic Number
            readline(ppm_file, ppm_line);
            read(ppm_line, magic_number, read_ok);
            assert read_ok and (magic_number = "P2" or magic_number = "P3")
                report "Magic Number (" & magic_number & ") not known or not supported!"
                severity failure;

            -- Read Width and Height
            readline(ppm_file, ppm_line);
            read(ppm_line, file_params.width, read_ok);
            assert read_ok and file_params.width > 0
                report "Width (" & integer'image(file_params.width) & ") not valid!"
                severity failure;

            read(ppm_line, file_params.height, read_ok);
            assert read_ok and file_params.height > 0
                report "Height (" & integer'image(file_params.height) & ") not valid!"
                severity failure;

            -- Read Maximum Value
            readline(ppm_file, ppm_line);
            read(ppm_line, max_value, read_ok);
            assert read_ok and max_value > 0 and max_value < 2**16
                report "Maximum Value (" & integer'image(max_value) & ") not valid!"
                severity failure;

            if (use_bitdepth = 0) then
                file_params.bitdepth := integer(floor(log2(real(max_value)))) + 1;
                assert file_params.bitdepth >= 1 and file_params.bitdepth <= 16
                    report "Extracted bitdepth not in range [1, 16]."
                    severity failure;
            else
                file_params.bitdepth := use_bitdepth;
            end if;

            -- Create new Testvector with proper size
            if (magic_number = "P2") then
                file_params.channels := 1;
            elsif (magic_number = "P3") then
                file_params.channels := 3;
            else
                report "Only P2 and P3 PPM files are supported!" severity failure;
            end if;

            set_params(file_params);

            while not endfile(ppm_file) loop

                readline(ppm_file, ppm_line);
                read(ppm_line, readout_val, read_ok);

                while read_ok loop

                    p_image_data(coords.x, coords.y)(coords.ch) := readout_val;

                    if coords.ch = file_params.channels-1 then
                        coords.ch := 0;
                        if coords.x = file_params.width-1 then
                            coords.x := 0;
                            if coords.y = file_params.height-1 then
                                coords.y := 0;
                            else
                                coords.y := coords.y + 1;
                            end if;
                        else
                            coords.x := coords.x + 1;
                        end if;
                    else
                        coords.ch := coords.ch + 1;
                    end if;

                    read(ppm_line, readout_val, read_ok);

                end loop;

            end loop;

            read(ppm_line, readout_val, read_ok);

            assert read_ok = false
                report "There's still data left in the PPM file!"
                severity failure;

            set_filename(filename);

            if verbose then
                report_info("Load PPM file (" & magic_number & ") done" & LF);
            end if;

        end procedure;

        procedure report_info(prepend : string := "") is
        begin

            if p_name = null then
                set_name("N/A");
            end if;

            info(logger, prepend &
                "************************************************************************************************" & LF &
                "* Image Data Summary for: " & p_name.all & LF &
                "************************************************************************************************" & LF &
                "* Width / Height: " & integer'image(params.width) & " / " & integer'image(params.height) & LF &
                "* Bitdepth:       " & integer'image(params.bitdepth) & LF &
                "* Loaded File:    " & p_filename.all
            );

        end procedure;

        impure function get_entry(x, y, channel : natural := 0) return t_pixel_range is
        begin

            if (x < params.width and y < params.height and channel < params.channels) then
                return p_image_data(x, y)(channel);
            else
                report "Error while reading testvector entry @ " & LF &
                    "x / y:   " & integer'image(x) & " / " & integer'image(y) & LF &
                    "channel: " & integer'image(channel)
                    severity failure;
                return t_pixel_range'low;
            end if;

        end function;

        procedure set_entry(data : t_pixel_range; x, y, channel : natural := 0) is
        begin
            p_image_data(x, y)(channel) := data;
        end procedure;

    end protected body t_image;

    impure function compare_image_params(a, b : t_params) return boolean is
        variable result : boolean := true;
    begin

        if a = b then
            result := true;
        else
            result := false;
        end if;

        return result;

    end function;

    procedure compare_image(
        variable a, b        : inout t_image;
        variable result      : out   integer;
        variable first_error : out   t_coordinate
    ) is
        variable a_params   : t_params;
        variable b_params   : t_params;
        variable num_errors : integer;
        variable was_first  : boolean;
    begin

        a_params := a.get_params;
        b_params := b.get_params;

        -- Image need same params, otherwise they aren't comparable.
        if not compare_image_params(a_params, b_params) then
            result := -1;
            return;
        end if;

        num_errors := 0;
        was_first  := true;

        for x in 0 to a_params.width-1 loop
            for y in 0 to a_params.height-1 loop
                for channel in 0 to a_params.channels-1 loop
                if (a.get_entry(x, y, channel) /= b.get_entry(x, y, channel)) then

                        num_errors := num_errors + 1;

                        if was_first then
                            first_error.x  := x;
                            first_error.y  := y;
                            first_error.ch := channel;
                        end if;

                    end if;
                end loop;
            end loop;
        end loop;

        result := num_errors;

        return;

    end procedure;

    procedure assert_image_equal(
        variable a, b   : inout t_image;
        constant msg    : in    string   := "No Message";
        variable logger : in    logger_t := null_logger
    ) is
        variable a_params       : t_params;
        variable b_params       : t_params;
        variable compare_result : integer;
        variable total_values   : integer;
        variable first_error    : t_coordinate;
    begin

        a_params := a.get_params;
        b_params := b.get_params;

        compare_image(a, b, compare_result, first_error);

        -- Image geometry missmatch when result is lower 0
        if compare_result < 0 then

            error(logger,
                "Image Parameter Missmatch!" & LF &
                "" & LF &
                msg & LF &
                "" & LF &
                "Image A - width: " & justify(integer'image(a_params.width),    right, 5) & LF &
                "         height: " & justify(integer'image(a_params.height),   right, 5) & LF &
                "       bitdepth: " & justify(integer'image(a_params.bitdepth), right, 5) & LF &
                "       channels: " & justify(integer'image(a_params.channels), right, 5) & LF &
                "" & LF &
                "Image B - width: " & justify(integer'image(b_params.width),    right, 5) & LF &
                "         height: " & justify(integer'image(b_params.height),   right, 5) & LF &
                "       bitdepth: " & justify(integer'image(b_params.bitdepth), right, 5) & LF &
                "       channels: " & justify(integer'image(b_params.channels), right, 5) & LF &
                ""
            );

        elsif compare_result > 0 then

            total_values := a_params.width * a_params.height * a_params.channels;

            error(logger,
                "Image Data Missmatch!" & LF &
                "" & LF &
                msg & LF &
                "" & LF &
                "Number of failing values: " & justify(integer'image(compare_result),  right, 10) & LF &
                "Number of total values:   " & justify(integer'image(total_values),    right, 10) & LF &
                "" & LF &
                "First failing value        x: " & justify(integer'image(first_error.x),  right, 6) & LF &
                "                           y: " & justify(integer'image(first_error.y),  right, 6) & LF &
                "                     channel: " & justify(integer'image(first_error.ch), right, 6) & LF &
                ""
            );

        end if;

    end procedure;

end package body image_data_pkg;
