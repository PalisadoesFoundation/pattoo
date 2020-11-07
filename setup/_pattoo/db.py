"""Set up pattoo database."""

# Main python libraries

from __future__ import print_function
import random
import string
# pip3 imports
from sqlalchemy import create_engine
# Pattoo libraries
from pattoo_shared import log
from pattoo_shared import data
from pattoo.configuration import ConfigAPId as Config
from pattoo.db import URL
from pattoo.db.models import BASE
from pattoo.db.table import (
   language, pair_xlate_group, pair_xlate, agent_xlate, user, chart, favorite)
from pattoo.constants import DbRowUser, DbRowChart, DbRowFavorite


def insertions():
    """Insert the necessary table ForeignKey values to satisfy defaults.

    Args:
        None

    Returns:
        None

    """
    # Say what we are doing
    print('Inserting default database table entries.')

    # Insert Language
    _insert_language()

    # Insert PairXlateGroup
    _insert_pair_xlate_group()

    # Insert AgentXlate
    _insert_agent_xlate()

    # Insert User
    default_users = _insert_user()

    # Insert Chart
    _insert_chart()

    # Insert Favorite
    _insert_favorite()

    # Print default user credentials
    if bool(default_users) is True:
        print('''\
Creating default users. Change passwords immediately for better security.''')

    for username, password, role_no in default_users:
        role = 'Admin' if role_no == 0 else 'Basic'
        print('''\

Username: {}
Password: {}
Role: {}
'''.format(username, password, role))


def _insert_language():
    """Insert starting default entries into the Language table.

    Args:
        None

    Returns:
        None

    """
    # Insert into Language
    if language.idx_exists(1) is False:
        language.insert_row('en', 'English')


def _insert_pair_xlate_group():
    """Insert starting default entries into the PairXlate table.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    default_name = 'Pattoo Default'
    idx_pair_xlate_groups = {}
    language_dict = {}
    pair_xlate_data = [
        ('OPC UA Agents', [
            ('en', 'pattoo_agent_opcuad_opcua_server', 'OPC UA Server', '')]),
        ('IfMIB Agents', [
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.9', 'Interface Broadcast Packets (HC inbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.8', 'Interface Multicast Packets (HC inbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.6', 'Interface Traffic (HC inbound)', 'Bits / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.7', 'Interface Unicast Packets (inbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.13', 'Interface Broadcast Packets (HC outbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.12', 'Interface Multicast Packets (HC outbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.10', 'Interface Traffic (HC outbound)', 'Bits / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.11', 'Interface Unicast Packets (HC outbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.3', 'Interface Broadcast Packets (inbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.2.2.1.13', 'Interface Discard Errors (inbound)', 'Errors / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.2.2.1.14', 'Interface Errors (inbound)', 'Errors / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.2', 'Interface Multicast Packets (inbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.2.2.1.10', 'Interface Traffic (inbound)', 'Bits / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.2.2.1.11', 'Interface Traffic (inbound)', 'Bits / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.5', 'Interface Broadcast Packets (outbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.2.2.1.19', 'Interface Discard Errors (outbound)', 'Errors / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.2.2.1.20', 'Interface Errors (outbound)', 'Errors / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.4', 'Interface Multicast Packets (outbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.2.2.1.16', 'Interface Traffic (outbound)', 'Bits / Second'),
            ('en', 'pattoo_agent_snmpd_.1.3.6.1.2.1.2.2.1.17', 'Interface Unicast Packets (outbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_ifalias', 'Interface Alias', ''),
            ('en', 'pattoo_agent_snmp_ifmibd_ifdescr', 'Interface Description', ''),
            ('en', 'pattoo_agent_snmp_ifmibd_ifhcinbroadcastpkts', 'Interface Broadcast Packets (HC inbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_ifhcinmulticastpkts', 'Interface Multicast Packets (HC inbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_ifhcinoctets', 'Interface Traffic (HC inbound)', 'Bits / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_ifhcinucastpkts', 'Interface Unicast Packets (HC inbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_ifhcoutbroadcastpkts', 'Interface Broadcast Packets (HC outbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_ifhcoutmulticastpkts', 'Interface Multicast Packets (HC outbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_ifhcoutoctets', 'Interface Traffic (HC outbound)', 'Bits / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_ifhcoutucastpkts', 'Interface Unicast Packets (HC outbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_ifinbroadcastpkts', 'Interface Broadcast Packets (inbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_ifinmulticastpkts', 'Interface Multicast Packets (inbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_ifinoctets', 'Interface Traffic (inbound)', 'Bits / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_ifname', 'Interface Name', ''),
            ('en', 'pattoo_agent_snmp_ifmibd_ifoutbroadcastpkts', 'Interface Broadcast Packets (outbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_ifoutmulticastpkts', 'Interface Multicast Packets (outbound)', 'Packets / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_ifoutoctets', 'Interface Traffic (outbound)', 'Bits / Second'),
            ('en', 'pattoo_agent_snmp_ifmibd_oid', 'SNMP OID', ''),
            ('en', 'pattoo_agent_snmpd_ifalias', 'Interface Alias', ''),
            ('en', 'pattoo_agent_snmpd_ifdescr', 'Interface Description', ''),
            ('en', 'pattoo_agent_snmpd_ifname', 'Interface Name', ''),
            ('en', 'pattoo_agent_snmpd_oid', 'SNMP OID', '')]),
        ('Linux Agents', [
            ('en', 'pattoo_agent_linux_autonomousd_processor', 'Processor Type', ''),
            ('en', 'pattoo_agent_linux_autonomousd_release', 'OS Release', ''),
            ('en', 'pattoo_agent_linux_autonomousd_type', 'OS Type', ''),
            ('en', 'pattoo_agent_linux_autonomousd_version', 'OS Version', ''),
            ('en', 'pattoo_agent_linux_autonomousd_cpus', 'OS CPU Count', ''),
            ('en', 'pattoo_agent_linux_autonomousd_hostname', 'Hostname', ''),
            ('en', 'pattoo_agent_linux_autonomousd_disk_partition_device', 'Disk Partition', ''),
            ('en', 'pattoo_agent_linux_autonomousd_disk_partition_fstype', 'Filesystem Type', ''),
            ('en', 'pattoo_agent_linux_autonomousd_disk_partition_mountpoint', 'Mount Point', ''),
            ('en', 'pattoo_agent_linux_autonomousd_disk_partition_opts', 'Partition Options', ''),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_percent_user', 'User (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_percent_nice', 'Nice (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_percent_system', 'System (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_percent_idle', 'Idle (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_percent_iowait', 'IO Wait (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_percent_irq', 'IRQ (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_percent_softirq', 'Soft IRQ (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_percent_steal', 'Steal (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_percent_guest', 'Guest (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_percent_guest_nice', 'Guest / Nice (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_user', 'User (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_nice', 'Nice (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_system', 'System (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_idle', 'Idle (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_iowait', 'IO Wait (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_irq', 'IRQ (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_softirq', 'Soft IRQ (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_steal', 'Steal (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_guest', 'Guest (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_times_guest_nice', 'Guest / Nice (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_stats_ctx_switches', 'CPU (Context Switches)', 'Events / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_stats_interrupts', 'CPU (Context Switches)', 'Events / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_stats_soft_interrupts', 'CPU (Soft Interrupts)', 'Events / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_stats_syscalls', 'CPU (System Calls)', 'Events / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_memory_total', 'Memory (Total)', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_memory_available', 'Memory (Available)', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_memory_percent', 'Memory (Percent)', 'Percentage Utilization'),
            ('en', 'pattoo_agent_linux_autonomousd_memory_used', 'Memory (Used)', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_memory_free', 'Memory (Free)', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_memory_active', 'Memory (Active)', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_memory_inactive', 'Memory (Inactive)', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_memory_buffers', 'Memory (Buffers)', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_memory_cached', 'Memory (Cached)', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_memory_shared', 'Memory (Shared)', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_memory_slab', 'Memory (Slab)', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_swap_memory_total', 'Swap Memory (Total)', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_swap_memory_used', 'Swap Memory (Used)', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_swap_memory_free', 'Swap Memory (Free)', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_swap_memory_percent', 'Swap Memory (Percent)', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_swap_memory_sin', 'Swap Memory (In)', 'Bytes / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_swap_memory_sout', 'Swap Memory (Out)', 'Bytes / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_disk_partition_disk_usage_total', 'Disk size', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_disk_partition_disk_usage_used', 'Disk Utilization', 'Percent'),
            ('en', 'pattoo_agent_linux_autonomousd_disk_partition_disk_usage_free', 'Disk Free', 'Bytes'),
            ('en', 'pattoo_agent_linux_autonomousd_disk_partition_disk_usage_percent', 'Disk Percentage Utilization', ''),
            ('en', 'pattoo_agent_linux_autonomousd_disk_io_read_count', 'Disk I/O (Read Count)', 'Reads / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_disk_partition', 'Disk Partition', ''),
            ('en', 'pattoo_agent_linux_autonomousd_disk_io_write_count', 'Disk I/O (Write Count)', 'Writes / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_disk_io_read_bytes', 'Disk I/O (Bytes Read)', 'Bytes / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_disk_io_write_bytes', 'Disk I/O (Bytes Written)', 'Bytes / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_disk_io_read_time', 'Disk I/O (Read Time)', ''),
            ('en', 'pattoo_agent_linux_autonomousd_disk_io_write_time', 'Disk I/O (Write Time)', ''),
            ('en', 'pattoo_agent_linux_autonomousd_disk_io_read_merged_count', 'Disk I/O (Read Merged Count)', 'Reads / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_disk_io_write_merged_count', 'Disk I/O (Write Merged Count)', 'Writes / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_disk_io_busy_time', 'Disk I/O (Busy Time)', ''),
            ('en', 'pattoo_agent_linux_autonomousd_network_io_bytes_sent', 'Network I/O (Bandwidth Inbound)', 'Bits / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_network_io_interface', 'Network Interface', ''),
            ('en', 'pattoo_agent_linux_autonomousd_network_io_bytes_recv', 'Network I/O (Bandwidth Outbound)', 'Bits / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_network_io_packets_sent', 'Network I/O (Packets Sent)', 'Packets / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_network_io_packets_recv', 'Network I/O (Packets Received)', 'Packets / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_network_io_errin', 'Network I/O (Errors Inbound)', 'Errors / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_network_io_errout', 'Network I/O (Errors Outbound)', 'Errors / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_network_io_dropin', 'Network I/O (Drops Inbound)', 'Drops / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_network_io_dropout', 'Network I/O (Drops Outbound)', 'Drops / Second'),
            ('en', 'pattoo_agent_linux_autonomousd_cpu_frequency', 'CPU Frequency', 'Frequency'),
            ('en', 'pattoo_agent_linux_spoked_processor', 'Processor Type', ''),
            ('en', 'pattoo_agent_linux_spoked_release', 'OS Release', ''),
            ('en', 'pattoo_agent_linux_spoked_type', 'OS Type', ''),
            ('en', 'pattoo_agent_linux_spoked_version', 'OS Version', ''),
            ('en', 'pattoo_agent_linux_spoked_cpus', 'OS CPU Count', ''),
            ('en', 'pattoo_agent_linux_spoked_hostname', 'Hostname', ''),
            ('en', 'pattoo_agent_linux_spoked_disk_partition_device', 'Disk Partition', ''),
            ('en', 'pattoo_agent_linux_spoked_disk_partition_fstype', 'Filesystem Type', ''),
            ('en', 'pattoo_agent_linux_spoked_disk_partition_mountpoint', 'Mount Point', ''),
            ('en', 'pattoo_agent_linux_spoked_disk_partition_opts', 'Partition Options', ''),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_percent_user', 'User (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_percent_nice', 'Nice (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_percent_system', 'System (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_percent_idle', 'Idle (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_percent_iowait', 'IO Wait (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_percent_irq', 'IRQ (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_percent_softirq', 'Soft IRQ (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_percent_steal', 'Steal (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_percent_guest', 'Guest (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_percent_guest_nice', 'Guest / Nice (Percent CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_user', 'User (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_nice', 'Nice (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_system', 'System (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_idle', 'Idle (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_iowait', 'IO Wait (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_irq', 'IRQ (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_softirq', 'Soft IRQ (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_steal', 'Steal (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_guest', 'Guest (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_times_guest_nice', 'Guest / Nice (CPU Usage)', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_cpu_stats_ctx_switches', 'CPU (Context Switches)', 'Events / Second'),
            ('en', 'pattoo_agent_linux_spoked_cpu_stats_interrupts', 'CPU (Context Switches)', 'Events / Second'),
            ('en', 'pattoo_agent_linux_spoked_cpu_stats_soft_interrupts', 'CPU (Soft Interrupts)', 'Events / Second'),
            ('en', 'pattoo_agent_linux_spoked_cpu_stats_syscalls', 'CPU (System Calls)', 'Events / Second'),
            ('en', 'pattoo_agent_linux_spoked_memory_total', 'Memory (Total)', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_memory_available', 'Memory (Available)', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_memory_percent', 'Memory (Percent)', ''),
            ('en', 'pattoo_agent_linux_spoked_memory_used', 'Memory (Used)', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_memory_free', 'Memory (Free)', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_memory_active', 'Memory (Active)', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_memory_inactive', 'Memory (Inactive)', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_memory_buffers', 'Memory (Buffers)', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_memory_cached', 'Memory (Cached)', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_memory_shared', 'Memory (Shared)', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_memory_slab', 'Memory (Slab)', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_swap_memory_total', 'Swap Memory (Total)', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_swap_memory_used', 'Swap Memory (Used)', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_swap_memory_free', 'Swap Memory (Free)', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_swap_memory_percent', 'Swap Memory (Percent)', ''),
            ('en', 'pattoo_agent_linux_spoked_swap_memory_sin', 'Swap Memory (In)', 'Bytes / Second'),
            ('en', 'pattoo_agent_linux_spoked_swap_memory_sout', 'Swap Memory (Out)', 'Bytes / Second'),
            ('en', 'pattoo_agent_linux_spoked_disk_partition_disk_usage_total', 'Disk size', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_disk_partition_disk_usage_used', 'Disk Utilization', 'Percent'),
            ('en', 'pattoo_agent_linux_spoked_disk_partition_disk_usage_free', 'Disk Free', 'Bytes'),
            ('en', 'pattoo_agent_linux_spoked_disk_partition_disk_usage_percent', 'Disk Percentage Utilization', ''),
            ('en', 'pattoo_agent_linux_spoked_disk_io_read_count', 'Disk I/O (Read Count)', 'Reads / Second'),
            ('en', 'pattoo_agent_linux_spoked_disk_partition', 'Disk Partition', ''),
            ('en', 'pattoo_agent_linux_spoked_disk_io_write_count', 'Disk I/O (Write Count)', 'Writes / Second'),
            ('en', 'pattoo_agent_linux_spoked_disk_io_read_bytes', 'Disk I/O (Bytes Read)', 'Bytes / Second'),
            ('en', 'pattoo_agent_linux_spoked_disk_io_write_bytes', 'Disk I/O (Bytes Written)', 'Bytes / Second'),
            ('en', 'pattoo_agent_linux_spoked_disk_io_read_time', 'Disk I/O (Read Time)', ''),
            ('en', 'pattoo_agent_linux_spoked_disk_io_write_time', 'Disk I/O (Write Time)', ''),
            ('en', 'pattoo_agent_linux_spoked_disk_io_read_merged_count', 'Disk I/O (Read Merged Count)', 'Reads / Second'),
            ('en', 'pattoo_agent_linux_spoked_disk_io_write_merged_count', 'Disk I/O (Write Merged Count)', 'Writes / Second'),
            ('en', 'pattoo_agent_linux_spoked_disk_io_busy_time', 'Disk I/O (Busy Time)', ''),
            ('en', 'pattoo_agent_linux_spoked_network_io_bytes_sent', 'Network I/O (Bandwidth Inbound)', 'Bits / Second'),
            ('en', 'pattoo_agent_linux_spoked_network_io_interface', 'Network Interface', ''),
            ('en', 'pattoo_agent_linux_spoked_network_io_bytes_recv', 'Network I/O (Bandwidth Outbound)', 'Bits / Second'),
            ('en', 'pattoo_agent_linux_spoked_network_io_packets_sent', 'Network I/O (Packets Sent)', 'Packets / Second'),
            ('en', 'pattoo_agent_linux_spoked_network_io_packets_recv', 'Network I/O (Packets Received)', 'Packets / Second'),
            ('en', 'pattoo_agent_linux_spoked_network_io_errin', 'Network I/O (Errors Inbound)', 'Errors / Second'),
            ('en', 'pattoo_agent_linux_spoked_network_io_errout', 'Network I/O (Errors Outbound)', 'Errors / Second'),
            ('en', 'pattoo_agent_linux_spoked_network_io_dropin', 'Network I/O (Drops Inbound)', 'Drops / Second'),
            ('en', 'pattoo_agent_linux_spoked_network_io_dropout', 'Network I/O (Drops Outbound)', 'Drops / Second'),
            ('en', 'pattoo_agent_linux_spoked_cpu_frequency', 'CPU Frequency', '')
        ])
    ]

    # Insert into PairXlateGroup
    if pair_xlate_group.idx_exists(1) is False:
        # Create the default PairXlateGroup
        pair_xlate_group.insert_row(default_name)

        # Create PairXlateGroup for some pattoo agents
        for name, rows in pair_xlate_data:
            # Get PairXlateGroup index value after creating an entry
            pair_xlate_group.insert_row(name)
            idx_pair_xlate_group = pair_xlate_group.exists(name)
            idx_pair_xlate_groups[name] = idx_pair_xlate_group

            # Insert values into the PairXlate table for PairXlateGroup
            for row in rows:
                if len(row) != 4:
                    log_message = (
                        'Translation line "{}" is invalid.'.format(row))
                    log.log2die_safe(20140, log_message)
                (code, _key, _value, _units) = row
                idx_language = language_dict.get(language)
                if bool(idx_language) is False:
                    idx_language = language.exists(code)
                    language_dict[code] = idx_language
                pair_xlate.insert_row(
                    _key, _value, _units, idx_language, idx_pair_xlate_group)


def _insert_agent_xlate():
    """Insert starting default entries into the AgentXlate table.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    agent_xlate_data = [
        ('en', 'pattoo_agent_linux_autonomousd', 'Pattoo Standard Linux Autonomous Agent'),
        ('en', 'pattoo_agent_linux_spoked', 'Pattoo Standard Linux Spoked Agent'),
        ('en', 'pattoo_agent_snmpd', 'Pattoo Standard SNMP Agent'),
        ('en', 'pattoo_agent_snmp_ifmibd', 'Pattoo Standard IfMIB SNMP Agent'),
        ('en', 'pattoo_agent_modbustcpd', 'Pattoo Standard Modbus TCP Agent'),
        ('en', 'pattoo_agent_opcuad', 'Pattoo Standard OPC UA Agent'),
        ('en', 'pattoo_agent_bacnetipd', 'Pattoo Standard BACnet IP Agent')
    ]

    # Insert into AgentXlate
    if agent_xlate.agent_xlate_exists(
            1, 'pattoo_agent_linux_autonomousd') is False:
        for row in agent_xlate_data:
            _key = row[1]
            _value = row[2]
            agent_xlate.insert_row(_key, _value, 1)


def _insert_user():
    """Insert starting default entries into the User table.

    Args:
        None

    Returns:
        default_users: dictionary containing the default user credentials

    """
    default_users = []

    # Insert into User
    if user.idx_exists(1) is False:

        # Creating initial password
        password = data.hashstring(''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(50)))

        # Inserting default user
        user.insert_row(
            DbRowUser(
                username='pattoo',
                password=password,
                first_name='pattoo',
                last_name='pattoo',
                role=1,
                password_expired=1,
                enabled=0)
            )
        default_users.append(('pattoo', password, 1))

    # Insert admin into User table
    if user.idx_exists(2) is False:
        # Creating initial password
        password = data.hashstring(''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(50)))
        user.insert_row(
            DbRowUser(
                username='admin',
                password=password,
                first_name='admin',
                last_name='admin',
                role=0,
                password_expired=1,
                enabled=1)
            )
        default_users.append(('admin', password, 0))

    return default_users

def _insert_chart():
    """Insert starting default entries into the Chart table.

    Args:
        None

    Returns:
        None

    """
    # Insert into Chart
    if chart.idx_exists(1) is False:
        chart.insert_row(
            DbRowChart(name='pattoo', checksum='pattoo', enabled=0))


def _insert_favorite():
    """Insert starting default entries into the Favorite table.

    Args:
        None

    Returns:
        None

    """
    # Insert into Favorite
    if favorite.idx_exists(1) is False:
        favorite.insert_row(
            DbRowFavorite(idx_chart=1, idx_user=1, order=0, enabled=0))


def _mysql():
    """Create database tables.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    config = Config()
    pool_size = config.db_pool_size()
    max_overflow = config.db_max_overflow()

    # Add MySQL to the pool
    engine = create_engine(
        URL, echo=True,
        encoding='utf8',
        max_overflow=max_overflow,
        pool_size=pool_size, pool_recycle=3600)

    # Try to create the database
    print('Connecting to configured database. Altering character set.')
    try:
        sql_string = ('''\
ALTER DATABASE {} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci\
'''.format(config.db_name()))
        engine.execute(sql_string)
    except:
        log_message = (
            '''\
ERROR: Cannot connect to database "{}" on server "{}". Verify database server \
is started. Verify database is created. Verify that the configured database \
authentication is correct.'''.format(config.db_name(), config.db_hostname()))
        log.log2die(20086, log_message)

    # Apply schemas
    print('Creating database tables.')
    BASE.metadata.create_all(engine)


def install():
    """
    Create pattoo database with the necessary insertions.

    Args:
        None

    Returns:
        True for a successful creation
    """
    # Initialize key variables
    use_mysql = True

    # Create DB
    if use_mysql is True:
        _mysql()

    # Insert starting default entries in database tables
    insertions()

    # Done
    print('Database setup complete.')
