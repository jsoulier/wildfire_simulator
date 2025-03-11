#pragma once

#include <iostream>
#include <string>
#include <behave/surface.h>
#include <behave/fuelModels.h>
#include <nlohmann/json.hpp>

struct State
{
    double slope;
    double aspect;
    int fuelModelNumber;
    double windDirection;
    double windSpeed;
    int x;
    int y;

    double ignitionTime;
    bool willIgnite;
    bool ignited;

    State()
        : ignitionTime(INFINITY)
        , ignited(false)
        , willIgnite(false)
        , x(0)
        , y(0) {}
};

inline bool operator!=(const State& x, const State& y)
{
    return x.ignited != y.ignited || x.willIgnite != y.willIgnite;
}

inline std::ostream& operator<<(std::ostream& os, const State& x)
{
    return os << x.x << ":" << x.y << ":" << x.ignited;
}

inline void from_json(const nlohmann::json& j, State& s)
{
    s.ignited = j.at("ignited");
    s.x = j.at("x");
    s.y = j.at("y");
    s.slope = j.at("slope");
    s.aspect = j.at("aspect");
    s.fuelModelNumber = j.at("fuelModelNumber");
    s.windDirection = j.at("windDirection");
    s.windSpeed = j.at("windSpeed");
}