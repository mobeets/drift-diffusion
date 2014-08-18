
__Goal__: Simulating drift diffusion processes with varying drift and diffusion rates.
__Why__: To model 2AFC discrimination decisions in trials of varying stimulus strengths and durations.

## The model

On a given time step, a particle's next position is a sample from a gaussian with mean mu ("drift rate") and standard deviation sigma ("diffusion rate").

x(t+1) = x(t) + N(mu, sigma)

Also, if at any time t0 a particle reaches either the upper or lower bound, x(t+1) = x(t) for all t > t0.

In the decision model, each trial's decision is a function of the position of a single particle, where its drift rate is proportional to the signal strength on that trial. In a trial of duration t, the subject responds "Signal present / Yes" if x(t) > 0, and "Signal absent / No" otherwise. (Note that in this simulation the drift rates are all positive, and the correct response is always "Signal present / Yes".)

In the image below, the plot is of all simulated particle positions as a function of time, x(t), where warmer colors represent drift rates closer to zero.

![particles](/images/particles.png?raw=true "particles")

## Accuracy as a function of stimulus strength

__Usage__: `python sim_sat_exp.py`

The image below shows the subjects' accuracy as a function of stimulus duration, where each color represents varying drift rates. Note how the subject's accuracy saturates with increased time, where accuracy at lower stimulus strengths may not ever reach perfect accuracy. The curves are fits of the data to a saturating exponential with two parameters: the time constant, tau, and the saturating accuracy.

![sat-exp](/images/sat_exp.png?raw=true "sat-exp")

## Accuracy as a function of stimulus duration

__Usage__: `python sim_pmf.py`

![pmf](/images/pmf.png?raw=true "pmf")
