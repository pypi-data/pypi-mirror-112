/* -*- mode: C -*-  */
/*
   IGraph library.
   Copyright (C) 2007-2012  Gabor Csardi <csardi.gabor@gmail.com>
   334 Harvard street, Cambridge, MA 02139 USA

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc.,  51 Franklin Street, Fifth Floor, Boston, MA
   02110-1301 USA

*/

#include "igraph_error.h"
#include "igraph_types.h"
#include "igraph_stack.h"

#define BASE_IGRAPH_REAL
#include "igraph_pmt.h"
#include "stack.pmt"
#include "igraph_pmt_off.h"
#undef BASE_IGRAPH_REAL

#define BASE_LONG
#include "igraph_pmt.h"
#include "stack.pmt"
#include "igraph_pmt_off.h"
#undef BASE_LONG

#define BASE_INT
#include "igraph_pmt.h"
#include "stack.pmt"
#include "igraph_pmt_off.h"
#undef BASE_INT

#define BASE_CHAR
#include "igraph_pmt.h"
#include "stack.pmt"
#include "igraph_pmt_off.h"
#undef BASE_CHAR

#define BASE_BOOL
#include "igraph_pmt.h"
#include "stack.pmt"
#include "igraph_pmt_off.h"
#undef BASE_BOOL

#define BASE_PTR
#include "igraph_pmt.h"
#include "stack.pmt"
#include "igraph_pmt_off.h"
#undef BASE_PTR

/**
 * \ingroup stack
 * \brief Calls free() on all elements of a pointer stack.
 */

void igraph_stack_ptr_free_all(igraph_stack_ptr_t* v) {
    void **ptr;
    IGRAPH_ASSERT(v != 0);
    IGRAPH_ASSERT(v->stor_begin != 0);
    for (ptr = v->stor_begin; ptr < v->end; ptr++) {
        IGRAPH_FREE(*ptr);
    }
}

/**
 * \ingroup stack
 * \brief Calls free() on all elements and destroys the stack.
 */

void igraph_stack_ptr_destroy_all(igraph_stack_ptr_t* v) {
    IGRAPH_ASSERT(v != 0);
    IGRAPH_ASSERT(v->stor_begin != 0);
    igraph_stack_ptr_free_all(v);
    igraph_stack_ptr_destroy(v);
}


