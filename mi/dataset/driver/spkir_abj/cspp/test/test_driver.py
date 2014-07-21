"""
@package mi.dataset.driver.spkir_abj.cspp.test.test_driver
@file marine-integrations/mi/dataset/driver/spkir_abj/cspp/driver.py
@author Jeff Roy
@brief Test cases for spkir_abj_cspp driver

USAGE:
 Make tests verbose and provide stdout
   * From the IDK
       $ bin/dsa/test_driver
       $ bin/dsa/test_driver -i [-t testname]
       $ bin/dsa/test_driver -q [-t testname]
"""

__author__ = 'Jeff Roy'
__license__ = 'Apache 2.0'

import unittest

from nose.plugins.attrib import attr

from mi.core.log import get_logger ; log = get_logger()
from mi.idk.exceptions import SampleTimeout

from mi.idk.dataset.unit_test import DataSetTestCase
from mi.idk.dataset.unit_test import DataSetIntegrationTestCase
from mi.idk.dataset.unit_test import DataSetQualificationTestCase

from mi.dataset.dataset_driver import \
    DataSourceConfigKey, \
    DataSetDriverConfigKeys

from mi.dataset.driver.spkir_abj.cspp.driver import \
    SpkirAbjCsppDataSetDriver, \
    DataTypeKey

from mi.dataset.parser.spkir_abj_cspp import \
    SpkirAbjCsppParser, \
    SpkirAbjCsppMetadataTelemeteredDataParticle, \
    SpkirAbjCsppMetadataRecoveredDataParticle, \
    SpkirAbjCsppInstrumentTelemeteredDataParticle, \
    SpkirAbjCsppInstrumentRecoveredDataParticle

DIR_SPKIR_TELEMETERED = '/tmp/spkir/telem/test'
DIR_SPKIR_RECOVERED = '/tmp/spkir/recov/test'

SPKIR_PATTERN = '*_OCR.txt'

# Fill in driver details
DataSetTestCase.initialize(
    driver_module='mi.dataset.driver.spkir_abj.cspp.driver',
    driver_class='SpkirAbjCsppDataSetDriver',
    agent_resource_id='123xyz',
    agent_name='Agent007',
    agent_packet_config=SpkirAbjCsppDataSetDriver.stream_config(),
    startup_config={
        DataSourceConfigKey.RESOURCE_ID: 'spkir_abj_cspp',
        DataSourceConfigKey.HARVESTER:
        {
            DataTypeKey.SPKIR_ABJ_CSPP_TELEMETERED: {
                DataSetDriverConfigKeys.DIRECTORY: DIR_SPKIR_TELEMETERED,
                DataSetDriverConfigKeys.PATTERN: SPKIR_PATTERN,
                DataSetDriverConfigKeys.FREQUENCY: 1,
            },
            DataTypeKey.SPKIR_ABJ_CSPP_RECOVERED: {
                DataSetDriverConfigKeys.DIRECTORY: DIR_SPKIR_RECOVERED,
                DataSetDriverConfigKeys.PATTERN: SPKIR_PATTERN,
                DataSetDriverConfigKeys.FREQUENCY: 1,
            }
        },
        DataSourceConfigKey.PARSER: {
            DataTypeKey.SPKIR_ABJ_CSPP_TELEMETERED: {},
            DataTypeKey.SPKIR_ABJ_CSPP_RECOVERED: {}
        }
    }
)

SAMPLE_STREAM = 'spkir_abj_cspp_parsed'

# The integration and qualification tests generated here are suggested tests,
# but may not be enough to fully test your driver. Additional tests should be
# written as needed.

###############################################################################
#                            INTEGRATION TESTS                                #
# Device specific integration tests are for                                   #
# testing device specific capabilities                                        #
###############################################################################
@attr('INT', group='mi')
class IntegrationTest(DataSetIntegrationTestCase):
 
    def test_get(self):
        """
        Test that we can get data from files.  Verify that the driver
        sampling can be started and stopped
        """
        log.info("================ START INTEG TEST GET =====================")

        # Start sampling.
        self.driver.start_sampling()
        self.clear_async_data()

        # test that everything works for the telemetered harvester
        self.create_sample_data_set_dir('11079364_PPD_OCR.txt', DIR_SPKIR_TELEMETERED)

        log.debug('### Sample file created in dir = %s ', DIR_SPKIR_TELEMETERED)

        # check the metadata particle and the first 19 insturment particles
        self.assert_data((SpkirAbjCsppMetadataTelemeteredDataParticle,
                          SpkirAbjCsppInstrumentTelemeteredDataParticle),
                         '11079364_PPD_OCR_telem.yml',
                         count=20, timeout=10)

        # test that everything works for the recovered harvester
        self.create_sample_data_set_dir('11079419_PPB_OCR.txt', DIR_SPKIR_RECOVERED)

        log.debug('### Sample file created in dir = %s ', DIR_SPKIR_RECOVERED)

        # check the metadata particle and the first 19 insturment particles
        self.assert_data((SpkirAbjCsppMetadataRecoveredDataParticle,
                          SpkirAbjCsppInstrumentRecoveredDataParticle),
                         '11079419_PPB_OCR_recov.yml',
                         count=20, timeout=10)

    def test_mid_state_start(self):
        """
        Test the ability to start the driver with a saved state
        """
        pass

    def test_stop_start_resume(self):
        """
        Test the ability to stop and restart sampling, ingesting files in the
        correct order
        """
        pass

    def test_sample_exception(self):
        """
        Test a case that should produce a sample exception and confirm the
        sample exception occurs
        """
        pass

###############################################################################
#                            QUALIFICATION TESTS                              #
# Device specific qualification tests are for                                 #
# testing device specific capabilities                                        #
###############################################################################
@attr('QUAL', group='mi')
class QualificationTest(DataSetQualificationTestCase):

    def test_publish_path(self):
        """
        Setup an agent/driver/harvester/parser and verify that data is
        published out the agent
        """
        pass

    def test_large_import(self):
        """
        Test importing a large number of samples from the file at once
        """
        pass

    def test_stop_start(self):
        """
        Test the agents ability to start data flowing, stop, then restart
        at the correct spot.
        """
        pass

    def test_shutdown_restart(self):
        """
        Test a full stop of the dataset agent, then restart the agent 
        and confirm it restarts at the correct spot.
        """
        pass

    def test_parser_exception(self):
        """
        Test an exception is raised after the driver is started during
        record parsing.
        """
        pass

