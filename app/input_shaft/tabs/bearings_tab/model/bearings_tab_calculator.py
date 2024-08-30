import numpy as np

class BearingsTabCalculator():
    def init_data(self, component_data, inputs, outputs):
        self._component_data = component_data
        self._inputs = inputs
        self._outputs = outputs
    
    def calculate_bearing_load_capacity(self, bearing_section_id, data):
        """
        Calculate bearing load capacity.
        """
        p = 3.0
        nwe = self._component_data['nwe'][0]
        F = self._component_data['Bearings'][bearing_section_id]['F'][0]

        attributes = data['Bearings'][bearing_section_id]
    
        lh = attributes['Lh'][0]
        fd = attributes['fd'][0]
        ft = attributes['ft'][0]

        l = 60 * lh * nwe / np.power(10, 6)
        c = np.abs(F) * np.power(l, 1 / p) * ft / fd / 1000 # [kN]

        # attributes['Lr'][0] = l
        return c