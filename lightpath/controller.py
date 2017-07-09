####################
# Standard Library #
####################
import inspect
import logging

####################
#    Third Party   #
####################
from happi import Client

####################
#     Package      #
####################
from .errors import PathError

class LightController:
    """
    Controller for the LCLS Lightpath


    Attributes
    ----------
    paths
    devices
    device_types
    """
    conn = None

    def __init__(self, host=None, port=None):

        #Connect to Happi Database
        self.conn    = Client(host=host, port=port)
        self.paths   = []
        
        #Load devices and beamlines
        raw = [d for d in self.conn.search({}, as_dict=True)]
#               if d.get('lightpath', False)]

        devices = []

        #Temporary Data Structure before instantiating paths
        beamlines = dict.fromkeys(set([d.beamline
                                        for d in devices]),
                                        {'parents'  : list(),
                                         'beampath' : None})

        #Create segemnted paths
        for line in beamlines.keys():
            beamlines[line]['beampath'] = BeamPath([d
                                                    for d in devices
                                                    if d.beamline==line],
                                                    name=line)
        #Map branches together
        #TODO catch bad branches
        for (line, branches) in [(d.beamline, d.branching)
                                  for d in devices
                                  if d.branching]:
            for branch in branches:
                try:
                    beamlines[branch]['branches'].append(line)

                except KeyError:
                    raise PathError('No beamline found with name '
                                    '{}'.format(branch))

        #Create joined beampaths
        for line, info in beamlines.items():

            path = info['beampath']
            if info.get('parents'):
                for source in info['parents']:
                    path.join(beamlines[source]['beampath'])

            #Make accessible
            self.paths[line] = path
            setattr(self, line, path)

        #Organize devices
        self.devices = list(set([d for p in self.paths for d in p.devices]))


    @property
    def destinations(self):
        """
        Current beam destinations
        """
        d = set([p.impediment for p in self.paths if p.impediment])

        if not d:
            return None

        else:
            return d


    def find_device(self, **kwargs):
        """
        Find a device along the beamline

        If multiple devices are found, only the one is returned.

        Parameters
        ----------
        kwargs :
            Search the database for a device by giving key, value pairs


        Returns
        -------
        device:
            A device of type or subtype :class:`.LightDevice`


        Raises
        ------
        SearchError
            If no device is found that meets the specifications

        See Also
        --------
        :meth:`.happi.Client.load_device`
        """
        device = self.conn.load_device(*args, **kwargs)

        if not device.beamline:
            return None

        #Search in path for object instantiated in BeamPath
        path = self.paths[device.beamline]

        return path._device_lookup(device.base)


    def path_to(self, **kwargs):
        """
        Create a BeamPath from the source to the requested device

        Parameters
        ----------
        kwargs :
            Search the database for a device by giving key, value pairs

        Raises
        ------
        SearchError
            If the device is not found 

        See Also
        --------
        :meth:`.LightController.find_device`
        """
        device = self.find_device(**kwargs)

        prior, after = self.paths[device.beamline].split(device)

        return prior
