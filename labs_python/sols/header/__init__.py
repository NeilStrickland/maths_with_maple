import numpy as np
import sympy as sp
import scipy as sc
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
from IPython.display import display, HTML, Math, Latex

def move_legend(fig, x = 0.5, y=1):
    fig.update_layout(legend=dict(yanchor="top",y=y,xanchor="center",x=x))

def equal_aspect(fig):
    fig.update_yaxes(scaleanchor="x",scaleratio=1)

def use_pi_ticks(fig, k0=-1, k1=1, d = 1, x0=None, x1=None):
    if x0 is not None:
        k0 = sp.Rational(int(np.ceil(x0*d/np.pi)),d)
    if x1 is not None:
        k1 = sp.Rational(int(np.floor(x1*d/np.pi)),d)
    ticks = [sp.Rational(i,d) * sp.pi for i in range(int(k0*d),int(k1*d)+1)]
    tickvals = [float(tick) for tick in ticks]
    ticktext = [f"${sp.latex(tick)}$" for tick in ticks]
    fig.update_xaxes(tickvals=tickvals, ticktext=ticktext)

pio.templates['maths'] = go.layout.Template(
 layout = go.Layout(
  margin=dict(l=0, r=0, t=20, b=20),
  xaxis = dict(zeroline=True, zerolinewidth=1, zerolinecolor='black'),
  yaxis = dict(zeroline=True, zerolinewidth=1, zerolinecolor='black')
 )
)

pio.templates.default = 'plotly+maths'
plotly.offline.init_notebook_mode()
display(HTML(
    '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_SVG"></script>'
))