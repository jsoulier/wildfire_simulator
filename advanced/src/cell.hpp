#pragma once

#include <cmath>
#include <cfloat>
#include <nlohmann/json.hpp>
#include <cadmium/celldevs/asymm/cell.hpp>
#include <cadmium/celldevs/asymm/config.hpp>
#include <behave/surface.h>
#include <behave/fuelModels.h>
#include "state.hpp"

class Cell : public cadmium::celldevs::AsymmCell<State, double>
{
public:
    Cell(const std::string& id, const std::shared_ptr<const cadmium::celldevs::AsymmCellConfig<State, double>>& config)
        : cadmium::celldevs::AsymmCell<State, double>(id, config) {}

    [[nodiscard]] State localComputation(State state, const std::unordered_map<
        std::string, cadmium::celldevs::NeighborData<State, double>>& neighborhood) const override
    {
        if (state.ignited || (state.willIgnite && state.ignitionTime <= this->clock))
        {
            state.ignited = true;
            return state;
        }
        for (const auto& [neighborId, neighborData]: neighborhood)
        {
            if (!neighborData.state->ignited)
            {
                continue;
            }
            double deltaX = state.x - neighborData.state->x;
            double deltaY = state.y - neighborData.state->y;
            double direction = atan2(deltaX, deltaY) * 180.0 / M_PI;
            FuelModels fuelModels;
            Surface surface(fuelModels);
            surface.updateSurfaceInputsForTwoFuelModels(
                neighborData.state->fuelModelNumber,
                state.fuelModelNumber,
                1.0, // moistureOneHour
                1.0, // moistureTenHour
                1.0, // moistureHundredHour
                0.0, // moistureLiveHerbaceous
                0.0, // moistureLiveWoody,
                FractionUnits::Percent, // moistureUnits
                neighborData.state->windSpeed,
                SpeedUnits::MetersPerMinute, // windSpeedUnits
                WindHeightInputMode::DirectMidflame, // windHeightInputMode
                neighborData.state->windDirection,
                WindAndSpreadOrientationMode::RelativeToNorth, // windAndSpreadOrientationMode
                50.0, // firstFuelModelCoverage,
                FractionUnits::Percent, // firstFuelModelCoverageUnits
                TwoFuelModelsMethod::Arithmetic, // twoFuelModelMethod
                neighborData.state->slope,
                SlopeUnits::Degrees, // slopeUnits
                neighborData.state->aspect,
                30.0, // canopyCover
                FractionUnits::Percent, // canopyCoverUnits
                10.0, // canopyHeight,
                LengthUnits::Meters, // canopyHeightUnits,
                40.0, // crownRatio,
                FractionUnits::Percent // crownRatioUnits
            );
            surface.doSurfaceRunInDirectionOfInterest(direction, SurfaceFireSpreadDirectionMode::FromIgnitionPoint);
            const double spreadRate = surface.getSpreadRateInDirectionOfInterest(SpeedUnits::MetersPerSecond);
            if (spreadRate < DBL_EPSILON || spreadRate != spreadRate)
            {
                continue;
            }
            const double timeToWait = neighborData.vicinity / spreadRate;
            state.ignitionTime = std::min(state.ignitionTime, this->clock + timeToWait);
            state.willIgnite = true;
        }
        return state;
    }

    [[nodiscard]] double outputDelay(const State& state) const override
    {
        if (state.ignited)
        {
            return 1.0;
        }
        else if (state.willIgnite)
        {
            return std::max(state.ignitionTime - this->clock, 0.0);
        }
        else
        {
            return 1.0;
        }
    }
};
