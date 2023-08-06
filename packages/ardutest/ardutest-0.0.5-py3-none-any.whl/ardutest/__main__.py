from hashlib import md5
from json import dump as json_dump
from logging import getLogger, INFO, DEBUG, basicConfig
from sys import stdout
from typing import List, TypedDict, Sequence

from click import command, argument, option
from staliro import staliro
from staliro.optimizers import Iteration

from .blackbox import ardupilot_blackbox_factory
from .module import load_module

logger = getLogger("ardutest")

class IterationDict(TypedDict, total=False):
    sample: List[float]
    robustness: float
    sample_hash: str


class RunDict(TypedDict):
    run: int
    iterations: List[IterationDict]


def _iter_dict(iteration: Iteration, include_hash: bool = False) -> IterationDict:
    if not include_hash:
        return IterationDict(
            sample=list(iteration.sample),
            robustness=iteration.robustness,
        )

    return IterationDict(
        sample=list(iteration.sample),
        robustness=iteration.robustness,
        sample_hash=md5(iteration.sample.tobytes()).hexdigest(),
    )


def _run_dict(num: int, history: Sequence[Iteration], include_hash: bool = False) -> RunDict:
    return RunDict(run=num, iterations=[_iter_dict(iteration, include_hash) for iteration in history])


@command()
@option("-v", "--verbose", is_flag=True)
@option("-o", "--outfile", default="results.json")
@argument("module_name")
def ardutest(verbose: bool, outfile: str, module_name: str) -> None:
    basicConfig(stream=stdout, level=DEBUG if verbose else INFO)
    getLogger("urllib3").level = INFO
    getLogger("docker").level = INFO

    module = load_module(module_name)
    blackbox = ardupilot_blackbox_factory(module.config, module.stack_config, module.mission_factory)

    logger.debug("Configuring destination directories")

    log_dest = module.config.log_dest
    if log_dest is not None and not log_dest.is_dir():
        log_dest.mkdir()

    mission_dest = module.config.mission_dest
    if mission_dest is not None and not mission_dest.is_dir():
        mission_dest.mkdir()

    result = staliro(module.specification, blackbox, module.options, module.optimizer)
    
    include_hash = module.config.mission_dest is not None or module.config.log_dest is not None
    json_objs = [_run_dict(num, run.history, include_hash) for num, run in enumerate(result.runs)]

    with open(outfile, "w") as results_file:
        json_dump(json_objs, results_file)


if __name__ == "__main__":
    ardutest()
