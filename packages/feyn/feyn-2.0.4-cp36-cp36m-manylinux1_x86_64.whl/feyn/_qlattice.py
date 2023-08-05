"""Classes and functions to interact with a remote QLattice."""

from os import cpu_count
from typing import Dict, List, Optional, Set, Iterable, Union, Callable
from urllib.parse import urlparse
import requests

import numpy as np

import _feyn
import feyn

from feyn import Model
from feyn.losses import _get_loss_function
from ._config import (
    DEFAULT_SERVER,
    PROVISIONING_SERVER,
    Config,
    resolve_config,
    resolve_config_failed_message,
)
from ._httpclient import HttpClient
from ._register import RegisterCollection
from ._snapshots import SnapshotCollection


class QLattice:
    """Class for representing a remote QLattice connection."""

    def __init__(self, cfg: Config):
        """Construct a new 'QLattice' object."""
        headers = {
            "Authorization": f'Bearer {cfg.api_token or "none"}',
            "User-Agent": f"feyn/{feyn.__version__}",
        }

        qlattice_server = cfg.server.rstrip("/")
        api_base_url = f"{qlattice_server}/api/v1/qlattice/{cfg.qlattice}"
        self._http_client = HttpClient(api_base_url, headers)

        self._load_qlattice()

        self._snapshots = SnapshotCollection(self)
        self._registers = RegisterCollection(self)

    def __repr__(self):
        return "<Abzu QLattice[%i,%i] '%s'>" % (
            self.width,
            self.height,
            self._http_client.api_base_url,
        )

    @property
    def snapshots(self):
        """
        Collection of snapshots for this QLattice

        Use this collection to capture, list and restore the complete state of a QLattice.
        """
        return self._snapshots

    @property
    def registers(self):
        """
        The RegisterCollection of the QLattice

        The RegisterCollection is used to find, create and remove registers from the QLattice.
        """
        return self._registers

    def sample_models(
        self,
        input_names: List[str],
        output_name: str,
        kind: str = "regression",
        stypes: Optional[Dict[str, str]] = None,
        max_complexity: int = 10,
        query_string: Optional[str] = None,
        function_names: Optional[List[str]] = None,
    ) -> List[Model]:
        """
        Sample models from the QLattice simulator. The QLattice has a probability density for generating different models, and this function samples from that density.

        Arguments:
            input_names {List[str]} -- The names of the input features.
            output_name {str} -- The name of the output feature.

        Keyword Arguments:
            kind {str} -- Specify the kind of models that are sampled. One of ["classification", "regression"]. (default: {"regression"})
            stypes {Optional[Dict[str, str]]} -- An optional map from feature names to semantic types. (default: {None})
            max_complexity {int} -- The maximum complexity for sampled models. Currently the maximum number of edges that the graph representation of the models has. (default: {10})
            query_string {Optional[str]} -- An optional query string for specifying specific model structures. (default: {None})
            function_names {Optional[List[str]]} -- A list of function names to use in the QLattice simulation. Defaults to all available functions being used. (default: {None})

        Returns:
            List[Model] -- The list of sampled models.
        """
        input_names = _sanitize_iterable(input_names)

        _validate_names(input_names, output_name)
        max_complexity = _validate_mc(max_complexity)

        if query_string and not isinstance(query_string, str):
            raise ValueError("query_string is not a string.")

        stypes = stypes or {}
        stypes[output_name] = _kind_to_output_stype(kind)

        if output_name not in input_names:
            input_names = input_names.copy()
            input_names.append(output_name)


        regmap = {}
        for reg in input_names:
            stype = stypes.get(reg, "f")

            if stype in ["cat", "categorical"]:
                stype = "c"
            if stype in ["float", "numerical"]:
                stype = "f"
            if stype in ["bool"]:
                stype = "b"
            if reg == output_name:
                pattern = f"out:*(*)->{stype}"
            else:
                pattern = f"in:*({stype})->*"

            regmap[reg] = pattern

        if function_names:
            specs = _build_spec_list(function_names)
        else:
            specs = _feyn.get_specs()

        models_json = self._generate(specs, regmap, max_complexity, query_string or "")
        return list(
            filter(
                lambda m: m.edge_count <= max_complexity, _models_from_json(models_json)
            )
        )

    def update(self, models: Union[Model, Iterable[Model]]) -> None:
        """Update QLattice with learnings from a list of models. When updated, the QLattice learns to produce models that are similar to what is included in the update. Without updating, the QLattice will keep generating models with a random structure.

        Arguments:
            models {Union[Model, Iterable[Model]]} -- The models to use in a QLattice update.
        """

        if isinstance(models, Model):
            models = [models]

        resp = self._http_client.post(
            "/update", json={"graphs": [m._to_dict() for m in models]}
        )

        resp.raise_for_status()

    def reset(self, random_seed: int = -1) -> None:
        """Clear all learnings in this QLattice.

        Keyword Arguments:
            random_seed {int} -- If not -1, seed the qlattice and feyn random number generator to get reproducible results. (default: {-1})
        """
        req = self._http_client.post("/reset", json={"seed": random_seed})
        req.raise_for_status()

        if random_seed != -1:
            np.random.seed(random_seed)
            _feyn.srand(random_seed)

        self._load_qlattice()

    def auto_run(
        self,
        data: Iterable,  # TODO: Typing!
        output_name: str,
        kind: str = "regression",
        stypes: Optional[Dict[str, str]] = None,
        n_epochs: int = 10,
        threads: Union[int, str] = "auto",
        max_complexity: int = 10,
        query_string: Optional[str] = None,
        loss_function: Optional[Union[str, Callable]] = None,  # TODO: Write test!
        criterion: Optional[str] = None,
        sample_weights: Optional[Iterable[float]] = None,
        function_names: Optional[List[str]] = None,
        starting_models: Optional[List[feyn.Model]] = None,
    ) -> List[feyn.Model]:
        """A convenience function for running the QLattice simulator for many epochs. This process can be interrupted with a KeyboardInterrupt, and you will get back the best models that have been found thus far. Roughly equivalent to the following:

        >>> models = []
        >>> for i in range(n_epochs):
        >>>     models += ql.sample_models(data, output_name, kind, stypes, max_complexity, query_string, function_names)
        >>>     models = feyn.fit_models(models, data, loss_function, criterion, None, sample_weights)
        >>>     models = feyn.prune_models(models)
        >>>     best = feyn.best_diverse_models(models)
        >>>     ql.update(best)

        Arguments:
            data {Iterable} -- The data to train models on. Feature names are inferred from the columns (pd.DataFrame) or keys (dict) of this variable.
            output_name {str} -- The name of the output feature.

        Keyword Arguments:
            kind {str} -- Specify the kind of models that are sampled. One of ["classification", "regression"]. (default: {"regression"})
            stypes {Optional[Dict[str, str]]} -- An optional map from feature names to semantic types. (default: {None})
            n_epochs {int} -- Number of training epochs. (default: {10})
            threads {int} -- Number of concurrent threads to use for fitting. If a number, that many threads are used. If "auto", set to your CPU count - 1. (default: {"auto"})
            max_complexity {int} -- The maximum complexity for sampled models. (default: {10})
            query_string {Optional[str]} -- An optional query string for specifying specific model structures. (default: {None})
            loss_function {Optional[Union[str, Callable]]} -- The loss function to optimize models for. If None (default), 'MSE' is chosen for regression problems and 'binary_cross_entropy' for classification problems. (default: {None})
            criterion {Optional[str]} -- Sort by information criterion rather than loss. Either "aic", "bic" or None. (default: {None})
            sample_weights {Optional[Iterable[float]]} -- An optional numpy array of weights for each sample. If present, the array must have the same size as the data set, i.e. one weight for each sample. (default: {None})
            function_names {Optional[List[str]]} -- A list of function names to use in the QLattice simulation. Defaults to all available functions being used. (default: {None})
            starting_models {Optional[List[feyn.Model]]} -- A list of preexisting feyn models you would like to start finding better models from. The inputs and output of these models should match the other arguments to this function. (default: {None})

        Returns:
            List[feyn.Model] -- The best models found during this run.
        """
        if loss_function is None:
            output_type = _kind_to_output_stype(kind)
            loss_function = _get_loss_function(output_type)

        if threads == "auto":
            # TODO: Is this sane?
            found = cpu_count()
            if found is None:
                threads = 4
            else:
                threads = cpu_count() - 1

        # TODO: Make immutable copy of starting models
        models = starting_models or []
        m_count = len(models)

        try:
            for i in range(n_epochs):
                new_sample = self.sample_models(
                    data,
                    output_name,
                    kind,
                    stypes,
                    max_complexity,
                    query_string,
                    function_names,
                )
                models += new_sample
                m_count += len(new_sample)

                models = feyn.fit_models(
                    models, data, loss_function, criterion, None, sample_weights
                )
                models = feyn.prune_models(models)

                feyn.show_model(
                    models[0],
                    f"Epoch no. {i+1} - Tried {m_count} models - Best loss: {models[0].loss_value:.2e}",
                    update_display=True
                )

                best = feyn.best_diverse_models(models)
                self.update(best)
            return best
        except KeyboardInterrupt:
            return feyn.best_diverse_models(models)
        except Exception as ex:
            raise ex


    def _generate(
        self,
        specs: List[str],
        registers: Dict[str, str],
        max_complexity: int,
        query_string: str,
    ) -> Dict:
        req = self._http_client.post(
            "/generate",
            json={
                "specs": specs,
                "registers": registers,
                "max_complexity": max_complexity,
                "query": query_string,
            },
        )

        if req.status_code == 422:
            raise ValueError(req.text)

        req.raise_for_status()

        return req.json()

    def _load_qlattice(self):
        req = self._http_client.get("/")

        # The purpose of this special handling is to create a channel for messaging the user about issues that we have somehow
        # failed to consider beforehand.
        if req.status_code == 400:
            raise ConnectionError(req.text)

        req.raise_for_status()

        qlattice = req.json()

        self.width = qlattice["width"]
        self.height = qlattice["height"]


def connect_qlattice(
    qlattice: Optional[str] = None,
    api_token: Optional[str] = None,
    server: str = DEFAULT_SERVER,
    config: Optional[str] = None,
    provisioning_server: str = PROVISIONING_SERVER,
) -> QLattice:
    """
    Utility function for connecting to a QLattice. A QLattice (short for Quantum Lattice) is a device which can be used to generate and explore a vast number of models linking a set of input observations to an output prediction. The actual QLattice runs on a dedicated computing cluster which is operated by Abzu. The `feyn.QLattice` class provides a client interface to communicate with, sample models from, and update the QLattice.

    Keyword Arguments:
        qlattice {Optional[str]} -- The qlattice you want to connect to, such as: `a1b2c3d4`. (Should not to be used in combination with the config parameter). (default: {None})
        api_token {Optional[str]} -- Authentication token for the communicating with this QLattice. (Should not to be used in combination with the config parameter). (default: {None})
        server {str} -- The server hosting your QLattice. (Should not to be used in combination with the config parameter). (default: {DEFAULT_SERVER})
        config {Optional[str]} -- The configuration setting in your feyn.ini or .feynrc file to load the url and api_token from. These files should be located in your home folder. (default: {None})
        provisioning_server {str} -- The service to provision CE QLattices. (default: {PROVISIONING_SERVER})

    Returns:
        QLattice -- The QLattice connection handler to your remote QLattice.
    """
    # Config cannot be combined with anything else
    if config and (qlattice or api_token):
        raise ValueError("Must specify either a config or both qlattice and token.")

    # If either qlattice or token specified, then both must be specified.
    if qlattice or api_token:
        if not (qlattice and api_token):
            raise ValueError("Must specify either a config or both qlattice and token.")

    if qlattice:
        cfg = Config(qlattice, api_token, server)
    else:
        cfg = resolve_config(config)

        if cfg is None:
            cfg = _get_community_qlattice_config(provisioning_server)

    return QLattice(cfg)


def _get_community_qlattice_config(provisioning_server: str) -> Config:
    resp = requests.post(f"{provisioning_server}/api/v1/qlattice/community/create", timeout=20)
    resp.raise_for_status()
    data = resp.json()
    print(
        "A new Community QLattice has been allocated for you. This temporary QLattice is available for personal/non-commercial use. "
        "By using this Community QLattice you agree to the terms and conditions which can be found at https://abzu.ai/privacy."
    )

    return Config(data["qlattice_id"], data["api_token"], data["server"])


def _sanitize_iterable(iter: Iterable) -> List:

    if not hasattr(iter, '__iter__'):
        raise ValueError(f"Can not interpret {iter} as a list")

    else:
        return list(iter)

def _validate_names(input_names, output_name):

    if len(input_names) < 1:
            raise Exception(
                "A QLattice simulation must have at least one input feature."
            )

    if not isinstance(output_name, str):
        raise ValueError(f"output_name {output_name} is not a string.")

    if not _check_str_list(input_names):
        raise ValueError(f"Input names needs to be a python list of strings.")

    if len(input_names) != len(set(input_names)):
        raise ValueError("Duplicate input names are found")

def _validate_mc(mc) -> int:
    try:
        mc = int(mc)
    except:
        raise ValueError(f"Could not interpret max_complexity {mc} as an integer.")
    if mc <= 0:
        raise ValueError(f"max_complexity needs to be greater than 0, but was {mc}.")
    return mc



def _is_url(maybe_url):
    try:
        result = urlparse(maybe_url)
        return all([result.scheme, result.netloc])
    except:
        return False


def _kind_to_output_stype(kind: str) -> str:
    """Parse kind into an output spec for the QLattice."""
    if kind in ["regression", "regressor"]:
        return "f"
    if kind in ["classification", "classifier"]:
        return "b"
    raise ValueError(
        "Model kind not understood. Please choose either a 'regressor' or a 'classifier'."
    )


def _models_from_json(model_dict: dict) -> Set[Model]:
    nodemap = {node["id"]: node for node in model_dict["nodes"]}

    ## Add the links to the nodes themselves.
    # TODO: Change wire format to avoud this conversion
    for node in nodemap.values():
        node["links"] = [None, None]

    for link in model_dict["links"]:
        source_id = link["source"]
        target_node = nodemap[link["target"]]
        ord_int = int(link["ord"])
        target_node["links"][ord_int] = source_id

    new_models = set()

    out_ids = [n["id"] for n in nodemap.values() if n["spec"].startswith("out:")]
    for out_id in out_ids:
        # The following algorithm builds a 1D array of nodes
        # that preserverves execution order
        nodelist = []
        current = [out_id]
        while len(current) > 0:
            node_id = current.pop(0)
            if node_id in nodelist:
                nodelist.remove(node_id)
            nodelist.insert(0, node_id)

            for pred_id in nodemap[node_id]["links"]:
                if pred_id is not None:
                    current.append(pred_id)

        # Convert the list of ids to a list of nodes
        nodelist = [nodemap[nodeid] for nodeid in nodelist]
        new_models.add(_build_model(nodelist))

    return new_models


def _build_model(nodelist: List[Dict]):
    nodes = []
    links = []
    node_index = {node["id"]: ix for ix, node in enumerate(nodelist)}

    for ix, node in enumerate(nodelist):
        nodes.append(
            {
                "id": ix,
                "spec": node["spec"],
                "location": node["location"],
                "peerlocation": node["location"],
                "name": node["name"],
                "state": {},
            }
        )
        for ordinal, source_id in enumerate(node["links"]):
            if source_id is not None:
                source = node_index[source_id]
                links.append({"source": source, "target": ix, "ord": ordinal})

    return Model._from_dict({"nodes": nodes, "links": links})


def _check_str_list(str_list:List) -> bool:
    """Return True if the input is a list of strings, else False."""
    if not isinstance(str_list, list):
        return False
    else:
        types = map(type, str_list)
        if not set(types) == {str}:
            return False

    return True


def _build_spec_list(fnames: List[str]) -> List[str]:
    """From a list of function names, build a list of specs for the simulator."""
    all_specs = _feyn.get_specs()

    if not _check_str_list(fnames):
        raise ValueError("function_names needs to be a python list of strings.")

    ret = []
    for spec_str in all_specs:
        if spec_str.startswith("in:") or spec_str.startswith("out:"):
            ret.append(spec_str)
        elif _spec_to_fname(spec_str) in fnames:
            ret.append(spec_str)

    if not list(filter(lambda s: s.startswith("cell:"), ret)):
        raise ValueError(f"No functions in {fnames} were recognised.")

    return ret


def _spec_to_fname(spec: str) -> str:
    """Separate a function name from a QLattice spec."""
    return spec.split(":")[1].split("(")[0]
