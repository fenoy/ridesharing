#include "oracle.hpp"

int main(int argc, char *argv[]) {

	// Assuming that a request goes from zone i to zone j, the corresponding "req" is an integer = i * Z + j
	// Z = number of zones (63 in this dataset)

        /* Create data structures */

	// Requests (pool)
	vector<req> reqs;
	// Timestep of arrival in the system for each request in the pool 
	vector<step> steps;
	// Max waiting time for each request in the pool
	vector<step> deltas;
	// Distance matrix
	vector<value> distance;
	// Time matrix
	vector<value> time;
	// Weight for environmental benefits
	const float env_k = 0.5;
	
	/* Read data */
	read_reqs(argv[1], reqs, steps, deltas);
	const req n = reqs.size();
	read_matrix("./data/gmaps_distance.csv", Z, Z, distance);
	read_matrix("./data/gmaps_time.csv", Z, Z, time);

        // Data structure necessary for compute_value (see compute_value.hpp for more information)
	cv_data data = { n, PTR(reqs), PTR(steps), PTR(deltas), PTR(distance), PTR(time), env_k };

        // Example coalition (see coal_type.hpp for more information on the fields)
        // Just fill the first field "c" with the *indexes* (0-indexed) of the requests in "reqs" (pool)
        // c[0] is the size of coalition (number of request in the coalition)
        // The indexes are in c[1] ... c[c[0]]
        // In this example the coalition contains the first 5 requests in "reqs"
        coal input_coal;
        input_coal.c[0] = argc - 2;

        for (uint i = 2; i < argc; ++i) {
                input_coal.c[i - 1] = atoi(argv[i]);
        }

        // Computes other fields of coal ("p", "w", "dr", "qos")
        compute_value(input_coal, &data);

	return 0;
}
