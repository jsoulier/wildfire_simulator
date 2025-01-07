#include <cadmium/celldevs/grid/coupled.hpp>
#include <cadmium/core/logger/csv.hpp>
#include <cadmium/core/simulation/root_coordinator.hpp>
#include <fstream>
#include <iostream>
#include <string>
#include "cell.hpp"
#include "state.hpp"

std::shared_ptr<cadmium::celldevs::GridCell<State, double>> addGridCell(
	const cadmium::celldevs::coordinates & cellId, const std::shared_ptr<
		const cadmium::celldevs::GridCellConfig<State, double>>& cellConfig)
{
	const auto& cellModel = cellConfig->cellModel;
	if (cellModel == "default" || cellModel == "")
	{
		return std::make_shared<GridCell>(cellId, cellConfig);
	}
	else
	{
		throw std::bad_typeid();
	}
}

int main(int argc, char ** argv)
{
	if (argc < 2)
	{
		std::cout << "Program used with wrong parameters. The program must be invoked as follows:";
		std::cout << argv[0] << " SCENARIO_CONFIG.json [MAX_SIMULATION_TIME (default: 500)]" << std::endl;
		return 1;
	}
	std::string configFilePath = argv[1];
	double simTime = (argc > 2) ? std::stod(argv[2]) : 500;
	auto model = std::make_shared<cadmium::celldevs::GridCellDEVSCoupled<State, double>>("behave", addGridCell, configFilePath);
	model->buildModel();
	auto rootCoordinator = cadmium::RootCoordinator(model);
	auto logger = std::make_shared<cadmium::CSVLogger>("grid_log.csv", ";");
	rootCoordinator.setLogger(logger);
	rootCoordinator.start();
	rootCoordinator.simulate(simTime);
	rootCoordinator.stop();
    return 0;
}