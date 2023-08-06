library ieee;
use ieee.math_real.all;

use std.textio.all;

library vunit_lib;
use vunit_lib.logger_pkg.all;

package stream_data_pkg is

    type t_params is record
        size       : natural;
        data_width : natural;
        channels   : natural;
    end record;

    constant DEFAULT_PARAMS : t_params := (
        size       =>  0,
        data_width => 16,
        channels   =>  1
    );

    constant MAX_SIZE       : natural := 2**16;
    constant MAX_DATA_WIDTH : natural :=  32;
    constant MAX_CHANNELS   : natural := 256;

    subtype t_data_range is integer;

    type t_coordinate is record
        x  : natural;
        ch : natural;
    end record;

    type t_stream is protected
        procedure init(constant name : in string);
        procedure set_params(size, data_width, channels : natural);
        procedure set_params(stream_params : t_params);
        impure function get_params return t_params;
        procedure set_name(name : string);
        procedure set_logger(name : string);
        impure function get_logger_handler return logger_t;
        procedure load(filename : string; verbose : boolean := true);
        procedure report_info(prepend : string := "");
        impure function get_entry(x, channel : natural := 0) return t_data_range;
        procedure set_entry(data : t_data_range; x, channel : natural := 0);
    end protected;

    impure function compare_stream_params(a, b : t_params) return boolean;
    procedure compare_stream(
        variable a, b        : inout t_stream;
        variable result      : out   integer;
        variable first_error : out   t_coordinate
    );

    procedure assert_stream_equal(
        variable a, b   : inout t_stream;
        constant msg    : in    string   := "No Message";
        variable logger : in    logger_t := null_logger
    );

end package stream_data_pkg;

package body stream_data_pkg is

    type t_stream is protected body

        variable logger : logger_t := null_logger;

        variable params : t_params := DEFAULT_PARAMS;

        type t_p_string is access string;
        variable p_filename : t_p_string;
        variable p_name     : t_p_string;

        type t_stream_data is array (natural range <>, natural range <>) of t_data_range;

        type t_p_stream_data is access t_stream_data;
        variable p_stream_data : t_p_stream_data;

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

        procedure set_params(size, data_width, channels : natural) is
        begin

            if (params.size /= size) then
                deallocate(p_stream_data);
                p_stream_data := new t_stream_data(
                    0 to size-1,
                    0 to channels-1
                );
            end if;

            params.size       := size;
            params.data_width := data_width;
            params.channels   := channels;

        end procedure set_params;

        procedure set_params(stream_params : t_params) is
        begin
            set_params(
                stream_params.size,
                stream_params.data_width,
                stream_params.channels
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

        procedure load(filename : string; verbose : boolean := true) is

            file     txt_file    : text open read_mode is filename;
            variable txt_line    : line;
            variable readout_val : integer;
            variable read_ok     : boolean;

            variable file_params : t_params     := DEFAULT_PARAMS;
            variable coords      : t_coordinate := (others => 0);

        begin

            -- Read Header
            readline(txt_file, txt_line);
            read(txt_line, file_params.size, read_ok);
            assert read_ok and file_params.size > 0
                report "Width (" & integer'image(file_params.size) & ") not valid!"
                severity failure;

            readline(txt_file, txt_line);
            read(txt_line, file_params.data_width, read_ok);
            assert read_ok and file_params.data_width > 0
                report "Height (" & integer'image(file_params.data_width) & ") not valid!"
                severity failure;

            readline(txt_file, txt_line);
            read(txt_line, file_params.channels, read_ok);
            assert read_ok and file_params.channels > 0
                report "Height (" & integer'image(file_params.channels) & ") not valid!"
                severity failure;

            set_params(file_params);

            while not endfile(txt_file) loop

                readline(txt_file, txt_line);
                read(txt_line, readout_val, read_ok);

                while read_ok loop

                    p_stream_data(coords.x, coords.ch) := readout_val;

                    if coords.ch = file_params.channels-1 then
                        coords.ch := 0;
                        if coords.x = file_params.size-1 then
                            coords.x := 0;
                        else
                            coords.x := coords.x + 1;
                        end if;
                    else
                        coords.ch := coords.ch + 1;
                    end if;

                    read(txt_line, readout_val, read_ok);

                end loop;

            end loop;

            read(txt_line, readout_val, read_ok);

            assert read_ok = false
                report "There's still data left in the PPM file!"
                severity failure;

            set_filename(filename);

            if verbose then
                report_info("Load TXT file done" & LF);
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
                "* Size / Channels: " & integer'image(params.size) & " / " & integer'image(params.channels) & LF &
                "* Data Width:      " & integer'image(params.data_width) & LF &
                "* Loaded File:     " & p_filename.all
            );

        end procedure;

        impure function get_entry(x, channel : natural := 0) return t_data_range is
        begin

            if (x < params.size and channel < params.channels) then
                return p_stream_data(x, channel);
            else
                report "Error while reading testvector entry @ " & LF &
                    "x:       " & integer'image(x) & LF &
                    "channel: " & integer'image(channel)
                    severity failure;
                return t_data_range'low;
            end if;

        end function;

        procedure set_entry(data : t_data_range; x, channel : natural := 0) is
        begin
            p_stream_data(x, channel) := data;
        end procedure;

    end protected body t_stream;

    impure function compare_stream_params(a, b : t_params) return boolean is
    begin
        if a = b then
            return true;
        end if;
        return false;
    end function;

    procedure compare_stream(
        variable a, b        : inout t_stream;
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

        -- Stream need same params, otherwise they aren't comparable.
        if not compare_stream_params(a_params, b_params) then
            result := -1;
            return;
        end if;

        num_errors := 0;
        was_first  := true;

        for x in 0 to a_params.size-1 loop
            for channel in 0 to a_params.channels-1 loop
                if (a.get_entry(x, channel) /= b.get_entry(x, channel)) then
                    num_errors := num_errors + 1;
                    if was_first then
                        first_error.x  := x;
                        first_error.ch := channel;
                    end if;
                end if;
            end loop;
        end loop;

        result := num_errors;

        return;

    end procedure;

    procedure assert_stream_equal(
        variable a, b   : inout t_stream;
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

        compare_stream(a, b, compare_result, first_error);

        -- Image geometry missmatch when result is lower 0
        if compare_result < 0 then

            error(logger,
                "Stream Parameter Missmatch!" & LF &
                "" & LF &
                msg & LF &
                "" & LF &
                "Image A - size: " & justify(integer'image(a_params.size),       right, 5) & LF &
                "    data_width: " & justify(integer'image(a_params.data_width), right, 5) & LF &
                "      channels: " & justify(integer'image(a_params.channels),   right, 5) & LF &
                "" & LF &
                "Image B - size: " & justify(integer'image(b_params.size),       right, 5) & LF &
                "    data_width: " & justify(integer'image(b_params.data_width), right, 5) & LF &
                "      channels: " & justify(integer'image(b_params.channels),   right, 5) & LF &
                ""
            );

        elsif compare_result > 0 then

            total_values := a_params.size * a_params.channels;

            error(logger,
                "Image Data Missmatch!" & LF &
                "" & LF &
                msg & LF &
                "" & LF &
                "Number of failing values: " & justify(integer'image(compare_result), right, 10) & LF &
                "Number of total values:   " & justify(integer'image(total_values),   right, 10) & LF &
                "" & LF &
                "First failing value    x: " & justify(integer'image(first_error.x),  right, 6) & LF &
                "                 channel: " & justify(integer'image(first_error.ch), right, 6) & LF &
                ""
            );

        end if;

    end procedure;

end package body stream_data_pkg;
