import panel as pn
import os
import sys
import numpy as np
import bokeh

from bokeh.layouts import column, row, Spacer
from bokeh.models import CustomJS, Slider, RadioButtonGroup, TextInput, Button, MultiChoice
from bokeh.models import BoxAnnotation, PreText, Range1d, LinearAxis, Span, HoverTool, DataTable, TableColumn
from bokeh.events import SelectionGeometry
from bokeh.plotting import ColumnDataSource, figure, show

import notebook_testing as nt

from tclean_options import TCleanOptionsBaseClass

class TCleanPanel(TCleanOptionsBaseClass):
    
    def __init__(self, terminal=False):
        self.terminal = terminal

        self.standard = nt.Test_standard()
        self.standard.setUp()

        self.standard.read_configuration('config/tclean.yaml')
        
        # Image

        self.file_widget = pn.widgets.FileSelector(os.getcwd() + '/../', name="File Selector")
        self.file_widget.param.watch(self.update, 'value')
        
        self.imsize_widget = pn.Param(
            self.standard.param.imsize, 
            widgets={
                'imsize': pn.widgets.LiteralInput
        })
        
        self.npixels_widget = pn.Param(
            self.standard.param.npixels, 
            widgets={
                'npixel': pn.widgets.IntInput
        })

        # Analysis

        self.cell_widget = pn.Param(
            self.standard.param.cell, 
            widgets={
                'cell': pn.widgets.TextInput
        })
        
        self.specmode_widget = pn.Param(
            TCleanOptionsBaseClass.param.specmode, 
            widgets={
                'specmode': {'widget_type': pn.widgets.Select, 'options':['mfs', 'cube', 'cubedata']}
        })

        self.interpolation_widget = pn.Param(
            self.standard.param.interpolation, 
            widgets={
                'Interpolation': {'widget_type': pn.widgets.Select, 'options': ['nearest', 'linear', 'cubic']}
        })

        self.start_widget = pn.Param(
            TCleanOptionsBaseClass.param.start, 
            widgets={
                'start': pn.widgets.TextInput
        })
        
        self.width_widget = pn.Param(
            TCleanOptionsBaseClass.param.width, 
            widgets={
                'width': pn.widgets.TextInput
        })

        self.pblimit_widget = pn.Param(
            TCleanOptionsBaseClass.param.pblimit, 
            widgets={
                'pblimit': pn.widgets.FloatInput
        })

        self.deconvolver_widget = pn.Param(
            self.standard.param.deconvolver, 
            widgets={
                'deconvolver': {'widget_type': pn.widgets.Select, 'options': ['hogbom', 'clark', 'multiscale', 'mtmfs', 'mem', 'clarkstokes']}
        })


        self.scales_widget = pn.Param(
            self.standard.param.scales, 
            widgets={
                'scales': {'widget_type': pn.widgets.LiteralInput, 'type':  list}
        })


        # Iteration

        self.nchan_widget = pn.Param(
            self.standard.param.nchan, 
            widgets={
                'nchan': pn.widgets.IntSlider
            })

        self.terminal_widget = pn.widgets.Terminal(
            "CASA TClean Terminal Experience\n\n",
            options={"cursorBlink": True},
            height=500, width=1000,
            name='Terminal'
        )
        
        sys.stdout = self.terminal_widget

        self.interactive_widget = pn.widgets.Toggle(
            name="Interactive", 
            button_type='primary'
        )
        
        self.interactive_widget.param.watch(self.set_interactive, 'value')

        # ------------------------------------ #
    
        self.play_button = pn.widgets.Button(
            name="Play", 
            button_type="success",  
            width=300
        )  
        
        self.play_button.on_click(self.clean)
    
    
        simple_controls = pn.Column(
            self.imsize_widget,
            self.cell_widget,
            self.specmode_widget,
            self.nchan_widget,
            self.interactive_widget,
            self.scales_widget,
            self.play_button
        )
        
        advanced_controls = pn.Column(
            self.play_button)
    
        if self.terminal is True:
            self.layout = pn.Column(
                self.file_widget, 
                pn.Tabs(('Simple', simple_controls), ('Advanced', advanced_controls)),
                self.terminal_widget,
            )
            self.layout.show()
        else:
            self.layout = pn.Row(
            pn.Column(
                pn.Card(
                    self.file_widget, 
                    width=800, 
                    header_background = '#21618C',
                    header_color = 'white', 
                    title='File Selector'),
                pn.Card( 
                    pn.Tabs(
                        ('Simple', simple_controls), 
                        ('Advanced', advanced_controls)), 
                    width=800,
                    header_background=' #21618C',
                    header_color = 'white', 
                    title='TClean Controls'
                ),
                pn.Card(
                    self.terminal_widget, 
                    width=800, 
                    header_background=' #21618C',
                    header_color = 'white', 
                    title='Terminal')
            )
        )
    
    def update(self, event):
            self.vis = self.file_widget.value[0]

    def clean(self, event):
        self.standard.test_standard_cube()
    
    def set_interactive(self, event):
            if self.interactive_widget.value is True:
                self.interactive = 1
            elif self.interactive_widget.value is False:
                self.interactive = 0
            else:
                pass
        