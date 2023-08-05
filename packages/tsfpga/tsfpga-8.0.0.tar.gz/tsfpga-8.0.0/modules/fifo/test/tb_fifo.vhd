-- -------------------------------------------------------------------------------------------------
-- Copyright (c) Lukas Vik. All rights reserved.
--
-- This file is part of the tsfpga project.
-- https://tsfpga.com
-- https://gitlab.com/tsfpga/tsfpga
-- -------------------------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library osvvm;
use osvvm.RandomPkg.all;

library vunit_lib;
use vunit_lib.axi_stream_pkg.all;
use vunit_lib.sync_pkg.all;
context vunit_lib.com_context;
context vunit_lib.vunit_context;

library common;
use common.types_pkg.all;


entity tb_fifo is
  generic (
    depth : integer;
    almost_full_level : integer := 0;
    almost_empty_level : integer := 0;
    read_stall_probability_percent : integer := 0;
    write_stall_probability_percent : integer := 0;
    enable_last : boolean := false;
    enable_packet_mode : boolean := false;
    enable_drop_packet : boolean := false;
    runner_cfg : string
  );
end entity;

architecture tb of tb_fifo is

  constant width : integer := 8;

  signal clk : std_logic := '0';
  signal level : integer;

  signal read_ready, read_valid, read_last, almost_empty : std_logic := '0';
  signal write_ready, write_valid, write_last, almost_full : std_logic := '0';
  signal read_data, write_data : std_logic_vector(width - 1 downto 0) := (others => '0');
  signal drop_packet : std_logic := '0';

  signal has_gone_full_times, has_gone_empty_times : integer := 0;

  constant read_stall_config : stall_config_t := new_stall_config(
    stall_probability => real(read_stall_probability_percent) / 100.0,
    min_stall_cycles => 1,
    max_stall_cycles => 4);
  constant read_slave : axi_stream_slave_t := new_axi_stream_slave(
    data_length => width,
    stall_config => read_stall_config,
    protocol_checker => new_axi_stream_protocol_checker(data_length => width,
                                                        logger => get_logger("read_slave")));

  constant write_stall_config : stall_config_t := new_stall_config(
    stall_probability => real(write_stall_probability_percent) / 100.0,
    min_stall_cycles => 1,
    max_stall_cycles => 4);
  constant write_master : axi_stream_master_t := new_axi_stream_master(
    data_length => width,
    stall_config => write_stall_config,
    protocol_checker => new_axi_stream_protocol_checker(data_length => width,
                                                        logger => get_logger("write_master")));

begin

  test_runner_watchdog(runner, 1 ms);
  clk <= not clk after 2 ns;


  ------------------------------------------------------------------------------
  main : process

    variable data_queue, last_queue, axi_stream_pop_reference_queue : queue_t := new_queue;
    variable rnd : RandomPType;

    procedure run_test(read_count, write_count : natural; set_last_flag : boolean := true) is
      variable data : std_logic_vector(write_data'range);
      variable last, last_expected : std_logic := '0';
      variable axi_stream_pop_reference : axi_stream_reference_t;
    begin
      for write_idx in 0 to write_count - 1 loop
        data := rnd.RandSLV(data'length);
        last := to_sl(write_idx = write_count - 1 and set_last_flag);

        push_axi_stream(net, write_master, data, last);

        push(data_queue, data);
        push(last_queue, last);
      end loop;

      -- Queue up reads in order to get full throughput
      for read_idx in 0 to read_count - 1 loop
        pop_axi_stream(net, read_slave, axi_stream_pop_reference);
        -- We need to keep track of the pop_reference when we read the reply later.
        -- Hence it is pushed to a queue.
        push(axi_stream_pop_reference_queue, axi_stream_pop_reference);
      end loop;

      for read_idx in 0 to read_count - 1 loop
        axi_stream_pop_reference := pop(axi_stream_pop_reference_queue);
        await_pop_axi_stream_reply(net, axi_stream_pop_reference, data, last);

        check_equal(data, pop_std_ulogic_vector(data_queue), "read_idx " & to_string(read_idx));
        last_expected := pop(last_queue);
        if enable_last then
          check_equal(last, last_expected, "read_idx " & to_string(read_idx));
        end if;
      end loop;

      wait_until_idle(net, as_sync(write_master));
      wait until rising_edge(clk);
    end procedure;

    procedure run_read(count : natural) is
    begin
      run_test(count, 0);
    end procedure;

    procedure run_write(count : natural) is
    begin
      run_test(0, count);
    end procedure;

    procedure clear_queue(queue : queue_t) is
      variable dummy : character;
    begin
      while not is_empty(queue) loop
        dummy := unsafe_pop(queue);
      end loop;
    end procedure;

    procedure pulse_drop_packet is
    begin
      drop_packet <= '1';
      wait until rising_edge(clk);
      drop_packet <= '0';
    end procedure;

  begin
    test_runner_setup(runner, runner_cfg);
    rnd.InitSeed(rnd'instance_name);

    -- Decrease noise
    disable(get_logger("read_slave:rule 4"), warning);
    disable(get_logger("write_master:rule 4"), warning);
    -- Some tests leave data unread in the FIFO
    disable(get_logger("read_slave:rule 9"), error);


    if run("test_init_state") then
      check_equal(read_valid, '0');
      check_equal(write_ready, '1');
      check_equal(almost_full, '0');
      check_equal(almost_empty, '1');

      wait until
        read_valid'event or write_ready'event or almost_full'event or almost_empty'event
        for 1 us;

      check_equal(read_valid, '0');
      check_equal(write_ready, '1');
      check_equal(almost_full, '0');
      check_equal(almost_empty, '1');

    elsif run("test_write_faster_than_read") then
      run_test(5000, 5000);
      check_true(is_empty(data_queue));
      check_relation(has_gone_full_times > 500, "Got " & to_string(has_gone_full_times));

    elsif run("test_read_faster_than_write") then
      run_test(5000, 5000);
      check_true(is_empty(data_queue));
      check_relation(has_gone_empty_times > 500, "Got " & to_string(has_gone_empty_times));

    elsif run("test_packet_mode") then
      -- Write and immediately read a short packet
      run_test(read_count=>1, write_count=>1);

      -- Write a few words, without setting last
      run_test(read_count=>0, write_count=>3, set_last_flag=>false);
      check_relation(level > 0);
      check_equal(read_valid, False);

      -- Writing another word, with last set, shall enable read valid.
      -- Note that the read_valid latency is one cycle higher in packet_mode.
      run_test(read_count=>0, write_count=>1);
      wait until rising_edge(clk);
      check_equal(read_valid, True);

      -- Write further packets
      for i in 1 to 3 loop
        run_test(read_count=>0, write_count=>4);
        check_equal(read_valid, True);
      end loop;

      -- Read and check all the packets (will only work if read_valid is set properly)
      run_read(4 * 4);
      check_equal(read_valid, False);
      check_equal(level, 0);

      -- Write a few words, without setting last
      run_test(read_count=>0, write_count=>3, set_last_flag=>false);
      check_relation(level > 0);
      check_equal(read_valid, False);

      -- Writing another word, with last set, shall enable read valid.
      -- Note that the read_valid latency is one cycle higher in packet_mode.
      run_test(read_count=>0, write_count=>1);
      wait until rising_edge(clk);
      check_equal(read_valid, True);

    elsif run("test_packet_mode_deep") then
      -- Show that the FIFO can be filled with lasts

      -- Fill the FIFO with lasts
      for i in 1 to depth loop
        run_test(read_count=>0, write_count=>1, set_last_flag=>true);
      end loop;
      check_equal(read_valid, True);

      run_read(1);
      check_equal(read_valid, True);

      run_write(1);
      check_equal(read_valid, True);

      run_read(depth);
      check_equal(read_valid, False);

      -- Fill the FIFO with lasts again
      for i in 1 to depth loop
        run_test(read_count=>0, write_count=>1, set_last_flag=>true);
      end loop;
      check_equal(read_valid, True);

      run_read(depth - 1);
      check_equal(read_valid, True);

      run_read(1);
      check_equal(read_valid, False);

    elsif run("test_drop_packet_random_data") then
      -- Write and read some data, to make the pointers advance a little.
      -- Note that this will set write_last on the last write, and some data will be left unread.
      run_test(read_count=>depth / 2, write_count=>depth * 3 / 4);
      check_equal(level, depth / 4);

      -- Write some data without setting last, simulating a packet in progress.
      -- Drop the packet, and then read out the remainder of the previous packet.
      -- Note that the counts chosen will make the pointers wraparound.
      run_test(read_count=>0, write_count=>depth / 2, set_last_flag=>false);
      pulse_drop_packet;
      run_read(depth / 4);

      check_equal(read_valid, '0');
      check_equal(level, 0);

      -- Clear the data in the reference queues. This will be the data that was written, and then
      -- cleared. Hence it was never read and therefore the data is left in the queues.
      clear_queue(data_queue);
      clear_queue(last_queue);

      -- Write and verify a packet. Should be the only thing remaining in the FIFO.
      run_write(4);
      check_equal(level, 4);

      run_read(4);
      check_equal(read_valid, '0');
      check_equal(level, 0);

    elsif run("test_drop_packet_in_same_cycle_as_write_last_should_drop_the_packet") then
      check_equal(level, 0);

      push_axi_stream(net, write_master, tdata=>x"00", tlast=>'0');
      push_axi_stream(net, write_master, tdata=>x"00", tlast=>'1');

      -- Time the behavior of the AXI-Stream master. Appears to be a one cycle delay.
      wait until rising_edge(clk);

      -- The first write happens at this rising edge.
      wait until rising_edge(clk);

      -- Set drop signal on same cycle as the "last" write
      drop_packet <= '1';
      wait until rising_edge(clk);

      check_equal(level, 1);
      check_equal(write_ready and write_valid and write_last and drop_packet, '1');
      wait until rising_edge(clk);

      -- Make sure the packet was dropped
      check_equal(level, 0);
      check_equal(read_valid, '0');
      wait until rising_edge(clk);
      check_equal(read_valid, '0');

    elsif run("test_almost_full") then
      check_equal(almost_full, '0');

      run_write(almost_full_level - 1);
      check_equal(almost_full, '0');

      run_write(1);
      check_equal(almost_full, '1');

      run_read(1);
      check_equal(almost_full, '0');

    elsif run("test_almost_empty") then
      check_equal(almost_empty, '1');

      run_write(almost_empty_level);
      check_equal(almost_empty, '1');

      run_write(1);
      if almost_empty_level = 0 then
        -- almost_empty is updated one cycle later, since write must propagate into RAM before
        -- read data is valid
        wait until rising_edge(clk);
      end if;
      check_equal(almost_empty, '0');

      run_read(1);
      check_equal(almost_empty, '1');
    end if;

    test_runner_cleanup(runner, allow_disabled_errors=>true);
  end process;


  ------------------------------------------------------------------------------
  status_tracking : process
    variable read_transaction, write_transaction : std_logic := '0';
  begin
    wait until rising_edge(clk);

    -- If there was a read transaction last clock cycle, and we now want to read but there is no
    -- data available.
    if read_transaction and read_ready and not read_valid then
      has_gone_empty_times <= has_gone_empty_times + 1;
    end if;

    -- If there was a write transaction last clock cycle, and we now want to write but the fifo
    -- is full.
    if write_transaction and write_valid and not write_ready then
      has_gone_full_times <= has_gone_full_times + 1;
    end if;

    read_transaction := read_ready and read_valid;
    write_transaction := write_ready and write_valid;
  end process;


  ------------------------------------------------------------------------------
  axi_stream_slave_inst : entity vunit_lib.axi_stream_slave
    generic map(
      slave => read_slave
    )
    port map(
      aclk => clk,
      tvalid => read_valid,
      tready => read_ready,
      tdata => read_data,
      tlast => read_last
    );


  ------------------------------------------------------------------------------
  axi_stream_master_inst : entity vunit_lib.axi_stream_master
    generic map(
      master => write_master)
    port map(
      aclk => clk,
      tvalid => write_valid,
      tready => write_ready,
      tdata => write_data,
      tlast => write_last
    );


  ------------------------------------------------------------------------------
  dut : entity work.fifo
    generic map (
      width => width,
      depth => depth,
      almost_full_level => almost_full_level,
      almost_empty_level => almost_empty_level,
      enable_last => enable_last,
      enable_packet_mode => enable_packet_mode,
      enable_drop_packet => enable_drop_packet
    )
    port map (
      clk => clk,
      level => level,

      read_ready => read_ready,
      read_valid => read_valid,
      read_data => read_data,
      read_last => read_last,
      almost_empty => almost_empty,

      write_ready => write_ready,
      write_valid => write_valid,
      write_data => write_data,
      write_last => write_last,
      almost_full => almost_full,
      drop_packet => drop_packet
    );

end architecture;
