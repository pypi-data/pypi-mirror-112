import logging
import time

from sielc_dompser.autosampler.autosampler import Autosampler, ProtocolError

# todo find out the angle for the arm to be over the waste port

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    port = 'COM5'
    # autosampler = Autosampler(port)

    # protocol A - system
    # autosampler.firmware_version()

    # protocol B

    # protocol C
    # autosampler.home_tray_arm()  # not protocol c but the tray should be in the home position
    # autosampler.recalibrate_arm()
    # for i in [90, 45]:
    #     autosampler.arm_angle(i)
    # autosampler.arm_to_injection_port()

    # protocol D - tray
    # autosampler.recalibrate_tray()
    # initial_angle = autosampler.tray_angle()
    # autosampler.tray_angle(0)
    # autosampler.tray_angle()
    # autosampler.tray_angle(90)
    # autosampler.tray_angle(initial_angle)
    # mode = autosampler.tray_shaking_mode()
    # for i in range(1, 4):
    #     # todo for some reason looks like no different shaking modes can be set. The only mode is "no shaking",
    #     #  but the tray will still do a shake/vibrate motion
    #     autosampler.tray_shaking_mode(i)
    #     autosampler.shake_tray(10)
    #     # Seems like after shaking the tray, the tray encounters an error (maybe tray angle position unknown) and the
    #     # autosampler LED flashes orange/red, and the tray looks like it performs a recalibration automatically
    #     # afterwards (tray does at least a 360 rotation). Therefore, force the needle to be in the maximum
    #     # height to ensure it doesnt get hit by the needle
    # autosampler.disable_tray_shaking()

    # # protocol F - needle
    # # not implemented anymore
    # # autosampler.washing()  # todo not working getting absent property error, why?!!
    # # autosampler.start_washing()  # todo not working getting absent property error, why?!!
    # # autosampler.stop_washing()  # todo not working getting absent property error, why?!!

    # protocol E - tray and arm
    # # autosampler.recalibrate_tray_arm()  # todo get error, 10001 is too big?
    # autosampler.home_tray_arm()
    # autosampler.move_tray_arm(3)
    # autosampler.vial_number()
    # autosampler.needle_to_min_y()
    # autosampler.move_tray_arm(20)
    # autosampler.vial_number()
    # autosampler.home_tray_arm()
    # try:
    #     autosampler.move_tray_arm(50)
    # except ProtocolError:
    #     pass

    # protocol F - needle
    # autosampler.recalibrate_needle()
    # autosampler.needle_to_max_y()
    # autosampler.needle_to_min_y()

    # convenience methods - moving arm to wash port
    # autosampler.arm_to_injection_port()
    # autosampler.recalibrate_needle()
    # autosampler.needle_to_max_y()
    # autosampler.recalibrate_arm()
    # autosampler.needle_to_bottom_of_waste_port()
    # autosampler.needle_to_above_a_vial(1)
    # autosampler.needle_to_top_of_waste_port()
    # autosampler.needle_to_bottom_of_injection_port()
    # autosampler.needle_to_top_of_vial(5)
    # autosampler.needle_to_top_of_injection_port()
    # autosampler.needle_to_bottom_of_vial(2)
    # autosampler.needle_to_bottom_of_injection_port()

    # protocol G - valve
    # autosampler.recalibrate_valve()
    # autosampler.valve_position()
    # autosampler.valve_position(1)
    # autosampler.valve_position(2)
    # # todo with the autosampler being tested, seems like only positions that can be set are only 1 and 2
    # try:
    #     autosampler.valve_position(6)
    # except ProtocolError:
    #     pass

    # # protocol H - syringe
    # autosampler.recalibrate_plunger()
    # autosampler.plunger_position()
    # autosampler.plunger_position(1000)
    # autosampler.zero_plunger()
    # autosampler.plunger_position(1000)
    # autosampler.zero_plunger(wait=False)
    # time.sleep(1)
    # autosampler.stop_plunger()
    # autosampler.plunger_position()
    # todo seems like after stopping the plunger, it will need to be recalibrated because the autosampler will not
    #  know what the plunger position after it has been stopped
    # autosampler.recalibrate_plunger()
    # autosampler.plunger_position()
    # draw_rate = autosampler.plunger_draw_flow_rate()
    # autosampler.plunger_draw_flow_rate(1000)
    # autosampler.plunger_draw_flow_rate(draw_rate)
    # refill_rate = autosampler.plunger_refill_flow_rate()
    # autosampler.plunger_refill_flow_rate(1000)
    # autosampler.plunger_refill_flow_rate(refill_rate)

    # # protocol I - fan
    # autosampler.fan_speed()
    # autosampler.fan_speed(50)
    # autosampler.fan_speed()
    # autosampler.fan_speed(100)
    # autosampler.fan_speed()
    # autosampler.fan_speed(65)
    # autosampler.fan_speed()

    print('done')
