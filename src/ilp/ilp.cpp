#include "ilp.hpp"

template <typename cont, typename type>
__attribute__((always_inline)) inline
void print_solution(cont &vars, type &xa, IloCplex &cplex) { //, const std::vector<req> &reqs, const std::vector<value> &time) {

	for (uint i = 0; i < xa.getSize(); ++i) {
		try {
			if (fabs(cplex.getValue(xa[i])) > EPSILON) {
				cout << xa[i].getName() << endl;
				//coal c = *std::next(vars.begin(), i);
				//print_buf(c.p, 2 * c.c[0], "Path");
				//printf("Distance reduction = %.2f\n", c.dr);
				//print_buf(c.qos.icd, c.c[0], "In-car delays");
				//print_buf(c.qos.qos, c.c[0], "QoS values", "%.2f");
			}
		}
		catch (IloException& e) { e.end(); }
	}
	puts("");
}

int main(int argc, char *argv[]) {

	if (argc != 4) {
		printf(RED("Usage: %s POOL_CSV VARS_CSV TIME_BUDGET\n"), argv[0]);
		return EXIT_FAILURE;
	}

	// Data structures
	vector<req> reqs;
	vector<step> steps;
	vector<step> deltas;
	vector<coal> vars;

	// Parse commandline arguments
	read_reqs(argv[1], reqs, steps, deltas);
	const req n = reqs.size();
	read_vars(argv[2], vars);
	const float tb = atof(argv[3]); // Milliseconds

	#ifdef PRINT_VARS
	cout << CYAN("Variables:") << endl;
	print_coals(vars.begin(), vars.end());
	cout << endl;
	#endif

	// CPLEX data structures
	IloEnv env;
	IloIntVarArray xa(env);
	IloModel model(env);
	IloExprArray constr(env, n);
	IloExpr obj(env);

	// Initialise empty constraints (avoids segfaults)
	for (uint i = 0; i < n; ++i) {
		constr[i] = IloExpr(env);
	}

	for (auto it = vars.begin() ; it != vars.end(); ++it) {

		// Create variable
		ostringstream ostr;
		//ostr << "X_[" << reqs[it->c[1]];
		ostr << reqs[it->c[1]];
		for (uint i = 1; i < it->c[0]; ++i) {
			ostr << "," << reqs[it->c[i + 1]];
		}
		//ostr << "]";
		//cout << ostr.str() << endl;
		IloIntVar x = IloIntVar(env, 0, 1, ostr.str().c_str());
		xa.add(x);

		// Update constraints
		for (uint i = 0; i < it->c[0]; ++i) {
			constr[it->c[i + 1]] += x;
		}

		// Update objective function
		obj += it->w * x;
	}

	//cout << endl << "Objective function:" << endl << obj << endl;
	model.add(IloMaximize(env, obj));
	obj.end();

	// Finalise creation of constraints for Weighted Set Packing
	for (uint i = 0; i < n; ++i) {
		model.add(constr[i] <= 1);
		constr[i].end();
	}

	IloCplex cplex(model);
	#if CPX_VERSION >= 12060000
	cplex.setParam(IloCplex::Param::TimeLimit, tb);
	#else
	cplex.setParam(IloCplex::TiLim, tb);
	#endif
	//cplex.setParam(IloCplex::Threads, n_threads);
	cplex.setParam(IloCplex::MIPDisplay, 4);

	#ifdef EXPORT_ILP
	char lp_name[50];
	strcpy(lp_name, argv[1]);
	strcat(lp_name, ".lp");
	cout << "ILP model exported to " << lp_name << endl;
	cplex.exportModel(lp_name);
	#endif

	#ifdef HIDE_CPLEX
	cplex.setOut(env.getNullStream());
	cout << BLUE("Solving ILP model...") << endl;
	#else
	cout << BLUE("Solving ILP model:") << endl;
	#endif

	try {
		if (!cplex.solve()) {
			cout << RED("Unable to find a solution") << endl;
			exit(EXIT_FAILURE);
		}
	}
	catch (IloCplex::Exception e) {
		cout << RED("An exception occurred") << endl;
		exit(EXIT_FAILURE);
	}

	// End solution

	cout << endl;
	#ifdef PRINT_SOLUTION
	cout << GREEN("Solution:") << endl;
	print_solution(vars[0], xa, cplex);
	#endif
	cout << GREEN("Total reward") << " = " << cplex.getObjValue();
	if (cplex.getStatus() == IloAlgorithm::Optimal) {
		cout << GREEN(" [OPTIMAL]")  << endl;
	} else {
		cout << YELLOW(" [SUBOPTIMAL]")  << endl;
	}

	return EXIT_SUCCESS;
}
