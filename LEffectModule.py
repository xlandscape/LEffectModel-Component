"""
Landscape Model component of the LEffectModel effect module.
"""
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
    Encapsulation of the LEffectModel module as a Landscape Model component.
    """
    # RELEASES
    VERSION = base.VersionCollection(
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
    VERSION.changed("1.3.34", "`components.Lguts` renamed to components.LgutsRed")
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
    VERSION.fixed("2.0.3", "Determination of last year o simulation and application")
    VERSION.changed("2.0.4", "Module updated to version 20210127")
    VERSION.changed("2.0.4", "Markdown in changelog")
    VERSION.changed("2.0.4", "Proofreading")
    VERSION.fixed("2.0.4", "Data type access")

    def __init__(self, name, observer, store):
        super(LEffectModel, self).__init__(name, observer, store)
        self._module = base.Module("LEffectModel", "20201208")
        self._inputs = base.InputContainer(self, [
            base.Input(
                "ProcessingPath",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "Model",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "MinimumClutchSize",
                (attrib.Class(int, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "BackgroundMortalityRate",
                (attrib.Class(float, 1), attrib.Unit("1/d", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "DensityDependentMortalityRate",
                (attrib.Class(float, 1), attrib.Unit("m²/d", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "DominantRateConstant",
                (attrib.Class(float, 1), attrib.Unit("1/d", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "BackgroundHazardRate",
                (attrib.Class(float, 1), attrib.Unit("1/d", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ParameterZOfSDModel",
                (attrib.Class(float, 1), attrib.Unit("ng/l", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ParameterBOfSDModel",
                (attrib.Class(float, 1), attrib.Unit("l/(ng*d)"), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ThresholdOfITModel",
                (attrib.Class(float, 1), attrib.Unit("ng/l", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "BetaOfITModel",
                (attrib.Class(float, 1), attrib.Unit("1", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "AverageTemperatureParameterOfForcingFunction",
                (attrib.Class(float, 1), attrib.Unit("°C", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "AmplitudeTemperatureFluctuationsParameter",
                (attrib.Class(float, 1), attrib.Unit("°C", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ShiftForwardOfDayNumberWithLowestTemperature",
                (attrib.Class(int, 1), attrib.Unit("d", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "PerIndividualProbabilityOfMigration",
                (attrib.Class(float, 1), attrib.Unit("1/d", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ProbabilityOfAMigratingIndividualToMoveDownstream",
                (attrib.Class(float, 1), attrib.Unit("1", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ReachListHydrography",
                (attrib.Class("list[int]", 1), attrib.Unit(None, 1), attrib.Scales("space/base_geometry", 1)),
                self.default_observer
            ),
            base.Input(
                "SimulationStart",
                (attrib.Class(datetime.date, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ReachListConcentrations",
                (attrib.Class("list[int]", 1), attrib.Unit(None, 1), attrib.Scales("space/reach", 1)),
                self.default_observer
            ),
            base.Input(
                "Concentrations",
                (
                    attrib.Class(np.ndarray, 1),
                    attrib.Unit("ng/l", 1),
                    attrib.Scales("time/hour, space/base_geometry", 1)
                ),
                self.default_observer
            ),
            base.Input(
                "NumberOfWarmUpYears",
                (attrib.Class(int, 1), attrib.Unit("y", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "NumberOfStepsWithinOneHour",
                (attrib.Class(int, 1), attrib.Unit("1", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "MultiplicationFactors",
                (attrib.Class("list[float]", 1), attrib.Unit("1", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input("Verbosity", (attrib.Class(int, 1), attrib.Scales("global", 1)), self.default_observer),
            base.Input(
                "NumberRuns",
                (attrib.Class(int, 1), attrib.Scales("global", 1), attrib.Unit(None)),
                self.default_observer
            )
        ])
        self._outputs = base.OutputContainer(self, [
            base.Output("AdultMetaPopulation", store, self),
            base.Output("AdultPopulationByReach", store, self),
            base.Output("EmbryoMetaPopulation", store, self),
            base.Output("EmbryoPopulationByReach", store, self),
            base.Output("ExtentLocalPopulationsMetaPopulation", store, self),
            base.Output("JuvenileAndAdultMetaPopulation", store, self),
            base.Output("JuvenileAndAdultPopulationByReach", store, self),
            base.Output("JuvenileMetaPopulation", store, self),
            base.Output("JuvenilePopulationByReach", store, self),
            base.Output("GutsSurvivalReaches", store, self)
        ])
        return

    def run(self):
        """
        Runs the component.
        :return: Nothing.
        """
        processing_path = self.inputs["ProcessingPath"].read().values
        model = self.inputs["Model"].read().values
        multiplication_factors = self._inputs["MultiplicationFactors"].read().values
        simulation_start = self.inputs["SimulationStart"].read().values
        number_of_warm_up_years = self._inputs["NumberOfWarmUpYears"].read().values
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
                processing_path, "ETInput", model + "ModelSystem", "parameters", model + "ModelSystem_coefs.csv"),
            model
        )
        # noinspection SpellCheckingInspection
        self.prepare_reach_list(os.path.join(
            processing_path, "ETInput", model + "ModelSystem", "maps", "shapes", "reachlist_shp", "Reachlist_shp.shp"
        ))
        time_slices = self.get_time_slices()
        self.prepare_concentrations(
            os.path.join(processing_path, "ETInput", "CatchmentModelSystem", "data"), time_slices, simulation_start)
        if model in ["LPopSD", "LPopIT"]:
            self.prepare_control_population_model(
                os.path.join(
                    processing_path, "ETInput", model + "ModelSystem", "parameters", model + "ModelSystem_control.csv"),
                simulation_start,
                number_of_warm_up_years
            )
            self.run_module(processing_path)
            # noinspection SpellCheckingInspection
            self.store_results_per_day(
                os.path.join(processing_path, "ecotalk", model + "ModelSystem_MoS", "x1", "x1s{}"),
                {
                    "x1s{}r{}_adultMetapop.txt": "AdultMetaPopulation",
                    "x1s{}r{}_embryoMetapop.txt": "EmbryoMetaPopulation",
                    "x1s{}r{}_extantLocalPopsMetapop.txt": "ExtentLocalPopulationsMetaPopulation",
                    "x1s{}r{}_juvAndAdultMetapop.txt": "JuvenileAndAdultMetaPopulation",
                    "x1s{}r{}_juvenileMetapop.txt": "JuvenileMetaPopulation"
                },
                simulation_start.year,
                len(time_slices),
                number_of_warm_up_years,
                len(multiplication_factors),
                number_runs
            )
            # noinspection SpellCheckingInspection
            self.store_results_per_day_and_reach(
                os.path.join(processing_path, "ecotalk", model + "ModelSystem_Mos", "x1", "x1s{}"),
                {
                    "x1s{}r{}_adultPopByReach.txt": "AdultPopulationByReach",
                    "x1s{}r{}_embryoPopByReach.txt": "EmbryoPopulationByReach",
                    "x1s{}r{}_juvAndAdultPopByReach.txt": "JuvenileAndAdultPopulationByReach",
                    "x1s{}r{}_juvenilePopByReach.txt": "JuvenilePopulationByReach"
                },
                simulation_start.year,
                len(time_slices),
                number_of_warm_up_years,
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
                        model + "ModelSystem",
                        "parameters",
                        model + "ModelSystem_control.csv"
                    ),
                    simulation_start,
                    y
                )
                self.run_module(processing_path)
                # noinspection SpellCheckingInspection
                os.rename(
                    os.path.join(processing_path, "ecotalk", model + "ModelSystem_MoS.modelscript"),
                    os.path.join(processing_path, "ecotalk", model + "ModelSystem_MoS.modelscript." + str(y))
                )
                # noinspection SpellCheckingInspection
                os.rename(
                    os.path.join(processing_path, "ecotalk", model + "ModelSystem_MoS"),
                    os.path.join(processing_path, "ecotalk", model + "ModelSystem_MoS_" + str(y))
                )
            # noinspection SpellCheckingInspection
            self.store_results_per_year_and_reach(
                os.path.join(processing_path, "ecotalk", model + "ModelSystem_MoS_{}", "x1"),
                {"guts_survival_reaches.txt_mfactors.txt": "GutsSurvivalReaches"},
                len(time_slices),
                self._inputs["Concentrations"].describe()["shape"][1],
                len(multiplication_factors)
            )
        else:
            raise ValueError("Unexpected model: " + model)
        return

    @staticmethod
    def prepare_runtime_environment(processing_path, files, model):
        """
        Prepares the runtime environment of the module.
        :param processing_path: The working directory of the module.
        :param files: The files required for the runtime environment to work properly.
        :param model: The identifier of the model used.
        :return: Nothing.
        """
        # noinspection SpellCheckingInspection
        os.makedirs(os.path.join(processing_path, "ecotalk"))
        os.makedirs(os.path.join(processing_path, "ETInput", model + "ModelSystem", "parameters"))
        # noinspection SpellCheckingInspection
        os.makedirs(os.path.join(processing_path, "ETInput", model + "ModelSystem", "maps", "shapes", "reachlist_shp"))
        os.makedirs(os.path.join(processing_path, "ETInput", "CatchmentModelSystem", "data"))
        for file in files:
            shutil.copyfile(file[0], file[1])
        return

    @staticmethod
    def prepare_startup_statements(statements_file, model, multiplication_factors, number_runs):
        """
        Prepares the SmallTalk statement file.
        :param statements_file: The path for the statement file.
        :param model: The identifier of the model used.
        :param multiplication_factors: A list of multiplication factors for margin-of-safety analyses.
        :param number_runs: The number of runs to perform in a population model run.
        :return: Nothing.
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
            f.write("mfs := #({}).\n".format(" ".join([str(x) for x in multiplication_factors])))
            f.write("scriptFile := {}Project scriptMoSAnalysis{}MultiplicationFactors: mfs{}.\n".format(
                project_type, project_name, " runs: " + str(number_runs) if project_type == "LPop" else "")
            )
            f.write("(ModelProject fromScriptFile: scriptFile) runModelProjectForeground.\n")
            f.write("Smalltalk quitPrimitive\n")
        return

    def prepare_coefficients(self, coefficient_file, model):
        """
        Prepares the coefficients used by the module.
        :param coefficient_file: The file path for the coefficient file.
        :param model: The model name.
        :return: Nothing.
        """
        with open(coefficient_file, "w") as f:
            f.write("Component,model-dependent,inhabitantClass\n")
            if model in ["LPopSD", "LPopIT"]:
                f.write("minClutchSize:,{},minimum clutch size [ind]\n".format(
                    self._inputs["MinimumClutchSize"].read().values))
                f.write("backgroundMortality:,{},background mortality rate [d-1]\n".format(
                    self._inputs["BackgroundMortalityRate"].read().values))
                f.write("muDD:,{},(default 0.000010) density-dependent mortality rate [m2 ind-1 d-1]\n".format(
                    self._inputs["DensityDependentMortalityRate"].read().values))
            elif model in ["CatchmentGUTSSD", "CatchmentGUTSIT"]:
                pass
            else:
                raise ValueError("Unexpected model: " + model)
            f.write("kd:,{},dominant rate constant [1/d]\n".format(
                self._inputs["DominantRateConstant"].read().values, model))
            f.write("hb:,{},background hazard rate [1/d]\n".format(
                self._inputs["BackgroundHazardRate"].read().values, model))
            if model in ["LPopSD", "CatchmentGUTSSD"]:
                f.write("z:,{},threshold concentration [ng/L]\n".format(
                    self._inputs["ParameterZOfSDModel"].read().values))
                f.write("b:,{},killing rate [L/(ng*d)]\n".format(self._inputs["ParameterBOfSDModel"].read().values))
            elif model in ["LPopIT", "CatchmentGUTSIT"]:
                f.write("m:,{},threshold distribution [ng/L]\n".format(
                    self._inputs["ThresholdOfITModel"].read().values))
                f.write("beta:,{},width of distribution []\n".format(self._inputs["BetaOfITModel"].read().values))
            else:
                raise ValueError("Unexpected model: " + model)
            f.write("Component,model-dependent,landscapeClass\n")
            if model in ["LPopSD", "LPopIT"]:
                f.write("envTav:,{},average temperature parameter of forcing function [oC]\n".format(
                    self._inputs["AverageTemperatureParameterOfForcingFunction"].read().values))
                f.write("envTamp:,{},amplitude temperature fluctuations parameter [oC]\n".format(
                    self._inputs["AmplitudeTemperatureFluctuationsParameter"].read().values))
                # noinspection SpellCheckingInspection
                f.write("envTminShift:,{},shift forward of daynr with lowest temperature [d]\n".format(
                    self._inputs["ShiftForwardOfDayNumberWithLowestTemperature"].read().values))
            elif model in ["CatchmentGUTSSD", "CatchmentGUTSIT"]:
                pass
            else:
                raise ValueError("Unexpected model: " + model)
            f.write("conversionToGutsFactor:,1.0,(concentrations are given in ng/l; no conversion))\n")
            if model in ["LPopSD", "LPopIT"]:
                f.write("migrationProb:,{},per individual probability of migration [d-1]\n".format(
                    self._inputs["PerIndividualProbabilityOfMigration"].read().values))
                f.write("downStreamProb:,{},probability of a migrating individual to move downstream\n".format(
                    self._inputs["ProbabilityOfAMigratingIndividualToMoveDownstream"].read().values))
            elif model in ["CatchmentGUTSSD", "CatchmentGUTSIT"]:
                pass
            else:
                raise ValueError("Unexpected model: " + model)
        return

    def prepare_reach_list(self, reaches_file):
        """
        Prepares the reach list.
        :param reaches_file: The file path for the reach list.
        :return: Nothing.
        """
        reaches = self.inputs["ReachListHydrography"].read().values
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
            reach_id = feature
            reach.SetField("key", reach_id)
            reach_list_layer.CreateFeature(reach)
        return

    def get_time_slices(self):
        """
        Slices the simulation time span into individual years for module inputs and outputs.
        :return: A list of indices indicating the hours where slicing should be done.
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
        :param time_slice_path: The path for the prepared input files.
        :param time_slices: The indices by which input concentrations are sliced.
        :param simulation_start: The first day of the simulation.
        :return: Nothing.
        """
        reaches = self.inputs["ReachListConcentrations"].read().values
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
                    os.path.join(time_slice_path, "rummen_" + str(simulation_start.year + y) + ".msgpack"),
                    "wb"
            ) as f:
                msgpack.pack(concentrations, f)
        return

    def run_module(self, processing_path):
        """
        Runs the module.
        :param processing_path: The path used for processing.
        :return: Nothing.
        """
        squeak = os.path.join(os.path.dirname(__file__), "module", "squeak.exe")
        base.run_process((squeak, "LPop.image", "startup.st"), processing_path, self.default_observer)
        return

    def prepare_control_population_model(self, control_file, simulation_start, number_of_warm_up_years):
        """
        Prepares the control file.
        :param control_file: The name of the control file.
        :param simulation_start: The first day of the simulation.
        :param number_of_warm_up_years: The number of years used to warm-up the module.
        :return: Nothing.
        """
        number_hours = self.inputs["Concentrations"].describe()["shape"][0]
        with open(control_file, "w") as f:
            f.write("startYear:,{},start year of the simulation\n".format(
                simulation_start.year - number_of_warm_up_years))
            f.write("endYear:,{},last year of the simulation\n".format(
                (simulation_start + datetime.timedelta(number_hours / 24 - 1)).year))
            f.write("startApplicationYear:,{},start year of pesticide application\n".format(simulation_start.year))
            f.write("endApplicationYear:,{},last year of pesticide application\n".format(
                (simulation_start + datetime.timedelta(number_hours / 24 - 1)).year))
            f.write("useCSV:,0,use the slow csv input format (1) or much faster msgpack format(0)\n")
            f.write("stepsInHr:,{},the number of steps within 1 hourly time step for GUTS simulation".format(
                self._inputs["NumberOfStepsWithinOneHour"].read().values))
        return

    def prepare_control_individual_model(self, control_file, simulation_start, year_index):
        """
        Prepares the control file.
        :param control_file: The name of the control file.
        :param simulation_start: The first day of the simulation.
        :param year_index: The index of the current year to simulate.
        :return: Nothing.
        """
        with open(control_file, "w") as f:
            f.write("applicationYear:,{},year of pesticide application\n".format(simulation_start.year + year_index))
            f.write("verbose:,{},survival output per day (1) or end of the year only (0)\n".format(
                self._inputs["Verbosity"].read().values))
            f.write("useCSV:,0,use the slow csv input format (1) or much faster msgpack format(0)\n")
            f.write("stepsInHr:,{},the number of steps within 1 hourly time step for GUTS simulation".format(
                self._inputs["NumberOfStepsWithinOneHour"].read().values))
            f.write("useCSV:,0,use the slow csv input format (1) or much faster msgpack format(0)\n")
            f.write("stepsInHr:,{},the number of steps within 1 hourly time step for GUTS simulation".format(
                self._inputs["NumberOfStepsWithinOneHour"].read().values))
        return

    def store_results_per_day(
            self,
            time_slice_path,
            result_set,
            first_year,
            number_years,
            number_warm_up_years,
            number_multiplication_factors,
            number_runs
    ):
        """
        Reads the results into the Landscape Model.
        :param time_slice_path: The file path of the sliced module output files.
        :param result_set: A dictionary that maps file names to outputs.
        :param first_year: The first year of the simulation as an integer number.
        :param number_years: The number of years simulated.
        :param number_warm_up_years: The number of years used to warm-up the module.
        :param number_multiplication_factors: The number of multiplication factors used for the module run.
        :param number_runs: The number of runs of the population model.
        :return: Nothing.
        """
        number_days = (
                datetime.date(first_year + number_years, 1, 1) - datetime.date(first_year - number_warm_up_years, 1, 1)
        ).days
        for file_name, output_name in result_set.items():
            self._outputs[output_name].set_values(
                np.ndarray,
                shape=(number_days, number_multiplication_factors, number_runs),
                data_type=np.int,
                chunks=(number_days, 1, 1),
                scales="time/year, other/factor, other/runs",
                unit="1"
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
        return

    def store_results_per_day_and_reach(
            self,
            time_slice_path,
            result_set,
            first_year,
            number_years,
            number_warm_up_years,
            number_reaches,
            number_multiplication_factors,
            number_runs
    ):
        """
        Reads the results into the Landscape Model.
        :param time_slice_path: The file path of the sliced module output files.
        :param result_set: A dictionary that maps file names to outputs.
        :param first_year: The first year of the simulation as an integer number.
        :param number_years: The number of years simulated.
        :param number_warm_up_years: The number of years used to warm-up the module.
        :param number_reaches: The number of reaches simulated.
        :param number_multiplication_factors: The number of multiplication factors used for the module run.
        :param number_runs: The number of runs of the population model.
        :return: Nothing.
        """
        number_days = (
                datetime.date(first_year + number_years, 1, 1) - datetime.date(first_year - number_warm_up_years, 1, 1)
        ).days
        for file_name, output_name in result_set.items():
            self._outputs[output_name].set_values(
                np.ndarray,
                shape=(number_days, number_reaches, number_multiplication_factors, number_runs),
                data_type=np.int,
                chunks=(number_days, 1, 1, 1),
                scales="time/year, space/base_geometry, other/factor, other/runs",
                unit="1"
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
        return

    def store_results_per_year_and_reach(
            self, time_slice_path, result_set, number_years, number_reaches, number_multiplication_factors):
        """
        Reads the results into the Landscape Model.
        :param time_slice_path: The file path of the sliced module output files.
        :param result_set: A dictionary that maps file names to outputs.
        :param number_years: The number of years simulated.
        :param number_reaches: The number of reaches simulated.
        :param number_multiplication_factors: The number of multiplication factors used for the module run.
        :return: Nothing.
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
                scales="time/year, space/base_geometry, other/factor",
                unit="1"
            )
        return
