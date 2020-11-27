"""


"""
import math
import random


class Fluid:
    def __init__(self, name, temperature, specific_heat, kinematic_viscosity,
                 thermal_conductivity, prandtl):
        self.name = name
        self.temperature = temperature
        self.specific_heat = specific_heat
        self.kinematic_viscosity = kinematic_viscosity
        self.thermal_conductivity = thermal_conductivity
        self.prandtl = prandtl


class Pipe:
    def __init__(self, type, length):
        self.ODiameter = pipe_diameter(type, 'ODiameter')
        self.IDiameter = pipe_diameter(type, 'IDiameter')
        self.length = length


class AnnularPipe(Pipe):
    def __init__(self, type, length, tubular_OD=None):
        super().__init__(type, length)
        IDP = self.IDiameter
        if tubular_OD:
            ODP = tubular_OD
            self.flow_area = (math.pi * ((IDP ** 2)-(ODP ** 2))) / 4


class TubularPipe(Pipe):
    def __init__(self, type, length):
        super().__init__(type, length)
        IDP = self.IDiameter
        self.flow_area = (math.pi * (IDP ** 2)) / 4


class Exchanger:     # todo: automatically route fluid to annular or tubular
    """
    T2 =  T * (R - 1) - R * t * (1 - e)
         -----------------------------------
                    ((R * e) - 1)

    """
    def __init__(self, hot_fluid, cold_fluid, tubular, annular,
                 exchanger_type):
        # init fluid in exchanger
        self.hot_flow = flow_rate('Hot')
        self.cold_flow = flow_rate('Cold')
        self.hot_fluid = hot_fluid
        self.cold_fluid = cold_fluid

        # init pipe in exchanger
        self.tubular = tubular
        self.annular = annular
        self.type = exchanger_type

        # init convection based on pipe and fluid
        self.hot_convection = convection('Hot')  # todo finish convection
        self.cold_convection = convection('Cold')

        # variables to change
        self.hot_fluid.outlet_temp = None
        self.cold_fluid.outlet_temp = None
        self.hot_fluid.velocity = None
        self.cold_fluid.velocity = None

        # coefficients
        self.r = None
        self.exchanger_coefficient = None

    def read_fluid(self):
        print('Hot Density:', self.hot_fluid.density)
        print('Cold Density:', self.cold_fluid.density)

    def start(self):
        T = self.hot_fluid.temperature
        t = self.cold_fluid.temperature
        e = self.exchanger_coefficient


    def outlet_temps(self):
        print(self.hot_fluid.outlet_temp)
        print(self.cold_fluid.outlet_temp)

    def __str__(self):
        attributes = [
            'Hot Fluid',
            'Hot Flowrate',
            'Cold Fluid',
            'Cold Flowrate',
            'OPD',
            'IPD',
            'Pipe Length',
            'Type'
        ]

        values = [
            self.hot_fluid.name,
            self.hot_flow,
            self.cold_fluid.name,
            self.cold_flow,
            self.annular.ODiameter,
            self.annular.IDiameter,
            self.tubular.ODiameter,
            self.tubular.IDiameter,
            self.annular.length,
            self.type
        ]

        return '\n\n{:^15}{:^15}\n=============================\n' \
               '{:<15}: {:<15}\n{:<15}: {:<15}\n{:<15}: {:<15}\n' \
               '{:<15}: {:<15}\n{:<15}: {:<15}\n{:<15}: {:<15}\n' \
               '{:<15}: {:<15}\n{:<15}: {:<15}'.format(
                'Attribute', 'Value',
                attributes[0], values[0], attributes[1], values[1],
                attributes[2], values[2], attributes[3], values[3],
                attributes[4], values[4], attributes[5], values[5],
                attributes[6], values[6], attributes[7], values[7],
                )


def flow_rate(side):    # todo: can we make this better?
    if side.lower() == 'hot':
        return 30000
    elif side.lower() == 'cold':
        return 5000


def convection(side):  # todo
    return 1


def pipe_diameter(type, value):
    """
    choose the pipe diameter by type

    :param type: str()
    :param value: str()
    :return: float()
    """


    pipes = {'ODiameter':
                {'M': .1146},
             'IDiameter':
                {'M': .1076}
             }
    return pipes[value][type]


def nusselt():
    pass


def build_exchanger():
    hot = Fluid('Water', 'Hot Density', None, None, None, None)
    cold = Fluid('Ethanol', 'Cold Density', None, None, None, None)
    pipe_length = 24
    tubular = TubularPipe('M', pipe_length)
    annular = AnnularPipe('M', pipe_length, tubular.ODiameter)
    exchanger = Exchanger(hot, cold, tubular, annular, 'Counterflow')
    return exchanger


def build_data(iterations):
    data = dict()
    for i in range(iterations):
        exchanger = build_exchanger()
        exchanger.start()
        data[i] = [exchanger.hot_fluid.outlet_temp, exchanger.hot_fluid.name,
                   exchanger.cold_fluid.name, exchanger.tubular.IDiameter,
                   exchanger.annular.ODiameter]

    return data


def main():

    exchanger = build_exchanger()
    print(exchanger)


if __name__ == '__main__':
    main()
