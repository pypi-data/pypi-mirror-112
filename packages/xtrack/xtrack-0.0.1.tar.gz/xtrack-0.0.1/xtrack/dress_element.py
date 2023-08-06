import xobjects as xo
from .particles import ParticlesData, gen_local_particle_api
from .dress import dress
from .general import _pkg_root

def dress_element(XoElementData):

    DressedElement = dress(XoElementData)
    assert XoElementData.__name__.endswith('Data')
    name = XoElementData.__name__[:-4]

    DressedElement.track_kernel_source = ('''
            /*gpukern*/
            '''
            f'void {name}_track_particles(\n'
            f'               {name}Data el,\n'
'''
                             ParticlesData particles){
            LocalParticle lpart;
            int64_t part_id = 0;                    //only_for_context cpu_serial cpu_openmp
            int64_t part_id = blockDim.x * blockIdx.x + threadIdx.x; //only_for_context cuda
            int64_t part_id = get_global_id(0);                    //only_for_context opencl

            int64_t n_part = ParticlesData_get_num_particles(particles);
            if (part_id<n_part){
                Particles_to_LocalParticle(particles, &lpart, part_id);
                if (check_is_not_lost(&lpart)>0){
'''
            f'      {name}_track_local_particle(el, &lpart);\n'
'''
                }
                if (check_is_not_lost(&lpart)>0){
                        increment_at_element(&lpart);
                }
            }
        }
''')
    DressedElement._track_kernel_name = f'{name}_track_particles'
    DressedElement.track_kernel_description = {DressedElement._track_kernel_name:
        xo.Kernel(args=[xo.Arg(XoElementData, name='el'),
                        xo.Arg(ParticlesData, name='particles')])}
    DressedElement.iscollective = False

    def compile_track_kernel(self, save_source_as=None):
        context = self._buffer.context

        context.add_kernels(sources=[
                gen_local_particle_api(),
                _pkg_root.joinpath("tracker_src/tracker.h")]
                + self.XoStruct.extra_sources
                + [self.track_kernel_source],
            kernels=self.track_kernel_description,
            save_source_as=save_source_as)


    def track(self, particles):

        if not hasattr(self, '_track_kernel'):
            context = self._buffer.context
            if self._track_kernel_name not in context.kernels.keys():
                self.compile_track_kernel()
            self._track_kernel = context.kernels[self._track_kernel_name]

        self._track_kernel.description.n_threads = particles.num_particles
        self._track_kernel(el=self._xobject, particles=particles)

    DressedElement.compile_track_kernel = compile_track_kernel
    DressedElement.track = track

    return DressedElement


class MetaBeamElement(type):

    def __new__(cls, name, bases, data):
        XoStruct_name = name+'Data'
        if '_xofields' in data.keys():
            xofields = data['_xofields']
        else:
            for bb in bases:
                if hasattr(bb,'_xofields'):
                    xofields = bb._xofields
                    break
        XoStruct = type(XoStruct_name, (xo.Struct,), xofields)

        bases = (dress_element(XoStruct),) + bases

        return type.__new__(cls, name, bases, data)

class BeamElement(metaclass=MetaBeamElement):
    _xofields={}
