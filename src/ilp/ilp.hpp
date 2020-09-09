#ifndef ILP_HPP_
#define ILP_HPP_

// Enable stable sorting algorithm
//#define STABLE_SORT

// Headers
#include <vector>

// CPLEX
#include <ilcplex/ilocplex.h>

// Modules
#include "types.hpp"
#include "params.h"
#include "coal_type.hpp"

#include "io.hpp"
#include "colours.h"

// Profiling
//#include <gperftools/profiler.h>
#define BREAKPOINT(MSG) do { puts(MSG); fflush(stdout); while (getchar() != '\n'); } while (0)

#endif /* ILP_HPP_ */
