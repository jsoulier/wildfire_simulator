#pragma once

#include <cmath>
#include <nlohmann/json.hpp>
#include <cadmium/celldevs/grid/cell.hpp>
#include <cadmium/celldevs/grid/config.hpp>
#include <behave/surface.h>
#include <behave/fuelModels.h>
#include "state.hpp"

class GridCell : public cadmium::celldevs::GridCell<State, double>
{
    double slope;
    double aspect;
    int fuelModelNumber;
    double windDirection;
    double windSpeed;

public:
    GridCell(const std::vector<int>& id, const std::shared_ptr<
        const cadmium::celldevs::GridCellConfig<State, double>>& config)
        : cadmium::celldevs::GridCell<State, double>(id, config)
    {
        slope = config->rawCellConfig.at("slope");
        aspect = config->rawCellConfig.at("aspect");
        fuelModelNumber = config->rawCellConfig.at("fuelModelNumber");
        windDirection = config->rawCellConfig.at("windDirection");
        windSpeed = config->rawCellConfig.at("windSpeed");
    }

    [[nodiscard]] State localComputation(State state, const std::unordered_map<
        std::vector<int>, cadmium::celldevs::NeighborData<State, double>>& neighborhood) const override
    {
        if (state.ignited)
        {
            return state;
        }
        state.slope = slope;
        state.aspect = aspect;
        state.fuelModelNumber = fuelModelNumber;
        state.windDirection = windDirection;
        state.windSpeed = windSpeed;
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
            cadmium::celldevs::coordinates vectorFromNeighbor = distanceVectorFrom(neighborId);
            double directionFromNeighbor = atan2(vectorFromNeighbor.at(0), vectorFromNeighbor.at(1));
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