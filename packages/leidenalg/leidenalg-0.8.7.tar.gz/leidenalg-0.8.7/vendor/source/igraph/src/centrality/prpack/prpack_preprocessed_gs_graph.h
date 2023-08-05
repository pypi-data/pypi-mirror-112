#ifndef PRPACK_PREPROCESSED_GS_GRAPH
#define PRPACK_PREPROCESSED_GS_GRAPH
#include "prpack_preprocessed_graph.h"
#include "prpack_base_graph.h"

namespace prpack {

    // Pre-processed graph class
    class prpack_preprocessed_gs_graph : public prpack_preprocessed_graph {
        private:
            // helper methods
            void initialize();
            void initialize_weighted(const prpack_base_graph* bg);
            void initialize_unweighted(const prpack_base_graph* bg);
        public:
            // instance variables
            int* heads;
            int* tails;
            double* vals;
            double* ii;
            double* num_outlinks;
            // constructors
            prpack_preprocessed_gs_graph(const prpack_base_graph* bg);
            // destructor
            ~prpack_preprocessed_gs_graph();
    };

}

#endif
