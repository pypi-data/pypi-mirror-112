import numpy as np
import pytest

import probnum.problems.zoo.diffeq as diffeq_zoo
from probnum import diffeq, randprocs, randvars, statespace

from ._known_initial_derivatives import LV_INITS, THREEBODY_INITS

# Jax dependency handling
# pylint: disable=unused-import
try:
    import jax
    import jax.numpy as jnp
    from jax.config import config

    config.update("jax_enable_x64", True)

    JAX_AVAILABLE = True

except ImportError:
    JAX_AVAILABLE = False


# Pytest decorators to select tests for each case
only_if_jax_available = pytest.mark.skipif(not JAX_AVAILABLE, reason="requires jax")


@pytest.fixture
def order():
    return 5


@pytest.fixture
def lv():
    y0 = np.array([20.0, 20.0])

    # tmax is ignored anyway
    return diffeq_zoo.lotkavolterra(t0=0.0, tmax=np.inf, y0=y0)


@pytest.fixture
def lv_inits(order):
    lv_dim = 2
    vals = LV_INITS[: lv_dim * (order + 1)]
    return statespace.Integrator._convert_derivwise_to_coordwise(
        vals, ordint=order, spatialdim=lv_dim
    )


def test_initialize_with_rk(lv, lv_inits, order):
    """Make sure that the values are close(ish) to the truth."""
    ode_dim = len(lv.y0)
    prior = statespace.IBM(
        ordint=order,
        spatialdim=ode_dim,
        forward_implementation="sqrt",
        backward_implementation="sqrt",
    )
    initrv = randvars.Normal(
        np.zeros(prior.dimension),
        np.eye(prior.dimension),
        cov_cholesky=np.eye(prior.dimension),
    )
    prior_process = randprocs.MarkovProcess(
        transition=prior, initrv=initrv, initarg=lv.t0
    )
    received_rv = diffeq.initialize_odefilter_with_rk(
        lv.f,
        lv.y0,
        lv.t0,
        prior_process=prior_process,
        df=lv.df,
        h0=1e-1,
        method="RK45",
    )
    # Extract the relevant values
    expected = lv_inits

    # The higher derivatives will have absolute difference ~8%
    # if things work out correctly
    np.testing.assert_allclose(received_rv.mean, expected, rtol=0.25)
    assert np.linalg.norm(received_rv.std) > 0


@pytest.mark.parametrize("any_order", [0, 1, 2])
@only_if_jax_available
def test_initialize_with_taylormode(any_order):
    """Make sure that the values are close(ish) to the truth."""
    r2b_jax = diffeq_zoo.threebody_jax()
    ode_dim = 4
    expected = statespace.Integrator._convert_derivwise_to_coordwise(
        THREEBODY_INITS[: ode_dim * (any_order + 1)],
        ordint=any_order,
        spatialdim=ode_dim,
    )

    prior = statespace.IBM(
        ordint=any_order,
        spatialdim=ode_dim,
        forward_implementation="sqrt",
        backward_implementation="sqrt",
    )

    initrv = randvars.Normal(np.zeros(prior.dimension), np.eye(prior.dimension))
    prior_process = randprocs.MarkovProcess(
        transition=prior, initrv=initrv, initarg=r2b_jax.t0
    )

    received_rv = diffeq.initialize_odefilter_with_taylormode(
        r2b_jax.f, r2b_jax.y0, r2b_jax.t0, prior_process=prior_process
    )

    np.testing.assert_allclose(received_rv.mean, expected)
    np.testing.assert_allclose(received_rv.std, 0.0)
