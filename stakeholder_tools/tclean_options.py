import yaml
import param

class TCleanOptionsBaseClass(param.Parameterized):
    vis = param.String(default="E2E6.1.00034.S_tclean.ms", doc="Measurement file.") 
    imagename = param.String(default="test", doc="Name stub of output file.") 
    imsize = param.Integer(512, bounds=(0, None))
    cell = param.String(default="12.0arcsec", doc="Cell size") 
    specmode = param.String(default="cube", doc="Specmode") 
    interpolation = param.String(default="nearest", doc="") 
    nchan = param.Integer(5, bounds=(1, 5000))
    start = param.String(default="1.0GHz", doc="") 
    width = param.String(default="0.2GHz", doc="") 
    pblimit = param.Number(-0.00001)
    deconvolver = param.String(default="hogbom", doc="") 
    niter = param.Integer(5000, bounds=(1, None))
    cyclefactor = param.Integer(2, bounds=(1, 50))
    scales = param.ListSelector(default=[0, 3, 10], objects=[0, 3, 5, 7, 9, 10], precedence=0.5)
    interactive = param.Integer(0, doc="Interactive mode")
    
    def read_configuration(self)->None:
        with open('config/tclean.yaml') as file:
            config = yaml.full_load(file)
        
            self.vis = config['tclean']['vis']
            self.imagename = config['tclean']['imagename']
            self.imsize = config['tclean']['imsize']
            self.cell = config['tclean']['cell']
            self.specmode = config['tclean']['specmode']
            self.interpolation = config['tclean']['interpolation']
            self.nchan = config['tclean']['nchan']
            self.start = config['tclean']['start']
            self.width = config['tclean']['width']
            self.pblimit = config['tclean']['pblimit']
            self.deconvolver = config['tclean']['deconvolver']
            self.niter = config['tclean']['niter']
            self.cyclefactor = config['tclean']['cyclefactor']
            self.scales = config['tclean']['scales']
            self.interactive = config['tclean']['interactive']

