"""Landscape Model component of the LEffectModel effect module."""
from osgeo import ogr
import shutil
import numpy as np
import os
import base
import datetime
import attrib
import msgpack


class LEffectModel(base.Component):
    """
    Encapsulation of the LEffectModel module as a Landscape Model component. The module provides two models: LGUTS and
    LPop. LGUTS is a reduced GUTS model at catchment scale. It has two variants: GUTS-RED-IT, a reduced GUTS model
    version with Individual Tolerance, and GUTS-RED-SD, a reduced GUTS version with Stochastic Death. LPop is a
    DEB-based population model at catchment scale, parameterized for Asellus aquaticus. It makes use of the
    GUTS- RED-IT or GUTS-RED-SD models. There is also an Abj-DEB version with population regulation through
    density-dependent mortality.
    """
    # RELEASES
    VERSION = base.VersionCollection(
        base.VersionInfo("2.1.5", "2023-09-18"),
        base.VersionInfo("2.1.4", "2023-09-13"),
        base.VersionInfo("2.1.3", "2023-09-12"),
        base.VersionInfo("2.1.2", "2023-09-11"),
        base.VersionInfo("2.1.1", "2023-03-09"),
        base.VersionInfo("2.1.0", "2022-03-08"),
        base.VersionInfo("2.0.14", "2021-12-10"),
        base.VersionInfo("2.0.13", "2021-11-18"),
        base.VersionInfo("2.0.12", "2021-10-12"),
        base.VersionInfo("2.0.11", "2021-10-11"),
        base.VersionInfo("2.0.10", "2021-09-17"),
        base.VersionInfo("2.0.9", "2021-08-18"),
        base.VersionInfo("2.0.8", "2021-08-16"),
        base.VersionInfo("2.0.7", "2021-08-05"),
        base.VersionInfo("2.0.6", "2021-07-21"),
        base.VersionInfo("2.0.5", "2021-07-16"),
        base.VersionInfo("2.0.4", "2021-02-02"),
        base.VersionInfo("2.0.3", "2021-01-23"),
        base.VersionInfo("2.0.2", "2020-12-09"),
        base.VersionInfo("2.0.1", "2020-12-03"),
        base.VersionInfo("2.0.0", "2020-10-22"),
        base.VersionInfo("1.4.0", "2020-10-23"),
        base.VersionInfo("1.3.35", "2020-08-12"),
        base.VersionInfo("1.3.34", "2020-08-04"),
        base.VersionInfo("1.3.33", "2020-07-30"),
        base.VersionInfo("1.3.30", "2020-06-22"),
        base.VersionInfo("1.3.29", "2020-06-15"),
        base.VersionInfo("1.3.27", "2020-05-20"),
        base.VersionInfo("1.3.24", "2020-04-02"),
        base.VersionInfo("1.3.18", "2020-03-12"),
        base.VersionInfo("1.3.14", "2020-02-07"),
        base.VersionInfo("1.3.13", "2020-02-07"),
        base.VersionInfo("1.3.11", "2020-01-27"),
        base.VersionInfo("1.3.10", "2020-01-23"),
        base.VersionInfo("1.3.9", "2020-02-24"),
        base.VersionInfo("1.3.8", "2020-01-14"),
        base.VersionInfo("1.2.37", None),
        base.VersionInfo("1.2.5", None)
    )

    # AUTHORS
    VERSION.authors.extend((
        "Sascha Bub (component) - sascha.bub@gmx.de",
        "Thorsten Schad (component) - thorsten.schad@bayer.com",
        "Hans Baveco (module) - hans.baveco@wur.nl"
    ))

    # ACKNOWLEDGEMENTS
    VERSION.acknowledgements.extend((
        "[MessagePack](https://msgpack.org)",
        "[NumPy](https://numpy.org)"
    ))

    # ROADMAP
    VERSION.roadmap.extend((
        """Start module GUI in background 
        ([#2](https://gitlab.bayer.com/aqrisk-landscape/leffectmodel-component/-/issues/2))""",
        "Numbering of reaches ([#4](https://gitlab.bayer.com/aqrisk-landscape/leffectmodel-component/-/issues/4))"
    ))

    # CHANGELOG
    # noinspection SpellCheckingInspection
    VERSION.added("1.2.5", "`components.Lguts` component")
    # noinspection SpellCheckingInspection
    VERSION.changed("1.2.5", "`components.Lguts` updated")
    # noinspection SpellCheckingInspection
    VERSION.fixed("1.3.8", "Fix of `components.Lguts` concentration input for large sets of concentrations")
    # noinspection SpellCheckingInspection
    VERSION.fixed("1.3.9", "Update of `components.Lguts` to fit temporal output scale of module")
    # noinspection SpellCheckingInspection
    VERSION.fixed("1.3.10", "`components.Lguts` for single-year runs")
    # noinspection SpellCheckingInspection
    VERSION.fixed("1.3.11", "`components.Lguts` temporal referencing")
    # noinspection SpellCheckingInspection
    VERSION.changed("1.3.13", "Margin of Safety outputs from `components.Lguts` added")
    # noinspection SpellCheckingInspection
    VERSION.fixed("1.3.14", "`components.Lguts` error introduced during re-factory")
    # noinspection SpellCheckingInspection
    VERSION.changed("1.3.18", "Storage of individual survival for all multiplication factors in `components.Lguts` ")
    # noinspection SpellCheckingInspection
    VERSION.changed("1.3.24", "`components.Lguts` uses base function to call module")
    # noinspection SpellCheckingInspection
    VERSION.changed("1.3.27", "`components.Lguts` specifies scales")
    # noinspection SpellCheckingInspection
    VERSION.changed("1.3.29", "Input slicing in `components.Lguts`")
    # noinspection SpellCheckingInspection
    VERSION.fixed("1.3.30", "`components.Lguts` GUTS-SD parameterization")
    # noinspection SpellCheckingInspection
    VERSION.changed("1.3.33", "`components.Lguts` checks input types strictly")
    # noinspection SpellCheckingInspection
    VERSION.changed("1.3.33", "`components.Lguts` checks for physical units")
    # noinspection SpellCheckingInspection
    VERSION.changed("1.3.33", "`components.Lguts` checks for scales")
    # noinspection SpellCheckingInspection
    VERSION.changed("1.3.34", "`components.Lguts` renamed to `components.LgutsRed` ")
    # noinspection SpellCheckingInspection
    VERSION.fixed("1.3.34", "Physical units of killing rate in `components.LgutsRed` ")
    # noinspection SpellCheckingInspection
    VERSION.fixed("1.3.35", "`components.LgutsRed` output scale")
    # noinspection SpellCheckingInspection
    VERSION.changed("1.4.0", "`components.LgutsRed` renamed to `LEffectModel` ")
    # noinspection SpellCheckingInspection
    VERSION.changed("1.4.0", "`components.LgutsRed` uses new LEffectModel module")
    VERSION.changed("2.0.0", "First independent release")
    VERSION.added("2.0.1", "Changelog and release history")
    VERSION.changed("2.0.2", "Module updated to version 20201208")
    VERSION.changed("2.0.3", "`ReachListHydrography` expects list of identifiers now, no longer file name")
    VERSION.fixed("2.0.3", "Determination of last year of simulation and application")
    VERSION.changed("2.0.4", "Module updated to version 20210127")
    VERSION.changed("2.0.5", "Markdown in changelog")
    VERSION.changed("2.0.5", "Proofreading")
    VERSION.fixed("2.0.5", "Data type access")
    VERSION.added("2.0.6", "`NumberRuns` input")
    VERSION.changed("2.0.6", "Output scales to cover internal Monte Carlo runs")
    VERSION.added("2.0.7", "`Reaches` output")
    VERSION.fixed("2.0.8", "Temporal scale of some outputs")
    VERSION.added("2.0.9", "Base documentation")
    VERSION.changed("2.0.10", "Make use of generic types for class attributes")
    VERSION.changed("2.0.11", "Replaced legacy format strings by f-strings")
    VERSION.changed("2.0.12", "Switched to Google docstring style")
    VERSION.changed("2.0.13", "Removed reach inputs and output")
    VERSION.changed("2.0.13", "Scale of multiplication factors from `global` to `other/factor` ")
    VERSION.changed("2.0.13", "Reports element names of outputs")
    VERSION.changed("2.0.14", "Specifies offset of outputs")
    VERSION.changed("2.1.0", "Module updated to version 20211111")
    VERSION.changed("2.1.1", "Module updated to version 20211111-1")
    VERSION.added("2.1.2", "Information on runtime environment")
    VERSION.changed("2.1.3", "Extended module information for Squeak runtime environment")
    VERSION.added("2.1.3", "Creation of repository info during documentation")
    VERSION.added("2.1.3", "Repository info, changelog, contributing note and readme to module")
    VERSION.changed("2.1.4", "Spatial scale of `Concentrations` input")
    VERSION.added("2.1.4", "Unit attribute to `Verbosity` input")
    VERSION.changed("2.1.4", "Spatial scales of outputs")
    VERSION.changed("2.1.5", "Updated component description")
    VERSION.changed("2.1.5", "Updated input descriptions and removed stub descriptions")
    VERSION.added("2.1.5", "Runtime note regarding removal of SimulationStart input")

    def __init__(self, name, observer, store):
        """
        Initializes a LEffectModule component.

        Args:
            name: The name of the component.
            observer: The default observer of the component.
            store: The default store of the component.
        """
        super(LEffectModel, self).__init__(name, observer, store)
        self._module = base.Module(
            "LEffectModel",
            "20211111-1",
            "module",
            r"\module\doc\LEffectModel_Manual_20211111.pdf",
            base.Module(
                "Squeak",
                "5.3",
                "module",
                "https://squeak.org/",
                None,
                True,
                "module/release-notes/README"
            )
        )
        self._inputs = base.InputContainer(self, [
            base.Input(
                "ProcessingPath",
                (attrib.Class(str), attrib.Unit(None), attrib.Scales("global")),
                self.default_observer,
                description="The working directory for the module. It is used for all files prepared as module inputs "
                            " or generated as (temporary) module outputs."
            ),
            base.Input(
                "Model",
                (
                    attrib.Class(str),
                    attrib.Unit(None),
                    attrib.Scales("global"),
                    attrib.InList(("CatchmentGUTSSD", "CatchmentGUTSIT", "LPopSD", "LPopIT"))
                ),
                self.default_observer,
                description="Specifies the model that is applied to the input data. This can either be an individual "
                            "based GUTS model (choices starting with `CatchmentGUTS`) or a population based effect "
                            "model (choices starting with `LPop`). The choice of model also determines whether a"
                            "stochastic death version (choices ending with `SD`) or an individual tolerance version "
                            "(choices ending with `IT`) is used."
            ),
            base.Input(
                "MinimumClutchSize",
                (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                self.default_observer,
                description="Used by population models."
            ),
            base.Input(
                "BackgroundMortalityRate",
                (attrib.Class(float), attrib.Unit("1/d"), attrib.Scales("global")),
                self.default_observer,
                description="Used by population models."
            ),
            base.Input(
                "DensityDependentMortalityRate",
                (attrib.Class(float), attrib.Unit("m²/d"), attrib.Scales("global")),
                self.default_observer,
                description="Used by population models."
            ),
            base.Input(
                "DominantRateConstant",
                (attrib.Class(float), attrib.Unit("1/d"), attrib.Scales("global")),
                self.default_observer,
                description="Used by all models."
            ),
            base.Input(
                "BackgroundHazardRate",
                (attrib.Class(float), attrib.Unit("1/d"), attrib.Scales("global")),
                self.default_observer,
                description="Used by all models."
            ),
            base.Input(
                "ParameterZOfSDModel",
                (attrib.Class(float), attrib.Unit("ng/l"), attrib.Scales("global")),
                self.default_observer,
                description="Used by stochastic death models."
            ),
            base.Input(
                "ParameterBOfSDModel",
                (attrib.Class(float), attrib.Unit("l/(ng*d)"), attrib.Scales("global")),
                self.default_observer,
                description="Used by stochastic death models."
            ),
            base.Input(
                "ThresholdOfITModel",
                (attrib.Class(float), attrib.Unit("ng/l"), attrib.Scales("global")),
                self.default_observer,
                description="Used by individual tolerance models."
            ),
            base.Input(
                "BetaOfITModel",
                (attrib.Class(float), attrib.Unit("1"), attrib.Scales("global")),
                self.default_observer,
                description="Used by individual tolerance models."
            ),
            base.Input(
                "AverageTemperatureParameterOfForcingFunction",
                (attrib.Class(float), attrib.Unit("°C"), attrib.Scales("global")),
                self.default_observer,
                description="Used by population models."
            ),
            base.Input(
                "AmplitudeTemperatureFluctuationsParameter",
                (attrib.Class(float), attrib.Unit("°C"), attrib.Scales("global")),
                self.default_observer,
                description="Used by population models."
            ),
            base.Input(
                "ShiftForwardOfDayNumberWithLowestTemperature",
                (attrib.Class(int), attrib.Unit("d"), attrib.Scales("global")),
                self.default_observer,
                description="Used by population models."
            ),
            base.Input(
                "PerIndividualProbabilityOfMigration",
                (attrib.Class(float), attrib.Unit("1/d"), attrib.Scales("global")),
                self.default_observer,
                description="Used by population models."
            ),
            base.Input(
                "ProbabilityOfAMigratingIndividualToMoveDownstream",
                (attrib.Class(float), attrib.Unit("1"), attrib.Scales("global")),
                self.default_observer,
                description="Used by population models."
            ),
            base.Input(
                "SimulationStart",
                (attrib.Class(datetime.date), attrib.Unit(None), attrib.Scales("global")),
                self.default_observer,
                description="The first time step for which concentration input data is provided. This input also "
                            "defines the base year for LEffectModel simulations. Actual simulation starts "
                            "`NumberOfWarmUpYears` earlier and ends `RecoveryPeriodYears` later. This input will be "
                            "removed in a future version of the `LEffectModule` component."
            ),
            base.Input(
                "Concentrations",
                (attrib.Class(np.ndarray), attrib.Unit("ng/l"), attrib.Scales("time/hour, space/reach")),
                self.default_observer
            ),
            base.Input(
                "NumberOfWarmUpYears",
                (attrib.Class(int), attrib.Unit("y"), attrib.Scales("global")),
                self.default_observer
            ),
            base.Input(
                "RecoveryPeriodYears",
                (attrib.Class(int), attrib.Unit("y"), attrib.Scales("global")),
                self.default_observer
            ),
            base.Input(
                "NumberOfStepsWithinOneHour",
                (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                self.default_observer
            ),
            base.Input(
                "MultiplicationFactors",
                (attrib.Class(list[float]), attrib.Unit("1"), attrib.Scales("other/factor")),
                self.default_observer,
                description="To determine LP50 values, the concentration multiplication factor leading to a 50% "
                            "reduction of final survival in the GUTS model, simulations for all reaches are run "
                            "applying a series of multiplication factors to the hourly concentration time series. "
                            "Ideally, the full range from 0 to 100% effect (reduction of survival) should be covered, "
                            "to ensure a reliable LP50 estimation by fitting a dose-response relationship. As a kind "
                            "of brute-force approach, multiplication factors could be set according to a power "
                            "function, e.g., ranging from 2^-10 to 2^15 (1/512 to 16384)."
            ),
            base.Input(
                "Verbosity",
                (attrib.Class(int), attrib.Scales("global"), attrib.Unit(None), attrib.InList((0, 1))),
                self.default_observer,
                description="If set to `1`, survival is reported per day, else only at the end of each simulated year. "
                            "This affects only the output of the module, but not of the component. Vhanging this input "
                            "is therefore mainly useful for debugging."
            ),
            base.Input(
                "NumberRuns",
                (attrib.Class(int), attrib.Scales("global"), attrib.Unit("1")),
                self.default_observer
            ),
            base.Input(
                "UseTemperatureInput",
                (attrib.Class(bool), attrib.Scales("global"), attrib.Unit(None)),
                self._defaultObserver,
                description="Specifies, whether the empirical water temperature data from the `WaterTemperature` input "
                            "is used or whether this data is ignored and a forcing function is applied, instead."
            ),
            base.Input(
                "WaterTemperature",
                (attrib.Class(np.ndarray), attrib.Scales("time/day"), attrib.Unit("°C")),
                self._defaultObserver
            )
        ])
        self._outputs = base.OutputContainer(self, [
            base.Output(
                "AdultMetaPopulation",
                store,
                self,
                {"data_type": np.int, "scales": "time/day, other/factor, other/runs", "unit": "1"},
                "The total number of all adults.",
                {
                    "type": np.ndarray,
                    "shape": (
                        """the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period""",
                        "the number of items in the [MultiplicationFactors](#MultiplicationFactors) input",
                        "the `NumberRuns`"
                    ),
                    "chunks": "for fast retrieval of time series"
                }
            ),
            base.Output(
                "AdultPopulationByReach",
                store,
                self,
                {"data_type": np.int, "scales": "time/day, space/reach, other/factor, other/runs", "unit": "1"},
                "The number of adults.",
                {
                    "type": np.ndarray,
                    "shape": (
                        """the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period""",
                        "the number of reaches reported by the [Concentrations](#Concentrations) input",
                        "the number of items in the [MultiplicationFactors](#MultiplicationFactors) input",
                        "the `NumberRuns`"
                    ),
                    "chunks": "for fast retrieval of time series"
                }
            ),
            base.Output(
                "EmbryoMetaPopulation",
                store,
                self,
                {"data_type": np.int, "scales": "time/day, other/factor, other/runs", "unit": "1"},
                "The total number of all embryos.",
                {
                    "type": np.ndarray,
                    "shape": (
                        """the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period""",
                        "the number of items in the [MultiplicationFactors](#MultiplicationFactors) input",
                        "the `NumberRuns`"
                    ),
                    "chunks": "for fast retrieval of time series"
                }
            ),
            base.Output(
                "EmbryoPopulationByReach",
                store,
                self,
                {"data_type": np.int, "scales": "time/day, space/reach, other/factor, other/runs", "unit": "1"},
                "The number of embryos.",
                {
                    "type": np.ndarray,
                    "shape": (
                        """the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period""",
                        "the number of reaches reported by the [Concentrations](#Concentrations) input",
                        "the number of items in the [MultiplicationFactors](#MultiplicationFactors) input",
                        "the `NumberRuns`"
                    ),
                    "chunks": "for fast retrieval of time series"
                }
            ),
            base.Output(
                "ExtantLocalPopulationsMetaPopulation",
                store,
                self,
                {"data_type": np.int, "scales": "time/day, other/factor, other/runs", "unit": "1"},
                "The total number of populations that went extant.",
                {
                    "type": np.ndarray,
                    "shape": (
                        """the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period""",
                        "the number of items in the [MultiplicationFactors](#MultiplicationFactors) input",
                        "the `NumberRuns`"
                    ),
                    "chunks": "for fast retrieval of time series"
                }
            ),
            base.Output(
                "JuvenileAndAdultMetaPopulation",
                store,
                self,
                {"data_type": np.int, "scales": "time/day, other/factor, other/runs", "unit": "1"},
                "The total number of all adults and juveniles combined.",
                {
                    "type": np.ndarray,
                    "shape": (
                        """the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period""",
                        "the number of items in the [MultiplicationFactors](#MultiplicationFactors) input",
                        "the `NumberRuns`"
                    ),
                    "chunks": "for fast retrieval of time series"
                }
            ),
            base.Output(
                "JuvenileAndAdultPopulationByReach",
                store,
                self,
                {"data_type": np.int, "scales": "time/day, space/reach, other/factor, other/runs", "unit": "1"},
                "The number of juveniles and adults combined.",
                {
                    "type": np.ndarray,
                    "shape": (
                        """the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period""",
                        "the number of reaches reported by the [Concentrations](#Concentrations) input",
                        "the number of items in the [MultiplicationFactors](#MultiplicationFactors) input",
                        "the `NumberRuns`"
                    ),
                    "chunks": "for fast retrieval of time series"
                }
            ),
            base.Output(
                "JuvenileMetaPopulation",
                store,
                self,
                {"data_type": np.int, "scales": "time/day, other/factor, other/runs", "unit": "1"},
                "The total number of all juveniles.",
                {
                    "type": np.ndarray,
                    "shape": (
                        """the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period""",
                        "the number of items in the [MultiplicationFactors](#MultiplicationFactors) input",
                        "the `NumberRuns`"
                    ),
                    "chunks": "for fast retrieval of time series"
                }
            ),
            base.Output(
                "JuvenilePopulationByReach",
                store,
                self,
                {"data_type": np.int, "scales": "time/day, space/reach, other/factor, other/runs", "unit": "1"},
                "The number of juveniles.",
                {
                    "type": np.ndarray,
                    "shape": (
                        """the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period""",
                        "the number of reaches reported by the [Concentrations](#Concentrations) input",
                        "the number of items in the [MultiplicationFactors](#MultiplicationFactors) input",
                        "the `NumberRuns`"
                    ),
                    "chunks": "for fast retrieval of time series"
                }
            ),
            base.Output(
                "GutsSurvivalReaches",
                store,
                self,
                {"scales": "time/year, space/reach, other/factor", "unit": "1"},
                "The probability of an individual to survive.",
                {
                    "type": np.ndarray,
                    "data_type": np.float,
                    "shape": (
                        """the number of years at least partly covered by the [Concentrations](#Concentrations) input 
                        plus the number of years of the warm-up period plus the number of years of the recovery 
                        period""",
                        "the number of reaches reported by the [Concentrations](#Concentrations) input",
                        "the number of items in the [MultiplicationFactors](#MultiplicationFactors) input"
                    ),
                    "chunks": "for allowing compression (only one chunk used)"
                }
            )
        ])
        if self.default_observer:
            self.default_observer.write_message(
                3,
                "The SimulationStart input will be removed in a future version of the CascadeToxswa component",
                "The time offset will be retrieved from the metadata of the Concentrations input"
            )

    def run(self):
        """
        Runs the component.

        Returns:
            Nothing.
        """
        processing_path = self.inputs["ProcessingPath"].read().values
        model = self.inputs["Model"].read().values
        multiplication_factors = self._inputs["MultiplicationFactors"].read().values
        simulation_start = self.inputs["SimulationStart"].read().values
        number_of_warm_up_years = self._inputs["NumberOfWarmUpYears"].read().values
        recovery_period_years = self.inputs["RecoveryPeriodYears"].read().values
        number_runs = self.inputs["NumberRuns"].read().values if model in ["LPopSD", "LPopIT"] else None
        self.prepare_runtime_environment(
            processing_path,
            (
                (
                    os.path.join(os.path.dirname(__file__), "module", "LEffectModel.image"),
                    os.path.join(processing_path, "LEffectModel.image")
                ),
                (
                    os.path.join(os.path.dirname(__file__), "module", "LEffectModel.changes"),
                    os.path.join(processing_path, "LEffectModel.changes")
                )
            ),
            model
        )
        self.prepare_startup_statements(
            os.path.join(processing_path, "startup.st"), model, multiplication_factors, number_runs)
        # noinspection SpellCheckingInspection
        self.prepare_coefficients(
            os.path.join(
                processing_path, "ETInput", f"{model}ModelSystem", "parameters", f"{model}ModelSystem_coefs.csv"),
            model
        )
        # noinspection SpellCheckingInspection
        self.prepare_reach_list(os.path.join(
            processing_path, "ETInput", f"{model}ModelSystem", "maps", "shapes", "reachlist_shp", "Reachlist_shp.shp"
        ))
        time_slices = self.get_time_slices()
        self.prepare_concentrations(
            os.path.join(processing_path, "ETInput", "CatchmentModelSystem", "data"), time_slices, simulation_start)
        if model in ["LPopSD", "LPopIT"]:
            self.prepare_control_population_model(
                os.path.join(
                    processing_path, "ETInput", f"{model}ModelSystem", "parameters", f"{model}ModelSystem_control.csv"),
                simulation_start,
                number_of_warm_up_years,
                recovery_period_years
            )
            if self.inputs["UseTemperatureInput"].read().values:
                self.prepare_water_temperatures(
                    os.path.join(
                        processing_path,
                        "ETInput",
                        "CatchmentModelSystem",
                        "data",
                        "water_temperature_101096_1979-2020.csv"
                    ),
                    simulation_start.year - number_of_warm_up_years,
                    simulation_start.year + len(time_slices) + recovery_period_years
                )
            self.run_module(processing_path)
            # noinspection SpellCheckingInspection
            self.store_results_per_day(
                os.path.join(processing_path, "ecotalk", f"{model}ModelSystem_MoS", "x1", "x1s{}"),
                {
                    "x1s{}r{}_adultMetapop.txt": "AdultMetaPopulation",
                    "x1s{}r{}_embryoMetapop.txt": "EmbryoMetaPopulation",
                    "x1s{}r{}_extantLocalPopsMetapop.txt": "ExtantLocalPopulationsMetaPopulation",
                    "x1s{}r{}_juvAndAdultMetapop.txt": "JuvenileAndAdultMetaPopulation",
                    "x1s{}r{}_juvenileMetapop.txt": "JuvenileMetaPopulation"
                },
                simulation_start.year,
                len(time_slices),
                number_of_warm_up_years,
                recovery_period_years,
                len(multiplication_factors),
                number_runs
            )
            # noinspection SpellCheckingInspection
            self.store_results_per_day_and_reach(
                os.path.join(processing_path, "ecotalk", f"{model}ModelSystem_Mos", "x1", "x1s{}"),
                {
                    "x1s{}r{}_adultPopByReach.txt": "AdultPopulationByReach",
                    "x1s{}r{}_embryoPopByReach.txt": "EmbryoPopulationByReach",
                    "x1s{}r{}_juvAndAdultPopByReach.txt": "JuvenileAndAdultPopulationByReach",
                    "x1s{}r{}_juvenilePopByReach.txt": "JuvenilePopulationByReach"
                },
                simulation_start.year,
                len(time_slices),
                number_of_warm_up_years,
                recovery_period_years,
                self._inputs["Concentrations"].describe()["shape"][1],
                len(multiplication_factors),
                number_runs
            )
        elif model in ["CatchmentGUTSSD", "CatchmentGUTSIT"]:
            for y in range(len(time_slices)):
                self.prepare_control_individual_model(
                    os.path.join(
                        processing_path,
                        "ETInput",
                        f"{model}ModelSystem",
                        "parameters",
                        f"{model}ModelSystem_control.csv"
                    ),
                    simulation_start,
                    y
                )
                self.run_module(processing_path)
                # noinspection SpellCheckingInspection
                os.rename(
                    os.path.join(processing_path, "ecotalk", f"{model}ModelSystem_MoS.modelscript"),
                    os.path.join(processing_path, "ecotalk", f"{model}ModelSystem_MoS.modelscript.{y}")
                )
                # noinspection SpellCheckingInspection
                os.rename(
                    os.path.join(processing_path, "ecotalk", f"{model}ModelSystem_MoS"),
                    os.path.join(processing_path, "ecotalk", f"{model}ModelSystem_MoS_{y}")
                )
            # noinspection SpellCheckingInspection
            self.store_results_per_year_and_reach(
                os.path.join(processing_path, "ecotalk", model + "ModelSystem_MoS_{}", "x1"),
                {"guts_survival_reaches.txt_mfactors.txt": "GutsSurvivalReaches"},
                len(time_slices),
                self._inputs["Concentrations"].describe()["shape"][1],
                len(multiplication_factors),
                simulation_start.year
            )
        else:
            raise ValueError("Unexpected model: " + model)

    @staticmethod
    def prepare_runtime_environment(processing_path, files, model):
        """
        Prepares the runtime environment of the module.

        Args:
            processing_path: The working directory of the module.
            files: The files required for the runtime environment to work properly.
            model: The identifier of the model used.

        Returns:
            Nothing.
        """
        # noinspection SpellCheckingInspection
        os.makedirs(os.path.join(processing_path, "ecotalk"))
        os.makedirs(os.path.join(processing_path, "ETInput", f"{model}ModelSystem", "parameters"))
        # noinspection SpellCheckingInspection
        os.makedirs(os.path.join(processing_path, "ETInput", f"{model}ModelSystem", "maps", "shapes", "reachlist_shp"))
        os.makedirs(os.path.join(processing_path, "ETInput", "CatchmentModelSystem", "data"))
        for file in files:
            shutil.copyfile(file[0], file[1])

    @staticmethod
    def prepare_startup_statements(statements_file, model, multiplication_factors, number_runs):
        """
        Prepares the SmallTalk statement file.

        Args:
            statements_file: The path for the statement file.
            model: The identifier of the model used.
            multiplication_factors: A list of multiplication factors for margin-of-safety analyses.
            number_runs: The number of runs to perform in a population model run.

        Returns:
            Nothing.
        """
        if model in ["LPopSD", "LPopIT"]:
            project_name = model
            project_type = "LPop"
        elif model == "CatchmentGUTSSD":
            # noinspection SpellCheckingInspection
            project_name = "GUTSSD"
            # noinspection SpellCheckingInspection
            project_type = "LGUTS"
        elif model == "CatchmentGUTSIT":
            # noinspection SpellCheckingInspection
            project_name = "GUTSIT"
            # noinspection SpellCheckingInspection
            project_type = "LGUTS"
        else:
            raise ValueError("Unexpected model: " + model)
        if project_type != "LPop" and number_runs is not None:
            raise ValueError("Number of runs may not be provided except for LPop runs")
        with open(statements_file, "w") as f:
            # noinspection SpellCheckingInspection
            f.write("| mfs scriptFile |\n")
            f.write("ModelIO invalidateRootDirectories.\n")
            if model in ["LPopSD", "LPopIT"]:
                pass
            elif model in ["CatchmentGUTSSD", "CatchmentGUTSIT"]:
                # noinspection SpellCheckingInspection
                f.write("CatchmentConcDataBase removeAllDataBases.\n")
                f.write("RInterface rDirectory: nil. \"\"\n")
            else:
                raise ValueError("Unexpected model: " + model)
            f.write(f"mfs := #({' '.join([str(x) for x in multiplication_factors])}).\n")
            f.write(
                f"scriptFile := {project_type}Project scriptMoSAnalysis{project_name}MultiplicationFactors: "
                f"mfs{' runs: ' + str(number_runs) if project_type == 'LPop' else ''}.\n"
            )
            f.write("(ModelProject fromScriptFile: scriptFile) runModelProjectForeground.\n")
            f.write("Smalltalk quitPrimitive\n")

    def prepare_coefficients(self, coefficient_file, model):
        """
        Prepares the coefficients used by the module.

        Args:
            coefficient_file: The file path for the coefficient file.
            model: The model name.

        Returns:
            Nothing.
        """
        with open(coefficient_file, "w") as f:
            f.write("Component,model-dependent,inhabitantClass\n")
            if model in ["LPopSD", "LPopIT"]:
                f.write(f"minClutchSize:,{self._inputs['MinimumClutchSize'].read().values},minimum clutch size [ind]\n")
                f.write(
                    f"backgroundMortality:,{self._inputs['BackgroundMortalityRate'].read().values},"
                    "background mortality rate [d-1]\n"
                )
                f.write(
                    f"muDD:,{self._inputs['DensityDependentMortalityRate'].read().values},"
                    "(default 0.000010) density-dependent mortality rate [m2 ind-1 d-1]\n"
                )
            elif model in ["CatchmentGUTSSD", "CatchmentGUTSIT"]:
                pass
            else:
                raise ValueError("Unexpected model: " + model)
            f.write(f"kd:,{self._inputs['DominantRateConstant'].read().values},dominant rate constant [1/d]\n")
            f.write(f"hb:,{self._inputs['BackgroundHazardRate'].read().values},background hazard rate [1/d]\n")
            if model in ["LPopSD", "CatchmentGUTSSD"]:
                f.write(f"z:,{self._inputs['ParameterZOfSDModel'].read().values},threshold concentration [ng/L]\n")
                f.write(f"b:,{self._inputs['ParameterBOfSDModel'].read().values},killing rate [L/(ng*d)]\n")
            elif model in ["LPopIT", "CatchmentGUTSIT"]:
                f.write(f"m:,{self._inputs['ThresholdOfITModel'].read().values},threshold distribution [ng/L]\n")
                f.write(f"beta:,{self._inputs['BetaOfITModel'].read().values},width of distribution []\n")
            else:
                raise ValueError("Unexpected model: " + model)
            f.write("Component,model-dependent,landscapeClass\n")
            if model in ["LPopSD", "LPopIT"]:
                f.write(
                    f"envTav:,{self._inputs['AverageTemperatureParameterOfForcingFunction'].read().values},"
                    "average temperature parameter of forcing function [oC]\n"
                )
                f.write(
                    f"envTamp:,{self._inputs['AmplitudeTemperatureFluctuationsParameter'].read().values},"
                    "amplitude temperature fluctuations parameter [oC]\n"
                )
                # noinspection SpellCheckingInspection
                # noinspection GrazieInspection
                f.write(
                    f"envTminShift:,{self._inputs['ShiftForwardOfDayNumberWithLowestTemperature'].read().values},"
                    "shift forward of daynr with lowest temperature [d]\n"
                )
            elif model in ["CatchmentGUTSSD", "CatchmentGUTSIT"]:
                pass
            else:
                raise ValueError("Unexpected model: " + model)
            f.write("conversionToGutsFactor:,1.0,(concentrations are given in ng/l; no conversion)\n")
            if model in ["LPopSD", "LPopIT"]:
                f.write(
                    f"migrationProb:,{self._inputs['PerIndividualProbabilityOfMigration'].read().values},"
                    "per individual probability of migration [d-1]\n"
                )
                f.write(
                    "downStreamProb:,"
                    f"{self._inputs['ProbabilityOfAMigratingIndividualToMoveDownstream'].read().values},"
                    "probability of a migrating individual to move downstream\n"
                )
            elif model in ["CatchmentGUTSSD", "CatchmentGUTSIT"]:
                pass
            else:
                raise ValueError("Unexpected model: " + model)

    def prepare_reach_list(self, reaches_file):
        """
        Prepares the reach list.

        Args:
            reaches_file: The file path for the reach list.

        Returns:
            Nothing.
        """
        reaches = self.inputs["Concentrations"].describe()["element_names"][1].get_values()
        driver = ogr.GetDriverByName("ESRI Shapefile")
        reach_list_data_source = driver.CreateDataSource(reaches_file)
        reach_list_layer = reach_list_data_source.CreateLayer("reaches", None, ogr.wkbPoint)
        reach_list_layer.CreateField(ogr.FieldDefn("key", ogr.OFTInteger))
        reach_list_layer_definition = reach_list_layer.GetLayerDefn()
        for i, feature in enumerate(reaches):
            reach = ogr.Feature(reach_list_layer_definition)
            first_point = ogr.Geometry(ogr.wkbPoint)
            first_point.AddPoint(0, 0, 0)
            reach.SetGeometry(first_point)
            reach.SetField("key", int(feature))
            reach_list_layer.CreateFeature(reach)

    def get_time_slices(self):
        """
        Slices the simulation time span into individual years for module inputs and outputs.

        Returns:
            A list of indices indicating the hours when slicing should be done.
        """
        simulation_start = self.inputs["SimulationStart"].read().values
        concentrations_info = self.inputs["Concentrations"].describe()
        number_hours = int(concentrations_info["shape"][0])
        result = []
        current_year = simulation_start.year
        i = None
        for i in range(number_hours):
            current_date = simulation_start + datetime.timedelta(hours=i)
            if current_date.year != current_year:
                result.append(i)
                current_year = current_date.year
        if len(result) == 0 or result[-1] != i:
            result.append(i + 1)
        return result

    def prepare_concentrations(self, time_slice_path, time_slices, simulation_start):
        """
        Prepares input concentrations for individual module runs.

        Args:
            time_slice_path: The path for the prepared input files.
            time_slices: The indices by which input concentrations are sliced.
            simulation_start: The first day of the simulation.

        Returns:
            Nothing.
        """
        reaches = self.inputs["Concentrations"].describe()["element_names"][1].get_values()
        start_day_of_year = simulation_start.timetuple().tm_yday
        concentrations = [[]] * len(reaches)
        for y in range(len(time_slices)):
            time_slice_from = 0 if y == 0 else time_slices[y - 1]
            for i, reach in enumerate(reaches):
                reported_concentrations = self.inputs["Concentrations"].read(
                    slices=(slice(time_slice_from, time_slices[y]), i)).values
                concentrations[i] = [0.] * 8786
                concentrations[i][0] = float(reach)
                start_index = (start_day_of_year - 1) * 24 + 1 if y == 0 else 1
                concentrations[i][start_index:(start_index + reported_concentrations.shape[0])] = \
                    reported_concentrations.tolist()
            # noinspection SpellCheckingInspection
            with open(
                    os.path.join(time_slice_path, f"rummen_{simulation_start.year + y}.msgpack"),
                    "wb"
            ) as f:
                msgpack.pack(concentrations, f)

    def run_module(self, processing_path):
        """
        Runs the module.

        Args:
            processing_path: The path used for processing.

        Returns:
            Nothing.
        """
        squeak = os.path.join(os.path.dirname(__file__), "module", "squeak.exe")
        base.run_process((squeak, "LPop.image", "startup.st"), processing_path, self.default_observer)

    def prepare_control_population_model(
            self, control_file, simulation_start, number_of_warm_up_years, recovery_period_year):
        """
        Prepares the control file.

        Args:
            control_file: The name of the control file.
            simulation_start: The first day of the simulation.
            number_of_warm_up_years: The number of years used to warm up the module.
            recovery_period_year: The number of years added as recovery period to the simulation.

        Returns:
            Nothing.
        """
        number_hours = self.inputs["Concentrations"].describe()["shape"][0]
        with open(control_file, "w") as f:
            f.write(f"startYear:,{simulation_start.year - number_of_warm_up_years},start year of the simulation\n")
            f.write(
                "endYear:,"
                f"{(simulation_start + datetime.timedelta(number_hours / 24 - 1)).year + recovery_period_year},"
                "last year of the simulation\n"
            )
            f.write(f"startApplicationYear:,{simulation_start.year},start year of pesticide application\n")
            f.write(
                f"endApplicationYear:,{(simulation_start + datetime.timedelta(number_hours / 24 - 1)).year},"
                "last year of pesticide application\n"
            )
            f.write("useCSV:,0,use the slow csv input format (1) or much faster msgpack format(0)\n")
            f.write(
                f"stepsInHr:,{self._inputs['NumberOfStepsWithinOneHour'].read().values},"
                "the number of steps within 1 hourly time step for GUTS simulation\n"
            )
            f.write(
                f"useTemperatureData:,{'1' if self.inputs['UseTemperatureInput'].read().values else '0'},"
                "define water temperature from data (1) or forcing functions (0)"
            )

    def prepare_control_individual_model(self, control_file, simulation_start, year_index):
        """
        Prepares the control file.

        Args:
            control_file: The name of the control file.
            simulation_start: The first day of the simulation.
            year_index: The index of the current year to simulate.

        Returns:
            Nothing.
        """
        with open(control_file, "w") as f:
            f.write(f"applicationYear:,{simulation_start.year + year_index},year of pesticide application\n")
            f.write(
                f"verbose:,{self._inputs['Verbosity'].read().values},"
                "survival output per day (1) or end of the year only (0)\n"
            )
            f.write("useCSV:,0,use the slow csv input format (1) or much faster msgpack format(0)\n")
            f.write(
                f"stepsInHr:,{self._inputs['NumberOfStepsWithinOneHour'].read().values},"
                "the number of steps within 1 hourly time step for GUTS simulation"
            )

    def store_results_per_day(
            self,
            time_slice_path,
            result_set,
            first_year,
            number_years,
            number_warm_up_years,
            recovery_period_years,
            number_multiplication_factors,
            number_runs
    ):
        """
        Reads the results into the Landscape Model.

        Args:
            time_slice_path: The file path of the sliced module output files.
            result_set: A dictionary that maps file names to component outputs.
            first_year: The first year of the simulation as an integer number.
            number_years: The number of years simulated.
            number_warm_up_years: The number of years used to warm up the module.
            recovery_period_years: The number of years added as recovery period to the simulation.
            number_multiplication_factors: The number of multiplication factors used for the module run.
            number_runs: The number of runs of the population model.

        Returns:
            Nothing.
        """
        number_days = (
                datetime.date(first_year + number_years + recovery_period_years, 1, 1) -
                datetime.date(first_year - number_warm_up_years, 1, 1)
        ).days
        for file_name, output_name in result_set.items():
            self._outputs[output_name].set_values(
                np.ndarray,
                shape=(number_days, number_multiplication_factors, number_runs),
                chunks=(number_days, 1, 1),
                element_names=(None, self.inputs["MultiplicationFactors"].describe()["element_names"][0], None),
                offset=(first_year, None, None)
            )
            for multiplication_factor in range(1, number_multiplication_factors + 1):
                for run in range(1, number_runs + 1):
                    values = np.zeros((number_days, 1, 1), np.int)
                    with open(os.path.join(
                            time_slice_path.format(multiplication_factor),
                            file_name.format(multiplication_factor, run)
                    )) as f:
                        for line in f:
                            record = line[:-1].split("\t")
                            values[int(record[0]) - 1, 0, 0] = int(record[2])
                    self._outputs[output_name].set_values(
                        values,
                        slices=(
                            slice(number_days),
                            slice(multiplication_factor - 1, multiplication_factor),
                            slice(run - 1, run)
                        ),
                        create=False
                    )

    def store_results_per_day_and_reach(
            self,
            time_slice_path,
            result_set,
            first_year,
            number_years,
            number_warm_up_years,
            recovery_period_years,
            number_reaches,
            number_multiplication_factors,
            number_runs
    ):
        """
        Reads the results into the Landscape Model.

        Args:
            time_slice_path: The file path of the sliced module output files.
            result_set: A dictionary that maps file names to component outputs.
            first_year: The first year of the simulation as an integer number.
            number_years: The number of years simulated.
            number_warm_up_years: The number of years used to warm up the module.
            recovery_period_years: The number of years added as recovery period to the simulation.
            number_reaches: The number of reaches simulated.
            number_multiplication_factors: The number of multiplication factors used for the module run.
            number_runs: The number of runs of the population model.

        Returns:
            Nothing.
        """
        number_days = (
                datetime.date(first_year + number_years + recovery_period_years, 1, 1) -
                datetime.date(first_year - number_warm_up_years, 1, 1)
        ).days
        for file_name, output_name in result_set.items():
            self._outputs[output_name].set_values(
                np.ndarray,
                shape=(number_days, number_reaches, number_multiplication_factors, number_runs),
                chunks=(number_days, 1, 1, 1),
                element_names=(
                    None,
                    self.inputs["Concentrations"].describe()["element_names"][1],
                    self.inputs["MultiplicationFactors"].describe()["element_names"][0],
                    None
                ),
                offset=(first_year, None, None, None)
            )
            for multiplication_factor in range(1, number_multiplication_factors + 1):
                for run in range(1, number_runs + 1):
                    values = np.zeros((number_days, number_reaches, 1, 1), np.int)
                    with open(os.path.join(
                            time_slice_path.format(multiplication_factor),
                            file_name.format(multiplication_factor, run)
                    )) as f:
                        for i, line in enumerate(f):
                            record = line[:-1].split("\t")
                            values[(int(record[0]) - 1), slice(number_reaches), 0, 0] = [int(x) for x in record[2:]]
                    self._outputs[output_name].set_values(
                        values,
                        slices=(
                            slice(number_days),
                            slice(number_reaches),
                            slice(multiplication_factor - 1, multiplication_factor),
                            slice(run - 1, run)
                        ),
                        create=False
                    )

    def store_results_per_year_and_reach(
            self, time_slice_path, result_set, number_years, number_reaches, number_multiplication_factors, first_year):
        """
        Reads the results into the Landscape Model.

        Args:
            time_slice_path: The file path of the sliced module output files.
            result_set: A dictionary that maps file names to component outputs.
            number_years: The number of years simulated.
            number_reaches: The number of reaches simulated.
            number_multiplication_factors: The number of multiplication factors used for the module run.
            first_year: The first year of the simulation as an integer number.

        Returns:
            Nothing.
        """
        for file_name, output_name in result_set.items():
            values = np.zeros((number_years, number_reaches, number_multiplication_factors), np.float)
            for y in range(number_years):
                with open(os.path.join(time_slice_path.format(y), file_name)) as f:
                    for i, line in enumerate(f):
                        record = line.replace("\n", "").split("\t")
                        values[y, i, slice(number_multiplication_factors)] = [float(x) for x in record]
            self._outputs[output_name].set_values(
                values,
                chunks=(number_years, number_reaches, number_multiplication_factors),
                element_names=(
                    None,
                    self.inputs["Concentrations"].describe()["element_names"][1],
                    self.inputs["MultiplicationFactors"].describe()["element_names"][0]
                ),
                offset=(first_year, None, None)
            )

    def prepare_water_temperatures(
            self, temperature_file, from_year, to_year):
        """
        Prepares a CSV-file containing daily water temperatures.

        Args:
            temperature_file: The file path for the temperature file.
            from_year: The first year for which temperature data is needed.
            to_year: The last year for which temperature data is needed.

        Returns:
            Nothing.
        """
        water_temperatures = self.inputs["WaterTemperature"].read(
            select={"time/day": {"from": datetime.date(from_year, 1, 1), "to": datetime.date(to_year + 1, 1, 1)}})
        day = datetime.date(from_year, 1, 1)
        with open(temperature_file, "w") as f:
            for value in water_temperatures.values:
                f.write(f"{day.strftime('%Y%m%d')},{round(float(value), 2)}\n")
                day += datetime.timedelta(1)
