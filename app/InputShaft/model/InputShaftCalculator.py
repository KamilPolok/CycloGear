import numpy as np
from sympy import symbols, Piecewise

class InputShaftCalculator():
    def calculate_initial_functions(self, data):
        self._data = data
        # Extract necessary data from the model
        L, LA, LB, L1 = self._data['L'][0], self._data['LA'][0], self._data['LB'][0], self._data['L1'][0]
        x, e, B = self._data['x'][0], self._data['e'][0], self._data['B'][0]
        F, Mwe = self._data['F'][0], self._data['Mwe'][0]
        Zgo, Zsj, G = self._data['Materiał']['Zgo'][0], self._data['Materiał']['Zsj'][0], self._data['Materiał']['G'][0],
        xz, qdop = self._data['xz'][0], self._data['qdop'][0]

        # Calculate coordinate of second cyclo disc
        L2 = L1 + B + x

        # Calculate support reactions
        Rb = (F * (L2 - L1)) / (LB - LA) # Pin support
        Ra = Rb                   # Roller support

       # Create Force and reaction list
        FVals = [0, Ra, F, F, Rb, L]

        # Create z arguments for chart data
        key_points = [LA, L1, L2, LB]
        z = symbols('z')
        zVals = np.union1d(key_points, np.linspace(0, L, 400))

        # Calculate bending moment Mg [Nm]
        Mg0_A = 0          
        MgA_1 = Ra * (z - LA) * 0.001 
        Mg1_2 = (Ra * (z - LA) - F * (z - L1)) * 0.001
        Mg2_B = (Ra * (z - LA) - F * (z - L1) + F * (z - L2)) * 0.001
        MgB_K = 0

        MgFunction = Piecewise(
            (Mg0_A, z <= LA),
            (MgA_1, z <= L1),
            (Mg1_2, z <= L2),
            (Mg2_B, z <= LB),
            (MgB_K, z <= L)
        )
        Mg = np.array([round(float(MgFunction.subs(z, val).evalf()), 2) for val in zVals])

        # Calculate torque Ms
        MsFunction = Piecewise(
            (0, z < L1),
            (Mwe, z <= L),
            
        )
        Ms = np.array([round(float(MsFunction.subs(z, val).evalf()), 2) for val in zVals])
        # Calculate equivalent bending moment Mz
        reductionFactor = 2 * np.sqrt(3)
        Mz = np.sqrt(np.power(Mg, 2) + np.power(reductionFactor / 2 * Ms, 2))
        Mz = np.array([round(float(val), 2) for val in Mz])
        # Calculate minimal shaft diameter d - based on equivalent stress condition
        kgo = Zgo / xz * 1000000
        dMz = np.power(32 * Mz / (np.pi * kgo), 1/3) * 1000
        dMz = np.array([round(float(val), 2) for val in dMz])

        # Calculate minimal shaft diameter d - based on torsional strength condition
        ksj = Zsj / xz * 1000000
        dMs = np.sqrt(16 * Ms / (np.pi * ksj)) * 1000
        dMs = np.array([round(float(val), 2) for val in dMs])

        # Calculate minimal shaft diameter d - based allowable angle of twist condition
        dqdop = np.sqrt(32 * Ms / (np.pi * G * 1000000 * qdop)) * 1000
        dqdop = np.array([round(float(val), 2) for val in dqdop])

        # Save the calculated parameters
        self._data['L2'][0] = L2
        self._data['dsc'][0] = max(dMz + dMs)
        self._data['dec'][0] = self._data['dsc'][0] + 2 * e
        self._data['Ra'][0] = Ra
        self._data['Rb'][0] = Rb

        # Set shaft designer data for visualization
        return  {
            'z': zVals, 
            'F': FVals,
            'Mg': Mg, 
            'Ms': Ms,
            'Mz': Mz,
            'dMz': dMz,
            'dMs': dMs,
            'dqdop': dqdop,
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

