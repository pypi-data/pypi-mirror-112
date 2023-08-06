# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "09/10/2020"


import unittest
import shutil
import tempfile
import h5py
import numpy
import os
from nxtomomill import converter
from nxtomomill.converter.hdf5.acquisition.utils import get_nx_detectors
from nxtomomill.converter.hdf5.acquisition.utils import guess_nx_detector
from nxtomomill.converter.hdf5.acquisition.baseaquisition import EntryReader
from nxtomomill.converter.hdf5.acquisition.baseaquisition import DatasetReader
from nxtomomill.io.config import HDF5Config
from tomoscan.esrf.hdf5scan import HDF5TomoScan
from nxtomomill.test.utils.bliss import MockBlissAcquisition
from silx.io.url import DataUrl
from silx.io.utils import get_data
from glob import glob
from nxtomomill.io.framegroup import FrameGroup


def url_has_been_copied(file_path: str, url: DataUrl):
    """util function to parse the `duplicate_data` folder and
    insure the copy of the dataset has been done"""
    duplicate_data_url = DataUrl(
        file_path=file_path, data_path="/duplicate_data", scheme="silx"
    )
    url_path = url.path()
    with EntryReader(duplicate_data_url) as duplicate_data_node:
        for _, dataset in duplicate_data_node.items():
            if "original_url" in dataset.attrs:
                original_url = dataset.attrs["original_url"]
                # the full dataset is registered in the attributes.
                # Here we only check the scan entry name
                if original_url.startswith(url_path):
                    return True
    return False


class TestH5ToNxConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.folder = tempfile.mkdtemp()
        self.config = HDF5Config()

    def tearDown(self) -> None:
        shutil.rmtree(self.folder)

    def test_simple_converter_with_nx_detector_attr(self):
        """
        Test a simple conversion when NX_class is defined
        """
        bliss_mock = MockBlissAcquisition(
            n_sample=2,
            n_sequence=1,
            n_scan_per_sequence=10,
            n_darks=5,
            n_flats=5,
            with_nx_detector_attr=True,
            output_dir=self.folder,
            detector_name="pcolinux",
        )
        for sample in bliss_mock.samples:
            self.assertTrue(os.path.exists(sample.sample_file))
            self.config.output_file = sample.sample_file.replace(".h5", ".nx")
            self.config.input_file = sample.sample_file
            converter.from_h5_to_nx(
                configuration=self.config,
            )
            # insure only one file is generated
            self.assertTrue(os.path.exists(self.config.output_file))
            # insure data is here
            with h5py.File(self.config.output_file, mode="r") as h5s:
                for _, entry_node in h5s.items():
                    self.assertTrue("instrument/detector/data" in entry_node)
                    dataset = entry_node["instrument/detector/data"]
                # check virtual dataset are relative and valid
                self.assertTrue(dataset.is_virtual)
                for vs in dataset.virtual_sources():
                    self.assertFalse(os.path.isabs(vs.file_name))
                # insure connection is valid. There is no
                # 'VirtualSource.is_valid' like function
                self.assertFalse(dataset[()].min() == 0 and dataset[()].max() == 0)

    def test_invalid_tomo_n(self):
        """Test translation fails if no detector can be found"""
        bliss_mock = MockBlissAcquisition(
            n_sample=1,
            n_sequence=1,
            n_scan_per_sequence=10,
            n_darks=5,
            n_flats=5,
            with_nx_detector_attr=True,
            output_dir=self.folder,
        )
        self.assertTrue(len(bliss_mock.samples), 1)
        sample = bliss_mock.samples[0]
        self.assertTrue(os.path.exists(sample.sample_file))
        output_file = sample.sample_file.replace(".h5", ".nx")

        # rewrite tomo_n
        with h5py.File(sample.sample_file, mode="a") as h5s:
            for _, entry_node in h5s.items():
                if "technique/scan/tomo_n" in entry_node:
                    del entry_node["technique/scan/tomo_n"]
                    entry_node["technique/scan/tomo_n"] = 9999

        with self.assertRaises(ValueError):
            self.config.input_file = sample.sample_file
            self.config.output_file = output_file
            self.config.single_file = True
            self.config.no_input = True
            self.config.raises_error = True
            converter.from_h5_to_nx(configuration=self.config)

    def test_simple_converter_without_nx_detector_attr(self):
        """
        Test a simple conversion when no NX_class is defined
        """
        bliss_mock = MockBlissAcquisition(
            n_sample=1,
            n_sequence=3,
            n_scan_per_sequence=10,
            n_darks=5,
            n_flats=5,
            with_nx_detector_attr=True,
            output_dir=self.folder,
            detector_name="tata_detector",
        )
        self.assertTrue(len(bliss_mock.samples), 1)
        sample = bliss_mock.samples[0]
        self.assertTrue(os.path.exists(sample.sample_file))
        output_file = sample.sample_file.replace(".h5", ".nx")
        self.config.input_file = sample.sample_file
        self.config.output_file = output_file
        self.config.single_file = True
        self.config.no_input = True
        converter.from_h5_to_nx(configuration=self.config)
        # insure only one file is generated
        self.assertTrue(os.path.exists(output_file))
        # insure data is here
        with h5py.File(output_file, mode="r") as h5s:
            for _, entry_node in h5s.items():
                self.assertTrue("instrument/detector/data" in entry_node)
                dataset = entry_node["instrument/detector/data"]
            # check virtual dataset are relative and valid
            self.assertTrue(dataset.is_virtual)
            for vs in dataset.virtual_sources():
                self.assertFalse(os.path.isabs(vs.file_name))
            # insure connection is valid. There is no
            # 'VirtualSource.is_valid' like function
            self.assertFalse(dataset[()].min() == 0 and dataset[()].max() == 0)

    def test_providing_existing_camera_name(self):
        """Test that detector can be provided to the h5_to_nx function and
        using linux wildcard"""
        bliss_mock = MockBlissAcquisition(
            n_sample=1,
            n_sequence=3,
            n_scan_per_sequence=10,
            n_darks=5,
            n_flats=5,
            with_nx_detector_attr=True,
            output_dir=self.folder,
            detector_name="my_detector",
        )
        self.assertTrue(len(bliss_mock.samples), 1)
        sample = bliss_mock.samples[0]
        self.assertTrue(os.path.exists(sample.sample_file))
        self.config.output_file = sample.sample_file.replace(".h5", ".nx")
        self.config.valid_camera_names = ("my_detec*",)
        self.config.input_file = sample.sample_file
        self.config.single_file = True
        self.config.request_input = False
        self.config.raises_error = True
        converter.from_h5_to_nx(configuration=self.config)
        # insure only one file is generated
        self.assertTrue(os.path.exists(self.config.output_file))
        # insure data is here
        with h5py.File(self.config.output_file, mode="r") as h5s:
            for _, entry_node in h5s.items():
                self.assertTrue("instrument/detector/data" in entry_node)
                dataset = entry_node["instrument/detector/data"]
            # check virtual dataset are relative and valid
            self.assertTrue(dataset.is_virtual)
            for vs in dataset.virtual_sources():
                self.assertFalse(os.path.isabs(vs.file_name))
            # insure connection is valid. There is no
            # 'VirtualSource.is_valid' like function
            self.assertFalse(dataset[()].min() == 0 and dataset[()].max() == 0)

    def test_providing_non_existing_camera_name(self):
        """Test translation fails if no detector can be found"""
        bliss_mock = MockBlissAcquisition(
            n_sample=1,
            n_sequence=3,
            n_scan_per_sequence=10,
            n_darks=5,
            n_flats=5,
            with_nx_detector_attr=True,
            output_dir=self.folder,
            detector_name="toto_detector",
        )
        self.assertTrue(len(bliss_mock.samples), 1)
        sample = bliss_mock.samples[0]
        self.assertTrue(os.path.exists(sample.sample_file))
        self.config.input_file = sample.sample_file
        self.config.output_file = sample.sample_file.replace(".h5", ".nx")
        self.config.valid_camera_names = ("my_detec",)
        self.config.raises_error = True
        with self.assertRaises(ValueError):
            converter.from_h5_to_nx(configuration=self.config)

    def test_z_series_conversion(self):
        """Test conversion of a zseries bliss (mock) acquisition"""
        bliss_mock = MockBlissAcquisition(
            n_sample=1,
            n_sequence=1,
            n_scan_per_sequence=10,
            n_darks=5,
            n_flats=5,
            with_nx_detector_attr=True,
            output_dir=self.folder,
            detector_name="frelon1",
            acqui_type="zseries",
            z_values=(1, 2, 3),
        )
        self.assertTrue(len(bliss_mock.samples), 1)
        sample = bliss_mock.samples[0]
        self.assertTrue(os.path.exists(sample.sample_file))
        self.config.input_file = sample.sample_file
        self.config.output_file = sample.sample_file.replace(".h5", ".nx")
        res = converter.from_h5_to_nx(configuration=self.config)
        # insure the 4 files are generated: master file and one per z
        files = glob(os.path.dirname(sample.sample_file) + "/*.nx")
        self.assertEqual(len(files), 4)
        # try to create HDF5TomoScan from those to insure this is valid
        # and check z values for example
        for res_tuple in res:
            scan = HDF5TomoScan(scan=res_tuple[0], entry=res_tuple[1])
            if hasattr(scan, "z_translation"):
                self.assertTrue(scan.z_translation is not None)

    def test_ignore_sub_entries(self):
        """
        Test we can ignore some sub entries
        """
        from nxtomomill.test.utils.bliss import MockBlissAcquisition

        bliss_mock = MockBlissAcquisition(
            n_sample=1,
            n_sequence=1,
            n_scan_per_sequence=10,
            n_darks=0,
            n_flats=0,
            with_nx_detector_attr=True,
            output_dir=self.folder,
            detector_name="pcolinux",
        )
        for sample in bliss_mock.samples:
            self.assertTrue(os.path.exists(sample.sample_file))
            self.config.output_file = sample.sample_file.replace(".h5", ".nx")
            self.config.input_file = sample.sample_file
            self.config.single_file = True
            self.config.sub_entries_to_ignore = ("6.1", "7.1")
            self.config.request_input = False
            converter.from_h5_to_nx(configuration=self.config)
            # insure only one file is generated
            self.assertTrue(os.path.exists(self.config.output_file))
            # insure data is here
            with h5py.File(self.config.output_file, mode="r") as h5s:
                for _, entry_node in h5s.items():
                    self.assertTrue("instrument/detector/data" in entry_node)
                    dataset = entry_node["instrument/detector/data"]
                # check virtual dataset are relative and valid
                self.assertTrue(dataset.is_virtual)
                self.assertEqual(
                    dataset.shape,
                    (10 * (10 - len(self.config.sub_entries_to_ignore)), 64, 64),
                )
                for vs in dataset.virtual_sources():
                    self.assertFalse(os.path.isabs(vs.file_name))
                # insure connection is valid. There is no
                # 'VirtualSource.is_valid' like function
                self.assertFalse(dataset[()].min() == 0 and dataset[()].max() == 0)


class TestDetectorDetection(unittest.TestCase):
    """
    Test functions to find nxdetector groups
    """

    def setUp(self) -> None:
        self.folder = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.folder)

    @staticmethod
    def create_nx_detector(node: h5py.Group, name, with_nx_class):
        det_node = node.require_group(name)
        data = numpy.random.random(10 * 10 * 10).reshape(10, 10, 10)
        det_node["data"] = data
        if with_nx_class:
            if "NX_class" not in det_node.attrs:
                det_node.attrs["NX_class"] = "NXdetector"

    def test_get_nx_detectors(self):
        """test get_nx_detectors function"""
        h5file = os.path.join(self.folder, "h5file.hdf5")
        with h5py.File(h5file, mode="w") as h5s:
            self.create_nx_detector(node=h5s, name="det1", with_nx_class=True)
            self.create_nx_detector(node=h5s, name="det2", with_nx_class=False)
        with h5py.File(h5file, mode="r") as h5s:
            dets = get_nx_detectors(h5s)
            self.assertEqual(len(dets), 1)
            self.assertEqual(dets[0].name, "/det1")
            self.assertEqual(len(guess_nx_detector(h5s)), 2)
        with h5py.File(h5file, mode="a") as h5s:
            self.create_nx_detector(node=h5s, name="det3", with_nx_class=True)
            self.create_nx_detector(node=h5s, name="det4", with_nx_class=True)
        with h5py.File(h5file, mode="r") as h5s:
            dets = get_nx_detectors(h5s)
            self.assertEqual(len(dets), 3)

    def test_guess_nx_detector(self):
        """test guess_nx_detector function"""
        h5file = os.path.join(self.folder, "h5file.hdf5")
        with h5py.File(h5file, mode="w") as h5s:
            self.create_nx_detector(node=h5s, name="det2", with_nx_class=False)
        with h5py.File(h5file, mode="r") as h5s:
            dets = get_nx_detectors(h5s)
            self.assertEqual(len(dets), 0)
            dets = guess_nx_detector(h5s)
            self.assertEqual(dets[0].name, "/det2")
        with h5py.File(h5file, mode="w") as h5s:
            self.create_nx_detector(node=h5s, name="det3", with_nx_class=False)
            self.create_nx_detector(node=h5s, name="det4", with_nx_class=True)
        with h5py.File(h5file, mode="a") as h5s:
            dets = guess_nx_detector(h5s)
            self.assertEqual(len(dets), 2)


class TestXRDCTConversion(unittest.TestCase):
    def setUp(self) -> None:
        self.folder = tempfile.mkdtemp()
        self.config = HDF5Config()

    def tearDown(self) -> None:
        shutil.rmtree(self.folder)

    def test_simple_converter_with_nx_detector_attr(self):
        """
        Test a simple conversion when NX_class is defined
        """
        from nxtomomill.test.utils.bliss import MockBlissAcquisition

        bliss_mock = MockBlissAcquisition(
            n_sample=1,
            n_sequence=1,
            n_scan_per_sequence=10,
            n_darks=0,
            n_flats=0,
            with_nx_detector_attr=True,
            output_dir=self.folder,
            detector_name="pilatus",
            acqui_type="xrd-ct",
        )
        for sample in bliss_mock.samples:
            self.assertTrue(os.path.exists(sample.sample_file))
            self.config.input_file = sample.sample_file
            self.config.output_file = sample.sample_file.replace(".h5", ".nx")
            self.config.single_file = True
            self.config.request_input = False
            converter.from_h5_to_nx(configuration=self.config)

            # insure only one file is generated
            self.assertTrue(os.path.exists(self.config.output_file))
            # insure data is here
            with h5py.File(self.config.output_file, mode="r") as h5s:
                for _, entry_node in h5s.items():
                    self.assertTrue("instrument/detector/data" in entry_node)
                    dataset = entry_node["instrument/detector/data"]
                # check virtual dataset are relative and valid
                self.assertTrue(dataset.is_virtual)
                for vs in dataset.virtual_sources():
                    self.assertFalse(os.path.isabs(vs.file_name))
                # insure connection is valid. There is no
                # 'VirtualSource.is_valid' like function
                self.assertFalse(dataset[()].min() == 0 and dataset[()].max() == 0)


class TestStandardAcqConversionWithExternalUrls(unittest.TestCase):
    """Test conversion when frames are provided from urls"""

    def setUp(self) -> None:
        self.folder = tempfile.mkdtemp()
        self.config = HDF5Config()
        self.config.output_file = os.path.join(self.folder, "output.nx")

    def create_scan(self, n_projection_scans, n_flats, n_darks, output_dir):
        """
        :param int n_projection_scans: number of scans beeing projections
        :param int n_flats: number of frame per flats
        :param int n_darks: number of frame per dark
        """
        bliss_mock = MockBlissAcquisition(
            n_sample=1,
            n_sequence=1,
            n_scan_per_sequence=n_projection_scans,
            n_darks=n_darks,
            n_flats=n_flats,
            with_nx_detector_attr=True,
            output_dir=output_dir,
            detector_name="pcolinux",
        )
        return bliss_mock.samples[0].sample_file

    def tearDown(self) -> None:
        shutil.rmtree(self.folder)

    def test_dataset_1(self):
        """test a conversion where projections are contained in the
        input_file. Dark and flats are on a different file"""
        folder_1 = os.path.join(self.folder, "acqui_1")
        input_file = self.create_scan(
            n_projection_scans=6, n_flats=0, n_darks=0, output_dir=folder_1
        )
        folder_2 = os.path.join(self.folder, "acqui_2")
        dark_flat_file = self.create_scan(
            n_projection_scans=0, n_flats=1, n_darks=1, output_dir=folder_2
        )
        self.config.input_file = input_file

        # we want to take two scan of projections from the input file: 5.1
        # and 6.1. As the input file is provided we don't need to
        # specify it
        self.config.data_frame_grps = (
            FrameGroup(frame_type="proj", url=DataUrl(data_path="/5.1", scheme="silx")),
            FrameGroup(frame_type="proj", url=DataUrl(data_path="/6.1", scheme="silx")),
            FrameGroup(
                frame_type="flat",
                url=DataUrl(file_path=dark_flat_file, data_path="/2.1", scheme="silx"),
            ),
            FrameGroup(
                frame_type="dark",
                url=DataUrl(file_path=dark_flat_file, data_path="/3.1", scheme="silx"),
            ),
        )

        converter.from_h5_to_nx(
            configuration=self.config,
        )

        self.assertTrue(os.path.exists(self.config.output_file))

        with h5py.File(self.config.output_file, mode="r") as h5s:
            self.assertEqual(len(h5s.items()), 1)
            self.assertTrue("entry0000" in h5s)

        scan = HDF5TomoScan(scan=self.config.output_file, entry="entry0000")

        # check the `data`has been created
        self.assertTrue(len(scan.projections), 20)
        self.assertTrue(len(scan.darks), 10)
        # check data is a virtual dataset
        with h5py.File(self.config.output_file, mode="r") as h5f:
            dataset = h5f["entry0000/instrument/detector/data"]
            self.assertTrue(dataset.is_virtual)
        # check the `data` virtual dataset is valid
        # if the link fail then all values are zeros
        url = tuple(scan.projections.values())[0]
        proj_data = get_data(url)
        self.assertTrue(proj_data.min() != proj_data.max())

        url = tuple(scan.darks.values())[0]
        dark_data = get_data(url)
        self.assertTrue(dark_data.min() != dark_data.max())

        self.assertTrue(len(scan.flats), 10)
        url = tuple(scan.flats.values())[0]
        flat_data = get_data(url)
        self.assertTrue(flat_data.min() != flat_data.max())

    def test_dataset_2(self):
        """test a conversion where no input file is provided and
        where we have 2 projections in a file, 3 in an other.
        Flat and darks are also in another file. No flat provided.
        """
        folder_1 = os.path.join(self.folder, "acqui_1")
        file_1 = self.create_scan(
            n_projection_scans=6, n_flats=0, n_darks=0, output_dir=folder_1
        )
        folder_2 = os.path.join(self.folder, "acqui_2")
        file_2 = self.create_scan(
            n_projection_scans=6, n_flats=0, n_darks=0, output_dir=folder_2
        )
        folder_3 = os.path.join(self.folder, "acqui_3")
        file_3 = self.create_scan(
            n_projection_scans=0, n_flats=0, n_darks=1, output_dir=folder_3
        )
        folder_4 = os.path.join(self.folder, "acqui_4")
        file_4 = self.create_scan(
            n_projection_scans=0, n_flats=1, n_darks=0, output_dir=folder_4
        )

        # we want to take two scan of projections from the input file: 5.1
        # and 6.1. As the input file is provided we don't need to
        # specify it
        dark_url_1 = DataUrl(file_path=file_3, data_path="/2.1", scheme="silx")
        flat_url_1 = DataUrl(file_path=file_4, data_path="/2.1", scheme="silx")
        proj_url_1 = DataUrl(file_path=file_1, data_path="/5.1", scheme="silx")
        proj_url_2 = DataUrl(file_path=file_1, data_path="/6.1", scheme="silx")
        proj_url_3 = DataUrl(file_path=file_2, data_path="/4.1", scheme="silx")
        proj_url_4 = DataUrl(file_path=file_2, data_path="/2.1", scheme="silx")

        self.config.default_copy_behavior = True
        self.config.data_frame_grps = (
            FrameGroup(frame_type="dark", url=dark_url_1),
            FrameGroup(frame_type="flat", url=flat_url_1),
            FrameGroup(frame_type="proj", url=proj_url_1, copy=False),
            FrameGroup(frame_type="proj", url=proj_url_2, copy=False),
            FrameGroup(frame_type="proj", url=proj_url_3),
            FrameGroup(frame_type="proj", url=proj_url_4),
        )
        urls_copied = (dark_url_1, flat_url_1, proj_url_3, proj_url_4)
        urls_not_copied = (proj_url_1, proj_url_2)

        self.config.raises_error = True
        converter.from_h5_to_nx(
            configuration=self.config,
        )

        self.assertTrue(os.path.exists(self.config.output_file))

        with h5py.File(self.config.output_file, mode="r") as h5s:
            self.assertEqual(len(h5s.items()), 2)
            self.assertTrue("entry0000" in h5s)
            self.assertTrue("duplicate_data" in h5s)

        detector_url = DataUrl(
            file_path=self.config.output_file,
            data_path="/entry0000/instrument/detector/data",
            scheme="silx",
        )
        with DatasetReader(detector_url) as detector_dataset:
            self.assertTrue(detector_dataset.is_virtual)
            for i_vs, vs in enumerate(detector_dataset.virtual_sources()):
                self.assertFalse(os.path.isabs(vs.file_name))
                if i_vs in (0, 1, 4, 5):
                    self.assertEqual(vs.file_name, "output.nx")
                else:
                    self.assertEqual(vs.file_name, "acqui_1/sample_0/sample_0.h5")

        scan = HDF5TomoScan(scan=self.config.output_file, entry="entry0000")

        # check the `data`has been created
        self.assertTrue(len(scan.projections), 40)
        self.assertTrue(len(scan.darks), 10)

        # check the `data` virtual dataset is valid
        # if the link fail then all values are zeros
        url = tuple(scan.projections.values())[0]
        proj_data = get_data(url)
        self.assertTrue(proj_data.min() != proj_data.max())

        url = tuple(scan.darks.values())[0]
        dark_data = get_data(url)
        self.assertTrue(dark_data.min() != dark_data.max())

        self.assertTrue(len(scan.flats), 10)
        url = tuple(scan.flats.values())[0]
        flat_data = get_data(url)
        self.assertTrue(flat_data.min() != flat_data.max())

        with h5py.File(self.config.output_file, mode="r") as h5f:
            dataset = h5f["entry0000/instrument/detector/data"]
            self.assertTrue(dataset.shape, (60, 10, 10))
            with EntryReader(dark_url_1) as dark_entry:
                numpy.testing.assert_array_equal(
                    dark_entry["instrument/pcolinux/data"], dataset[0:10]
                )
            with EntryReader(flat_url_1) as flat_entry:
                numpy.testing.assert_array_equal(
                    flat_entry["instrument/pcolinux/data"], dataset[10:20]
                )
            with EntryReader(proj_url_1) as proj_entry_1:
                numpy.testing.assert_array_equal(
                    proj_entry_1["instrument/pcolinux/data"], dataset[20:30]
                )
            with EntryReader(proj_url_2) as proj_entry_2:
                numpy.testing.assert_array_equal(
                    proj_entry_2["instrument/pcolinux/data"], dataset[30:40]
                )
            with EntryReader(proj_url_3) as proj_entry_3:
                numpy.testing.assert_array_equal(
                    proj_entry_3["instrument/pcolinux/data"], dataset[40:50]
                )
            with EntryReader(proj_url_4) as proj_entry_4:
                numpy.testing.assert_array_equal(
                    proj_entry_4["instrument/pcolinux/data"], dataset[50:60]
                )

        for url in urls_copied:
            self.assertTrue(
                url_has_been_copied(file_path=self.config.output_file, url=url)
            )

        for url in urls_not_copied:
            self.assertFalse(
                url_has_been_copied(file_path=self.config.output_file, url=url)
            )


class TestZSeriesConversionWithExternalUrls(unittest.TestCase):
    """
    Test Zseries conversion from HDF5Config and providing urls
    """

    def setUp(self) -> None:
        self.folder = tempfile.mkdtemp()

        self.config = HDF5Config()
        self.config.output_file = os.path.join(self.folder, "output.nx")

        camera_name = "frelon"
        bliss_mock = MockBlissAcquisition(
            n_sample=1,
            n_sequence=1,
            n_scan_per_sequence=2,
            n_darks=1,
            n_flats=0,
            with_nx_detector_attr=True,
            output_dir=os.path.join(self.folder, "seq_1"),
            detector_name=camera_name,
            acqui_type="zseries",
            z_values=(1, 2, 3),
        )
        self._zseries_1_file = bliss_mock.samples[0].sample_file

        bliss_mock = MockBlissAcquisition(
            n_sample=1,
            n_sequence=1,
            n_scan_per_sequence=2,
            n_darks=0,
            n_flats=1,
            with_nx_detector_attr=True,
            output_dir=os.path.join(self.folder, "seq_2"),
            detector_name=camera_name,
            acqui_type="zseries",
            z_values=(4, 5, 6),
        )
        self._zseries_2_file = bliss_mock.samples[0].sample_file

    def tearDown(self) -> None:
        shutil.rmtree(self.folder)

    def test_dataset_zseries(self):
        """Test a zseries with only external scan entries"""

        # create the sequence to create: take two scan of two z (2, 3) from
        # the first sequence and two scan of one z from the second
        # sequence (z==4)
        dark_url_1 = DataUrl(
            file_path=self._zseries_1_file, data_path="/5.1", scheme="silx"
        )
        proj_url_1 = DataUrl(
            file_path=self._zseries_1_file, data_path="/6.1", scheme="silx"
        )
        proj_url_2 = DataUrl(
            file_path=self._zseries_1_file, data_path="/7.1", scheme="silx"
        )
        proj_url_3 = DataUrl(
            file_path=self._zseries_1_file, data_path="/9.1", scheme="silx"
        )
        proj_url_4 = DataUrl(
            file_path=self._zseries_1_file, data_path="/10.1", scheme="silx"
        )
        proj_url_5 = DataUrl(
            file_path=self._zseries_2_file, data_path="/3.1", scheme="silx"
        )
        proj_url_6 = DataUrl(
            file_path=self._zseries_2_file, data_path="/4.1", scheme="silx"
        )
        flat_url_1 = DataUrl(
            file_path=self._zseries_2_file, data_path="/2.1", scheme="silx"
        )
        self.config.default_copy_behavior = True
        self.config.single_file = True
        self.config.data_frame_grps = (
            FrameGroup(frame_type="dark", url=dark_url_1, copy=False),
            FrameGroup(frame_type="flat", url=flat_url_1, copy=False),
            FrameGroup(frame_type="proj", url=proj_url_1),
            FrameGroup(frame_type="proj", url=proj_url_2),
            FrameGroup(frame_type="proj", url=proj_url_3),
            FrameGroup(frame_type="proj", url=proj_url_4),
            FrameGroup(frame_type="proj", url=proj_url_5),
            FrameGroup(frame_type="proj", url=proj_url_6),
        )
        urls_copied = (
            proj_url_1,
            proj_url_2,
            proj_url_3,
            proj_url_4,
            proj_url_5,
            proj_url_6,
        )
        urls_not_copied = (flat_url_1, dark_url_1)

        # do conversion
        converter.from_h5_to_nx(
            configuration=self.config,
        )
        self.assertTrue(os.path.exists(self.config.output_file))
        with h5py.File(self.config.output_file, mode="r") as h5f:
            self.assertTrue("entry0000" in h5f)
            self.assertTrue("entry0001" in h5f)
            self.assertTrue("entry0002" in h5f)

        scan_z0 = HDF5TomoScan(scan=self.config.output_file, entry="entry0000")
        scan_z1 = HDF5TomoScan(scan=self.config.output_file, entry="entry0001")
        scan_z2 = HDF5TomoScan(scan=self.config.output_file, entry="entry0002")
        # check the `data`has been created
        self.assertTrue(len(scan_z0.projections), 40)
        self.assertTrue(len(scan_z1.projections), 40)
        self.assertTrue(len(scan_z2.projections), 40)

        for url in urls_copied:
            self.assertTrue(
                url_has_been_copied(file_path=self.config.output_file, url=url)
            )

        for url in urls_not_copied:
            self.assertFalse(
                url_has_been_copied(file_path=self.config.output_file, url=url)
            )

        # test a few slices
        with h5py.File(self.config.output_file, mode="r") as h5f:
            dataset = h5f["entry0000/instrument/detector/data"]
            self.assertTrue(dataset.shape, (60, 10, 10))

            with EntryReader(proj_url_1) as proj_entry_1:
                numpy.testing.assert_array_equal(
                    proj_entry_1["instrument/frelon/data"], dataset[10:20]
                )
            with EntryReader(proj_url_2) as proj_entry_2:
                numpy.testing.assert_array_equal(
                    proj_entry_2["instrument/frelon/data"], dataset[20:30]
                )


def suite():
    test_suite = unittest.TestSuite()
    for ui in (
        TestDetectorDetection,
        TestH5ToNxConverter,
        TestXRDCTConversion,
        TestStandardAcqConversionWithExternalUrls,
        TestZSeriesConversionWithExternalUrls,
    ):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
