"""Functions to prune models and select better ones."""
from typing import List, Optional
from math import exp

import feyn
from ._config_evolution_params import _HalfLife_params

def prune_models(
    models: List[feyn.Model],
    keep_n: Optional[int] = None,
) -> List[feyn.Model]:
    """Prune a list of models to remove redunant and poorly performing ones.

    Arguments:
        models {List[feyn.Model]} -- The list of models to prune.

    Keyword Arguments:
        keep_n {Optional[int]} -- At most this many models will be returned. If None, models are left to be pruned by other redundancies. (default: {None})

    Returns:
        List[feyn.Model] -- The list of pruned models.
    """
    max_model_density = 4000

    res = []
    hashes = set()

    if keep_n is None:
        keep_n = len(models)

    # Select best three unique models
    for i, m in enumerate(models):
        model_hash = hash(m)
        if model_hash in hashes:
            continue
        res.append(m)
        if len(res) >= 3:
            break

    for m in models[i + 1 :]:
        if len(res) == keep_n:
            break

        # Check for duplicate structure
        model_hash = hash(m)+m.qid
        if model_hash in hashes:
            continue

        """Calculate the half-life of the model and decide if it should die."""
        A0 = _HalfLife_params.get("A0", 100)
        n = _HalfLife_params.get("n", 7)
        tau = _HalfLife_params.get("tau", 0.693)
        if m.age > A0 * exp(-len(res) / (max_model_density / (n * tau))) + 1:
            continue

        hashes.add(model_hash)
        res.append(m)

    return res


def best_diverse_models(
    models: List[feyn.Model],
    n: int = 10,
) -> List[feyn.Model]:
    """Separate the n best performing models from a collection, such that they are sufficiently diverse in the context of some distance function.

    Arguments:
        models {List[feyn.Model]} -- The list of models to find the best ones in.

    Keyword Arguments:
        n {int} -- The maximum number of best models to identify. (default: {10})

    Returns:
        List[feyn.Model] -- The best models from each qcell.
    """

    res = []
    qids = set()
    for m in models:
        if m.qid not in qids:
            qids.add(m.qid)
            res.append(m)

        if len(res) >= n:
            break
    return res

