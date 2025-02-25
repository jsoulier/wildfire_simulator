#include <cadmium/celldevs/asymm/coupled.hpp>
#include <cadmium/core/logger/csv.hpp>
#include <cadmium/core/simulation/root_coordinator.hpp>
#include <fstream>
#include <iostream>
#include <string>
#include "cell.hpp"
#include "state.hpp"
#include "logger.hpp"

std::shared_ptr<cadmium::celldevs::AsymmCell<State, double>> addCell(
    const std::string& cellId, const std::shared_ptr<const cadmium::celldevs::AsymmCellConfig<State, double>>& cellConfig)
{
    return std::make_shared<Cell>(cellId, cellConfig);
}

int main(int argc, char** argv)
{
    if (argc < 2)
    {
        std::cout << "Missing source json and destination csv" << std::endl;
        return 1;
    }
    auto model = std::make_shared<cadmium::celldevs::AsymmCellDEVSCoupled<State, double>>("behave", addCell, argv[1]);
    model->buildModel();
    auto coordinator = cadmium::RootCoordinator(model);
    auto logger = std::make_shared<Logger>(argv[2]);
    coordinator.setLogger(logger);
    coordinator.start();
    coordinator.simulate(10000000.0);
    coordinator.stop();
    return 0;
}