
class Bunch:
    def __init__(self,npart):
        self.x=np.zeros(npart);
        self.y=np.zeros(npart);
        self.px=np.zeros(npart);
        self.py=np.zeros(npart);
        self.z=np.zeros(npart);
        self.delta=np.zeros(npart);
        self.weigth=np.zeros(npart);


class Particles(xo.Struct):
    x=xo.Double[:]
    y=xo.Double[:]
    px=xo.Double[:]
    py=xo.Double[:]
    z=xo.Double[:]
    delta=xo.Double[:]








