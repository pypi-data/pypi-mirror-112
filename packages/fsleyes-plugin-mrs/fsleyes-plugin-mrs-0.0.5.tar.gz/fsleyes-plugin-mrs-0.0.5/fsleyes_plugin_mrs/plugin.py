#!/usr/bin/env python
#
# plugin.py - The fsleyes MRS plugin.
#
# Author: Will Clarke <william.clarke@ndcn.ox.ac.uk>
#

import logging
import json
import os.path as op
import re

import numpy as np
from numpy import fft
import wx

from fsleyes.views.powerspectrumpanel import PowerSpectrumPanel
import fsleyes.controls.controlpanel as ctrlpanel
import fsleyes.actions as actions
import fsleyes.controls.powerspectrumcontrolpanel as pscontrol
import fsleyes.profiles.shortcuts as fsleyes_shortcuts
import fsleyes_props as props
import fsl.data.image as fslimage
import fsleyes.plotting.powerspectrumseries as psseries
import fsl.utils.cache as cache
from fsleyes.layouts import BUILT_IN_LAYOUTS

# Imports for MRSToolBar
from fsleyes.controls import plottoolbar
import fsleyes.icons as icons
import fsleyes.tooltips as tooltips

from fsleyes.views.orthopanel import OrthoPanel

from .mrsviewprofile import MRSViewProfile

icon_dir = op.join(op.dirname(__file__), 'icons')
log = logging.getLogger(__name__)


class MRSToolBar(plottoolbar.PlotToolBar):
    """The ``MRSToolBar`` is a toolbar for use with a
    :class:`.MRSView`. It extends :class:`.PlotToolBar`
    mostly replicates :class:`.PowerSpectrumToolBar`
    and adds a few controls specific to the :class:`.PoweSpectrumPanel`.
    """

    @staticmethod
    def title():
        """Overrides :meth:`.ControlMixin.title`. Returns a title to be used
        in FSLeyes menus.
        """
        return 'MRS toolbar'

    @staticmethod
    def supportedViews():
        """Overrides :meth:`.ControlMixin.supportedViews`. The
        ``MRSToolBar`` is only intended to be added to
        :class:`.MRSView` views.
        """
        return [MRSView]

    def __init__(self, parent, overlayList, displayCtx, psPanel):
        """Create a ``MRSToolBar``.

        :arg parent:      The :mod:`wx` parent object.
        :arg overlayList: The :class:`.OverlayList` instance.
        :arg displayCtx:  The :class:`.DisplayContext` instance.
        :arg psPanel:     The :class:`.PowerSpectrumPanel` instance.
        """

        plottoolbar.PlotToolBar.__init__(
            self, parent, overlayList, displayCtx, psPanel)

        self.togControl = actions.ToggleControlPanelAction(
            overlayList, displayCtx, psPanel, MRSControlPanel)
        self.togDimControl = actions.ToggleControlPanelAction(
            overlayList, displayCtx, psPanel, MRSDimControl)

        togControl = actions.ToggleActionButton(
            'togControl',
            actionKwargs={'floatPane': True},
            icon=[icons.findImageFile('spannerHighlight24'),
                  icons.findImageFile('spanner24')],
            tooltip='Show/hide the MRS control panel.')

        togDimControl = actions.ToggleActionButton(
            'togDimControl',
            icon=[op.join(icon_dir, 'nifti_mrs_icon-mrs_icon_highlight_thumb24.png'),
                  op.join(icon_dir, 'nifti_mrs_icon-mrs_icon_thumb24.png')],
            tooltip='Show/hide the NIfTI-MRS dimension control panel.')

        togList = actions.ToggleActionButton(
            'PlotListPanel',
            actionKwargs={'floatPane': True},
            icon=[icons.findImageFile('listHighlight24'),
                  icons.findImageFile('list24')],
            tooltip=tooltips.actions[psPanel, 'PlotListPanel'])

        togControl = props.buildGUI(self, self, togControl)
        togDimControl = props.buildGUI(self, self, togDimControl)
        togList = props.buildGUI(self, psPanel, togList)

        self.InsertTools([togControl, togDimControl, togList], 0)

        nav = [togControl, togDimControl, togList] + self.getCommonNavOrder()

        self.setNavOrder(nav)


class MRSControlPanel(pscontrol.PowerSpectrumControlPanel):
    """Control panel for the MRS view. Identical to the
    PowerSpectrumControlPanel, but defined so it can be given a distinct name.
    """

    @staticmethod
    def title():
        """Overrides :meth:`.ControlMixin.title`. Returns a title to be used
        in FSLeyes menus.
        """
        return 'MRS control panel'

    @staticmethod
    def supportedViews():
        """Overrides :meth:`.ControlMixin.supportedViews`. The
        ``MRSControlPanel`` is only intended to be added to
        :class:`.MRSView` views.
        """
        return [MRSView]


class MRSDimControl(ctrlpanel.SettingsPanel):
    """Control panel for the MRS view. Controls access to higher dimensions
    of a NIFTI MRS image.
    """

    @staticmethod
    def title():
        """Overrides :meth:`.ControlMixin.title`. Returns a title to be used
        in FSLeyes menus.
        """
        return 'MRS Dimension control'

    @staticmethod
    def defaultLayout():
        """Overrides :meth:`.ControlMixin.defaultLayout`. Returns arguments
        to be passed to :meth:`.ViewPanel.defaultLayout`.
        """
        return {'location': wx.RIGHT}

    @staticmethod
    def supportedViews():
        """Overrides :meth:`.ControlMixin.supportedViews`. The
        ``MRSDimControl`` is only intended to be added to
        :class:`.MRSView` views.
        """
        return [MRSView]

    def __init__(self, parent, overlayList, displayCtx, plotPanel):
        """Create a ``MRSDimControl``.

        :arg parent:      The :mod:`wx` parent object.
        :arg overlayList: The :class:`.OverlayList` instance.
        :arg displayCtx:  The :class:`.DisplayContext` instance.
        :arg psPanel:     The :class:`.PowerSpectrumPanel` instance.
        """
        super().__init__(parent, overlayList, displayCtx, plotPanel)

        self.__plotPanel = plotPanel

        displayCtx.addListener('selectedOverlay',
                               self.name,
                               self.__selectedOverlayChanged)
        overlayList.addListener('overlays',
                                self.name,
                                self.__selectedOverlayChanged)

        self.__selectedOverlay = None
        self.__selectedOverlayChanged()

    def destroy(self):
        """Must be called when this ``MRSDimControl`` is no
        longer needed. calls the
        :meth:`.PlotControlPanel.destroy` method.
        """
        self.displayCtx.removeListener('selectedOverlay', self.name)
        self.overlayList.removeListener('overlays', self.name)
        ctrlpanel.SettingsPanel.destroy(self)

    def generateDataSeriesWidgets(self, ds, groupName, dims):
        '''Create the required higher dimension spinner widgets in
        the dimension control pannel.'''

        widgetList = self.getWidgetList()

        widgets_out = []
        if dims > 4:
            dim5 = props.makeWidget(
                widgetList,
                ds,
                'dim_5',
                slider=True,
                showLimits=False)
            widgetList.AddWidget(
                dim5,
                displayName='DIM 5',
                tooltip="DIM 5 index",
                groupName=groupName)
            widgets_out.append(dim5)
        if dims > 5:
            dim6 = props.makeWidget(
                widgetList,
                ds,
                'dim_6',
                slider=True,
                showLimits=False)
            widgetList.AddWidget(
                dim6,
                displayName='DIM 6',
                tooltip="DIM 6 index",
                groupName=groupName)
            widgets_out.append(dim6)
        if dims > 6:
            dim7 = props.makeWidget(
                widgetList,
                ds,
                'dim_7',
                slider=True,
                showLimits=False)
            widgetList.AddWidget(
                dim7,
                displayName='DIM 7',
                tooltip="DIM 7 index",
                groupName=groupName)
            widgets_out.append(dim7)

        return widgets_out

    def refreshDataSeriesWidgets(self):
        '''Enable/disable and set bounds on the dimensions spinners
        appropriate for the shape of the currently selected overlay.
        '''
        widgetList = self.getWidgetList()

        if self.__selectedOverlay is not None:
            self.__selectedOverlay = None

        if widgetList.HasGroup('niftiMRSDimensions'):
            widgetList.RemoveGroup('niftiMRSDimensions')

        overlay = self.displayCtx.getSelectedOverlay()

        if overlay is None:
            return

        ds = self.__plotPanel.getDataSeries(overlay)

        if ds is None:
            return

        self.__selectedOverlay = overlay

        # Update prop limits now to ensure limits exist before
        # widgets are created
        # if isinstance(overlay, fslimage.Nifti) and overlay.ndim > 3:
        for dim in range(5, 8):
            prop = ds.getProp(f'dim_{dim}')
            prop.setAttribute(ds, 'minval', 0)
            if dim <= overlay.ndim:
                prop.setAttribute(ds, 'maxval', overlay.shape[dim - 1] - 1)
            else:
                prop.setAttribute(ds, 'maxval', 0)

        # Add listeners to the properties which will cause a
        # refresh of the Info Pannel.
        for dim in range(5, 8):
            prop = ds.getProp(f'dim_{dim}')
            prop.addListener(
                ds,
                f'dim_{dim}_info_update',
                self._selectedIndexChanged,
                overwrite=True)

        widgetList = self.getWidgetList()

        widgetList.AddGroup(
            'niftiMRSDimensions',
            'NIfTI-MRS Dimensions ')

        dsWidgets = self.generateDataSeriesWidgets(
            ds,
            'niftiMRSDimensions',
            overlay.ndim)

        self.__dsWidgets = dsWidgets

    def refreshInfoPanel(self):
        '''Create / re-create the NIfTI-MRS information panel'''
        widgetList = self.getWidgetList()

        if widgetList.HasGroup('niftiMRSInfo'):
            widgetList.RemoveGroup('niftiMRSInfo')

        overlay = self.displayCtx.getSelectedOverlay()

        if overlay is None:
            return

        ds = self.__plotPanel.getDataSeries(overlay)

        widgetList.AddGroup(
            'niftiMRSInfo',
            'NIfTI-MRS Information ')

        curr_hdr_exts = overlay.header.extensions
        hdr_ext_codes = curr_hdr_exts.get_codes()
        hdr_ext = json.loads(curr_hdr_exts[hdr_ext_codes.index(44)]
                             .get_content())

        def my_static_txt(text):
            st = wx.StaticText(widgetList,
                               label=text,
                               style=wx.ALIGN_LEFT)
            return st

        for dim in range(5, 8):
            if dim <= overlay.ndim:
                tag = hdr_ext[f'dim_{dim}']
                widgetList.AddWidget(
                    my_static_txt(tag),
                    f'dim_{dim} tag',
                    groupName='niftiMRSInfo')

                dim_size = overlay.shape[dim-1]
                widgetList.AddWidget(
                    my_static_txt(f'{dim_size}'),
                    f'dim_{dim} size',
                    groupName='niftiMRSInfo')

                # Optional dim headers
                if f'dim_{dim}_info' in hdr_ext:
                    widgetList.AddWidget(
                        my_static_txt(hdr_ext[f'dim_{dim}_info']),
                        f'dim_{dim}_info',
                        groupName='niftiMRSInfo')

                # Process dynamic header fields
                def interpret_dyn_header(obj, index):
                    if isinstance(obj, dict)\
                            and "Value" in obj:
                        return interpret_dyn_header(obj["Value"], index)
                    elif isinstance(obj, list):
                        return str(obj[index])
                    elif isinstance(obj, dict)\
                            and "start" in obj\
                            and "increment" in obj:
                        return str(obj['start']
                                   + index * obj['increment'])
                    else:
                        raise TypeError('Incorrect type for dynamic header.')

                d_hdr_str = f'dim_{dim}_header'
                if d_hdr_str in hdr_ext:
                    index = getattr(ds, f'dim_{dim}')
                    for key in hdr_ext[d_hdr_str]:
                        dim_hdr_value = interpret_dyn_header(
                            hdr_ext[d_hdr_str][key], index)

                        widgetList.AddWidget(
                            my_static_txt(dim_hdr_value),
                            f'dim_{dim}: {key}',
                            groupName='niftiMRSInfo')

        # Extract Nucleus and SpectrometerFrequency
        nucleus = hdr_ext['ResonantNucleus'][0]
        spec_freq = hdr_ext['SpectrometerFrequency'][0]
        specwidth = 1 / overlay.header['pixdim'][4]

        widgetList.AddWidget(
            my_static_txt(nucleus),
            'Nucleus ',
            groupName='niftiMRSInfo')

        widgetList.AddWidget(
            my_static_txt(f'{spec_freq:0.3f}'),
            'Frequency (MHz) ',
            groupName='niftiMRSInfo')

        widgetList.AddWidget(
            my_static_txt(f'{specwidth:0.0f}'),
            'Spectral width (Hz) ',
            groupName='niftiMRSInfo')

    def _check_nifti_mrs(self):
        '''Check that the overlay selected is a valid NIfTI-MRS overlay'''

        overlay = self.displayCtx.getSelectedOverlay()
        if overlay is None:
            return False

        nifti_mrs_re = re.compile(r'mrs_v\d+_\d+')
        intent_str = overlay.header.get_intent()[2]

        # Check that file is NIfTI-MRS by looking for suitable intent string
        if isinstance(overlay, fslimage.Nifti)\
                and overlay.ndim > 3\
                and nifti_mrs_re.match(intent_str):
            return True
        else:
            return False

    def __selectedOverlayChanged(self, *a):
        """Called when the :attr:`.DisplayContext.selectedOverlay` or
        :class:`.OverlayList` changes.
        """

        # Double check that the selected overlay has
        # changed before refreshing the panel, as it
        # may not have (e.g. new overlay added, but
        # selected overlay stayed the same).
        if self.displayCtx.getSelectedOverlay() is not self.__selectedOverlay\
                and self._check_nifti_mrs():
            self.refreshDataSeriesWidgets()
            self.refreshInfoPanel()

    def _selectedIndexChanged(self, *a):
        """Called when the dimension indices properties are changed.
        """
        self.refreshInfoPanel()


# Add shortcuts to open MRS controls.
# Currently FSLeyes does not have an
# API for this, so we hack the shortcuts
# into the fsleyes.shortcuts module.
fsleyes_shortcuts.actions['MRSView.MRSToolBar'] = 'Ctrl-Alt-3'
fsleyes_shortcuts.actions['MRSView.MRSControlPanel'] = 'Ctrl-Alt-4'
fsleyes_shortcuts.actions['MRSView.MRSDimControl'] = 'Ctrl-Alt-5'


class MRSView(PowerSpectrumPanel):
    """The ``MRSView`` is a FSLeyes view panel for plotting data from MRS
    NIFTI images.
    """

    @staticmethod
    def title():
        """Overrides :meth:`.ViewPanel.title`. Returns a title to be used
        in FSLeyes menus.
        """
        return 'MRS'

    @staticmethod
    def controlOrder():
        """Overrides :meth:`.ViewPanel.controlOrder`. Returns a suggested
        ordering of control panels for the FSLeyes settings menu.
        """
        return ['OverlayListPanel',
                'PlotListPanel',
                'MRSToolBar',
                'MRSControlPanel',
                'MRSDimControl']

    @staticmethod
    def defaultLayout():
        """Overrides :meth:`.ViewPanel.defaultLayout`. Returns a list
        of control panels that should be added by default for new ``MRSView``
        views.
        """

        return ['OverlayListPanel',
                'PlotListPanel',
                'MRSToolBar',
                'MRSDimControl']

    def __init__(self, parent, overlayList, displayCtx, frame):
        """Create a ``MRSView``.

        :arg parent:      The :mod:`wx` parent object.
        :arg overlayList: The :class:`.OverlayList`.
        :arg displayCtx:  The :class:`.DisplayContext`.
        :arg frame:       The :class:`.FSLeyesFrame`.
        """

        PowerSpectrumPanel.__init__(self,
                                    parent,
                                    overlayList,
                                    displayCtx,
                                    frame)

        self.initProfile(MRSViewProfile)

        self._add_annotation_listener()

    def destroy(self):
        """Must be called when this ``MRSView`` is no longer
        needed. Removes some property listeners, and calls
        :meth:`.OverlayPlotPanel.destroy`.
        """

        self.canvas.removeListener('dataSeries', 'mrs_voxel_annotations')
        PowerSpectrumPanel.destroy(self)

    def draw(self, *a):
        """Overrides :meth:`.PlotPanel.draw`. Draws some
        :class:`.PowerSpectrumSeries` using the
        :meth:`.PlotCanvas.drawDataSeries` method.
        """

        if not self or self.destroyed:
            return

        canvas = self.canvas
        pss = self.getDataSeriesToPlot()

        for ps in pss:
            with props.suppress(ps, 'label'):
                ps.label = ps.makeLabel()

        if len(pss) > 0:
            self._set_mrs_plot_scale(pss)

        canvas.drawDataSeries(extraSeries=pss)
        canvas.drawArtists()

    def createDataSeries(self, overlay):
        """Overrides :meth:`.OverlayPlotPanel.createDataSeries`. Creates a
        :class:`.PowerSpectrumSeries` instance for the given overlay.

        Overload the PowerSpectrumPanel definition to allow only complex
        fslimage.Image and implement the multi-dimensional
        ComplexPowerSpectrumSeries class (MDComplexPowerSpectrumSeries).
        """

        displayCtx = self.displayCtx
        overlayList = self.overlayList

        psargs = [overlay, overlayList, displayCtx, self]

        if isinstance(overlay, fslimage.Image) and overlay.ndim > 3:

            if overlay.iscomplex:
                ps = MDComplexPowerSpectrumSeries(*psargs)
            else:
                return None, None, None

            opts = displayCtx.getOpts(overlay)
            targets = [displayCtx, opts]
            propNames = ['location', 'volumeDim']

        else:
            return None, None, None

        ps.colour = self.getOverlayPlotColour(overlay)
        ps.lineStyle = '-'
        ps.lineWidth = 2
        ps.alpha = 1.0

        return ps, targets, propNames

    def _set_mrs_plot_scale(self, pss):
        # Extract NIfTI-MRS header extensions
        hdr_ext = []
        for ps in pss:
            curr_hdr_exts = ps.overlay.header.extensions
            hdr_ext_codes = curr_hdr_exts.get_codes()
            hdr_ext.append(
                json.loads(
                    curr_hdr_exts[hdr_ext_codes.index(44)].get_content()))

        # Extract Nucleus and SpectrometerFrequency
        nuclei = [he['ResonantNucleus'][0] for he in hdr_ext]
        spec_freq = [he['SpectrometerFrequency'][0] for he in hdr_ext]

        all_ps_match = True
        if len(nuclei) > 1:
            for nn in nuclei[1:]:
                if nn != nuclei[0]:
                    all_ps_match = False
        if len(spec_freq) > 1:
            for sf in spec_freq[1:]:
                if not np.isclose(sf, spec_freq[0], atol=1):
                    all_ps_match = False

        canvas = self.canvas
        if all_ps_match and canvas.xAutoScale:
            canvas.xAutoScale = False

            # Calculate and set x scaling
            canvas.xScale = -1 / spec_freq[0]

            # Calculate x offset
            if nuclei[0] == '1H':
                canvas.xOffset = 4.65

            canvas.invertX = True
            if nuclei[0] == '1H':
                new_lim = [5, 0, canvas.limits[2], canvas.limits[3]]
                canvas.limits = new_lim

    def _add_annotation_listener(self):
        pcanvas = self.canvas

        ortho = self.frame.getView(OrthoPanel)
        if len(ortho) == 0:
            log.error('No Ortho panel present')
            return
        else:
            # Assume only 1 ortho panel
            ortho = ortho[0]

        xcanvas = ortho.getXCanvas()
        ycanvas = ortho.getYCanvas()
        zcanvas = ortho.getZCanvas()
        self.dsannotations = {}

        def dataSeriesColourChanged(*a):
            '''Function called to change an annotation colour if
            the dataseries colour is changed.
            '''
            # Argument 0 is the colour changed to,
            # Argument 2 is the dataseries
            colour = a[0]
            edited_ds = a[2]
            for anno in self.dsannotations[edited_ds]:
                anno.colour = colour

            xcanvas.Refresh()
            ycanvas.Refresh()
            zcanvas.Refresh()

        def dataSeriesChanged(*a):
            '''Function called to add annotations on addition of a dataseries'''
            # remove annotation for any newly removed data series
            for ds in self.dsannotations:
                if ds not in pcanvas.dataSeries:
                    xa, ya, za = self.dsannotations.pop(ds)
                    xcanvas.getAnnotations().dequeue(xa, hold=True)
                    ycanvas.getAnnotations().dequeue(ya, hold=True)
                    zcanvas.getAnnotations().dequeue(za, hold=True)

                    # 2. Remove listener for colour changes
                    ds.removeListener('colour', f'{ds.name}_colour')

                    break  # To avoid changing the dictionary size during iteration.

            # create an annotation for any newly added data series
            for ds in pcanvas.dataSeries:
                if ds not in self.dsannotations:
                    # 1. Add annotation to ortho canvases
                    xpos, ypos, zpos = self.displayCtx.location
                    xa = xcanvas.getAnnotations().ellipse(ypos, zpos, 2, 2, colour=ds.colour, hold=True)
                    ya = ycanvas.getAnnotations().ellipse(xpos, zpos, 2, 2, colour=ds.colour, hold=True)
                    za = zcanvas.getAnnotations().ellipse(xpos, ypos, 2, 2, colour=ds.colour, hold=True)
                    self.dsannotations[ds] = [xa, ya, za]

                    # 2. Add listener for colour changes
                    ds.addListener('colour', f'{ds.name}_colour', dataSeriesColourChanged, weak=False)

            xcanvas.Refresh()
            ycanvas.Refresh()
            zcanvas.Refresh()

        # Add listener for new dataseries
        pcanvas.addListener('dataSeries', 'mrs_voxel_annotations', dataSeriesChanged, weak=False)


class MDComplexPowerSpectrumSeries(psseries.ComplexPowerSpectrumSeries):
    '''Sub class of ComplexPowerSpectrumSeries to overload the
       dataAtCurrentVoxel method'''

    dim_5 = props.Int(default=0, clamped=True)
    dim_6 = props.Int(default=0, clamped=True)
    dim_7 = props.Int(default=0, clamped=True)
    """Higher order dimension indicies. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Needs it's own cache or a hack around the name mangling
        self.__cache = cache.Cache(maxsize=1000)

    # The PlotPanel uses a new thread to access
    # data every time the displaycontext location
    # changes. So we mark this method as mutually
    # exclusive to prevent multiple
    # near-simultaneous accesses to the same voxel
    # location. The first time that a voxel location
    # is accessed, its data is cached. So when
    # subsequent (blocked) accesses execute, they
    # will hit the cache instead of hitting the disk
    # (which is a good thing).
    # @idle.mutex
    def dataAtCurrentVoxel(self):
        """Returns the data for the current voxel of the overlay.  This method
        is intended to be used within the :meth:`DataSeries.getData` method
        of sub-classes.

        An internal cache is used to avoid the need to retrieve data for the
        same voxel multiple times, as retrieving data from large compressed
        4D images can be time consuming.

        The location for the current voxel is calculated by the
        :meth:`currentVoxelLocation` method, and the data lookup is performed
        by the :meth:`currentVoxelData` method. These methods may be
        overridden by sub-classes.

        :returns: A ``numpy`` array containing the data at the current
                  voxel, or ``None`` if the current location is out of bounds
                  of the image.
        """

        location = self.currentVoxelLocation(with_time_dim=False)

        if location is None:
            return None

        data = self.__cache.get(location, None)

        if data is None:
            data = self.currentVoxelData(self.currentVoxelLocation())
            self.__cache.put(location, data)

        return data

    def currentVoxelLocation(self, with_time_dim=True):
        """Used by :meth:`dataAtCurrentVoxel`. Returns the current voxel
        location. This is used as a key for the voxel data cache implemented
        within the :meth:`dataAtCurrentVoxel` method, and subsequently passed
        to the :meth:`currentVoxelData` method.

        This implements the higher dimension indexing

        If with_time_dim is True (default) then a slice(None) is inserted as
        a fourth dimension.
        """

        opts = self.displayCtx.getOpts(self.overlay)
        vdim = slice(None)
        voxel = opts.getVoxel()

        if voxel is None:
            return None

        x, y, z = voxel

        if with_time_dim:
            return (x, y, z, vdim, self.dim_5, self.dim_6, self.dim_7)
        else:
            return (x, y, z, self.dim_5, self.dim_6, self.dim_7)

    def currentVoxelData(self, location):
        """Used by :meth:`dataAtCurrentVoxel`. Returns the data at the
        specified location.

        This method may be overridden by sub-classes.
        """
        data = self.overlay[location].copy()
        data = calcSpectrum(data)

        return data


def calcSpectrum(data):
    """Calculates a spectrum for the given one-dimensional data array.
    Includes scaling of first FID point.

    :arg data:    Numpy array containing the time series data

    :returns:     The complex spectrum is returned.
    """

    # Fourier transform on complex data
    data[0] *= 0.5
    data = fft.fft(data)
    data = fft.fftshift(data)

    return data


###############################
# Define a default mrs layout #
###############################

# Abuse the layouts to embed an MRS view by default
BUILT_IN_LAYOUTS.update({'mrs': 'fsleyes.views.orthopanel.OrthoPanel,fsleyes_plugin_mrs.plugin.MRSView\nlayout2|name=OrthoPanel 1;caption=Ortho View 1;state=67377088;dir=5;layer=0;row=0;pos=0;prop=100000;bestw=-1;besth=-1;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|name=MRSView 2;caption=MRS view 2;state=67377148;dir=2;layer=0;row=1;pos=0;prop=100000;bestw=1296;besth=262;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|dock_size(5,0,0)=22|dock_size(2,0,1)=648|\nfsleyes.controls.orthotoolbar.OrthoToolBar,fsleyes.controls.overlaydisplaytoolbar.OverlayDisplayToolBar,fsleyes.controls.overlaylistpanel.OverlayListPanel,fsleyes.controls.locationpanel.LocationPanel;syncLocation=True,syncOverlayOrder=True,syncOverlayDisplay=True,syncOverlayVolume=True,movieRate=400,movieAxis=3;showCursor=True,bgColour=#000000ff,fgColour=#ffffffff,cursorColour=#00ff00ff,cursorGap=False,showColourBar=False,colourBarLocation=top,colourBarLabelSide=top-left,showXCanvas=True,showYCanvas=True,showZCanvas=True,showLabels=True,labelSize=12,layout=grid,xzoom=100.0,yzoom=100.0,zzoom=100.0,highDpi=False\nlayout2|name=Panel;caption=;state=768;dir=5;layer=0;row=0;pos=0;prop=100000;bestw=-1;besth=-1;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|name=OrthoToolBar;caption=Ortho view toolbar;state=67382012;dir=1;layer=10;row=0;pos=0;prop=100000;bestw=607;besth=35;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|name=OverlayDisplayToolBar;caption=Display toolbar;state=67382012;dir=1;layer=11;row=0;pos=0;prop=100000;bestw=922;besth=49;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|name=OverlayListPanel;caption=Overlay list;state=67373052;dir=3;layer=0;row=0;pos=0;prop=100000;bestw=201;besth=84;minw=1;minh=1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=201;floath=100;notebookid=-1;transparent=255|name=LocationPanel;caption=Location;state=67373052;dir=3;layer=0;row=0;pos=1;prop=100000;bestw=383;besth=111;minw=1;minh=1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=383;floath=127;notebookid=-1;transparent=255|dock_size(5,0,0)=22|dock_size(3,0,0)=139|dock_size(1,10,0)=37|dock_size(1,11,0)=51|\nfsleyes_plugin_mrs.plugin.MRSToolBar,fsleyes_plugin_mrs.plugin.MRSDimControl,fsleyes.controls.overlaylistpanel.OverlayListPanel,fsleyes.controls.plotlistpanel.PlotListPanel;;\nlayout2|name=FigureCanvasWxAgg;caption=;state=768;dir=5;layer=0;row=0;pos=0;prop=100000;bestw=640;besth=480;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|name=MRSToolBar;caption=MRS toolbar;state=67382012;dir=1;layer=10;row=0;pos=0;prop=100000;bestw=272;besth=34;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|name=MRSDimControl;caption=NIfTI-MRS;state=67373052;dir=2;layer=0;row=0;pos=0;prop=100000;bestw=188;besth=144;minw=1;minh=1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=188;floath=160;notebookid=-1;transparent=255|name=OverlayListPanel;caption=Overlay list;state=67373052;dir=2;layer=0;row=0;pos=1;prop=100000;bestw=201;besth=52;minw=1;minh=1;maxw=-1;maxh=-1;floatx=1194;floaty=492;floatw=201;floath=68;notebookid=-1;transparent=255|name=PlotListPanel;caption=Plot list;state=67373052;dir=2;layer=0;row=0;pos=2;prop=100000;bestw=201;besth=52;minw=1;minh=1;maxw=-1;maxh=-1;floatx=1212;floaty=692;floatw=201;floath=68;notebookid=-1;transparent=255|dock_size(5,0,0)=642|dock_size(1,10,0)=36|dock_size(2,0,0)=260|'}) # noqa
