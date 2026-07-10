import numpy as np
import sympy as sp
import scipy as sc
import mpmath
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from IPython.display import display, Math, Latex

def fix_axes(ax=None):
    if ax is None:
        ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    xl = ax.get_xlim()
    if xl[0] < 0 < xl[1]:
        ax.spines['left'].set_position('zero')
    yl = ax.get_ylim()
    if yl[0] < 0 < yl[1]:
        ax.spines['bottom'].set_position('zero')
    return ax

def use_pi_ticks(ax):
    ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter(r'%g $\pi$'))
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=1))
