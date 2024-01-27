import numpy as np
from collections import OrderedDict

class FunctionsCalculator():
    def __init__(self):
        self.d_min_by_permissible_deflection_angle = None
        self.d_min_by_permissible_deflection_arrow = None

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
    
    def _cutting_force_at_z(self, loads, z):
        cutting_force = 0
        for load in loads.values():
            if load['z'] <= z:
                cutting_force += load['val']
        return cutting_force
    
    def _psi_at_z(self, loads, z):
        # Funkcja do obliczania kąta ugięcia w punkcie z - bez stałych całkowania
        deflection_angle = 0
        for key, load in loads.items():
            if load['z'] <= z:
                if key.startswith('F') or key.startswith('Q'):
                    deflection_angle += 1 / 2 * load['val'] * ((z - load['z']) * 0.001)**2
                elif key.startswith('M'):
                    deflection_angle += load['val'] * ((z - load['z']) * 0.001)
        return deflection_angle
    
    def _phi_at_z(self, loads, z):
        # Funkcja do obliczania strzałki ugięcia w punkcie z - bez stałych całkowania
        deflection_arrow = 0
        for key, load in loads.items():
            if load['z'] <= z:
                if key.startswith('F') or key.startswith('Q'):
                    deflection_arrow += 1 / 6 * load['val'] * ((z - load['z']) * 0.001)**3
                elif key.startswith('M'):
                    deflection_arrow += load['val'] * ((z - load['z']) * 0.001)**2
        return deflection_arrow

    def _calculate_integration_constants(self):
        LA = self._data['LA'][0]
        LB = self._data['LB'][0]
        mA = self._phi_at_z(self._all_loads, LA)
        mB = self._phi_at_z(self._all_loads, LB)

        LA *= 0.001
        LB *= 0.001

        C = (mB - mA) / (LA - LB)
        D = -mB - C * LB

        return {'C': C, 'D': D}
    
    def _calculate_bending_moment(self):
        self.bending_moment = np.array([self._bending_moment_at_z(self._all_forces, z) for z in self._z_values])

    def _calculate_torque(self):
        self.torque = np.array([self._data['Mwe'][0] if z > self._data['L1'][0] else 0 for z in self._z_values])

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

    def _check_if_whole_shaft_designed(self):
        total_length = 0
        for step in self._shaft_steps:
                total_length += step['l']

        return  total_length == self._data['L'][0]
        
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
        self._all_forces = {}
        for forces in (self.active_forces, self.support_reactions): self._all_forces.update(forces)
        self._all_forces = OrderedDict(sorted(self._all_forces.items(), key=lambda x: x[1]['z']))

        # Create z arguments vector
        interval = 0.1
        self._z_values = np.arange(0,L + interval, interval)

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
        
    def calculate_remaining_functions(self, shaft_steps):
        self._shaft_steps = shaft_steps
        if self._check_if_whole_shaft_designed():
            L = self._data['L'][0]
            LA = self._data['LA'][0]
            LB = self._data['LB'][0]
            teta_dop = self._data['tetadop'][0]
            f_dop = self._data['fdop'][0]
            # Calculate the diameter and the moment of inertia of the equivalent smooth shaft
            d = sum(step['l'] * step['d'] for step in self._shaft_steps)/(sum(step['l'] for step in self._shaft_steps))
            E = self._data['Materiał']['E'][0] * 10**6
            I = np.pi * (d * 0.001)**4 / 64
            EI = E * I
            # Calculate coefficients k=I/Ij for every shaft step
            for step in self._shaft_steps:
                Ij = np.pi * (step['d'] * 0.001)**4 / 64
                step['k'] = I /  Ij
            # Calculate equivalent forces acting on equivalent smooth shaft
            self._updated_forces = {}
            for key, force in self._all_forces.items():
                for idx in range(len(self._shaft_steps)):
                    if idx == len(self._shaft_steps) - 1 or force['z'] < self._shaft_steps[idx+1]['z']:
                        self._updated_forces[key] = {'z': force['z'], 'val': force['val'] * self._shaft_steps[idx]['k']}
                        break
            # Calculate the increments of bending moments and shear forces acting at the beginning of each shaft step (j)
            self._moment_gains = {}
            self._cutting_force_gains = {}
            for idx, step in enumerate(self._shaft_steps[:-1]):
                # Coordinate of the shaft step start n + 1 = j
                lj = self._shaft_steps[idx+1]['z']
                # Increment of bending moment
                bending_moment = self._bending_moment_at_z(self._all_forces, lj)
                deltaM = {'z': lj, 'val': bending_moment * (self._shaft_steps[idx+1]['k'] - self._shaft_steps[idx]['k'])}
                self._moment_gains[f'M{idx+1}'] = deltaM
                # increment of shear force
                cutting_force = self._cutting_force_at_z(self._all_forces, lj)
                deltaQ = {'z': lj, 'val': cutting_force * (self._shaft_steps[idx+1]['k'] - self._shaft_steps[idx]['k'])}
                self._cutting_force_gains[f'Q{idx+1}'] = deltaQ
                # Add the increments of bending moments and shear forces to the remaining forces
                self._all_loads = {}
                for loads in (self._updated_forces, self._moment_gains, self._cutting_force_gains): self._all_loads.update(loads)
                self._all_loads = OrderedDict(sorted(self._all_loads.items(), key=lambda x: x[1]['z']))
                # Calculate the function ψ(z) (psi) - the integral of the bending moment, 
                # and Φ(z) (phi) - the double integral of the bending moment (but without integration constants)
                psi = np.array([self._psi_at_z(self._all_loads, z)  for z in self._z_values])
                phi = np.array([(self._phi_at_z(self._all_loads, z)) for z in self._z_values])
            # Calculate the angle θ(z) (theta) and the deflection curve f(z)
            # First, calculate the integration constants
            self.constants = self._calculate_integration_constants()
            C = self.constants['C']
            D = self.constants['D']
            # Add the integration constants to ψ(z) and Φ(z) - to obtain the integral and the double integral
            integral = psi + C
            double_integral = np.array([phi_at_z + C * z * 0.001 + D for z, phi_at_z in zip(self._z_values, phi)])
            self.deflection_angle = integral / EI
            self.deflection_arrow =  double_integral / EI * 1000
            ## Calculate the minimum diameters with respect to the angle θ(z) (theta) and the deflection curve f(z)
            self.d_min_by_permissible_deflection_angle = (64 / (np.pi * E * teta_dop) * np.sqrt(integral**2))**(1 / 4) * 1000
            self.d_min_by_permissible_deflection_arrow = [] 
            for z, di_at_z in zip(self._z_values, double_integral):
                if LA <= z <= LB:
                    self.d_min_by_permissible_deflection_arrow.append((64 / (np.pi * E * f_dop * 0.001) * np.sqrt(di_at_z**2))**(1 / 4) * 1000)
                else:
                    self.d_min_by_permissible_deflection_arrow.append(0)
        else:
            self.d_min_by_permissible_deflection_angle = None
            self.d_min_by_permissible_deflection_arrow = None
        
    def get_shaft_functions(self):
        functions = {
            'Mg': ('Mg(z)', 'Moment gnący Mg [Nm]', 'red', self.bending_moment),
            'Ms': ('Ms(z)', 'Moment skręcający Ms [Nm]', 'green', self.torque),
            'Mz': ('Mz(z)', 'Moment zastępczy Mz [Nm]', 'blue', self.equivalent_moment), 
            'dMz': ('d(Mz)', 'Średnica minimalna ze względu na moment zastępczy dMz [mm]', 'red', self.d_min_by_equivalent_stress),
            'dMs': ('d(Ms)', 'Średnica minimalna ze względu na moment skręcający dMs [mm]', 'green', self.d_min_by_torsional_strength),
            'dqdop': ('d(φ\')', 'Średnica minimalna ze względu na dopuszczalny kąt skręcenia dq\' [mm]', 'blue', self.d_min_by_permissible_angle_of_twist),
            'dkdop': ('d(θdop)', 'Średnica minimalna ze względu na dopuszczalny kąt ugięcia [mm]', 'purple', self.d_min_by_permissible_deflection_angle), 
            'dfdop': ('d(fdop)', 'Średnica minimalna ze względu na dopuszczalną stzrałkę ugięcia [mm]', 'orange', self.d_min_by_permissible_deflection_arrow)}
        
        return functions

    def get_shaft_z(self):
        return self._z_values

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
