from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import dbconfig as firestore
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# Create your views here.

# Example Post Request
@api_view(["POST"])
def post(data):
    datareturn =json.loads(data.body)
    doc_ref = firestore.db.collection(u'input_members').document(u'test1')
    doc_ref.set(datareturn)
    return JsonResponse(datareturn)

@api_view(["GET"])
def get(self):
    # New Antecedent/Consequent objects hold universe variables and membership
    # functions
    quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
    service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
    tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

    # Auto-membership function population is possible with .automf(3, 5, or 7)
    quality.automf(3)
    service.automf(3)

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
    tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
    tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])

    # quality.view()
    # service.view()
    # tip.view()

    rule1 = ctrl.Rule(quality['poor'] | service['poor'], tip['low'])
    rule2 = ctrl.Rule(service['average'], tip['medium'])
    rule3 = ctrl.Rule(service['good'] | quality['good'], tip['high'])

    tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

    tipping.input['quality'] = 6.5
    tipping.input['service'] = 9.8

    tipping.compute()

    print(tipping.output['tip'])
    #tip.view(sim=tipping)
    return Response(str(tipping.output['tip']),status.HTTP_200_OK)
