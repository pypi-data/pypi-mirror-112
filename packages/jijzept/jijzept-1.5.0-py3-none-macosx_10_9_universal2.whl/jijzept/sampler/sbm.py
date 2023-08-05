from jijzept.sampler import JijZeptSampler
from jijzept.entity.schema import SolverType
from typing import Any

class JijSBMSampler(JijZeptSampler):
    solver_type = SolverType(queue_name='sbmsolver', solver='SBM')

    def sample(self, bqm,
        steps=0,
        loops=1,
        timeout=None,
        maxwait=None,
        target=None,
        prefer='auto',
        stats='none',
        dt=0.1,
        C=None,
        sync=True
    ) -> Any:
        """Samples by SBM.

        Args:
            bqm (:obj:`dimod.BinaryQuadraticModel`): Binary quadratic model.
            steps (int, optional): The number of steps in SBM calculation. If `steps` is set to `0`, then the number of steps is set automatically. Defaults to 0.
            loops (int, optional): The number of loops in SBM calculation. If `loops` is set to `0`, then calculation will be repeated to the maximum calculation time. Defaults to 1.
            timeout (int, optional): The maximum calculation time in seconds. Defaults to None.
            maxwait (int, optional): The maximum waiting time in seconds. Defaults to None.
            target (float, optional): The end condition of calculation. Defaults to None.
            prefer (str, optional): Select `'speed'` or `'auto'`. Defaults to 'auto'.
            stats (str, optional): Select `'none'`, `'summary'`, or `'full`. Defaults to 'none'.
            dt (float, optional): Time step width. Defaults to 0.1.
            C (float, optional): Positive constant coefficient. If `0` is set to `C`, then the value of `C` is set automatically. Defaults to 0.
            sync (bool, optional): Synchronization mode. Defaults to True.

        Returns:
            :obj:`dimod.SampleSet`: Stores minimum energy sample.

        """
        return super().sample(
            bqm,
            steps=steps,
            loops=loops,
            timeout=timeout,
            maxwait=maxwait,
            target=target,
            prefer=prefer,
            stats=stats,
            dt=dt,
            C=C,
            sync=sync
        )
