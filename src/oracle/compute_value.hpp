#ifndef COMPUTEVALUE_HPP_
#define COMPUTEVALUE_HPP_

struct cv_data {

	// Number of requests in the pool
	req n;
	// Requests (pool)
	vector<req> *reqs;
	// Timestep of arrival in the system for each request in the pool 
	vector<step> *steps;
	// Max waiting time for each request in the pool
	vector<step> *deltas;
	// Distance matrix
	vector<value> *distance;
	// Time matrix
	vector<value> *time;
	// Weight for environmental benefits
	float k;
};

__attribute__((always_inline)) inline
void compute_value(coal &c, const cv_data *data) {

	req zones[2 * c.c[0]];
	step min_tpd = UINT_MAX;
	step max_t = 0;

	for (uint i = 0; i < c.c[0]; ++i) {
		const uint idx = c.c[i + 1];
		zones[2 * i] = (*data->reqs)[idx] / Z;
		zones[2 * i + 1] = (*data->reqs)[idx] % Z;
		step d = (*data->deltas)[idx];
		step t = (*data->steps)[idx];
		if (d != UINT_MAX && t + d < min_tpd) {
			min_tpd = t + d;
		}
		if (t > max_t) {
			max_t = t;
		}
	}

	if (min_tpd >= max_t) {
		const value dist_nors = singvalue(zones, c.c[0], &(*data->distance)[0]);
		const value dist_rs = srvalue(zones, c.c[0], c.p, &(*data->distance)[0]);
		const value dist_impr = (dist_nors == 0) ? 0 : ((dist_nors - dist_rs) / dist_nors);
		const value cong_nors = c.c[0];
		const value cong_rs = 1;
		const value cong_impr = (cong_nors - cong_rs) / cong_nors;
		c.qos = compute_qos(c, *data->reqs, *data->time);
		c.w = data->k * c.c[0] * (2 * dist_impr + cong_impr) / 3 - (1.0 - data->k) * c.qos.qos_tot;
		c.dr = dist_nors - dist_rs;
	} else {
		c.w = -FLT_MAX;
	}

	//print_buf(c.c + 1, c.c[0], NULL, NULL, " = ");
	printf("%f\n", c.w);
}

#endif /* COMPUTEVALUE_HPP_ */
