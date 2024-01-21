import numpy as np
from collections import OrderedDict

class InputShaftCalculator():
    def _calculate_support_reactions(self):
        LA = self._data['LA'][0]    # [mm]
        LB =  self._data['LB'][0]   # [mm]   

        sum_moments_A = 0
        sum_forces = 0

        # Adding active forces and moments caused by active forces relative to support A
        for force in self.active_forces.values():
            distance_from_A = force['z'] - LA
            sum_moments_A += force['val'] * distance_from_A
            sum_forces += force['val']

        # Calculating support reactions
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
        Zgo, Zsj = self._data['Materiał']['Zgo'][0] * 10**6, self._data['Materiał']['Zsj'][0] * 10**6   # [Pa]
        G = self._data['Materiał']['G'][0] * 10**6                                                      # [Pa]
        xz = self._data['xz'][0]                                                                        # [-]
        qdop = self._data['qdop'][0]                                                                    # [deg]

        # Calculate minimal shaft diameter based on equivalent stress condition         
        kgo = Zgo / xz                                                                                          
        self.d_min_by_equivalent_stress = np.power(32 * self.equivalent_moment / (np.pi * kgo), 1/3) * 1000

        # Calculate minimal shaft diameter based on torsional strength condition
        ksj = Zsj / xz
        self.d_min_by_torsional_strength = np.sqrt(16 * self.torque / (np.pi * ksj)) * 1000

        # Calculate minimal shaft diameter d - based permissible angle of twist condition
        self.d_min_by_permissible_angle_of_twist = np.sqrt(32 * self.torque / (np.pi * G * qdop)) * 1000

    def calculate_initial_functions(self, data):
        self._data = data
        # Extract necessary data
        L, L1 = self._data['L'][0], self._data['L1'][0]                                                 # [mm]
        x, e, B = self._data['x'][0], self._data['e'][0], self._data['B'][0]                            # [mm]
        F = self._data['F'][0]                                                                          # [N]

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
        
        # Set shaft designer data for visualization

        functions = {
            'z': self.z_values, 
            'F': self.all_forces,
            'Mg': self.bending_moment, 
            'Ms': self.torque,
            'Mz': self.equivalent_moment,
            'dMz': self.d_min_by_equivalent_stress,
            'dMs': self.d_min_by_torsional_strength,
            'dqdop': self.d_min_by_permissible_angle_of_twist}
        
        shaft_data = {
            'L': self._data['L'][0],
            'L1': self._data['L1'][0],
            'L2': self._data['L2'][0],
            'LA': self._data['LA'][0],
            'LB': self._data['LB'][0],
            'ds': self._data['dsc'][0],
            'de': self._data['dec'][0],
            'B1': self._data['B'][0],
            'B2': self._data['B'][0],
            'e': self._data['e'][0],
            'x': self._data['x'][0]
        }

        shaft_coordinates = [
            ('A', self._data['LA'][0]),
            ('L1', self._data['L1'][0]),
            ('L2', self._data['L2'][0]),
            ('B', self._data['LB'][0]),
            ('L', self._data['L'][0])
        ]

        return (functions, shaft_data, shaft_coordinates)
