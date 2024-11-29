#pragma once

#include <iostream>
#include <string>
#include <nlohmann/json.hpp>

struct State
{
    double spreadRate;
    double spreadDirection;
    double igniteTime;
    bool willIgnite;
    bool ignited;

    State()
        : spreadRate(0.0f)
        , spreadDirection(0.0f)
        , igniteTime(INFINITY)
        , ignited(false)
        , willIgnite(false)
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