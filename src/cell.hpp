#pragma once

#include <cmath>
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
        if (state.ignited)
        {
            return state;
        }
        if (state.willIgnite)
        {
            state.ignited = true;
            return state;
        }
        for (const auto& [neighborId, neighborData]: neighborhood)
        {
            if (neighborData.state->willIgnite && !neighborData.state->ignited)
            {
                state.neighborWillIgnite = true;
                state.timeToWait = neighborData.state->timeToWait;
                continue;
            }
            if (!neighborData.state->ignited)
            {
                continue;
            }
            double deltaX = state.x - neighborData.state->x;
            double deltaY = state.y - neighborData.state->y;
            double directionFromNeighbor = atan2(deltaX, deltaY);
            FuelModels fuelModels;
            Surface surface(fuelModels);
            surface.setSlope(neighborData.state->slope, SlopeUnits::Percent);
            surface.setAspect(neighborData.state->aspect);
            surface.setFuelModelNumber(neighborData.state->fuelModelNumber);
            surface.setWindDirection(neighborData.state->windDirection);
            surface.setWindSpeed(neighborData.state->windSpeed, SpeedUnits::MetersPerSecond, WindHeightInputMode::DirectMidflame);
            surface.doSurfaceRunInDirectionOfInterest(directionFromNeighbor, SurfaceFireSpreadDirectionMode::FromIgnitionPoint);
            const double spreadRate = surface.getSpreadRateInDirectionOfInterest(SpeedUnits::MetersPerSecond);
            if (spreadRate < DBL_EPSILON)
            {
                continue;
            }
            state.timeToWait = neighborData.vicinity / spreadRate;
            state.willIgnite = true;
        }
        return state;
    }

    [[nodiscard]] double outputDelay(const State& state) const override
    {
        if (state.ignited)
        {
            return 1.0f;
        }
        else if (state.willIgnite || state.neighborWillIgnite)
        {
            return state.timeToWait;
        }
        else
        {
            return 1.0f;
        }
    }
};