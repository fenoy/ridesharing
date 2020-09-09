#include <stdio.h>
#include <float.h>
#include <string.h>

#include "types.hpp"
#include "params.h"

// # of valid permutations of points in a path (given the # of agents)
#define R5 2520
#define R4 90
#define R3 6

__attribute__((always_inline)) inline
uint bufmin(const value *buf, uint n) {

	uint idx = 0;
	value min = buf[idx];

	for (uint i = 1; i < n; ++i) {
		if (min > buf[i]) {
			idx = i;
			min = buf[idx];
		}
	}

	return idx;
}

__attribute__((always_inline)) inline
void rot2buf(req *z, uint n) {

	req l[2] = { z[0], z[1] };
	memmove(z, z + 2, sizeof(req) * 2 * (n - 1));
	memcpy(z + 2 * (n - 1), l, sizeof(req) * 2);
}

__attribute__((always_inline)) inline
void copyzones(req *z, uint* ids, req* p, uint n) {

	for (uint i = 0; i < n; ++i) {
		p[i] = z[ids[i]];
	}
}

// sequences of points (paths)
#include "seq1.h"
#include "seq2.h"
#include "seq3.h"
#include "seq4.h"
#include "seq5.h"

value srvalue(req *z, uint n, req *p, const value *ac) {

	//printf("before = ");
	//printbuf(z, 2 * n, "\n");

	value r[R5];
	value min = FLT_MAX;

	for (uint d = 0; d < n; ++d) {

		//for (int i = 0; i < n; ++i) {
		//	printf("%d ", z[i]);
		//}
		//printf("\n");

		uint idx;

		switch (n) {
			case 5:
				#include "paths5.h"
				idx = bufmin(r, R5);
				break;
			case 4:
				#include "paths4.h"
				idx = bufmin(r, R4);
				break;
			case 3:
				#include "paths3.h"
				idx = bufmin(r, R3);
				break;
			case 2:
				#include "paths2.h"
				idx = 0;
				break;
			default:
				#include "paths1.h"
				idx = 0;
				break;
		}

		if (r[idx] < min) {
			min = r[idx];
			if (p) {
				switch (n) {
					case 5:
						copyzones(z, seq5 + idx * 2 * n, p, 2 * n);
						break;
					case 4:
						copyzones(z, seq4 + idx * 2 * n, p, 2 * n);
						break;
					case 3:
						copyzones(z, seq3 + idx * 2 * n, p, 2 * n);
						break;
					case 2:
						copyzones(z, seq2 + idx * 2 * n, p, 2 * n);
						break;
					default:
						copyzones(z, seq1 + idx * 2 * n, p, 2 * n);
						break;
				}
			}
		}

		if (d != n - 1) {
			#define SWAP(X, Y) do { __typeof__ (X) _T = X; X = Y; Y = _T; } while (0)
			SWAP(z[0], z[2 * (d + 1)]);
			SWAP(z[1], z[2 * (d + 1) + 1]);
		}
	}

	if (n != 1) {
		rot2buf(z, n);
	}

	//printf("after = ");
	//printbuf(z, 2 * n, "\n");

	return min;
}

__attribute__((always_inline)) inline
value singvalue(req *z, uint n, const value *ac) {

	value ret = 0;

	for (uint i = 0; i < n; ++i) {
		ret += srvalue(z + 2 * i, 1, NULL, ac);
	}

	return ret;
}
