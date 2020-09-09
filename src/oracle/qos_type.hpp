#ifndef QOS_TYPE_HPP_
#define QOS_TYPE_HPP_

#include <stdint.h>

struct qos_t {

	uint n;
	uint icd[K];
	value qos[K];
	value qos_tot;
};

#endif /* QOS_TYPE_HPP_ */
