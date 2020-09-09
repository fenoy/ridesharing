#ifndef COAL_HPP_
#define COAL_HPP_

#include "types.hpp"
#include "params.h"
#include "iqsort.h"

struct coal {
	req c[K + 1];   // c[0] = size of the coalition, c[1] ... c[c[0]] = requests 
	req p[2 * K];   // optimal path for coalition
	value w;        // coalitional value
	value dr;       // total distance reduction
	qos_t qos;      // quality of service information
};

#define LT(X, Y) ((*X) < (*Y))

struct lex_coal {

	inline bool operator() (const coal& c1, const coal& c2) const {

		if (c1.c[0] == c2.c[0]) {
			req a[c1.c[0]], b[c2.c[0]];
			memcpy(a, c1.c + 1, sizeof(req) * c1.c[0]);
			memcpy(b, c2.c + 1, sizeof(req) * c2.c[0]);
			QSORT(req, a, c1.c[0], LT);
			QSORT(req, b, c2.c[0], LT);
			return memcmp(a, b, sizeof(req) * c1.c[0]) < 0;
		} else {
			return c1.c[0] < c2.c[0];
		}
	}
};

struct greater_w {

	inline bool operator() (const coal& c1, const coal& c2) const {

		#ifdef STABLE_SORT
		if (c1.w == c2.w) {
			if (c1.c[0] == c2.c[0]) {
				req a[c1.c[0]], b[c2.c[0]];
				memcpy(a, c1.c + 1, sizeof(req) * c1.c[0]);
				memcpy(b, c2.c + 1, sizeof(req) * c2.c[0]);
				QSORT(req, a, c1.c[0], LT);
				QSORT(req, b, c2.c[0], LT);
				return memcmp(a, b, sizeof(req) * c1.c[0]) > 0;
			} else {
				return c1.c[0] > c2.c[0];
			}
		} else {
			return c1.w > c2.w;
		}
		#else
		return c1.w > c2.w;
		#endif
	}
};

#endif /* COAL_HPP_ */
