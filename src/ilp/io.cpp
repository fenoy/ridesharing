#include "io.hpp"

void read_reqs(const char *filename, vector<req> &reqs, vector<step> &steps, vector<step> &deltas) {

	ifstream f(filename);
	string cell;

	while (getline(f, cell, ',')) {
		steps.push_back(stoi(cell));
		getline(f, cell, ',');
		reqs.push_back(stoi(cell));
		getline(f, cell);
		int val = stoi(cell);
		deltas.push_back(val < 0 ? UINT_MAX : val);
	}

	f.close();
}

void read_matrix(const char *filename, uint nrows, uint ncols, vector<value> &mat) {

	ifstream f(filename);
	string cell;

	for (uint i = 0; i < nrows; ++i) {
		for (uint i = 0; i < ncols - 1; ++i) {
			getline(f, cell, ',');
			mat.push_back(stof(cell));
		}
		getline(f, cell);
		mat.push_back(stof(cell));
	}

	f.close();
}

void read_vars(const char *filename, vector<coal> &vars) {

	ifstream f(filename);
	string str;

	while (getline(f, str)) {
		char *dup = strdup(str.c_str());
		char *token = strtok(dup, ",");
		coal c;
		c.w = atof(token);
		token = strtok(NULL, ",");
		c.c[0] = 0;
		while (token != NULL) {
			c.c[++c.c[0]] = stoi(token);
			token = strtok(NULL, ",");
		}
		vars.push_back(c);
		free(dup);
	}

	f.close();
}
