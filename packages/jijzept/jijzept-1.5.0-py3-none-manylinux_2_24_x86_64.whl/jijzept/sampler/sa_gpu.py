from jijzept.sampler.jijmodel_post import JijModelingInterface
from jijzept.sampler import JijZeptSampler
from jijzept.entity.schema import SolverType
from jijmodeling.expression.expression import Expression
from typing import Any

class JijGPUSASampler(JijZeptSampler, JijModelingInterface):
    solver_type             = SolverType(queue_name='masolver', solver='GPUSA')
    jijmodeling_solver_type = SolverType(queue_name='masolver', solver='GPUSAParaSearch')

    def sample(self, bqm,
               beta_min=None, beta_max=None,
               num_reads=1, num_sweeps=1000,
               dimension=None,
               timeout=None, sync=True) -> Any:
        """Samples ising.

        Args:
            bqm (:obj:`dimod.BinaryQuadraticModel`): Binary quadratic model.
            beta_min (float, optional): Minimum beta (initial beta in SA).
            beta_max (float, optional): Maximum beta (final beta in SA).
            num_reads (int, optional): Number of samples. Defaults to 1.
            num_sweeps (int, optional): Number of MonteCarlo steps.
            timeout (float optional): Number of timeout for post request. Defaults to None.

        Returns:
            :obj:`dimod.SampleSet`: Stores minimum energy samples. `.info['energy']` stores all sample energies.
        """

        if beta_min and beta_max:
            if beta_min > beta_max:
                raise ValueError('beta_min < beta_max')

        return super().sample(
            bqm, num_reads=num_reads, num_sweeps=num_reads,
            beta_min=beta_min, beta_max=beta_max,
            timeout=timeout,
            dimension=dimension,
            sync=sync
        )


    def sample_model(self,
                     model: Expression,
                     feed_dict: dict,
                     multipliers: dict,
                     search: bool = False,
                     beta_min=None, beta_max=None,
                     num_reads=1, num_sweeps=1000,
                     dimension=None,
                     timeout=None, sync=True):

        if beta_min and beta_max:
            if beta_min > beta_max:
                raise ValueError('beta_min < beta_max')

        return super().sample_model(
            model,
            feed_dict=feed_dict,
            multipliers=multipliers,
            search=search,
            num_reads=num_reads,
            num_sweeps=num_sweeps,
            beta_min=beta_min, beta_max=beta_max,
            timeout=timeout,
            dimension=dimension,
            sync=sync
        )
