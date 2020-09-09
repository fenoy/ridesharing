.PHONY: all

ifndef OUT
OUT=./ilp
endif

CMP=g++ -std=c++11
WARN=-Wall -Wno-unused-result -Wno-deprecated-declarations -Wno-sign-compare -Wno-maybe-uninitialized -Wno-ignored-attributes -Wno-strict-aliasing -Wno-catch-value
OPTIM=-Ofast -march=native -funroll-loops -funsafe-loop-optimizations -falign-functions=16 -falign-loops=16 -fopenmp
NOOPTIM=-O0 -march=native -fopenmp
DBG=-g ${NOOPTIM}
PROF=-g -DWITHGPERFTOOLS ${OPTIM}

CPLEXROOT=/opt/ibm/ILOG/CPLEX_Studio1210
ARCH=x86-64_linux

INC=-DIL_STD -I${CPLEXROOT}/cplex/include -I${CPLEXROOT}/concert/include
LDIR=-L${CPLEXROOT}/concert/lib/${ARCH}/static_pic -L${CPLEXROOT}/cplex/lib/${ARCH}/static_pic
LINK=-lconcert -lilocplex -lcplex -ldl

COBJSUBDIR=cobj
DEPSUBDIR=dep

ECHOCC=>&2 echo "[\033[01;33m CC \033[0m]"
ECHOLD=>&2 echo "[\033[01;36m LD \033[0m]"
ECHOJC=>&2 echo "[\033[01;35m JC \033[0m]"

ifeq ($(PROFILE),1)
OPT=${PROF}
LINK+=-lprofiler
else
OPT=${OPTIM} # Put desired optimisation level here
endif

define compilec
${ECHOCC} $(notdir $<) ;\
mkdir -p ${DEPSUBDIR} ;\
tmp=`mktemp` ;\
${CMP} ${DEFS} ${INC} -MM ${OPT} $< >> $$tmp ;\
if [ $$? -eq 0 ] ;\
then echo -n "${COBJSUBDIR}/" > ${DEPSUBDIR}/$(notdir $<).d ;\
cat $$tmp >> ${DEPSUBDIR}/$(notdir $<).d ;\
rm $$tmp ;\
mkdir -p ${COBJSUBDIR} ;\
cd ${COBJSUBDIR} ;\
${CMP} ${DEFS} -c ${INC} ${OPT} ${WARN} ../$< ;\
else \
ret=$$? ;\
rm $$tmp ;\
exit $$ret ;\
fi
endef

all: ilp
	@true

-include ${DEPSUBDIR}/*.d

ilp: ${COBJSUBDIR}/ilp.o ${COBJSUBDIR}/io.o
	@${ECHOLD} ilp
	@${CMP} ${OPT} ${LDIR} $^ ${LINK} -o ${OUT}

${COBJSUBDIR}/ilp.o: ilp.cpp
	@$(compilec)

${COBJSUBDIR}/io.o: io.cpp
	@$(compilec)

clean:
	@echo "Removing subdirectories..."
	@rm -rf ${COBJSUBDIR} ${DEPSUBDIR}
