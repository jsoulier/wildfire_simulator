#pragma once

#include <iostream>
#include <string>
#include <nlohmann/json.hpp>

struct State
{
    /* params affecting neighbors */
    double intensity;
    double spreadRate;
    double spreadDirection;
    
    /* params affecting us */
    double timeToIgnition;
    bool willBeIgnited;
    bool ignited;

    State()
        : intensity(0.0f)
        , spreadRate(0.0f)
        , spreadDirection(0.0f)
        , timeToIgnition(INFINITY)
        , ignited(false)
        , willBeIgnited(false)
    {
    }
};

inline bool operator!=(const State& x, const State& y)
{
    return true;
}

inline std::ostream& operator<<(std::ostream& os, const State& x)
{
    return os << "ignited: " << x.ignited;
}

[[maybe_unused]] inline void from_json(const nlohmann::json& j, State& s)
{
    s.ignited = j.at("ignited");
}