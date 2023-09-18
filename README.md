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

Encapsulation of the LEffectModel module as a Landscape Model component. The module provides two models: LGUTS and
LPop. LGUTS is a reduced GUTS model at catchment scale. It has two variants: GUTS-RED-IT, a reduced GUTS model
version with Individual Tolerance, and GUTS-RED-SD, a reduced GUTS version with Stochastic Death. LPop is a
DEB-based population model at catchment scale, parameterized for Asellus aquaticus. It makes use of the
GUTS- RED-IT or GUTS-RED-SD models. There is also an Abj-DEB version with population regulation through
density-dependent mortality.  
This is an automatically generated documentation based on the available code and in-line documentation. The current
version of this document is from 2023-09-18.

### Built with

* Landscape Model core version 1.15.5
* LEffectModel version 20211111-1 (see `\module\doc\LEffectModel_Manual_20211111.pdf` for details)

## Getting Started

The component can be used in any Landscape Model based on core version 1.15.5 or newer. See the Landscape
Model core's `README` for general tips on how to add a component to a Landscape Model.

### Prerequisites

A model developer that wants to add the `LEffectModel` component to a Landscape Model needs to set up the general
structure for a Landscape Model first. See the Landscape Model core's `README` for details on how to do so.

### Installation

1. Copy the `LEffectModel` component into the `model\variant` sub-folder.
2. Make use of the component by including it into the model composition using `module=LEffectModel.LEffectModule` and
   `class=LEffectModel`.

## Usage

The following gives a sample configuration of the `LEffectModel` component. See [inputs](#inputs) and
[outputs](#outputs) for further details on the component's interface.

```xml
<IndEffect_StepsRiverNetwork_SD_Species1 module="LEffectModel" class="LEffectModel"
enabled_expression="'$(RunStepsRiverNetwork)' == 'true' and '$(RunLGuts)' == 'true'">
    <ProcessingPath
scales="global">
        $(_MCS_BASE_DIR_)\$(_MC_NAME_)\processing\effect\ind_steps_sd_$(Species1)
    </ProcessingPath>
<Model scales="global">CatchmentGUTSSD</Model>
    <MinimumClutchSize type="int" scales="global">14</MinimumClutchSize>
<BackgroundMortalityRate type="float" unit="1/d" scales="global">0.005</BackgroundMortalityRate>
<DensityDependentMortalityRate type="float" unit="m&#178;/d" scales="global">
        0.000025
</DensityDependentMortalityRate>
    <DominantRateConstant type="float" unit="1/h" scales="global">
$(Species1DominantRateConstantSD)
    </DominantRateConstant>
    <BackgroundHazardRate type="float" unit="1/h"
scales="global">
        $(LGUTS_BackgroundHazardRate)
    </BackgroundHazardRate>
    <ParameterZOfSDModel type="float"
unit="ng/l" scales="global">
        $(Species1ThresholdConcentrationSD)
    </ParameterZOfSDModel>
<ParameterBOfSDModel type="float" unit="l/(ng*h)" scales="global">
        $(Species1KillingRateSD)
</ParameterBOfSDModel>
    <AverageTemperatureParameterOfForcingFunction type="float" unit="&#176;C" scales="global">
10
    </AverageTemperatureParameterOfForcingFunction>
    <AmplitudeTemperatureFluctuationsParameter type="float"
unit="&#176;C" scales="global">
        10
    </AmplitudeTemperatureFluctuationsParameter>
<ShiftForwardOfDayNumberWithLowestTemperature type="int" unit="d" scales="global">
        31
</ShiftForwardOfDayNumberWithLowestTemperature>
    <PerIndividualProbabilityOfMigration type="float" unit="1/d"
scales="global">
        0.05
    </PerIndividualProbabilityOfMigration>
<ProbabilityOfAMigratingIndividualToMoveDownstream type="float" unit="1" scales="global">
        0.667
</ProbabilityOfAMigratingIndividualToMoveDownstream>
    <SimulationStart type="date"
scales="global">$(SimulationStart)</SimulationStart>
    <Concentrations>
        <FromOutput
component="StepsRiverNetwork" output="PEC_SW" />
    </Concentrations>
    <NumberOfWarmUpYears type="int" unit="y"
scales="global">$(NumberOfWarmUpYears)</NumberOfWarmUpYears>
    <RecoveryPeriodYears type="int" unit="y"
scales="global">$(RecoveryPeriodYears)</RecoveryPeriodYears>
    <NumberOfStepsWithinOneHour type="int" unit="1"
scales="global">2</NumberOfStepsWithinOneHour>
    <MultiplicationFactors type="list[float]" unit="1"
scales="other/factor" element_names="IndEffect_StepsRiverNetwork_SD_Species1/MultiplicationFactors">
$(MultiplicationFactors)
    </MultiplicationFactors>
    <Verbosity type="int" scales="global">0</Verbosity>
</IndEffect_StepsRiverNetwork_SD_Species1>
```

### Inputs

#### ProcessingPath

The working directory for the module. It is used for all files prepared as module inputs  or generated as (temporary)
module outputs.
`ProcessingPath` expects its values to be of type `str`.
Values of the `ProcessingPath` input may not have a physical unit.
Values have to refer to the `global` scale.

#### Model

Specifies the model that is applied to the input data. This can either be an individual based GUTS model (choices
starting with `CatchmentGUTS`) or a population based effect model (choices starting with `LPop`). The choice of model
also determines whether astochastic death version (choices ending with `SD`) or an individual tolerance version (choices
ending with `IT`) is used.
`Model` expects its values to be of type `str`.
Values of the `Model` input may not have a physical unit.
Values have to refer to the `global` scale.
Allowed values are: `CatchmentGUTSSD`, `CatchmentGUTSIT`, `LPopSD`, `LPopIT`.

#### MinimumClutchSize

Used by population models.
`MinimumClutchSize` expects its values to be of type `int`.
The physical unit of the `MinimumClutchSize` input values is `1`.
Values have to refer to the `global` scale.

#### BackgroundMortalityRate

Used by population models.
`BackgroundMortalityRate` expects its values to be of type `float`.
The physical unit of the `BackgroundMortalityRate` input values is `1/d`.
Values have to refer to the `global` scale.

#### DensityDependentMortalityRate

Used by population models.
`DensityDependentMortalityRate` expects its values to be of type `float`.
The physical unit of the `DensityDependentMortalityRate` input values is `m²/d`.
Values have to refer to the `global` scale.

#### DominantRateConstant

Used by all models.
`DominantRateConstant` expects its values to be of type `float`.
The physical unit of the `DominantRateConstant` input values is `1/d`.
Values have to refer to the `global` scale.

#### BackgroundHazardRate

Used by all models.
`BackgroundHazardRate` expects its values to be of type `float`.
The physical unit of the `BackgroundHazardRate` input values is `1/d`.
Values have to refer to the `global` scale.

#### ParameterZOfSDModel

Used by stochastic death models.
`ParameterZOfSDModel` expects its values to be of type `float`.
The physical unit of the `ParameterZOfSDModel` input values is `ng/l`.
Values have to refer to the `global` scale.

#### ParameterBOfSDModel

Used by stochastic death models.
`ParameterBOfSDModel` expects its values to be of type `float`.
The physical unit of the `ParameterBOfSDModel` input values is `l/(ng*d)`.
Values have to refer to the `global` scale.

#### ThresholdOfITModel

Used by individual tolerance models.
`ThresholdOfITModel` expects its values to be of type `float`.
The physical unit of the `ThresholdOfITModel` input values is `ng/l`.
Values have to refer to the `global` scale.

#### BetaOfITModel

Used by individual tolerance models.
`BetaOfITModel` expects its values to be of type `float`.
The physical unit of the `BetaOfITModel` input values is `1`.
Values have to refer to the `global` scale.

#### AverageTemperatureParameterOfForcingFunction

Used by population models.
`AverageTemperatureParameterOfForcingFunction` expects its values to be of type `float`.
The physical unit of the `AverageTemperatureParameterOfForcingFunction` input values is `°C`.
Values have to refer to the `global` scale.

#### AmplitudeTemperatureFluctuationsParameter

Used by population models.
`AmplitudeTemperatureFluctuationsParameter` expects its values to be of type `float`.
The physical unit of the `AmplitudeTemperatureFluctuationsParameter` input values is `°C`.
Values have to refer to the `global` scale.

#### ShiftForwardOfDayNumberWithLowestTemperature

Used by population models.
`ShiftForwardOfDayNumberWithLowestTemperature` expects its values to be of type `int`.
The physical unit of the `ShiftForwardOfDayNumberWithLowestTemperature` input values is `d`.
Values have to refer to the `global` scale.

#### PerIndividualProbabilityOfMigration

Used by population models.
`PerIndividualProbabilityOfMigration` expects its values to be of type `float`.
The physical unit of the `PerIndividualProbabilityOfMigration` input values is `1/d`.
Values have to refer to the `global` scale.

#### ProbabilityOfAMigratingIndividualToMoveDownstream

Used by population models.
`ProbabilityOfAMigratingIndividualToMoveDownstream` expects its values to be of type `float`.
The physical unit of the `ProbabilityOfAMigratingIndividualToMoveDownstream` input values is `1`.
Values have to refer to the `global` scale.

#### SimulationStart

The first time step for which concentration input data is provided. This input also defines the base year for
LEffectModel simulations. Actual simulation starts `NumberOfWarmUpYears` earlier and ends `RecoveryPeriodYears` later.
This input will be removed in a future version of the `LEffectModule` component.
`SimulationStart` expects its values to be of type `date`.
Values of the `SimulationStart` input may not have a physical unit.
Values have to refer to the `global` scale.

#### Concentrations

`Concentrations` expects its values to be of type `ndarray`.
The physical unit of the `Concentrations` input values is `ng/l`.
Values have to refer to the `time/hour, space/reach` scale.

#### NumberOfWarmUpYears

`NumberOfWarmUpYears` expects its values to be of type `int`.
The physical unit of the `NumberOfWarmUpYears` input values is `y`.
Values have to refer to the `global` scale.

#### RecoveryPeriodYears

`RecoveryPeriodYears` expects its values to be of type `int`.
The physical unit of the `RecoveryPeriodYears` input values is `y`.
Values have to refer to the `global` scale.

#### NumberOfStepsWithinOneHour

`NumberOfStepsWithinOneHour` expects its values to be of type `int`.
The physical unit of the `NumberOfStepsWithinOneHour` input values is `1`.
Values have to refer to the `global` scale.

#### MultiplicationFactors

To determine LP50 values, the concentration multiplication factor leading to a 50% reduction of final survival in the
GUTS model, simulations for all reaches are run applying a series of multiplication factors to the hourly concentration
time series. Ideally, the full range from 0 to 100% effect (reduction of survival) should be covered, to ensure a
reliable LP50 estimation by fitting a dose-response relationship. As a kind of brute-force approach, multiplication
factors could be set according to a power function, e.g., ranging from 2^-10 to 2^15 (1/512 to 16384).
`MultiplicationFactors` expects its values to be of type `list`.
The physical unit of the `MultiplicationFactors` input values is `1`.
Values have to refer to the `other/factor` scale.

#### Verbosity

If set to `1`, survival is reported per day, else only at the end of each simulated year. This affects only the output
of the module, but not of the component. Vhanging this input is therefore mainly useful for debugging.
`Verbosity` expects its values to be of type `int`.
Values have to refer to the `global` scale.
Values of the `Verbosity` input may not have a physical unit.
Allowed values are: `0`, `1`.

#### NumberRuns

`NumberRuns` expects its values to be of type `int`.
Values have to refer to the `global` scale.
The physical unit of the `NumberRuns` input values is `1`.

#### UseTemperatureInput

Specifies, whether the empirical water temperature data from the `WaterTemperature` input is used or whether this data
is ignored and a forcing function is applied, instead.
`UseTemperatureInput` expects its values to be of type `bool`.
Values have to refer to the `global` scale.
Values of the `UseTemperatureInput` input may not have a physical unit.

#### WaterTemperature

`WaterTemperature` expects its values to be of type `ndarray`.
Values have to refer to the `time/day` scale.
The physical unit of the `WaterTemperature` input values is `°C`.

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
The values apply to the following scale: `time/day, space/reach, other/factor, other/runs`.
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
The values apply to the following scale: `time/day, space/reach, other/factor, other/runs`.
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
The values apply to the following scale: `time/day, space/reach, other/factor, other/runs`.
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
The values apply to the following scale: `time/day, space/reach, other/factor, other/runs`.
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
The values apply to the following scale: `time/year, space/reach, other/factor`.
The physical unit of the values is `1`.

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
