from sympy import *
battery_emf = 0
expected_solar_input = 0
m=300.0

def calc_hold_power(velocity):
    #calculates the power recquired to hold a constant velocity velocity
    return velocity *20.0

def calc_remaining_charge(velocity, initial_charge):
    return

def calc_accel_time(max_power, target_velocity):
    v = Symbol('v')
    result = integrate((m*v) / (max_power - calc_hold_power(v)), (v, 0.0, target_velocity))
    return result # in seconds

print(calc_accel_time(2500, 20.0))