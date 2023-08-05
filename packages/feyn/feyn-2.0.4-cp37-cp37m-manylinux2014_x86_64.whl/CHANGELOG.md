# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [2.0.4] - 2021-07-07

## Changed

- `plot_partial` is now called `plot_response_1d` (`feyn.plots.plot_model_response_1d`)
    - The named argument `fixed` is now called `input_constraints`
    - `plot_partial` can still be called but now raises a FutureWarning about being deprecated.

## [2.0.1] - 2021-06-29

### Changed

- `model.plot` (`feyn.plots.plot_model_summary`) has been updated:
    - The named argument `test` is now called `compare_data`
    - Now supports `labels` param for custom labels for the summary metrics
    - Now supports a list of `compare data`, if you want to compare multiple things
    - Any additional metric added will be a more condensed column to make it easier to compare with the primary metrics

### Fixed

- Model graphs being cut off by jupyter's viewport in some instances should now be fixed by automatic rescaling to fit in view.

## [2.0.0] - 2021-06-18

### Changed

- `Graph` is now called `Model`
- The `QGraph` no longer exists. Instead you now work on lists of `Model`s.
- No longer directly instantiate a `QLattice`. Instead you call `feyn.connect_qlattice()`.
- The common `feyn` workflow is now contained in one function called `auto_run` which lives on a connected `QLattice`.

- In addition to the above automatic workflow, we now have a more expressive set of functions to replace the old:
  - A list of `Model`s can now be sampled from a connected `QLattice` using `sample_models`. This replaces part of the behaviour of the previous `get_regressor` and `get_classifier` on the `QGraph`.
  - You now fit a list of `Model`s using `feyn.fit_models`. This takes a list of `Model`s as an input and returns a list of fitted `Model`s. This replaces part of the previous fit step on the `QGraph`.
  - You now prune the worst `Model`s from a list using `prune_models`. This replaces part of the previous fit step on the `QGraph`. Default behaviour removes duplicate `Model`s, has a decay function on `Model`s and dropout.
  - You get the best diverse `Model`s using `feyn.best_diverse_models`. This replaces `QGraph.best`.
  - Now that you operate on a list of `Model`s, you have the freedom of using the native python `filter` function.
    - You still have a list of useful `feyn.filter` functions but instead apply to the native python `filter`. These functions are. Refer to the documentation for more details:
      - `Complexity`
      - `ContainsInputs`
      - `ExcludeFunctions`
      - `ContainsFunctions`
  - You can display a `Model` as a graph using the `show_model` function.
    - `show_model` detects whether you are in a `Jupyter` environment and decides what to display.

- Other changes:
  - `plot_summary` is now known as `plot` that lives on a `Model`.
  - The output of `sympify` has changed:
    - Categorical input features are now referenced as `<feature_name>_cat`.
    - Numerical input names get suffixed with `_in`.
    - Underscores and spaces in input names are truncated.
  - `sympify` now supports `include_weights=False` which gives an equation without weights and bias.
  - `sympify` now gives consistent results on up to 15 significant digits.
  - `plot_goodness_of_fit` is now called `plot_regression`.
  - `plot_regression_metrics` has been removed - its uses should be covered by `plot_regression`.

### Added

- `plot_roc_curve` has a `threshold` parameter that will plot on the false positive rate and true positive rate at the given `threshold`.
- `plot_confusion_matrix` has a `threshold` parameter.

### Removed

- Our experimental feature module `__future__` has for now outlived its purpose and has been removed.

## [1.6.1] - 2021-05-04
## [1.6.0] - 2021-05-04

### Added

- (__future__) Graph Recorder object that incorporates barcode and feature frequency matrix and heatmaps (now called feature occurrence)

### Fixed

- Fixed a warning from matplotlib about duplicate cmap registering for newer versions of mpl.

## [1.5.6] - 2021-04-23

### Fixed

- Fixed bug in ROC plot function.

## [1.5.5] - 2021-04-21

### Fixed

- Fixed bug in qlattice migration script.

## [1.5.4] - 2021-04-21

### Added

- New sematic type "bool" which will only use functions that makes sense for boolean data types (add, multiply, gaussian2)
- New statistical plots, `plot_goodness_of_fit` and `plot_residuals` to `feyn.plots`.
- New transient QLattice feature.
- `plot summary` improvements:
    - Pearson correlation is now default - and now properly displays negative instead of absolute correlation
    - MI correlation now follows a simple linear colormap that better represents it.
    - Spearman correlation is now available as an alternative correlation function
- Introduce `plot_flow` and a Jupyter-widget-enabled `plot_flow_interactive` for graphs, allowing you to play around with samples and see the activations through the graph.
- (__future__) Barcode plot and feature frequency matrix and heatmap plots.
- Query language available through `feyn.filters` updated
    - New matching starts from the output of the graph.
    - Can write queries using `+` and `*` operators.
    - Wildcards matching any subgraph `_`, complexity can be constrained with edge count in brackets.
- New `show_threshold` parameter in `plot_roc_curve` that colours the ROC curve by thresholds.


## Changed

- Backwards compatability QLattice-urls has been removed from `feyn.QLattice()`. Now the only accepted usages are:
  - `feyn.QLattice(qlattice="<qlattice-id>", api_token="<token>")`.
  - `feyn.QLattice(config="<name of a section in your config file>")`.
  - `feyn.QLattice()  # First section in your config file`.


## [1.5.3] - 2021-03-26

### Changed

- General algorithm improvements.

### Added

- Support for up to 2000 registers (Input features). Previously 200.
- Made it easier to trigger the hover information on graphs in notebooks.

## [1.5.2] - 2021-03-11

### Fixed

- Fixed bug in random seed, which caused QLattice.reset() to always use the same seed.

## [1.5.1] - 2021-03-10

### Changed

- Improve deprecation warning, so that it is obvious how to migrate the old configuration file.

## [1.5.0] - 2021-03-10

### Changed

- The parameters for the QLattice initializer has changed. You now only have to specify the `qlattice` and the `token` instead of the full url.
- With this, also the configuration-file format has changed accordingly. `url` has been replaced by `server` and `qlattice`. The old format still works, but support for it will be removed in a future release. A compatibility warning will be displayed for now.


### Fixed

- plot_partial2d: Fixed to use new contract when getting graph state.


## [1.4.8] - 2021-02-26

### Changed

- The QGraph.fit supports using Akaike Information Criterion (AIC) or Bayesian information criterion (BIC). This may become the default in the future, reducing the need for limiting depth and edges manually
- Default threads used for fitting ans sorting changed from 1 to 4

## [1.4.7] - 2021-02-12

### Changed

- General performance improvements in finding good graphs.

### Added

- Add roc_auc_score to `feyn.metrics` which will calculate the AUC of a graph. (Also accessible on `graph.roc_auc_score`).
- Plotting style improvements:
  - 'light' is now usable as alias to 'default' when setting theme.
  - Matplotlib plot styling now matches the theme choice.
  - Added colormaps to use with matplotlib: 'feyn', 'feyn-diverging'. 'feyn-partial', 'feyn-primary', 'feyn-secondary', 'feyn-highlight', 'feyn-accent'.
- Added `FeatureImportanceTable` to `feyn.insights`. (The equivalent functionality was previous in `pdheatmap` from `__future__`).
- (__future__) Add various stats functions. `graph_f_score` and `plot_graph_p_value`.

## [1.4.6] - 2021-01-08

### Added

- Targeted Maximum Likelihood Estimation (TMLE) introduced in `feyn.inference`. [See more in our docs](https://docs.abzu.ai/docs/guides/advanced/tmle.html)

### Changed

- Default graphs sort back to loss_value instead of bic.
- `feyn.tools.simpify_graph` default option is now to not formulate the logistic function, but instead output “logreg(…)“. Use argument `symbolic_lr=True` if you want to keep previous behavior.
- Categorical variables rendered in the sympify function from category(<X_featurename>) to category_<featurename>.

## [1.4.5] - 2020-12-18

### Added

- Python 3.9 support

### Fixed

- Fix memory bug when handling many registers (>165) in QLattice.

## [1.4.4] - 2020-12-18

### Removed

- `metrics.get_mutual_information()`, `metrics.get_pearson_correlations()`, `metrics.get_summary_information()`. The functionality is now covered by `metrics.calculate_mi()`, `metrics.calculate_pc()` in the public API.

### Changed

- Even more general performance improvements.

## [1.4.3] - 2020-12-04

### Changed

- General performance improvements.

### Added

- `Graph.plot_partial()` and `Graph.plot_partial2d()` to analyze the graph response.
- `metrics.calculate_mi()`, `metrics.calculate_pc()` to calculate mutual information and pearson correlations.

## [1.4.2] - 2020-10-26

- `Graph.sympify()` which returns a sympy expression mathcing the graph
- Mutual information and pearson correlations are now calculated on entire data set, giving more accurate results
- `Graph.fit()` function which can be used to fit or refit a single graph on a dataset
- Adding support to both numerical and categorical partial dependence plots
- Bugfix: 1d plots with categoricals ordered wrt their weights
- Bugfix: Fix support np-dict for graph_summary

## [1.4.1] - 2020-10-09

- Added linear and constant reference models (in `feyn.reference`) to compare with and calculate p-values (lives in `feyn.metrics`).
- Graph vizualizations rewritten and much improved.
- Dark theme support!

## [1.4.0] - 2020-09-03

- ql.update now accepts either a single graph or a list of graphs.
- Added methods: `QLattice.get_regressor` and `QLattice.get_classifier` to replace  `QLattice.get_qgraph`.
- New mathematical functions: `add`, `exp` and `log`.
- You can now control functions in graphs with new filters: `feyn.filters.Functions(["add", "multiply"])` and `feyn.filters.ExcludeFunctions("sine")`.
- New plot. ROC-curves.

## [1.3.3] - 2020-08-14

- Shorthands for plotting and score utility functions on feyn.Graph
- New approach to damping learning rates lead to more accurate fits
- Max-depth filter is less strict on which type of integers it accepts.
- Add automatric retries on failed http-requests
- Configurations can now also be stored in `<home_folder>/.config/.feynrc`

## [1.3.1] - 2020-07-07

- The new automatic scalar is now default on both input and output.
- Alternative input and output semantic types (f#) that does not scaling

## [1.3.0] - 2020-07-06

- Added a new scaler: f$. It is more automatic.

## [1.2.1] - 2020-06-16

- Changed the configuration environment variable `QLATTICE_BASE_URI` to `FEYN_QLATTICE_URL`.
- Changed the configuration environment variable `FEYN_TOKEN` to `FEYN_QLATTICE_API_TOKEN`.
- Support for configuration via config file. `feyn.ini` or `.feynrc` located in your home folder.
- Breaks compatibility with qlattice <= 1.1.2
  - Removed the neeed to add registers via qlattice.registers.get (and removed qlattice.registers.get)
  - New parameter to get_qgraph function to choose the semantic type of the data colums (this replaces the need cat/fixed register types)
- Fixes bug with numpy 1.15 and multiarray import in windows 64bit

## [1.1.2] - 2020-05-11

- Added Windows Support!
- Removed dependency to GraphViz
- Removed dependency to scikit-learn
