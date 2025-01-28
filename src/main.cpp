#include <cadmium/celldevs/asymm/coupled.hpp>
#include <cadmium/core/logger/csv.hpp>
#include <cadmium/core/simulation/root_coordinator.hpp>
#include <fstream>
#include <iostream>
#include <string>
#include "cell.hpp"
#include "state.hpp"
#include "temporal_logger.hpp"

std::shared_ptr<cadmium::celldevs::AsymmCell<State, double>> addCell(
    const std::string& cellId, const std::shared_ptr<const cadmium::celldevs::AsymmCellConfig<State, double>>& cellConfig)
{
    return std::make_shared<Cell>(cellId, cellConfig);
}

int main(int argc, char** argv)
{
    if (argc < 2)
    {
        std::cout << "Program used with wrong parameters. The program must be invoked as follows:";
        std::cout << argv[0] << " SCENARIO_CONFIG.json MAX_SIMULATION_TIME" << std::endl;
        return 1;
    }
    auto model = std::make_shared<cadmium::celldevs::AsymmCellDEVSCoupled<State, double>>("behave", addCell, argv[1]);
    model->buildModel();
    auto coordinator = cadmium::RootCoordinator(model);
    auto logger = std::make_shared<TemporalLogger>("log.csv");
    coordinator.setLogger(logger);
    coordinator.start();
    coordinator.simulate(std::stod(argv[2]));
    coordinator.stop();
    return 0;
}