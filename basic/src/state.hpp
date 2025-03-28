#ifndef CADMIUM_EXAMPLE_CELLDEVS_FIRE_STATE_HPP_
#define CADMIUM_EXAMPLE_CELLDEVS_FIRE_STATE_HPP_

#include <iostream>
#include <nlohmann/json.hpp>

namespace cadmium::celldevs::example::fire {
    //! Forest fire cell state.
    struct FIREState {
        int p;         //!< Cell tree population.
        double u;      //!< Ratio of unburnt trees (from 0 to 1).
        double b;      //!< Ratio of burning trees (from 0 to 1).
        double f;      //!< Ratio of fully burnt trees (from 0 to 1).
        double temp;   //!< Temperature of the cell (e.g., in Celsius).
        double burnRate; //!< Rate at which the trees burn once ignited.

        //! Default constructor function. By default, cells are unoccupied and all the population is considered unburnt.
        FIREState() : p(0), u(1), b(0), f(0), temp(20.0), burnRate(0.05) {
        }
    };

    //! It returns true if x and y are different.
    inline bool operator!=(const FIREState& x, const FIREState& y) {
        return x.p != y.p || x.u != y.u || x.b != y.b || x.f != y.f || x.temp != y.temp || x.burnRate != y.burnRate;
    }

    //! It prints a FIRE state in an output stream.
    std::ostream& operator<<(std::ostream& os, const FIREState& x) {
        os << "<" << x.p << "," << x.u << "," << x.b << "," << x.f << "," << x.temp << "," << x.burnRate << ">";
        return os;
    }

    //! It parses a JSON file and generates the corresponding FIRE state object.
    [[maybe_unused]] void from_json(const nlohmann::json& j, FIREState& s) {
        j.at("p").get_to(s.p);
        j.at("u").get_to(s.u);
        j.at("b").get_to(s.b);
        j.at("f").get_to(s.f);
        j.at("temp").get_to(s.temp);
        j.at("burnRate").get_to(s.burnRate);
    }
}  // namespace cadmium::celldevs::example::fire

#endif //CADMIUM_EXAMPLE_CELLDEVS_FIRE_STATE_HPP_
