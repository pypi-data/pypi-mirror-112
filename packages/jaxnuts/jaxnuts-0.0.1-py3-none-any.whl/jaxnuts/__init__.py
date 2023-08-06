"""jaxnuts

A python implementation of the No U-turn sampler from [Hoffman and Gelman, 2011](https://arxiv.org/pdf/1111.4246.pdf), Algorithm 6,
using JAX to speed up the the code.

**NOTE:** For low-dimensional problems, GPU overhead is not negligible. In this case, forcing JAX to run on the CPU 
results in significant performance increase. This can be achieved either by calling `jaxnuts.sampler.force_cpu()` 
right after importing the module, or alternatively `jax.config.update('jax_platform_name', 'cpu')` right after importing JAX.
"""