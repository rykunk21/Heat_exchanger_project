"""


"""
import math
import random
import csv
from operator import itemgetter


class Fluid:
    def __init__(self, name, density, temperature, specific_heat,
                 kinematic_viscosity, thermal_conductivity, prandtl):
        self.name = name
        self.density = density
        self.temperature = temperature
        self.specific_heat = specific_heat
        self.kinematic_viscosity = kinematic_viscosity
        self.thermal_conductivity = thermal_conductivity
        self.prandtl = prandtl
        self.tubular = None


class Pipe:
    def __init__(self, pipe_type, nominal_size, length):
        self.pipe_type = pipe_type
        self.ODiameter = float(pipe_diameter(pipe_type, nominal_size, True)['Outer'])
        self.IDiameter = float(pipe_diameter(pipe_type, nominal_size, True)['Inner'])
        self.length = length

    def __str__(self):
        return '\n'.join([self.ODiameter, self.IDiameter, self.length])


class AnnularPipe(Pipe):
    def __init__(self, pipe_type, direction, length, tubular_OD=None):
        super().__init__(pipe_type, direction, length)
        IDP = float(self.IDiameter)
        if tubular_OD:
            ODP = float(tubular_OD)
            self.flow_area = (math.pi * (((IDP /12) ** 2)-((ODP /12) ** 2))) / 4


class TubularPipe(Pipe):
    def __init__(self, pipe_type, length, direction):
        super().__init__(pipe_type, length, direction)
        IDP = self.IDiameter
        self.flow_area = (math.pi * (float(IDP) / 12) ** 2) / 4


class Exchanger:
    def __init__(self, hot_fluid, cold_fluid, tubular, annular,
                 exchanger_type, tubular_nominal, annular_nominal):
        self.tubular_nominal = tubular_nominal
        self.annular_nominal = annular_nominal
        # init fluid in exchanger
        self.hot_flow = flow_rate('Hot')
        self.cold_flow = flow_rate('Cold')
        self.hot_fluid = hot_fluid
        self.cold_fluid = cold_fluid

        # init pipe in exchanger
        self.tubular = tubular
        self.annular = annular
        self.exchanger_type = exchanger_type

        # variables to change
        self.hot_fluid.outlet_temp = None
        self.cold_fluid.outlet_temp = None

        # init flow area depending on which side has higher flow_area
        if self.tubular.flow_area > self.annular.flow_area:
            if self.hot_flow >= self.cold_flow:
                self.hot_fluid.tubular = True
                self.cold_fluid.tubular = False

                self.hot_fluid.velocity = self.hot_flow / (
                        self.hot_fluid.density * self.tubular.flow_area)
                self.cold_fluid.velocity = self.cold_flow / (
                        self.cold_fluid.density * self.annular.flow_area)

            elif self.hot_flow < self.cold_flow:
                self.hot_fluid.tubular = False
                self.cold_fluid.tubular = True

                self.hot_fluid.velocity = self.hot_flow / (
                        self.hot_fluid.density * self.annular.flow_area)
                self.cold_fluid.velocity = self.cold_flow / (
                        self.cold_fluid.density * self.tubular.flow_area)

        elif self.tubular.flow_area < self.annular.flow_area:
            if self.hot_flow >= self.cold_flow:
                self.hot_fluid.tubular = False
                self.cold_fluid.tubular = True

                self.hot_fluid.velocity = self.hot_flow / (
                        self.hot_fluid.density * self.annular.flow_area)
                self.cold_fluid.velocity = self.cold_flow / (
                        self.cold_fluid.density * self.tubular.flow_area)
            elif self.hot_flow < self.cold_flow:
                self.hot_fluid.tubular = True
                self.cold_fluid.tubular = False

                self.hot_fluid.velocity = self.hot_flow / (
                        self.hot_fluid.density * self.tubular.flow_area)
                self.cold_fluid.velocity = self.cold_flow / (
                        self.cold_fluid.density * self.annular.flow_area)

        # coefficients
        self.annulus_equivilant_diameter = (((annular.IDiameter / 12) ** 2)-((tubular.ODiameter / 12) ** 2)) / (tubular.ODiameter / 12)
        self.r = (self.cold_flow * self.cold_fluid.specific_heat) / (self.hot_flow * self.hot_fluid.specific_heat)

        if self.hot_fluid.tubular:
            self.tubular.reynold = (self.hot_fluid.velocity * (self.tubular.IDiameter / 12)) / self.hot_fluid.kinematic_viscosity
            self.annular.reynold = (self.cold_fluid.velocity * self.annulus_equivilant_diameter) / self.cold_fluid.kinematic_viscosity
            self.tubular.nusselt = .023 * (self.tubular.reynold ** (4/5)) * (self.hot_fluid.prandtl ** .3)
            self.annular.nusselt = .023 * (self.annular.reynold ** (4/5)) * (self.cold_fluid.prandtl ** .4)
            self.tubular.convection = self.tubular.nusselt * self.hot_fluid.thermal_conductivity / (self.tubular.ODiameter / 12)
            self.annular.convection = self.annular.nusselt * self.cold_fluid.thermal_conductivity / self.annulus_equivilant_diameter
        else:
            self.tubular.reynold = self.cold_fluid.velocity * (self.tubular.IDiameter / 12) / self.cold_fluid.kinematic_viscosity
            self.annular.reynold = self.hot_fluid.velocity * self.annulus_equivilant_diameter / self.hot_fluid.kinematic_viscosity
            self.tubular.nusselt = .023 * (self.tubular.reynold ** (4 / 5)) * (self.cold_fluid.prandtl ** .3)
            self.annular.nusselt = .023 * (self.annular.reynold ** (4 / 5)) * (self.hot_fluid.prandtl ** .4)
            self.tubular.convection = self.tubular.nusselt * self.cold_fluid.thermal_conductivity / (self.tubular.ODiameter / 12)
            self.annular.convection = self.annular.nusselt * self.hot_fluid.thermal_conductivity / self.annulus_equivilant_diameter


        self.exchanger_coefficient = 1 / ((1/self.tubular.convection)+(1/self.annular.convection))
        self.total_flow = math.pi * (self.tubular.ODiameter / 12) * self.tubular.length

        self.e_counter = math.e ** ((self.exchanger_coefficient * self.total_flow * (self.r - 1)) / ((self.cold_flow * 60 *60) * self.cold_fluid.specific_heat))
        self.e_para = math.e ** ((self.exchanger_coefficient * self.total_flow * (self.r + 1)) / ((self.cold_flow * 60 * 60) * self.cold_fluid.specific_heat))


    def read_fluid(self):
        print('Hot Density:', self.hot_fluid.density)
        print('Cold Density:', self.cold_fluid.density)

    def start(self):
        T = self.hot_fluid.temperature
        t = self.cold_fluid.temperature

        if self.exchanger_type.lower() == 'counterflow':
            e = self.e_counter
            # check which side which fluid is on

            self.hot_fluid.outlet_temp = (T * (self.r - 1) - self.r * t * (1 - e)) / ((self.r * e) - 1)

            self.cold_fluid.outlet_temp = t + ((T - self.hot_fluid.outlet_temp) / self.r)
        elif self.exchanger_type.lower() == 'parallel':
            e = self.e_para

            self.hot_fluid.outlet_temp = (((self.r + e) * T) + (self.r * t) * (e - 1)) / ((self.r + 1) * e)
            self.cold_fluid.outlet_temp = t + ((T - self.hot_fluid.outlet_temp) / self.r)

    def outlet_temps(self):
        return self.hot_fluid.outlet_temp, self.cold_fluid.outlet_temp

    def __str__(self):
        attributes = [
            'Hot Fluid',
            'Hot in Tubular',
            'Hot Flowrate',
            'Hot Velocity',
            'Cold Fluid',
            'Cold Flowrate',
            'Cold Velocity',
            'Annular OPD',
            'Annular IPD',
            'Tubular OPD',
            'Tubular IPD',
            'Annular Nominal',
            'Tubular Nominal',
            'Annular Type',
            'Tubular Type',
            'Pipe Length',
            'Type'
        ]

        values = [
            self.hot_fluid.name,
            self.hot_fluid.tubular,
            self.hot_flow,
            round(self.hot_fluid.velocity, 2),
            self.cold_fluid.name,
            self.cold_flow,
            round(self.cold_fluid.velocity, 2),
            self.annular.ODiameter,
            self.annular.IDiameter,
            self.tubular.ODiameter,
            self.tubular.IDiameter,
            self.tubular_nominal,
            self.annular_nominal,
            self.tubular.pipe_type,
            self.annular.pipe_type,
            self.annular.length,
            self.exchanger_type,

        ]
        out = '=' * 24
        out += '\n{:^24}'.format('EXCHANGER STATS')
        for i, entry in enumerate(attributes):
            if values[i] == self.hot_fluid.tubular:
                if self.hot_fluid.tubular == '1':
                    out += '\n{:<14}: {:<10}'.format(attributes[i], True)
                    continue
                else:
                    out += '\n{:<14}: {:<10}'.format(attributes[i], False)
                    continue
            out += '\n{:<14}: {:<10}'.format(attributes[i], values[i])

        out += '\n\n{:^24}'.format('OUTLET TEMPERATURES')
        out += '\n{:<14}: {:<10}'.format('Hot',
                                         round(self.hot_fluid.outlet_temp, 4))
        out += '\n{:<14}: {:<10}'.format('Cold',
                                         round(self.cold_fluid.outlet_temp, 4))
        out += '\n'
        out += '=' * 24

        return out

    def __repr__(self):
        attributes = [
            'Hot Fluid',
            'Hot in Tubular',
            'Hot Flowrate',
            'Hot Velocity',
            'Cold Fluid',
            'Cold Flowrate',
            'Cold Velocity',
            'Annular OPD',
            'Annular IPD',
            'Tubular OPD',
            'Tubular IPD',
            'Annular Nominal',
            'Tubular Nominal',
            'Annular Type',
            'Tubular Type',
            'Pipe Length',
            'Type'
        ]

        values = [
            self.hot_fluid.name,
            self.hot_fluid.tubular,
            self.hot_flow,
            round(self.hot_fluid.velocity, 2),
            self.cold_fluid.name,
            self.cold_flow,
            round(self.cold_fluid.velocity, 2),
            self.annular.ODiameter,
            self.annular.IDiameter,
            self.tubular.ODiameter,
            self.tubular.IDiameter,
            self.tubular_nominal,
            self.annular_nominal,
            self.tubular.pipe_type,
            self.annular.pipe_type,
            self.annular.length,
            self.exchanger_type,

        ]
        out = '=' * 24
        out += '\n{:^24}'.format('EXCHANGER STATS')
        for i, entry in enumerate(attributes):
            if values[i] == self.hot_fluid.tubular:
                if self.hot_fluid.tubular == 1:
                    values[i] = True
                else:
                    values[i] = False
            out += '\n{:<14}: {:<10}'.format(attributes[i], values[i])

        out += '\n\n{:^24}'.format('OUTLET TEMPERATURES')
        out += '\n{:<14}: {:<10}'.format('Hot',
                                         round(self.hot_fluid.outlet_temp, 4))
        out += '\n{:<14}: {:<10}'.format('Cold',
                                         round(self.cold_fluid.outlet_temp, 4))
        out += '\n'
        out += '=' * 24

        return out


def flow_rate(side):
    # these values are in different units
    if side.lower() == 'hot':
        return .3055
    elif side.lower() == 'cold':
        return 1.388


def pipe_diameter(pipe_type, nominal_size, bool):
    """
    choose the pipe diameter by type

    :param type: str()
    :param value: str()
    :return: float()
    """
    data = dict()
    pipe = None
    with open('pipe_sizes.csv', 'r') as fp:
        lines = csv.reader(fp)
        for line in lines:
            if line[0] == '\ufeffType K':   # too lazy to decode for this check
                pipe = 'K'
                continue
            elif line[0] == 'Type M':
                pipe = 'M'
                continue
            elif line[0] == 'Type L':
                pipe = 'L'
                continue
            else:
                if pipe in data.keys():
                    data[pipe].update({
                        line[0].strip(): {
                            'Outer': line[1],
                            'Inner': line[2]
                        }
                    })
                else:
                    data[pipe] = {
                        line[0].strip(): {
                            'Outer': line[1],
                            'Inner': line[2]
                        }
                    }

    if bool:
        return data[pipe_type][nominal_size]
    else:
        return data


def build_exchanger(pipe_sizes, design, pipe_length):
    annular_type = pipe_sizes['Annular']['Type']
    annular_size = pipe_sizes['Annular']['Size']
    tubular_type = pipe_sizes['Tubular']['Type']
    tubular_size = pipe_sizes['Tubular']['Size']

    cold = Fluid('Water', 61.8, 68, .9988, 10.83e-6, .345, 7.02)
    hot = Fluid('Exhaust', .03144, 380, .481, 2.61e-4, 0.01902, 1.03)
    tubular = TubularPipe(tubular_type, tubular_size, pipe_length)
    annular = AnnularPipe(annular_type, annular_size, pipe_length, tubular.ODiameter)
    exchanger = Exchanger(hot, cold, tubular, annular, design, tubular_size, annular_size)
    return exchanger


def build_data(data, i, exchanger):
    # 120 < exchanger.hot_fluid.outlet_temp < 130 and
    if exchanger.hot_fluid.outlet_temp > exchanger.cold_fluid.outlet_temp:
        data[i] = exchanger
        return data
    else:
        return data


def main():
    PROMPT = 'OPTIONS\n[1] Build All Possible Exchangers and display top performance\n------>'
    exchanger_compare = {}
    data = pipe_diameter(None, None, False)
    option = input(PROMPT)
    exchanger_number = 1
    if option == '1':
        for i in range(12, 50):
            length = i
            exhanger_designs = ['counterflow', 'parallel']

            for design in exhanger_designs:
                for first_key, first_value in data.items():
                    tubular_type = first_key
                    for first_size in first_value:
                        tubular_size = first_size
                        for second_key, second_value in data.items():
                            annular_type = second_key
                            for second_size in second_value:
                                annular_size = second_size
                                tubular_test = tubular_size.replace(' ', '+')
                                annular_test = annular_size.replace(' ', '+')
                                if eval(annular_test) <= eval(tubular_test):
                                    continue
                                else:
                                    pipe_sizes = {
                                        'Annular': {
                                            'Type': annular_type,
                                            'Size': annular_size},
                                        'Tubular': {
                                            'Type': tubular_type,
                                            'Size': tubular_size}
                                    }
                                    exchanger = build_exchanger(pipe_sizes, design, length)
                                    exchanger.start()
                                    exchanger_compare = build_data(exchanger_compare, exchanger_number, exchanger)
                                    print(exchanger)
                                    print(exchanger_number)
                                    exchanger_number += 1

    data = sorted(exchanger_compare.items(), key=lambda t: t[1].hot_fluid.outlet_temp,
                 reverse=False)

    for i in range(10):
        print(data[i])


if __name__ == '__main__':
    main()

