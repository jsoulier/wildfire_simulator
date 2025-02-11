#pragma once

#include <fstream>
#include <string>
#include <sstream>
#include <utility>
#include <cadmium/core/logger/logger.hpp>

class Logger : public cadmium::Logger
{
public:
    Logger(const std::string& filepath)
        : cadmium::Logger()
        , filepath(filepath)
        , file() {}

    void start() override
    {
        file.open(filepath);
        file << "time,x,y,ignited" << std::endl;
    }

    void stop() override
    {
        file.close();
    }

    void logOutput(double time, long modelId, const std::string& modelName, const std::string& portName, const std::string& output) override {}
    void logState(double time, long modelId, const std::string& modelName, const std::string& state) override
    {
        std::istringstream stream(state);
        std::string x, y, ignited;
        std::getline(stream, x, ':');
        std::getline(stream, y, ':');
        std::getline(stream, ignited, ':');
        if (!std::stoi(ignited))
        {
            return;
        }
        using namespace std::chrono;
        const std::time_t now = system_clock::to_time_t(system_clock::time_point(seconds(static_cast<long>(time))));
        file << std::put_time(std::localtime(&now), "%Y-%m-%d %H:%M:%S");
        file << ",";
        file << x;
        file << ",";
        file << y;
        file << ",";
        file << ignited;
        file << std::endl;;
    }

private:
    std::string filepath;
    std::ofstream file;
};