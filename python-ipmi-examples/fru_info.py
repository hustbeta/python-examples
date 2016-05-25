# -*- coding: utf-8 -*-
import pyipmi
import pyipmi.interfaces
import pyipmi.msgs

def get_component_properties(connection):
    cap = connection.get_target_upgrade_capabilities()
    for c in cap.components:
        properties = connection.get_component_properties(c)
        for p in  properties:
            print p

def main():
    interface = pyipmi.interfaces.create_interface('ipmitool', interface_type='lanplus')
    connection = pyipmi.create_connection(interface)
    connection.target = pyipmi.Target(0x20)
    connection.session.set_session_type_rmcp('192.168.65.27', port=623)
    connection.session.set_auth_type_user('admin', 'adminoseasy')
    connection.session.establish()

    ret = connection.get_fru_inventory(fru_id=0)
    b = ret.board_info_area
    print 'board_info_area:'
    print '    custom_mfg_info:', b.custom_mfg_info
    print '    format_version:', b.format_version
    print '    fru_file_id:', b.fru_file_id.value
    print '    language_code:', b.language_code
    print '    manufacturer:', b.manufacturer.value
    print '    mfg_date:', b.mfg_date
    print '    part_number:', b.part_number.value
    print '    product_name:', b.product_name.value
    print '    serial_number:', b.serial_number.value
    c = ret.chassis_info_area
    if c is not None:
        print 'chassis_info_area:', dir(c)
        print '    custom_chassis_info:', c.custom_chassis_info
        print '    format_version:', c.format_version
        print '    part_number:', c.part_number.value
        print '    serial_number:', c.serial_number.value
        print '    type:', c.type
        for t in (
            'TYPE_ALL_IN_ONE', 'TYPE_BUS_EXPANSION_CHASSIS', 'TYPE_DESKTOP',
            'TYPE_DOCKING_STATION', 'TYPE_EXPANSION_CHASSIS', 'TYPE_HAND_HELD',
            'TYPE_LAPTOP', 'TYPE_LOW_PROFILE_DESKTOP', 'TYPE_LUNCH_BOX',
            'TYPE_MAIN_SERVER_CHASSIS', 'TYPE_MINI_TOWER', 'TYPE_NOTEBOOK',
            'TYPE_OTHER', 'TYPE_PERIPHERAL_CHASSIS', 'TYPE_PIZZA_BOX',
            'TYPE_PORTABLE', 'TYPE_RACK_MOUNT_CHASSIS', 'TYPE_RAID_CHASSIS',
            'TYPE_SPACE_SAVING', 'TYPE_SUB_CHASSIS', 'TYPE_SUB_NOTEBOOK',
            'TYPE_TOWER', 'TYPE_UNKNOWN',
        ):
            print '        ', t, getattr(c, t)
    c = ret.common_header
    print 'common_header:'
    print '    board_info_area_offset:', c.board_info_area_offset
    print '    chassis_info_area_offset:', c.chassis_info_area_offset
    print '    format_version:', c.format_version
    print '    internal_use_area_offset:', c.internal_use_area_offset
    print '    multirecord_area_offset:', c.multirecord_area_offset
    print '    product_info_area_offset:', c.product_info_area_offset
    print 'multirecord_area:', ret.multirecord_area
    p = ret.product_info_area
    print 'product_info_area:'
    print '    asset_tag:', p.asset_tag.value
    print '    custom_mfg_info:', p.custom_mfg_info
    print '    format_version:', p.format_version
    print '    fru_file_id:', p.fru_file_id.value
    print '    language_code:', p.language_code
    print '    manufacturer:', p.manufacturer.value
    print '    name:', p.name.value
    print '    part_number:', p.part_number.value
    print '    serial_number:', p.serial_number.value
    print '    version:', p.version.value
    return

if __name__ == '__main__':
    main()

