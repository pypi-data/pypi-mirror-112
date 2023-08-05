from typing import Dict, List, Optional
from jijzept.sampler import JijZeptSampler
from jijzept.entity.schema import SolverType
from jijzept.response import DimodResponse


class JijDWaveSampler(JijZeptSampler):
    solver_type = SolverType(queue_name='dwavesolver', solver='DWave')

    def sample(
            self,
            bqm,
            num_reads: Optional[int] = 1,
            annealing_time: Optional[float] = None,
            auto_scale: Optional[bool] = False,
            sync=True
            )->DimodResponse:
        """Samples by D-Wave Sampler

        Args:
            bqm (dimod.BinaryQuadraticModel): Binary quadratic model.
            num_reads (Optional[int], optional): number of annealing sample. Defaults to 1.
            annealing_time (Optional[float], optional): quantum annealing time [μs]. Defaults to None.
            auto_scale (Optional[bool], optional): auto scale strength of interaction. Defaults to False.
            sync (bool): set sync mode.

        Returns:
            Response
        """

        params = dict(
            num_reads = num_reads,
            annealing_time = annealing_time,
            auto_scale = auto_scale,
            sync = sync,
        )
        return super().sample(bqm, **params)
