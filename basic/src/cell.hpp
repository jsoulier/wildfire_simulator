#ifndef CADMIUM_EXAMPLE_CELLDEVS_FIRE_GRID_CELL_HPP_
#define CADMIUM_EXAMPLE_CELLDEVS_FIRE_GRID_CELL_HPP_

#include <cmath>
#include <nlohmann/json.hpp>
#include <cadmium/celldevs/grid/cell.hpp>
#include <cadmium/celldevs/grid/config.hpp>
#include "state.hpp"

namespace cadmium::celldevs::example::fire {
    //! Grid fire cell.
    class GridFIRECell : public GridCell<FIREState, double> {
        double tempThreshold;  //!< Temperature threshold for ignition.
        double burnRate;      //!< Burn rate (how fast trees burn once ignited).
        double coolingRate;   //!< Cooling rate after burning is finished.
        double heatTransfer;  //!< Heat transfer rate from burning neighbors.

        public:
        GridFIRECell(const std::vector<int>& id, const std::shared_ptr<const GridCellConfig<FIREState, double>>& config):
          GridCell<FIREState, double>(id, config), tempThreshold(), burnRate(), coolingRate(), heatTransfer() {
            // Extract parameters from the configuration JSON.
            config->rawCellConfig.at("tempThreshold").get_to(tempThreshold);
            config->rawCellConfig.at("burnRate").get_to(burnRate);
            config->rawCellConfig.at("coolingRate").get_to(coolingRate);
            config->rawCellConfig.at("heatTransfer").get_to(heatTransfer);
        }

        [[nodiscard]] FIREState localComputation(FIREState state,
          const std::unordered_map<std::vector<int>, NeighborData<FIREState, double>>& neighborhood) const override {
            // Calculate the influence of neighboring cells on the temperature.
            double heatFromNeighbors = 0;
            for (const auto& [neighborId, neighborData]: neighborhood) {
                // Ensure that we correctly dereference the shared pointer to access the state.
                auto neighborState = neighborData.state;  // This is a std::shared_ptr<const FIREState>
                if (neighborState->b > 0) {  // Check if the neighbor is burning.
                    heatFromNeighbors += neighborState->temp * heatTransfer * neighborData.vicinity;
                }
            }

            // Update the cell's temperature based on its own burning and neighbor heating.
            if (state.b > 0) {
                state.temp += heatFromNeighbors;  // Add heat from neighbors.
                state.temp = std::min(state.temp, 100.0);  // Cap temperature to a reasonable max (e.g., 100°C).
            }

            // Cool down the temperature after burning is finished.
            if (state.b == 0 && state.f > 0) {
                state.temp = std::max(state.temp - coolingRate, 20.0);  // Cool down to at least 20°C.
            }

            // Transition to burning if the temperature threshold is reached.
            if (state.temp >= tempThreshold && state.u > 0 && state.b == 0) {
                // Ignite the cell if the temperature is above the threshold and it is not already burning.
                state.b = std::min(state.b + burnRate, 1.0);
                state.u -= state.b;  // Decrease the unburnt proportion.
            }

            // Update the state transitions.
            state.f = std::round((state.f + newFinished(state)) * 1000) / 1000;
            state.b = std::round((state.b + newBurning(state, neighborhood) - newFinished(state)) * 1000) / 1000;
            state.u = std::max(0.0, 1.0 - state.b - state.f);  // Ensure u is non-negative.

            return state;
        }

        [[nodiscard]] double outputDelay(const FIREState& state) const override {
            return 1.0;  // Adjust this delay if needed for simulation purposes.
        }

        [[nodiscard]] double newBurning(const FIREState& state,
            const std::unordered_map<std::vector<int>, NeighborData<FIREState, double>>& neighborhood) const {
            double aux = 0;
            for (const auto& [neighborId, neighborData]: neighborhood) {
                auto s = neighborData.state;  // This is a shared pointer to const FIREState.
                auto v = neighborData.vicinity;
                aux += s->b * static_cast<double>(s->p) * v;  // Accumulate burning potential from neighbors.
            }
            return state.u * std::min(1.0, aux / state.p);
        }

        [[nodiscard]] double newFinished(const FIREState& state) const {
            return state.b * burnRate;  // Burn rate determines how quickly trees turn to ash.
        }
    };
}  // namespace cadmium::celldevs::example::fire

#endif //CADMIUM_EXAMPLE_CELLDEVS_FIRE_GRID_CELL_HPP_