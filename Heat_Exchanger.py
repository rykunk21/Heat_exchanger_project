"""


"""
import math
import random
import csv


class Fluid:
    def __init__(self, name, density, temperature, specific_heat, kinematic_viscosity,
                 thermal_conductivity, prandtl):
        self.name = name
        self.density = density
        self.temperature = temperature
        self.specific_heat = specific_heat
        self.kinematic_viscosity = kinematic_viscosity
        self.thermal_conductivity = thermal_conductivity
        self.prandtl = prandtl


class Pipe:
    def __init__(self, pipe_type, direction, length):
        self.ODiameter = pipe_diameter(pipe_type, direction)
        self.IDiameter = pipe_diameter(pipe_type, direction)
        self.length = length


class AnnularPipe(Pipe):
    def __init__(self, pipe_type, direction, length, tubular_OD=None):
        super().__init__(pipe_type, direction, length)
        # IDP = self.IDiameter
        IDP = .1674         # todo: elim hard code
        if tubular_OD:      # todo: fucking watch this its gonna throw an error
            ODP = tubular_OD
            self.flow_area = (math.pi * ((IDP ** 2)-(ODP ** 2))) / 4


class TubularPipe(Pipe):
    def __init__(self, pipe_type, length, direction):
        super().__init__(pipe_type, length, direction)
        IDP = self.IDiameter
        self.flow_area = (math.pi * (IDP ** 2)) / 4


class Exchanger:
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

        # init flow area depending on which side has higher flow_area
        if self.tubular.flow_area > self.annular.flow_area:
            if self.hot_flow >= self.cold_flow:
                self.hot_fluid.velocity = self.hot_flow / (
                        self.hot_fluid.density * self.tubular.flow_area)
                self.cold_fluid.velocity = self.cold_flow / (
                        self.cold_fluid.density * self.annular.flow_area)
            elif self.hot_flow < self.cold_flow:
                self.hot_fluid.velocity = self.hot_flow / (
                        self.hot_fluid.density * self.annular.flow_area)
                self.cold_fluid.velocity = self.cold_flow / (
                        self.cold_fluid.density * self.tubular.flow_area)

        elif self.tubular.flow_area < self.annular.flow_area:
            if self.hot_flow >= self.cold_flow:
                self.hot_fluid.velocity = self.hot_flow / (
                        self.hot_fluid.density * self.annular.flow_area)
                self.cold_fluid.velocity = self.cold_flow / (
                        self.cold_fluid.density * self.tubular.flow_area)
            elif self.hot_flow < self.cold_flow:
                self.hot_fluid.velocity = self.hot_flow / (
                        self.hot_fluid.density * self.tubular.flow_area)
                self.cold_fluid.velocity = self.cold_flow / (
                        self.cold_fluid.density * self.annular.flow_area)
        else:
            print('yea bro idk')

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
    # these values are in different units
    if side.lower() == 'hot':
        return 1.38
    elif side.lower() == 'cold':
        return 5000


def convection(side):  # todo
    return 1


def pipe_diameter(pipe_type, direction):
    """
    choose the pipe diameter by type

    :param type: str()
    :param value: str()
    :return: float()
    """
    if direction == 'Annular':
        pass
    elif direction == 'Tubular':
        pass

    with open('pipe_sizes.csv', 'r') as fp:
        lines = csv.reader(fp)

    for line in lines:
        print(line)


    pipes = {'ODiameter':
                {'M': .1146},
             'IDiameter':
                {'M': .1076}
             }


def build_exchanger():
    hot = Fluid('Water', 61.8, 'Hot Density', None, None, None, None)
    cold = Fluid('Ethanol', 68, 'Cold Density', None, None, None, None)
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
    print(exchanger.hot_fluid.velocity)


if __name__ == '__main__':
    main()
