###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import pytest

from LbAPCommon import checks

pytest.importorskip("xrootd")


def test_num_entries_passing():
    result = checks.num_entries(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        1000,
        "DecayTree",
    )
    assert result.passed
    assert result.messages == ["Found 5135823 in DecayTree"]
    assert result.histograms == []


def test_num_entries_failing():
    result = checks.num_entries(
        "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
        1000000000,
        "DecayTree",
    )
    assert not result.passed
    assert result.messages == ["Found 5135823 in DecayTree"]
    assert result.histograms == []
