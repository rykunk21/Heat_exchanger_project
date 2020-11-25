"""


"""


class Fluid:
    def __init__(self, density):
        self.density = density


class Pipe:
    pass


class Exchanger:
    def __init__(self, fluid_args, pipe_args, exchanger_args):
        self.hot = Fluid(args)
        self.cold = Fluid(args)
        self.ODP = Pipe(args)  # outer pipe diameter
        self.IDP = Pipe(args)  # inner pipe diameter
        a_null =  # calculate pipe area
        self.nusselt =  # attain from fluid properties
        self.exchanger =  # attain from fluid properties

    def read_outlet_temp(self):
        pass


design1 = Exchanger()

print(design1.hot.density)
