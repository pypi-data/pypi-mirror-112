# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2015-2020 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

"""
Base class for tomography acquisition (defined by Bliss)
"""

__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "27/11/2020"

import h5py

try:
    import hdf5plugin
except ImportError:
    pass
from nxtomomill.plugins import get_plugins_positioners_resources
from silx.io.url import DataUrl
from nxtomomill.io.config import HDF5Config
from silx.io.utils import h5py_read_dataset
from tomoscan.unitsystem import metricsystem
from tomoscan.io import HDF5File
from silx.utils.enum import Enum as _Enum
from collections import OrderedDict
import numpy
import typing
import logging
import contextlib

_logger = logging.getLogger(__name__)


class _BaseReader(contextlib.AbstractContextManager):
    def __init__(self, url: DataUrl):
        if not isinstance(url, DataUrl):
            raise TypeError("url should be an instance of DataUrl")
        if url.scheme() not in ("silx", "h5py"):
            raise ValueError("Valid scheme are silx and h5py")
        if url.data_slice() is not None:
            raise ValueError(
                "Data slices are not managed. Data path should "
                "point to a bliss node (h5py.Group)"
            )
        self._url = url
        self._file_handler = None

    def __exit__(self, *exc):
        return self._file_handler.close()


class EntryReader(_BaseReader):
    """Context manager used to read a bliss node"""

    def __enter__(self):
        self._file_handler = HDF5File(filename=self._url.file_path(), mode="r")
        entry = self._file_handler[self._url.data_path()]
        if not isinstance(entry, h5py.Group):
            raise ValueError("Data path should point to a bliss node (h5py.Group)")
        return entry


class DatasetReader(_BaseReader):
    """Context manager used to read a bliss node"""

    def __enter__(self):
        self._file_handler = HDF5File(filename=self._url.file_path(), mode="r")
        entry = self._file_handler[self._url.data_path()]
        if not isinstance(entry, h5py.Dataset):
            raise ValueError("Data path should point to a dtaset (h5py.Dataset)")
        return entry


class BaseAcquisition:
    """
    Util class to group several hdf5 group together and to write the data
    Nexus / NXtomo compliant
    """

    _SCAN_NUMBER_PATH = "measurement/scan_numbers"

    _ENERGY_PATH = "technique/scan/energy"

    _NAME_PATH = "technique/scan/name"

    _GRP_SIZE_PATH = "technique/scan/nb_scans"

    _SAMPLE_NAME_PATH = "sample/name"

    _FOV_PATH = "technique/scan/field_of_view"

    _TOMO_N_PATH = "technique/scan/tomo_n"

    _START_TIME_PATH = "start_time"

    _END_TIME_PATH = "end_time"

    def __init__(
        self,
        root_url: typing.Union[DataUrl, None],
        configuration: HDF5Config,
        detector_sel_callback,
    ):
        self._root_url = root_url
        self._detector_sel_callback = detector_sel_callback
        self._registered_entries = OrderedDict()
        self._copy_frames = OrderedDict()
        # key is the entry, value his type
        self._entries_o_path = dict()
        # key is the entry, value his the entry path from the original file.
        # this value is different from `.name`. Don't know if this is a bug ?
        """user can have defined already some parameter values as energy.
        The idea is to avoid asking him if """
        self._plugins = []
        self._plugins_pos_resources = {}
        self._configuration = configuration

    @property
    def configuration(self):
        return self._configuration

    @property
    def raise_error_if_issue(self):
        """
        Should we raise an error if we encounter or an issue or should we
        just log an error message
        """
        return self.configuration.raises_error

    @property
    def is_xrd_ct(self):
        """Is this an XRD-CT acquisition"""
        raise NotImplementedError("Base class")

    @property
    def require_x_translation(self):
        """is `x_translation` expected"""
        raise NotImplementedError("Base class")

    @property
    def require_z_translation(self):
        """is `z_translation` expected"""
        raise NotImplementedError("Base class")

    @property
    def has_diode(self):
        """is the acquisition expect to have a diode (instead of an energy
        field)"""
        raise NotImplementedError("Base class")

    @property
    def root_url(self):
        return self._root_url

    def read_entry(self):
        return EntryReader(self._root_url)

    def is_different_sequence(self, entry):
        """
        Can we have several entries 1.1, 1.2, 1.3... to consider.
        This is the case for XRD-CT where 1.1, 1.2, 1.3 should be consider as
        being part of the same sequence. Not for 'standard tomography'
        """
        raise ValueError("Base class")

    @staticmethod
    def _get_node_values_for_frame_array(
        node: h5py.Group,
        n_frame: int,
        keys: typing.Iterable,
        info_retrieve,
        expected_unit,
    ):
        def get_values():
            # this is a two step process: first step we parse all the
            # the keys until we found one with the expected length
            # if first iteration fails then we return the first existing key
            for respect_length in (True, False):
                for possible_key in keys:
                    if possible_key in node and isinstance(
                        node[possible_key], h5py.Dataset
                    ):
                        values_ = h5py_read_dataset(node[possible_key])
                        unit_ = BaseAcquisition._get_unit(
                            node[possible_key], default_unit=expected_unit
                        )
                        # skip values containing '*DIS*'
                        if isinstance(values_, str) and values_ == "*DIS*":
                            continue

                        if n_frame is not None and respect_length is True:
                            if numpy.isscalar(values_):
                                length = 1
                            else:
                                length = len(values_)
                            if length in (n_frame, n_frame + 1):
                                return values_, unit_
                        else:
                            return values_, unit_
            return None, None

        values, unit = get_values()
        if values is None:
            raise ValueError(
                "Unable to retrieve {info} for {node_name}. Was looking for "
                "{keys} datasets"
                "".format(info=info_retrieve, node_name=node.name, keys=keys)
            )
        elif n_frame is None:
            return values, unit
        elif numpy.isscalar(values):
            return numpy.array([values] * n_frame), unit
        elif len(values) == n_frame:
            return values.tolist(), unit
        elif len(values) == (n_frame + 1):
            # for now we can have one extra position for rotation,
            # x_translation...
            # because saved after the last projection. It is recording the
            # motor position. For example in this case: 1 is the motor movement
            # (saved) and 2 is the acquisition
            #
            #  1     2    1    2     1
            #      -----     -----
            # -----     -----     -----
            #
            return values[:-1].tolist(), unit
        else:
            raise ValueError("incoherent number of angle position vs number of frame")

    def register_step(self, url: DataUrl, entry_type, copy_frames) -> None:
        """
        Add a bliss entry to the acquisition
        :param url:
        :param entry_type:
        """
        raise NotImplementedError("Base class")

    @staticmethod
    def _get_unit(node: h5py.Dataset, default_unit):
        """Simple process to retrieve unit from an attribute"""
        if "unit" in node.attrs:
            return node.attrs["unit"]
        elif "units" in node.attrs:
            return node.attrs["units"]
        else:
            _logger.info(
                "no unit found for %s, take default unit: %s"
                "" % (node.name, default_unit)
            )
            return default_unit

    @staticmethod
    def _get_instrument_node(entry_node: h5py.Group) -> h5py.Group:
        if not isinstance(entry_node, h5py.Group):
            raise TypeError("entry_node: h5py.group expected")
        return entry_node["instrument"]

    @staticmethod
    def _get_positioners_node(entry_node):
        if not isinstance(entry_node, h5py.Group):
            raise TypeError("entry_node is expected to be a h5py.Group")
        return BaseAcquisition._get_instrument_node(entry_node)["positioners"]

    def _get_rotation_angle(self, root_node, n_frame) -> tuple:
        """return the list of rotation angle for each frame"""
        if not isinstance(root_node, h5py.Group):
            raise TypeError("root_node is expected to be a h5py.Group")

        for grp in self._get_positioners_node(root_node), root_node:
            try:
                angles, unit = self._get_node_values_for_frame_array(
                    node=grp,
                    n_frame=n_frame,
                    keys=self.configuration.rotation_angle_keys,
                    info_retrieve="rotation angle",
                    expected_unit="degree",
                )
            except (ValueError, KeyError):
                pass
            else:
                return angles, unit

        mess = "Unable to find rotation angle for {}" "".format(self.root_url.path())
        if self.raise_error_if_issue:
            raise ValueError(mess)
        else:
            mess += "default value will be set. (0)"
            _logger.warning(mess)
            return [0] * n_frame, "degree"

    def _get_x_translation(self, root_node, n_frame) -> tuple:
        """return the list of translation for each frame"""
        for grp in self._get_positioners_node(root_node), root_node:
            try:
                x_tr, unit = self._get_node_values_for_frame_array(
                    node=grp,
                    n_frame=n_frame,
                    keys=self.configuration.x_trans_keys,
                    info_retrieve="x translation",
                    expected_unit="mm",
                )
                x_tr = (
                    numpy.asarray(x_tr)
                    * metricsystem.MetricSystem.from_value(unit).value
                )
            except (ValueError, KeyError):
                pass
            else:
                return x_tr, "m"

        mess = "Unable to find x translation for {}" "".format(self.root_url.path())
        if self.raise_error_if_issue:
            raise ValueError(mess)
        else:
            mess += "default value will be set. (0)"
            _logger.warning(mess)
            return 0, "m"

    def _get_y_translation(self, root_node, n_frame) -> tuple:
        """return the list of translation for each frame"""
        for grp in self._get_positioners_node(root_node), root_node:
            try:
                y_tr, unit = self._get_node_values_for_frame_array(
                    node=grp,
                    n_frame=n_frame,
                    keys=self.configuration.y_trans_keys,
                    info_retrieve="y translation",
                    expected_unit="mm",
                )
                y_tr = (
                    numpy.asarray(y_tr)
                    * metricsystem.MetricSystem.from_value(unit).value
                )
            except (ValueError, KeyError):
                pass
            else:
                return y_tr, "m"

        mess = "Unable to find y translation for {}" "".format(self.root_url.path())
        if self.raise_error_if_issue:
            raise ValueError(mess)
        else:
            mess += "default value will be set. (0)"
            _logger.warning(mess)
            return 0, "m"

    @staticmethod
    def get_z_translation_frm(root_node, n_frame: int, configuration: HDF5Config):
        for grp in BaseAcquisition._get_positioners_node(root_node), root_node:
            try:
                z_tr, unit = BaseAcquisition._get_node_values_for_frame_array(
                    node=grp,
                    n_frame=n_frame,
                    keys=configuration.z_trans_keys,
                    info_retrieve="z translation",
                    expected_unit="mm",
                )
                z_tr = (
                    numpy.asarray(z_tr)
                    * metricsystem.MetricSystem.from_value(unit).value
                )
            except (ValueError, KeyError):
                pass
            else:
                return z_tr, "m"

        mess = "Unable to find z translation on node {}" "".format(root_node.name)
        if configuration.raises_error:
            raise ValueError(mess)
        else:
            mess += "default value will be set. (0)"
            _logger.warning(mess)
            return 0, "m"

    def _get_z_translation(self, root_node, n_frame) -> tuple:
        """return the list of translation for each frame"""
        return self.get_z_translation_frm(
            root_node=root_node,
            n_frame=n_frame,
            configuration=self.configuration,
        )

    def _get_expo_time(self, root_node, n_frame, detector_node) -> tuple:
        """return expo time for each frame"""
        for grp in detector_node["acq_parameters"], root_node:
            try:
                expo, unit = self._get_node_values_for_frame_array(
                    node=grp,
                    n_frame=n_frame,
                    keys=self.configuration.exposition_time_keys,
                    info_retrieve="exposure time",
                    expected_unit="s",
                )
            except (ValueError, KeyError):
                pass
            else:
                return expo, unit

        mess = "Unable to find frame exposure time on entry {}" "".format(
            self.root_url.path()
        )
        if self.raise_error_if_issue:
            raise ValueError(mess)
        else:
            mess += "default value will be set. (0)"
            _logger.warning(mess)
            return 0, "s"

    def _get_plugin_pos_resource(self, root_node, resource_name, n_frame):
        """Reach a path provided by a plugin. In this case units are not
        managed"""
        for grp in self._get_positioners_node(root_node), root_node:
            try:
                values, _ = self._get_node_values_for_frame_array(
                    node=grp,
                    n_frame=n_frame,
                    keys=(resource_name,),
                    info_retrieve=resource_name,
                    expected_unit=None,
                )
            except (ValueError, KeyError):
                pass
            else:
                return values, None
        mess = "Unable to find {} on entry {}".format(
            resource_name, self.root_url.path()
        )
        if self.raise_error_if_issue:
            raise ValueError(mess)
        else:
            mess += "default value will be set. (0)"
            _logger.warning(mess)
            return 0, None

    def _ignore_sample_output(self, output_dataset_name):
        """Should will ignore management of this dataset. Can be the case
        if managed by a plugin"""
        for plugin in self._plugins:
            if output_dataset_name in plugin.sample_datasets_created:
                return True
        return False

    def _ignore_detector_output(self, output_dataset_name):
        """Should will ignore management of this dataset. Can be the case
        if managed by a plugin"""
        for plugin in self._plugins:
            if output_dataset_name in plugin.detector_datasets_created:
                return True
        return False

    def _ignore_beam_output(self, output_dataset_name):
        """Should will ignore management of this dataset. Can be the case
        if managed by a plugin"""
        for plugin in self._plugins:
            if output_dataset_name in plugin.beam_datasets_created:
                return True
        return False

    def set_plugins(self, plugins):
        """

        :param list plugins: list of plugins to call
        """
        self._plugins = plugins
        _plugins_req_resources = get_plugins_positioners_resources(plugins)
        self._plugins_pos_resources = {}
        for requested_resource in _plugins_req_resources:
            self._plugins_pos_resources[requested_resource] = []

    def get_axis_scale_types(self):
        """
        Return axis display for the detector data to be used by silx view
        """
        return ["linear", "linear"]

    def __str__(self):
        if self.root_url is None:
            return "NXTomo"
        else:
            return self.root_url.path()
