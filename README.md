## Table of Contents
* [About the project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Inputs](#inputs)
  * [Outputs](#outputs)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)


## About the project
Encapsulation of the LEffectModel module as a Landscape Model component.  
This is an automatically generated documentation based on the available code and in-line documentation. The current
version of this document is from 2021-10-11.  

### Built with
* Landscape Model core version 1.8
* LEffectModel version 20201208 (see `\module\doc\LEffectModel_Manual.pdf` for details)


## Getting Started
The component can be used in any Landscape Model based on core version 1.8 or newer. See the Landscape
Model core's `README` for general tips on how to add a component to a Landscape Model.

### Prerequisites
A model developer that wants to add the `IndEffect_StepsRiverNetwork_SD_Species1` component to a Landscape Model needs to set up the general 
structure for a Landscape Model first. See the Landscape Model core's `README` for details on how to do so.

### Installation
1. Copy the `LEffectModel` component into the `model\variant` sub-folder.
2. Make use of the component by including it into the model composition using `module=LEffectModel.LEffectModule` and 
   `class=LEffectModel`. 


## Usage
The following gives a sample configuration of the `IndEffect_StepsRiverNetwork_SD_Species1` component. See [inputs](#inputs) and 
[outputs](#outputs) for further details on the component's interface.
```xml
<IndEffect_StepsRiverNetwork_SD_Species1 module="LEffectModel" class="LEffectModel"
enabled_expression="'$(RunStepsRiverNetwork)' == 'true' and '$(RunLGuts)' == 'true'">
<ProcessingPath>$(_MCS_BASE_DIR_)\$(_MC_NAME_)\processing\effect\ind_steps_sd_$(Species1)</ProcessingPath>
<Model>CatchmentGUTSSD</Model>
    <MinimumClutchSize type="int">14</MinimumClutchSize>
    <BackgroundMortalityRate
type="float" unit="1/d">0.005</BackgroundMortalityRate>
    <DensityDependentMortalityRate type="float"
unit="m&#178;/d">0.000025</DensityDependentMortalityRate>
    <DominantRateConstant type="float"
unit="1/h">$(Species1DominantRateConstantSD)</DominantRateConstant>
    <BackgroundHazardRate type="float"
unit="1/h">$(LGUTS_BackgroundHazardRate)</BackgroundHazardRate>
    <ParameterZOfSDModel type="float"
unit="ng/l">$(Species1ThresholdConcentrationSD)</ParameterZOfSDModel>
    <ParameterBOfSDModel type="float"
unit="l/(ng*h)">$(Species1KillingRateSD)</ParameterBOfSDModel>
    <AverageTemperatureParameterOfForcingFunction
type="float" unit="&#176;C">
        10
    </AverageTemperatureParameterOfForcingFunction>
<AmplitudeTemperatureFluctuationsParameter type="float" unit="&#176;C">
        10
</AmplitudeTemperatureFluctuationsParameter>
    <ShiftForwardOfDayNumberWithLowestTemperature type="int" unit="d">
31
    </ShiftForwardOfDayNumberWithLowestTemperature>
    <PerIndividualProbabilityOfMigration type="float"
unit="1/d">0.05</PerIndividualProbabilityOfMigration>
    <ProbabilityOfAMigratingIndividualToMoveDownstream
type="float" unit="1">
        0.667
    </ProbabilityOfAMigratingIndividualToMoveDownstream>
    <ReachListHydrography>
<FromOutput component="LandscapeScenario" output="hydrography_id" />
    </ReachListHydrography>
    <SimulationStart
type="date">$(SimulationStart)</SimulationStart>
    <Concentrations>
        <FromOutput component="StepsRiverNetwork"
output="PEC_SW" />
    </Concentrations>
    <ReachListConcentrations>
        <FromOutput component="StepsRiverNetwork"
output="Reaches" />
    </ReachListConcentrations>
    <NumberOfWarmUpYears type="int"
unit="y">$(NumberOfWarmUpYears)</NumberOfWarmUpYears>
    <RecoveryPeriodYears type="int"
unit="y">$(RecoveryPeriodYears)</RecoveryPeriodYears>
    <NumberOfStepsWithinOneHour type="int"
unit="1">2</NumberOfStepsWithinOneHour>
    <MultiplicationFactors type="list[float]"
unit="1">$(MultiplicationFactors)</MultiplicationFactors>
    <Verbosity type="int">0</Verbosity>
</IndEffect_StepsRiverNetwork_SD_Species1>
```

### Inputs
#### ProcessingPath
The working directory for the module. It is used for all files prepared as module inputs
or generated as (temporary) module outputs.  
`ProcessingPath` expects its values to be of type `str`.
Values of the `ProcessingPath` input may not have a physical unit.
Values have to refer to the `global` scale.

#### Model
Specifies the model that is applied to the input data. This can either be an individual
based GUTS model (choices starting with _CatchmentGUTS_) or a population based effect model (choices
starting with _LPop_). The choice of model also determines whether sudden death (choices ending with 
_SD_) or an internal threshold (choices ending with _IT_) is assumed.  
`Model` expects its values to be of type `str`.
Values of the `Model` input may not have a physical unit.
Values have to refer to the `global` scale.
Allowed values are: `CatchmentGUTSSD`, `CatchmentGUTSIT`, `LPopSD`, `LPopIT`.

#### MinimumClutchSize
The minimum clutch size (minClutchSize) used by population models.  
`MinimumClutchSize` expects its values to be of type `int`.
Values of the `MinimumClutchSize` input may not have a physical unit.
Values have to refer to the `global` scale.

#### BackgroundMortalityRate
The background mortality rate (backgroundMortality) used by population models.  
`BackgroundMortalityRate` expects its values to be of type `float`.
The physical unit of the `BackgroundMortalityRate` input values is `1/d`.
Values have to refer to the `global` scale.

#### DensityDependentMortalityRate
The density-dependent mortality rate (muDD) used by population models.  
`DensityDependentMortalityRate` expects its values to be of type `float`.
The physical unit of the `DensityDependentMortalityRate` input values is `m²/d`.
Values have to refer to the `global` scale.

#### DominantRateConstant
The dominant rate constant (kd) used by all models.  
`DominantRateConstant` expects its values to be of type `float`.
The physical unit of the `DominantRateConstant` input values is `1/d`.
Values have to refer to the `global` scale.

#### BackgroundHazardRate
The background hazard rate (hb) used by all models.  
`BackgroundHazardRate` expects its values to be of type `float`.
The physical unit of the `BackgroundHazardRate` input values is `1/d`.
Values have to refer to the `global` scale.

#### ParameterZOfSDModel
The threshold concentration (z) used by sudden death models.  
`ParameterZOfSDModel` expects its values to be of type `float`.
The physical unit of the `ParameterZOfSDModel` input values is `ng/l`.
Values have to refer to the `global` scale.

#### ParameterBOfSDModel
The killing rate (b) used by sudden death models.  
`ParameterBOfSDModel` expects its values to be of type `float`.
The physical unit of the `ParameterBOfSDModel` input values is `l/(ng*d)`.
Values have to refer to the `global` scale.

#### ThresholdOfITModel
The threshold distribution  (m) used by internal threshold models.  
`ThresholdOfITModel` expects its values to be of type `float`.
The physical unit of the `ThresholdOfITModel` input values is `ng/l`.
Values have to refer to the `global` scale.

#### BetaOfITModel
The width of distribution (beta) used by internal threshold models.  
`BetaOfITModel` expects its values to be of type `float`.
The physical unit of the `BetaOfITModel` input values is `1`.
Values have to refer to the `global` scale.

#### AverageTemperatureParameterOfForcingFunction
The average temperature parameter of the forcing function (envTav) used by population
models.  
`AverageTemperatureParameterOfForcingFunction` expects its values to be of type `float`.
The physical unit of the `AverageTemperatureParameterOfForcingFunction` input values is `°C`.
Values have to refer to the `global` scale.

#### AmplitudeTemperatureFluctuationsParameter
The amplitude temperature fluctuations parameter of the forcing function (envTamp) used
by population models.  
`AmplitudeTemperatureFluctuationsParameter` expects its values to be of type `float`.
The physical unit of the `AmplitudeTemperatureFluctuationsParameter` input values is `°C`.
Values have to refer to the `global` scale.

#### ShiftForwardOfDayNumberWithLowestTemperature
The temporal shift forward with the lowest temperature (envTMinShift) used by population
models.  
`ShiftForwardOfDayNumberWithLowestTemperature` expects its values to be of type `int`.
The physical unit of the `ShiftForwardOfDayNumberWithLowestTemperature` input values is `d`.
Values have to refer to the `global` scale.

#### PerIndividualProbabilityOfMigration
The probability of an individual to migrate to an adjacent reach (migrationProb) used by
population models.  
`PerIndividualProbabilityOfMigration` expects its values to be of type `float`.
The physical unit of the `PerIndividualProbabilityOfMigration` input values is `1/d`.
Values have to refer to the `global` scale.

#### ProbabilityOfAMigratingIndividualToMoveDownstream
The probability of a migrating individual to migrate to the downstream reach (instead of
the upstream reach; downStreamProb) used by population models.  
`ProbabilityOfAMigratingIndividualToMoveDownstream` expects its values to be of type `float`.
The physical unit of the `ProbabilityOfAMigratingIndividualToMoveDownstream` input values is `1`.
Values have to refer to the `global` scale.

#### ReachListHydrography
The numeric identifiers for individual reaches (in the order of the scenario hydrography 
input) that apply scenario-wide. This is a temporary solution to ensure outputs to be in original 
scenario data order.  
`ReachListHydrography` expects its values to be of type `list`.
Values of the `ReachListHydrography` input may not have a physical unit.
Values have to refer to the `space/base_geometry` scale.

#### SimulationStart
The first time step for which concentration input data is provided. This input also 
defines the base year for LEffectModel simulations. Actual simulation starts `NumberOfWarmUpYears`
earlier and ends `RecoveryPeriodYears` later.  
`SimulationStart` expects its values to be of type `date`.
Values of the `SimulationStart` input may not have a physical unit.
Values have to refer to the `global` scale.

#### ReachListConcentrations
The numeric identifiers for individual reaches (in the order of the `Concentrations` 
input) that apply scenario-wide.  
`ReachListConcentrations` expects its values to be of type `list`.
Values of the `ReachListConcentrations` input may not have a physical unit.
Values have to refer to the `space/reach` scale.

#### Concentrations
The substance concentrations reported starting with the `SimulationStart`.
Concentrations during the warm-up years and during the recovery period are assumed to be globally 
zero.  
`Concentrations` expects its values to be of type `ndarray`.
The physical unit of the `Concentrations` input values is `ng/l`.
Values have to refer to the `time/hour, space/base_geometry` scale.

#### NumberOfWarmUpYears
The number of years the module runs before the year of the `SimulationStart`.  
`NumberOfWarmUpYears` expects its values to be of type `int`.
The physical unit of the `NumberOfWarmUpYears` input values is `y`.
Values have to refer to the `global` scale.

#### RecoveryPeriodYears
The number of years the module runs after the last year for which `Concentration` data is
available.  
`RecoveryPeriodYears` expects its values to be of type `int`.
The physical unit of the `RecoveryPeriodYears` input values is `y`.
Values have to refer to the `global` scale.

#### NumberOfStepsWithinOneHour
The number of steps within one hour used by the GUTS simulation.  
`NumberOfStepsWithinOneHour` expects its values to be of type `int`.
The physical unit of the `NumberOfStepsWithinOneHour` input values is `1`.
Values have to refer to the `global` scale.

#### MultiplicationFactors
The multiplication factors applied to enable LP50 analyses. Include a factor of 1 for
simulations returning unscaled LEffectModel results.  
`MultiplicationFactors` expects its values to be of type `list`.
The physical unit of the `MultiplicationFactors` input values is `1`.
Values have to refer to the `global` scale.

#### Verbosity
`Verbosity` expects its values to be of type `int`.
Values have to refer to the `global` scale.

#### NumberRuns
The number of internal Monte Carlo runs performed by the module.  
`NumberRuns` expects its values to be of type `int`.
Values have to refer to the `global` scale.
Values of the `NumberRuns` input may not have a physical unit.

### Outputs
#### AdultMetaPopulation
The total number of all adults.  
Values are expectedly of type `ndarray`.
Value representation is in a 3-dimensional array.
Dimension 1 spans the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period.
Dimension 2 spans the number of items in the [MultiplicationFactors](#MultiplicationFactors) input.
Dimension 3 spans the `NumberRuns`.
Chunking of the array is for fast retrieval of time series.
Individual array elements have a type of `int`.
The values apply to the following scale: `time/day, other/factor, other/runs`.
The physical unit of the values is `1`.
#### AdultPopulationByReach
The number of adults.  
Values are expectedly of type `ndarray`.
Value representation is in a 4-dimensional array.
Dimension 1 spans the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period.
Dimension 2 spans the number of reaches reported by the [Concentrations](#Concentrations) input.
Dimension 3 spans the number of items in the [MultiplicationFactors](#MultiplicationFactors) input.
Dimension 4 spans the `NumberRuns`.
Chunking of the array is for fast retrieval of time series.
Individual array elements have a type of `int`.
The values apply to the following scale: `time/day, space/base_geometry, other/factor, other/runs`.
The physical unit of the values is `1`.
#### EmbryoMetaPopulation
The total number of all embryos.  
Values are expectedly of type `ndarray`.
Value representation is in a 3-dimensional array.
Dimension 1 spans the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period.
Dimension 2 spans the number of items in the [MultiplicationFactors](#MultiplicationFactors) input.
Dimension 3 spans the `NumberRuns`.
Chunking of the array is for fast retrieval of time series.
Individual array elements have a type of `int`.
The values apply to the following scale: `time/day, other/factor, other/runs`.
The physical unit of the values is `1`.
#### EmbryoPopulationByReach
The number of embryos.  
Values are expectedly of type `ndarray`.
Value representation is in a 4-dimensional array.
Dimension 1 spans the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period.
Dimension 2 spans the number of reaches reported by the [Concentrations](#Concentrations) input.
Dimension 3 spans the number of items in the [MultiplicationFactors](#MultiplicationFactors) input.
Dimension 4 spans the `NumberRuns`.
Chunking of the array is for fast retrieval of time series.
Individual array elements have a type of `int`.
The values apply to the following scale: `time/day, space/base_geometry, other/factor, other/runs`.
The physical unit of the values is `1`.
#### ExtantLocalPopulationsMetaPopulation
The total number of populations that went extant.  
Values are expectedly of type `ndarray`.
Value representation is in a 3-dimensional array.
Dimension 1 spans the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period.
Dimension 2 spans the number of items in the [MultiplicationFactors](#MultiplicationFactors) input.
Dimension 3 spans the `NumberRuns`.
Chunking of the array is for fast retrieval of time series.
Individual array elements have a type of `int`.
The values apply to the following scale: `time/day, other/factor, other/runs`.
The physical unit of the values is `1`.
#### JuvenileAndAdultMetaPopulation
The total number of all adults and juveniles combined.  
Values are expectedly of type `ndarray`.
Value representation is in a 3-dimensional array.
Dimension 1 spans the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period.
Dimension 2 spans the number of items in the [MultiplicationFactors](#MultiplicationFactors) input.
Dimension 3 spans the `NumberRuns`.
Chunking of the array is for fast retrieval of time series.
Individual array elements have a type of `int`.
The values apply to the following scale: `time/day, other/factor, other/runs`.
The physical unit of the values is `1`.
#### JuvenileAndAdultPopulationByReach
The number of juveniles and adults combined.  
Values are expectedly of type `ndarray`.
Value representation is in a 4-dimensional array.
Dimension 1 spans the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period.
Dimension 2 spans the number of reaches reported by the [Concentrations](#Concentrations) input.
Dimension 3 spans the number of items in the [MultiplicationFactors](#MultiplicationFactors) input.
Dimension 4 spans the `NumberRuns`.
Chunking of the array is for fast retrieval of time series.
Individual array elements have a type of `int`.
The values apply to the following scale: `time/day, space/base_geometry, other/factor, other/runs`.
The physical unit of the values is `1`.
#### JuvenileMetaPopulation
The total number of all juveniles.  
Values are expectedly of type `ndarray`.
Value representation is in a 3-dimensional array.
Dimension 1 spans the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period.
Dimension 2 spans the number of items in the [MultiplicationFactors](#MultiplicationFactors) input.
Dimension 3 spans the `NumberRuns`.
Chunking of the array is for fast retrieval of time series.
Individual array elements have a type of `int`.
The values apply to the following scale: `time/day, other/factor, other/runs`.
The physical unit of the values is `1`.
#### JuvenilePopulationByReach
The number of juveniles.  
Values are expectedly of type `ndarray`.
Value representation is in a 4-dimensional array.
Dimension 1 spans the total number of days in the years at least partly covered by the 
                        [Concentrations](#Concentrations) input plus the years of the warm-up period plus the years of 
                        the recovery period.
Dimension 2 spans the number of reaches reported by the [Concentrations](#Concentrations) input.
Dimension 3 spans the number of items in the [MultiplicationFactors](#MultiplicationFactors) input.
Dimension 4 spans the `NumberRuns`.
Chunking of the array is for fast retrieval of time series.
Individual array elements have a type of `int`.
The values apply to the following scale: `time/day, space/base_geometry, other/factor, other/runs`.
The physical unit of the values is `1`.
#### GutsSurvivalReaches
The probability of an individual to survive.  
Values are expectedly of type `ndarray`.
Individual array elements have a type of `float`.
Value representation is in a 3-dimensional array.
Dimension 1 spans the number of years at least partly covered by the [Concentrations](#Concentrations) input 
                        plus the number of years of the warm-up period plus the number of years of the recovery 
                        period.
Dimension 2 spans the number of reaches reported by the [Concentrations](#Concentrations) input.
Dimension 3 spans the number of items in the [MultiplicationFactors](#MultiplicationFactors) input.
Chunking of the array is for allowing compression (only one chunk used).
The values apply to the following scale: `time/year, space/base_geometry, other/factor`.
The physical unit of the values is `1`.
#### Reaches
The numerical identifiers of the reaches in the order presented by the various outputs.  
Values are expectedly of type `same as of the [ReachListHydrography](#ReachListHydrography) input`.
Values have no physical unit.


## Roadmap
The following changes will be part of future `LEffectModel` versions:
* Start module GUI in background 
([#2](https://gitlab.bayer.com/aqrisk-landscape/leffectmodel-component/-/issues/2))
* Numbering of reaches ([#4](https://gitlab.bayer.com/aqrisk-landscape/leffectmodel-component/-/issues/4))


## Contributing
Contributions are welcome. Please contact the authors (see [Contact](#contact)). Also consult the `CONTRIBUTING` 
document for more information.


## License
Distributed under the CC0 License. See `LICENSE` for more information.


## Contact
Sascha Bub (component) - sascha.bub@gmx.de  
Thorsten Schad (component) - thorsten.schad@bayer.com  
Hans Baveco (module) - hans.baveco@wur.nl  


## Acknowledgements
* [MessagePack](https://msgpack.org)  
* [NumPy](https://numpy.org)  
