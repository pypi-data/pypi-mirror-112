from jijzept.sampler import JijZeptSampler
from jijzept.sampler.jijmodel_post import JijModelingInterface
from jijzept.entity.schema import SolverType

from typing import Dict, Union
from numbers import Number
from jijmodeling.expression.expression import Expression
import numpy as np
from typing import Any


class JijSQASampler(JijZeptSampler, JijModelingInterface):
    solver_type             = SolverType(queue_name='openjijsolver', solver='SQA')
    jijmodeling_solver_type = SolverType(queue_name='openjijsolver', solver='SQAParaSearch')

    def sample(self, bqm, beta=1.0, gamma=1.0, trotter=4,
               num_reads=1, num_sweeps=100, timeout=None, sync=True) -> Any:
        """Samples ising.
        
        Args:
            bqm (:obj:`dimod.BinaryQuadraticModel`): Binary quadratic model.
            beta (float, optional): Inverse temperature. Defaults to 1.0.
            gamma (float, optional): Minimum beta (initial beta in SA).
            trotter (int, optional): Number of trotter slices. should be even.
            num_reads (int, optional): Number of samples. Defaults to 1.
            num_sweeps (int, optional): Number of MonteCarlo steps
            timeout (float, optional): Number of timeout for post request. Defaults to None.

        Returns:
            :obj:`dimod.SampleSet`: Stores minimum energy samples. `.info['energy']` stores all sample energies.
        """

        # number of trotter should be even
        # since c++ implementation
        if trotter % 2 == 1:
            raise ValueError('trotter number should be even.')

        return super().sample(
            bqm, num_reads=num_reads, num_sweeps=num_sweeps,
            gamma=gamma, trotter=trotter, beta=beta,
            timeout=timeout,
            sync=sync
        )

    def sample_model(
            self,
            model: Expression,
            feed_dict: Dict[str, Union[Number, list, np.ndarray]],
            multipliers: Dict[str, Number],
            search: bool=False, timeout=10,
            num_reads:int = 1,
            num_sweeps:int = 100,
            beta=1.0, gamma=1.0, trotter=4,
            sync=True,
        ):

        return super().sample_model(
            model,
            feed_dict=feed_dict,
            multipliers=multipliers,
            search=search,
            sync=sync,
            num_reads=num_reads, num_sweeps=num_sweeps,
            beta=beta, gamma=gamma, trotter=trotter
        )
