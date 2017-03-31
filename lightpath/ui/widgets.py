"""
Definitions for Lightpath Widgets
"""
############
# Standard #
############
import copy
import logging

###############
# Third Party #
###############
import pedl
from pedl.choices import ColorChoice, AlignmentChoice
from pedl.widgets import Rectangle, StaticText, MessageButton

##########
# Module #
##########

logger = logging.getLogger(__name__)


class LightWidget(pedl.StackedLayout):
    """
    Generic Widget for LightDevice
    """
    #Default Widget sizes
    shape_size   = (30,  30)
    button_size  = (30,  15)
    label_size   = (100, 10)
    frame_margin = 10
    control_drop = 10 

    def __init__(self, prefix, name, **kwargs):
        super().__init__(name=name,
                         alignment = AlignmentChoice.Center,
                         **kwargs)

        #Store PV prefix
        self.prefix = prefix

        
        #Create central layout
        l = pedl.VBoxLayout(spacing=self.control_drop,
                            alignment=AlignmentChoice.Center)
        l.addWidget(self.label)
        l.addWidget(self.shape)
        l.addLayout(self.control)
        
        #Add background MPS frame
        self.addWidget(self.frame(l))

        #Add to stack
        self.addLayout(l)


    @property
    def shape(self):
        """
        Basic widget shape
        """
        r = Rectangle(w=self.shape_size[0],
                      h=self.shape_size[1],
                      fill=ColorChoice.Green,
                      lineWidth=3)
        return r

    @property
    def label(self):
        """
        Label for device
        """
        l = StaticText(text=self.name,
                       w=self.label_size[0],
                       h=self.label_size[1],
                       font = pedl.Font(size=12),
                       alignment=AlignmentChoice.Center)
        return l


    def frame(self, lay):
        """
        Frame for MPS alert
        """
        r = Rectangle(w=lay.w+self.frame_margin,
                      h=lay.h+self.frame_margin,
                      lineColor=ColorChoice.Red,
                      lineWidth=3)
        return r

    @property
    def control(self):
        """
        Control box for insert / remove control
        """
        #Button layout
        l    = pedl.VBoxLayout(spacing=1)

        #Create buttons
        _in  = MessageButton(w=self.button_size[0],
                             h=self.button_size[1])
        _out = MessageButton(w=self.button_size[0],
                             h=self.button_size[1])
        #Add to layout
        l.addWidget(_in)
        l.addWidget(_out)
        return l



class PipeWidget(pedl.StackedLayout):

    width  = 100
    height = 20

    def __init__(self, index, **kwargs):
        super().__init__(**kwargs)
        #Store index of beampipe
        self.index = index

        #Draw layered beampipes 
        self.addWidget(self.empty)
        self.addWidget(self.full)


    @property
    def beampipe(self):
        """
        Basic beampipe to be reimplemented by different states
        """
        r = Rectangle(w=self.width, h=self.height,
                      lineColor=ColorChoice.Black,
                      lineWidth=2)
        return r


    @property
    def empty(self):
        """
        Empty beampipe
        """
        r = self.beampipe
        r.fill = ColorChoice.Grey
        return r


    @property
    def full(self):
        """
        Beampipe when beam is present
        """
        r = self.beampipe
        r.fill = ColorChoice.Cyan
        return r
