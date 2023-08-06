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


import re
from dataclasses import dataclass, field
from itertools import combinations
from typing import List

import boost_histogram as bh
import numpy
import uproot
from hist import Hist


@dataclass
class CheckResult:
    """Class for representing the return result of ntuple checks"""

    passed: bool
    messages: List[str] = field(default_factory=list)
    histograms: List[Hist] = field(default_factory=list)


def num_entries(
    filepath,
    count,
    tree_pattern=r"(.*Tuple/DecayTree)|(MCDecayTreeTuple.*/MCDecayTree)",
):
    """Check that all matching TTree objects contain a minimum number of entries.

    :param filepath: Path to a file to analyse
    :param count: The minimum number of entries required
    :param tree_pattern: A regular expression for the TTree objects to check
    :returns: A CheckResult object
    """
    result = CheckResult(False)
    with uproot.open(filepath) as f:
        for key, obj in f.items(cycle=False):
            if not isinstance(obj, uproot.TTree):
                continue
            if re.fullmatch(tree_pattern, key):
                num_entries = obj.num_entries
                result.passed |= num_entries >= count
                result.messages += [f"Found {num_entries} in {key}"]
    # If no matches were found the check should be marked as failed
    if len(result.messages) == 0:
        result.passed = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]
    return result


def range_check(
    filepath,
    expression,
    limits,
    abs_tolerance,
    blind_ranges,
    tree_pattern=r"(.*Tuple/DecayTree)|(MCDecayTreeTuple.*/MCDecayTree)",
):
    """Check if there is at least one entry in the TTree object with a specific
    variable falling in a pre-defined range. The histogram is then produced as output.
    It is possible to blind some regions.

    :param filepath: Path to a file to analyse
    :param expression: Name of the variable (or expression depending on varibales in the TTree) to be checked
    :param limits: Pre-defined range
    :param abs_tolerance:
    :param blind_ranges: regions to be blinded in the histogram
    :param tree_pattern: A regular expression for the TTree object to check
    :returns: A CheckResult object
    """
    result = CheckResult(False)
    with uproot.open(filepath) as f:
        for key, obj in f.items(cycle=False):
            if not isinstance(obj, uproot.TTree):
                continue
            if not re.fullmatch(tree_pattern, key):
                continue

            values_obj = {}
            # Check if the branch is in the Tree or if the expression is correctly written
            try:
                values_obj = obj.arrays(expression, library="np")
            except uproot.exceptions.KeyInFileError as e:
                result.messages += [f"Missing branch in {key!r} with {e!r}"]
                result.passed |= False
                continue
            except Exception as e:
                result.messages += [
                    f"Failed to apply {expression!r} to {key!r} with error: {e!r}"
                ]
                result.passed |= False
                continue
            test_array = values_obj[expression]
            test_array = test_array[
                numpy.where((test_array < limits["max"]) & (test_array > limits["min"]))
            ]
            if isinstance(blind_ranges, dict):
                blind_ranges = [blind_ranges]
                # Take into account that there could be multiple regions to blind
            for blind_range in blind_ranges:
                lower, upper = blind_range["min"], blind_range["max"]
                test_array = test_array[~((lower < test_array) & (test_array < upper))]
            if len(test_array) == 0:
                result.passed |= False
                result.messages += [f"No events found in range for Tree {key}"]
                continue
            result.messages += [f"Found at least one event in range in Tree {key} "]
            result.passed |= True
            h = bh.Histogram(bh.axis.Regular(50, limits["min"], limits["max"]))
            h.fill(test_array)
            result.histograms += [h]
    # If no matches are found the check should be marked as failed
    if len(result.messages) == 0:
        result.passed = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]
    return result


def range_check_nd(
    filepath,
    expression,
    limits,
    abs_tolerance,
    tree_pattern=r"(.*Tuple/DecayTree)|(MCDecayTreeTuple.*/MCDecayTree)",
):
    """Produce 2-dimensional histograms of variables taken from a TTree object.

    :param filepath: Path to a file to analyse
    :param expression: Name of the variables (or expression) to be checked.
    :param limits: Pre-defined ranges
    :param abs_tolerance:
    :param tree_pattern: A regular expression for the TTree object to check
    :returns: A CheckResult object
    """
    result = CheckResult(False)
    # Check if the number of variables matches expectations
    lenght_expr = len(expression)
    lenght_limits = len(limits)
    if lenght_expr < 2 or lenght_expr > 4:
        result.messages += ["Expected at least two variables, but not more than four."]
        result.passed |= False
        return result
    if lenght_expr != lenght_limits:
        result.messages += [
            "For each variable, a corresponding range should be defined."
        ]
        result.passed |= False
        return result
    with uproot.open(filepath) as f:
        for key, obj in f.items(cycle=False):
            if not isinstance(obj, uproot.TTree):
                continue
            if not re.fullmatch(tree_pattern, key):
                continue
            dict_of_arrays = {}
            check_expr = False
            for k, exp in expression.items():
                values_obj = {}
                # Check if the branch is present in the TTree or if the expression is correctly written
                try:
                    values_obj = obj.arrays(exp, library="np")
                except uproot.exceptions.KeyInFileError as e:
                    result.messages += [f"Missing branch in {key!r} with {e!r}"]
                    result.passed |= False
                    check_expr = True
                    break
                except Exception as e:
                    result.messages += [
                        f"Failed to apply {exp!r} to {key!r} with error: {e!r}"
                    ]
                    result.passed |= False
                    check_expr = True
                    break
                test_array = values_obj[exp]
                dict_of_arrays[str(k)] = test_array
            # Continue if there is a missing branch or the expression is not correctly written
            if check_expr:
                continue
            # Fill the histograms
            list_keys = list(dict_of_arrays.keys())
            for key_i, key_j in combinations(list_keys, 2):
                h = bh.Histogram(
                    bh.axis.Regular(50, limits[key_i]["min"], limits[key_i]["max"]),
                    bh.axis.Regular(50, limits[key_j]["min"], limits[key_j]["max"]),
                )
                h.fill(dict_of_arrays[key_i], dict_of_arrays[key_j])
                if not h.empty():
                    result.histograms += [h]
                    result.messages += [
                        f"Found at least one event in range in Tree {key} "
                    ]
                    result.passed |= True
                else:
                    var1 = expression[key_i]
                    var2 = expression[key_j]
                    result.messages += [
                        f"No events found in range for Tree {key} and variables {var1}, {var2} "
                    ]
                    result.passed |= False
    # If no matches are found the check should be marked as failed
    if len(result.messages) == 0:
        result.passed = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]
    return result


def num_entries_per_invpb(
    filepath,
    count_per_invpb,
    tree_pattern=r"(.*Tuple/DecayTree)",
    lumi_pattern=r"(.*Luminosity/LumiTuple)",
):
    """Check that the matching TTree objects contain a minimum number of entries per unit luminosity (pb-1).

    :param filepath: Path to a file to analyse
    :param count_per_invpb: The minimum number of entries per unit luminosity required
    :param tree_pattern: A regular expression for the TTree objects to check
    :param lumi_pattern: A regular expression for the TTree object containing the luminosity information
    :returns: A CheckResult object
    """
    result = CheckResult(False)
    with uproot.open(filepath) as f:
        num_entries = {}
        lumi = 0.0
        for key, obj in f.items(cycle=False):
            if not isinstance(obj, uproot.TTree):
                continue
            if re.fullmatch(tree_pattern, key):
                num_entries[key] = obj.num_entries
            if re.fullmatch(lumi_pattern, key):
                try:
                    lumi = obj["IntegratedLuminosity"].array(library="np")
                except uproot.exceptions.KeyInFileError as e:
                    result.messages += [
                        f"Missing luminosity branch in {key!r} with error {e!r}"
                    ]
                    result.passed |= False
                    break
        if lumi == 0:
            result.passed |= False
            result.messages += ["Failed to get luminosity information"]
        else:
            for key, entries in num_entries.items():
                entries_per_lumi = entries / lumi
                result.passed |= entries_per_lumi >= count_per_invpb
                result.messages += [
                    f"Found {entries_per_lumi} entries per unit luminosity (pb-1) in {key}"
                ]
    # If no matches were found the check should be marked as failed
    if len(result.messages) == 0:
        result.passed = False
        result.messages += [f"No TTree objects found that match {tree_pattern}"]
    return result
