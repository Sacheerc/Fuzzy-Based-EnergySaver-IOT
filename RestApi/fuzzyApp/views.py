from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from skfuzzy import control as ctrl

import json
import dbconfig as firestore
import numpy as np
import fuzzyApp.utils as utils
import skfuzzy as fuzz



# Create your views here.

# Example Post Request
@api_view(["POST"])
def sensor_data_in(data):
    datareturn =json.loads(data.body)
    datareturn['timestamp']= datetime.now()
    data_front= json.loads(data.body)
    data_front['output_ac'] = 34
    data_front['output_lights'] = 55
    data_front['timestamp'] = datetime.now()

    doc_ref1 = firestore.db.collection(u'input_members').document()
    doc_ref2 = firestore.db.collection(u'current_env').document(u'c_env')
    doc_ref1.set(datareturn)
    doc_ref2.set(data_front)
    print(datareturn)
    return JsonResponse(datareturn)

@api_view(["GET"])
def get(self):
    # New Antecedent/Consequent objects hold universe variables and membership
    # functions
    # quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
    # service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
    # tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

    # Input and Output array declaration
    light_level = ctrl.Antecedent(np.arange(0, 21, 1), 'light_level') # should change the range according to the sensor value
    temp_level = ctrl.Antecedent(np.arange(0, 21, 1), 'temp_level') # should change the range according to the sensor value
    power_level_for_light = ctrl.Antecedent(np.arange(0, 11, 1), 'power_level_for_light') # should change the range according to the sensor value
    power_level_for_temp = ctrl.Antecedent(np.arange(0, 11, 1), 'power_level_for_temp') # should change the range according to the sensor value

    # Auto-membership function population is possible with .automf(3, 5, or 7)
    # quality.automf(3)
    # service.automf(3)

    # Auto membership function population
    light_level.automf(3) # poor, average, good
    temp_level.automf(3)
    power_level_for_light.automf(3)
    power_level_for_temp.automf(3)

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    # tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
    # tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
    # tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])

    # quality.view()
    # service.view()
    # tip.view()

    # rule1 = ctrl.Rule(quality['poor'] | service['poor'], tip['low'])
    # rule2 = ctrl.Rule(service['average'], tip['medium'])
    # rule3 = ctrl.Rule(service['good'] | quality['good'], tip['high'])

    # rules initialization
    rule1 = ctrl.Rule(light_level['poor'] & temp_level['poor'], (power_level_for_light['good'], power_level_for_temp['good']))
    rule2 = ctrl.Rule(light_level['poor'] & temp_level['poor'], (power_level_for_light['good'], power_level_for_temp['good']))
    rule3 = ctrl.Rule(light_level['poor'] & temp_level['poor'], (power_level_for_light['good'], power_level_for_temp['good']))

    # tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    # tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

    # Control system and simulation
    power_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    power = ctrl.ControlSystemSimulation(power_ctrl)

    # tipping.input['quality'] = 6.5
    # tipping.input['service'] = 9.8

    # tipping.compute()

    power.input['light_level'] = 6.5
    power.input['temp_level'] = 9.8

    power.compute()

    # print(tipping.output['tip'])
    #tip.view(sim=tipping)
    # return Response(str(tipping.output['tip']),status.HTTP_200_OK)
    return Response(str(power.output['power_level_for_light']) + ' - ' + str(power.output['power_level_for_temp']), status.HTTP_200_OK)
