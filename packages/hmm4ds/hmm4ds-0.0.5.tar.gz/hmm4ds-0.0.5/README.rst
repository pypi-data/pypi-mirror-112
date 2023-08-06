Hidden Markov Models
====================

HMM provides python3 code that implements the following algorithms
for hidden Markov models:

Forward: Recursive estimation of state probabilities at each time t,
	 given observation likelihoods for times 1 to t

Backward: Combined with Forward, provides estimates of state
	  probabilities at each time given _all_ of the observation
	  likelihoods

Train: Implements Baum Welch algorithm which finds a local maximum of
       likelihood of model parameters

Decode: Implements Viterbi algorithm for finding the most probable
	state sequence

Implementations of the above algrithms are independent of the
observation model.  HMM enables users to implement any observation
model by writing code for a class that provides methods for
calculating the likelihood of an observation given a state and for
reestimating model parameters given observations and state
likelihoods.

HMM includes implementations of the following observation models:

IntegerObservation: Integers in a finite range

Gauss: Floats with state dependent mean and variance

GaussMAP: Like Gauss but uses maximum a posteriori probability
estimation

MultivariateGaussian: Like GaussMAP but observations are vectors of
floats

AutoRegressive: Like GaussMAP but with linear autoregressive forecast
and Gaussian residual

Observation_with_bundles: Observations that can include classification data

I (Andy Fraser) restarted this project on 2021-01-22.  I will rewrite
the code for my book "Hidden Markov Models and Dynamical Systems"
using the following tools: python3, make, numpy, scipy, sphinx, pytest, qt5

and not using: gnuplot, swig, c, scons

I will sacrifice the appearance of plots to simplicity of the code.  I
hope that the scipy sparse matrix package will let me have simple fast
code.  I will choose simplicity over speed within reason.

I am developing in an environment defined by nix (see nixos.org).

I will use a single brief LaTeX document instead of the text that SIAM
owns to collect all of the figures.

You can redistribute and/or modify hmm under the terms of the GNU
General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later
version.  See the file "License" in the root directory of the
hmm distribution.

# Local Variables:
# mode: rst
# End:
