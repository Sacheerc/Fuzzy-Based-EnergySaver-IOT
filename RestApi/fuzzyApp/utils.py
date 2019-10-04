from skfuzzy import control as ctrl
import numpy as np

def fuzzy_val_generator(light_level_in,temp_level_in):

    # Input and Output array declaration
    light_level = ctrl.Antecedent(np.arange(0, 21, 1),'light_level')  # should change the range according to the sensor value
    temp_level = ctrl.Antecedent(np.arange(0, 21, 1),'temp_level')  # should change the range according to the sensor value
    power_level_for_light = ctrl.Consequent(np.arange(0, 11, 1),'power_level_for_light')  # should change the range according to the sensor value
    power_level_for_temp = ctrl.Consequent(np.arange(0, 11, 1),'power_level_for_temp')  # should change the range according to the sensor value

    # Auto membership function population
    light_level.automf(3)  # poor, average, good
    temp_level.automf(3)
    power_level_for_light.automf(3)
    power_level_for_temp.automf(3)

    # rules initialization
    rule1 = ctrl.Rule(light_level['poor'] & temp_level['poor'],(power_level_for_light['good'], power_level_for_temp['good']))
    rule2 = ctrl.Rule(light_level['poor'] & temp_level['average'],(power_level_for_light['good'], power_level_for_temp['average']))
    rule3 = ctrl.Rule(light_level['poor'] & temp_level['good'],(power_level_for_light['good'], power_level_for_temp['poor']))
    rule4 = ctrl.Rule(light_level['average'] & temp_level['poor'],(power_level_for_light['average'], power_level_for_temp['good']))
    rule5 = ctrl.Rule(light_level['average'] & temp_level['average'],(power_level_for_light['average'], power_level_for_temp['average']))
    rule6 = ctrl.Rule(light_level['average'] & temp_level['good'],(power_level_for_light['average'], power_level_for_temp['poor']))
    rule7 = ctrl.Rule(light_level['good'] & temp_level['poor'],(power_level_for_light['poor'], power_level_for_temp['good']))
    rule8 = ctrl.Rule(light_level['good'] & temp_level['average'],(power_level_for_light['poor'], power_level_for_temp['average']))
    rule9 = ctrl.Rule(light_level['good'] & temp_level['good'],(power_level_for_light['poor'], power_level_for_temp['poor']))

    # Control system and simulation
    power_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
    power = ctrl.ControlSystemSimulation(power_ctrl)

    power.input['light_level'] = light_level_in
    power.input['temp_level'] = temp_level_in

    power.compute()

    return power.output['power_level_for_light'],power.output['power_level_for_temp']
