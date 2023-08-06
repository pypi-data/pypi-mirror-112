##############################################################################
# PyLipID: A python module for analysing protein-lipid interactions
#
# Author: Wanling Song
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
##############################################################################

r"""
func module
==============
The ``func`` module provides functions for functions that do the heavy-lifting:

.. currentmodule:: pylipid.func

.. autosummary::
   :toctree: generated/

   cal_koff
   cal_survival_func
   calculate_koff_wrapper
   Duration
   cal_contact_residues
   cal_occupancy
   cal_lipidcount
   get_node_list
   collect_bound_poses
   vectorize_poses
   calculate_scores
   write_bound_poses
   calculate_surface_area_wrapper
   analyze_pose_wrapper
   cluster_DBSCAN
   cluster_KMeans

"""

from .kinetics import cal_koff
from .kinetics import cal_survival_func
from .interactions import Duration
from .interactions import cal_contact_residues, cal_occupancy, cal_lipidcount
from .binding_site import get_node_list
from .binding_site import collect_bound_poses, vectorize_poses, calculate_scores, write_bound_poses
from .clusterer import cluster_DBSCAN, cluster_KMeans
from .binding_site import analyze_pose_wrapper
from .binding_site import calculate_surface_area_wrapper
from .kinetics import calculate_koff_wrapper

