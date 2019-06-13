import matlab as ml
import numpy as np


# Run the following statement in your matlab session:
# matlab.engine.shareEngine()
class MatlabEnv():
    def __init__(self):
        self.eng = ml.engine.connect_matlab()
        self.eng.workspace['connected'] = 1
        print('Connected to matlab engine. Check for the connected-variable in matlab.')


    def __getitem__(self, key):
        values = np.asarray(self.eng.workspace[key])
        if values.shape[1] == 2:
            return values[:,1],values[:,0]
        return values

    def __setitem__(self, key, value):
        self.eng.workspace[key] = ml.double([value])

    def run_simulink(self, name, t_end):
        print('Running Simulink Model \'' + name + '\'')
        self.eng.sim(name, ml.double([t_end]))

    def get_value(self, name):
        return np.float(eng.workspace[name])



