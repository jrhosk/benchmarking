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
        #pn.extension(sizing_mode='stretch_width')
        self.terminal = terminal

        self.standard = nt.Test_standard()
        self.standard.setUp()

        self.standard.read_configuration('config/tclean.yaml')
        
        self.file_widget = pn.widgets.FileSelector(os.getcwd(), name="File Selector")
        self.file_widget.param.watch(self.update, 'value')
        
        imsize_widget = pn.Param(
            self.standard.param.imsize, 
            widgets={
                'imsize': pn.widgets.LiteralInput
            })
        
        cell_widget = pn.Param(
            self.standard.param.cell, 
            widgets={
                'cell': pn.widgets.TextInput
            })
        
        specmode_widget = pn.Param(
            self.standard.param.specmode, 
            widgets={
                'specmode': pn.widgets.TextInput
            })
        
        nchan_widget = pn.Param(
            self.standard.param.nchan, 
            widgets={
                'nchan': pn.widgets.IntSlider
            })
        
        interactive_widget = pn.Param(
            self.standard.param.interactive, 
            widgets={
                'interactive': pn.widgets.IntInput
            })

        self.terminal_widget = pn.widgets.Terminal(
            "CASA TClean Terminal Experience\n\n",
            options={"cursorBlink": True},
            height=500, width=1000,
            name='Terminal'
        )
        
        sys.stdout = self.terminal_widget

        # ------------------------------------ #
    
        self.play_button = pn.widgets.Button(
            name="Play", 
            button_type="success",  
            margin=(5,1,5,1), 
            sizing_mode='stretch_width') 
        
        self.play_button.on_click(self.clean)
    
    
        simple_controls = pn.Column(
            imsize_widget,
            cell_widget,
            specmode_widget,
            nchan_widget,
            interactive_widget,
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
            self.layout = pn.Column(
                pn.Accordion(self.file_widget),
                pn.Accordion( 
                    ("TClean", pn.Tabs(('Simple', simple_controls), ('Advanced', advanced_controls)))
                ),
                pn.Accordion(self.terminal_widget),
            )
    
    def update(self, event):
            self.vis = self.file_widget.value[0]

    def clean(self, event):
        self.standard.test_standard_cube()
        