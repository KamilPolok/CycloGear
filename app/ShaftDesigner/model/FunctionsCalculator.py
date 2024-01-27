import numpy as np
from collections import OrderedDict

class FunctionsCalculator():
    def _calculate_support_reactions(self):
        LA = self._data['LA'][0]
        LB =  self._data['LB'][0]

        sum_moments_A = 0
        sum_forces = 0

        # Add active forces and moments caused by active forces relative to support A
        for force in self.active_forces.values():
            distance_from_A = force['z'] - LA
            sum_moments_A += force['val'] * distance_from_A
            sum_forces += force['val']

        # Calculate support reactions
        # Equation of moments relative to A: RA * 0 + sum_moments_A + RB * (LB - LA) = 0
        # Equation of vertical forces: RA + RB + sum_forces = 0
        RB = (-sum_moments_A) / (LB - LA)
        RA = -sum_forces - RB

        self.support_reactions = {'Fa': {'z': LA, 'val': RA}, 'Fb': {'z': LB, 'val': RB}}

    def _bending_moment_at_z(self, forces, z):
        moment = 0
        for force in forces.values():
            if force['z'] <= z:
                moment += force['val'] * (z - force['z']) * 0.001
       
        return moment
    
    def _calculate_bending_moment(self):
        self.bending_moment = np.array([self._bending_moment_at_z(self.all_forces, z) for z in self.z_values])

    def _calculate_torque(self):
        self.torque = np.array([self._data['Mwe'][0] if z > self._data['L1'][0] else 0 for z in self.z_values])

    def _calculate_equivalent_moment(self):
        reductionFactor = 2 * np.sqrt(3)
        self.equivalent_moment = np.sqrt(np.power(self.bending_moment, 2) + np.power(reductionFactor / 2 * self.torque, 2))

    def _calculate_minimal_shaft_diameters(self):   
        Zgo, Zsj = self._data['Materiał']['Zgo'][0] * 10**6, self._data['Materiał']['Zsj'][0] * 10**6
        G = self._data['Materiał']['G'][0] * 10**6
        xz = self._data['xz'][0]
        qdop = self._data['qdop'][0]

        # Calculate minimal shaft diameter based on equivalent stress condition         
        kgo = Zgo / xz                                                                                          
        self.d_min_by_equivalent_stress = np.power(32 * self.equivalent_moment / (np.pi * kgo), 1/3) * 1000

        # Calculate minimal shaft diameter based on torsional strength condition
        ksj = Zsj / xz
        self.d_min_by_torsional_strength = np.sqrt(16 * self.torque / (np.pi * ksj)) * 1000

        # Calculate minimal shaft diameter d - based permissible angle of twist condition
        self.d_min_by_permissible_angle_of_twist = np.sqrt(32 * self.torque / (np.pi * G * qdop)) * 1000

    def calculate_initial_functions_and_attributes(self, data):
        self._data = data
        # Extract necessary data
        L, L1 = self._data['L'][0], self._data['L1'][0]
        x, e, B = self._data['x'][0], self._data['e'][0], self._data['B'][0]
        F = self._data['F'][0]

        # Calculate coordinate of second cyclo disc
        L2 = L1 + B + x
        self._data['L2'][0] = L2

        # Organize data
        self.active_forces = {'F1': {'z': L1, 'val': F}, 'F2': {'z': L2, 'val': -F}}

        # Calculate support reactions
        self._calculate_support_reactions()

        # Combine support reactions and active forces into one dict
        self.all_forces = {}
        for forces in (self.active_forces, self.support_reactions): self.all_forces.update(forces)
        self.all_forces = OrderedDict(sorted(self.all_forces.items(), key=lambda x: x[1]['z']))

        # Create z arguments vector
        interval = 0.1
        self.z_values = np.arange(0,L + interval, interval)

        # Calculate functions
        self._calculate_bending_moment()
        self._calculate_torque()
        self._calculate_equivalent_moment()
        
        self._calculate_minimal_shaft_diameters()

        # Save the calculated parameters
        self._data['L2'][0] = L2
        self._data['dsc'][0] = max(self.d_min_by_equivalent_stress.max(),
                                   self.d_min_by_torsional_strength.max(),
                                   self.d_min_by_permissible_angle_of_twist.max())
        self._data['dec'][0] = self._data['dsc'][0] + 2 * e
        self._data['Ra'][0] = self.support_reactions['Fa']['val']
        self._data['Rb'][0] = self.support_reactions['Fb']['val']
        
    def get_shaft_initial_functions(self):
        functions = {
        'Mg': ('Mg(z)', 'Moment gnący Mg [Nm]', 'red', self.bending_moment),
        'Ms': ('Ms(z)', 'Moment skręcający Ms [Nm]', 'green', self.torque),
        'Mz': ('Mz(z)', 'Moment zastępczy Mz [Nm]', 'blue', self.equivalent_moment), 
        'dMz': ('d(Mz)', 'Średnica minimalna ze względu na moment zastępczy dMz [mm]', 'red', self.d_min_by_equivalent_stress),
        'dMs': ('d(Ms)', 'Średnica minimalna ze względu na moment skręcający dMs [mm]', 'green', self.d_min_by_torsional_strength),
        'dqdop': ('d(φ\')', 'Średnica minimalna ze względu na dopuszczalny kąt skręcenia dq\' [mm]', 'blue', self.d_min_by_permissible_angle_of_twist)}

        return (self.z_values, functions)
    
    def get_shaft_initial_attributes(self):
        shaft_data = {
            'L': self._data['L'][0],
            'L1': self._data['L1'][0],
            'L2': self._data['L2'][0],
            'LA': self._data['LA'][0],
            'LB': self._data['LB'][0],
            'n': self._data['n'][0],
            'ds': self._data['dsc'][0],
            'de': self._data['dec'][0],
            'B': self._data['B'][0],
            'B1': self._data['B'][0],
            'B2': self._data['B'][0],
            'e': self._data['e'][0],
            'x': self._data['x'][0]}
        
        return shaft_data

    def get_shaft_coordinates(self):
        shaft_coordinates = [
            ('A', self._data['LA'][0]),
            ('L1', self._data['L1'][0]),
            ('L2', self._data['L2'][0]),
            ('B', self._data['LB'][0]),
            ('L', self._data['L'][0])]
        
        return shaft_coordinates
