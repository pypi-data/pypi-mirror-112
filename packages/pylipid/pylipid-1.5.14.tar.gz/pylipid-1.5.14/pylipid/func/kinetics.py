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

"""This module contains functions for calculating interaction residence time and koff.
"""
import warnings
import numpy as np
from scipy.optimize import curve_fit
from ..plot import plot_koff


__all__ = ["cal_koff", "cal_survival_func", "calculate_koff_wrapper"]


def cal_koff(durations, t_total, timestep, nbootstrap=10, initial_guess=[1., 1., 1., 1.], cap=True):
    r"""Calculate residence time and koff.

    This function calculates the normalized survival time correlation function of the given list of durations, and fits t
    he survival function to a bi-exponential curve [1]_.

    The survival time correlation function σ(t) is calculated as follow

    .. math::

        \sigma(t) = \frac{1}{N_{j}} \frac{1}{T-t} \sum_{j=1}^{N_{j}} \sum_{v=0}^{T-t}\tilde{n}_{j}(v, v+t)

    where T is the length of the simulation trajectory, :math:`N_{j}` is the total number of lipid contacts and
    :math:`\sum_{v=0}^{T-t} \tilde{n}_{j}(v, v+t)` is a binary function that takes the value 1 if the contact of
    lipid j lasts from time ν to time v+t and 0 otherwise. The values of :math:`\sigma(t)` are calculated for every
    value of t from 0 to T ns, for each time step of the trajectories, and normalized by dividing by :math:`\sigma(t)`,
    so that the survival time-correlation function has value 1 at t = 0.

    The normalized survival function is then fitted to a biexponential to model the long and short decays of
    lipid relaxation:

    .. math::
        \sigma(t) \sim A e^{-k_{1} t}+B e^{-k_{2} t}\left(k_{1} \leq k_{2}\right)

    This function then takes :math:`k_{1}` as the the dissociation :math:`k_{off}`, and calculates the residence time as
    :math:`\tau=1 / k_{o f f}`.

    This function also measures the :math:`r^{2}` of the biexponential fitting to the survival function to show the
    quality of the :math:`k_{off}` estimation. In addition, it bootstraps the contact durations and measures the
    :math:`k_{off}` of the bootstrapped data, to report how well lipid contacts are sampled from simulations. The
    lipid contact sampling, the curve-fitting and the bootstrap results can be conveniently checked via the
    :math:`k_{off}` plot. The :math:`r^{2}`, :math:`\sigma(t)` and bootstrapped data are stored in the returned data
    ``properties``.

    Parameters
    ----------
    durations : array_like
            A list of interaction durations

    t_total : scalar
            The duration, or the longest if using multiple simulations of different durations, of the
            simulation trajectories. Should be in the same time unit as durations.

    timestep : scalar
            :math:`\Delta t` of the survival function :math:`\sigma`. Often takes the time step of the simulation
            trajectories or multiples of the trajectory time step. Should be in the same time unit as durations.

    nbootstrap : int, optional, default=10
            Number of bootstrapping. The default is 10.

    initial_quess : list, optional, default=(1., 1., 1., 1.)
            The initial guess for fitting of a bi-exponential curve to the survival function. Used by
            `scipy.optimize.curve_fit <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html>`_.

    cap : bool, optional, default=True
            Cap the returned residence time to ``t_total``. This is useful for cases of poor samplings where the curve fitting
            may be bad and the calculated residence times may be unrealistically large.

    Returns
    ----------
    koff : scalar
            The calculated koff. In the unit of :math:`{timeunit^{-1}}` in which :math:`{timeunit}` is the same as
            what is used in ``durations``.

    res_time : scalar
            The calculated residence time. In the same time unit as used by ``durations``.

    properties : dict
            A dictionary of all the computed values, including the original and bootstrapped koffs, residence times, ks
            of the bi-expo curve :math:`y=A*e^{(-k_1*x)}+B*e^{(-k_2*x)}` and :math:`R^2`.

    See also
    -----------
    pylipid.plot.plot_koff
            Plotting function for interaction durations and the calculated survival function.
    pylipid.api.LipidInteraction.compute_residue_koff
        Calculate interaction koff and residence time for residues.
    pylipid.api.LipidInteraction.compute_site_koff
        Calculate interaction koff and residence time for binding sites.

    References
    -----------
    .. [1] García, Angel E.Stiller, Lewis. Computation of the mean residence time of water in the hydration shells
           of biomolecules. 1993. Journal of Computational Chemistry.

    """
    # calculate original residence time
    delta_t_list = np.arange(0, t_total, timestep)
    survival_func = cal_survival_func(durations, np.max(t_total), delta_t_list)
    survival_rates = np.array([survival_func[delta_t] for delta_t in delta_t_list])
    res_time, _, r_squared, params = _curve_fitting(survival_func, delta_t_list, initial_guess)
    if cap and res_time > t_total:
        res_time = t_total
    n_fitted = _bi_expo(np.array(delta_t_list), *params)
    r_squared = 1 - np.sum((np.nan_to_num(n_fitted) - np.nan_to_num(survival_rates)) ** 2) / np.sum(
        (survival_rates - np.mean(survival_rates)) ** 2)
    ks = [abs(k) for k in params[:2]]
    ks.sort() # the smaller k is considered as koff

    # calculate bootstrapped residence time
    if nbootstrap > 0:
        duration_boot_set = [np.random.choice(durations, size=len(durations)) for dummy in range(nbootstrap)]
        ks_boot_set = []
        r_squared_boot_set = []
        survival_rates_boot_set = []
        n_fitted_boot_set = []
        for duration_boot in duration_boot_set:
            survival_func_boot = cal_survival_func(duration_boot, np.max(t_total), delta_t_list)
            survival_rates_boot = np.array([survival_func_boot[delta_t] for delta_t in delta_t_list])
            _, _, r_squared_boot, params_boot = _curve_fitting(survival_func_boot, delta_t_list,
                                                                                                initial_guess)
            n_fitted_boot = _bi_expo(np.array(delta_t_list), *params_boot)
            r_squared_boot = 1 - np.sum((np.nan_to_num(n_fitted_boot) - np.nan_to_num(survival_rates_boot)) ** 2) / np.sum(
                (survival_rates_boot - np.mean(survival_rates_boot)) ** 2)
            ks_boot = [abs(k) for k in params_boot[:2]]
            ks_boot.sort()
            ks_boot_set.append(ks_boot)
            r_squared_boot_set.append(r_squared_boot)
            survival_rates_boot_set.append(survival_rates_boot)
            n_fitted_boot_set.append(n_fitted_boot)
    else:
        ks_boot_set = [0]
        r_squared_boot_set = [0]
        survival_rates_boot_set = [0]
        n_fitted_boot_set = [0]

    properties = {"ks": ks, "res_time": res_time, "delta_t_list": delta_t_list,
                  "survival_rates": survival_rates, "survival_rates_boot_set": survival_rates_boot_set,
                  "n_fitted": n_fitted, "n_fitted_boot_set": n_fitted_boot_set,
                  "ks_boot_set": ks_boot_set,
                  "r_squared": r_squared, "r_squared_boot_set": r_squared_boot_set}

    return ks[0], res_time, properties


def cal_survival_func(durations, t_total, delta_t_list):
    r"""Compute the normalised survival function.

    Calculate the normalized survival time correlation function of the given list of durations.
    The survival time correlation function σ(t) is calculated as follow

    .. math::

        \sigma(t) = \frac{1}{N_{j}} \frac{1}{T-t} \sum_{j=1}^{N_{j}} \sum_{v=0}^{T-t}\tilde{n}_{j}(v, v+t)

    where T is the length of the simulation trajectory, :math:`N_{j}` is the total number of lipid contacts and
    :math:`\sum_{v=0}^{T-t} \tilde{n}_{j}(v, v+t)` is a binary function that takes the value 1 if the contact of
    lipid j lasts from time ν to time v+t and 0 otherwise. The values of :math:`\sigma(t)` are calculated for every
    value of t from 0 to T ns, for each time step of the trajectories, and normalized by dividing by :math:`\sigma(t)`,
    so that the survival time-correlation function has value 1 at t = 0.

    Parameters
    -----------
    durations : array_like
            A list of contact durations.

    t_total : scalar
            The duration or length, or the longest if using multiple simulations of different durations/lengths, of the
            simulation trajectories. Should be in the same time unit as durations.

    delta_t_list : array_like
            The list of :math:`\Delta t` for the survival function :math:`\sigma` to check the interaction survival rate.

    Returns
    -----------
    survival_func : dict
            The survival function :math:`\sigma` stored in a dictionary {delta_t: survival rate}.

    See also
    -----------
    pylipid.func.cal_koff
        Calculate residence time and koff.

    """
    num_of_contacts = len(durations)
    survival_func = {}
    for delta_t in delta_t_list:
        if delta_t == 0:
            survival_func[delta_t] = 1
            survival_func0 = float(sum([res_time - delta_t for res_time in durations if res_time >= delta_t])) / \
                     ((t_total - delta_t) * num_of_contacts)
        else:
            try:
                survival_func[delta_t] = float(sum([res_time - delta_t for res_time in durations if res_time >= delta_t])) / \
                                 ((t_total - delta_t) * num_of_contacts * survival_func0)
            except ZeroDivisionError:
                survival_func[delta_t] = 0
    return survival_func


def _curve_fitting(survival_func, delta_t_list, initial_guess):
    """Fit the exponential curve :math:`y=Ae^{-k_1\Delta t}+Be^{-k_2\Delta t}`"""
    survival_rates = np.nan_to_num([survival_func[delta_t] for delta_t in delta_t_list]) # y
    try:
        popt, pcov = curve_fit(_bi_expo, np.array(delta_t_list), np.array(survival_rates), p0=initial_guess, maxfev=100000)
        n_fitted = _bi_expo(np.array(delta_t_list, dtype=np.float128), *popt)
        r_squared = 1 - np.sum((np.nan_to_num(n_fitted) -
                                np.nan_to_num(survival_rates))**2)/np.sum((survival_rates - np.mean(survival_rates))**2)
        ks = [abs(k) for k in popt[:2]]
        koff = np.min(ks)
        res_time = 1/koff
    except RuntimeError:
        koff = 0
        res_time = 0
        r_squared = 0
        popt = [0, 0, 0, 0]
    return res_time, koff, r_squared, popt


def _bi_expo(x, k1, k2, A, B):
    """The exponential curve :math:`y=Ae^{-k_1\Delta t}+Be^{-k_2\Delta t}`"""
    return A*np.exp(-k1*x) + B*np.exp(-k2*x)


def calculate_koff_wrapper(durations, title, fn, t_total=None, timestep=1, nbootstrap=10,
                           initial_guess=[1., 1., 1., 1.], plot_data=True, timeunit="us", fig_close=True):
    """Wrapper function that calculates koff and plot koff. """
    if np.sum(durations) == 0:
        koff = 0
        res_time = 0
        r_squared = 0
        koff_boot = 0
        r_squared_boot = 0
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            koff, res_time, properties = cal_koff(durations, t_total, timestep, nbootstrap, initial_guess)
        r_squared = properties["r_squared"]
        koff_boot = np.mean(properties["ks_boot_set"], axis=0)[0]
        r_squared_boot = np.mean(properties["r_squared_boot_set"])
        if plot_data:
            text = _format_koff_text(properties, timeunit)
            plot_koff(durations, properties["delta_t_list"], properties["survival_rates"],
                      properties["n_fitted"], survival_rates_bootstraps=properties["survival_rates_boot_set"],
                      fig_fn=fn, title=title, timeunit=timeunit, t_total=t_total, text=text, fig_close=fig_close)
    return koff, res_time, r_squared, koff_boot, r_squared_boot


def _format_koff_text(properties, timeunit):
    """Format text for koff plot. """
    tu = "ns" if timeunit == "ns" else r"$\mu$s"
    text = "{:18s} = {:.3f} {:2s}$^{{-1}} $\n".format("$k_{{off1}}$", properties["ks"][0], tu)
    text += "{:18s} = {:.3f} {:2s}$^{{-1}} $\n".format("$k_{{off2}}$", properties["ks"][1], tu)
    text += "{:14s} = {:.4f}\n".format("$R^2$", properties["r_squared"])
    ks_boot_avg = np.mean(properties["ks_boot_set"], axis=0)
    cv_avg = 100 * np.std(properties["ks_boot_set"], axis=0) / np.mean(properties["ks_boot_set"], axis=0)
    text += "{:18s} = {:.3f} {:2s}$^{{-1}}$ ({:3.1f}%)\n".format("$k_{{off1, boot}}$", ks_boot_avg[0],
                                                                 tu, cv_avg[0])
    text += "{:18s} = {:.3f} {:2s}$^{{-1}}$ ({:3.1f}%)\n".format("$k_{{off2, boot}}$", ks_boot_avg[1],
                                                                 tu, cv_avg[1])
    text += "{:14s} = {:.4f}\n".format("$R^2$$_{{boot}}$", np.mean(properties["r_squared_boot_set"]))
    text += "{:18s} = {:.3f} {:2s}".format("$Res. Time$", properties["res_time"], tu)
    return text