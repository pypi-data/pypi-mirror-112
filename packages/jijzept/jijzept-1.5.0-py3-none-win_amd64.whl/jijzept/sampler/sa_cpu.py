from jijzept.sampler import JijZeptSampler
from jijzept.sampler.jijmodel_post import JijModelingInterface
from jijzept.entity.schema import SolverType

from typing import Dict, Union
from numbers import Number
from jijmodeling.expression.expression import Expression
import numpy as np
from typing import Any


class JijSASampler(JijZeptSampler, JijModelingInterface):
    solver_type             = SolverType(queue_name='openjijsolver', solver='SA')
    hubo_solver_type        = SolverType(queue_name='openjijsolver', solver='HUBOSA')
    jijmodeling_solver_type = SolverType(queue_name='openjijsolver', solver='SAParaSearch')

    def sample(self, bqm,
               beta_min=None, beta_max=None,
               num_reads=1, num_sweeps=100,
               timeout=None, sync=True) -> Any:
        """Samples ising

        Args:
            bqm (:obj:`dimod.BinaryQuadraticModel`): Binary quadratic model.
            beta_min (float, optional): Minimum beta (initial beta in SA).
            beta_max (float, optional): Maximum beta (final beta in SA).
            num_reads (int, optional): Number of samples. Defaults to 1.
            num_sweeps (int, optional): Number of MonteCarlo steps.
            timeout (float, optional): Number of timeout for post request. Defaults to None.

        Returns:
            :obj:`dimod.SampleSet`: Stores minimum energy samples. `.info['energy']` stores all sample energies.
        """

        return super().sample(
            bqm, num_reads=num_reads, num_sweeps=num_sweeps, timeout=timeout,
            beta_min=beta_min, beta_max=beta_max,
            sync=sync
        )

    def sample_hubo(self, polynomial, vartype,
               beta_min=None, beta_max=None,
               num_reads=1, num_sweeps=100,
               timeout=None, sync=True) -> Any:

        return super().sample_hubo(
            polynomial, num_reads=num_reads, num_sweeps=num_sweeps, vartype=vartype, timeout=timeout,
            beta_min=beta_min, beta_max=beta_max,
            sync=sync
        )

                    


    def sample_model(self, 
                    model: Expression, 
                    feed_dict: Dict[str, Union[Number, list, np.ndarray]], 
                    multipliers: Dict[str, Number], 
                    search: bool=False, timeout=10,
                    num_reads:int = 1,
                    num_sweeps:int = 100,
                    beta_min=None, beta_max=None,
                    sync=True
                    ):

        return super().sample_model(
            model,
            feed_dict=feed_dict, 
            multipliers=multipliers,
            search=search,
            sync=sync,
            num_reads=num_reads, num_sweeps=num_sweeps,
            beta_min=beta_min, beta_max=beta_max
        )
