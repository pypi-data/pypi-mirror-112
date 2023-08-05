#ifndef NDARRAY_ARRAY_SCALAR_ARITHMETIC
#define NDARRAY_ARRAY_SCALAR_ARITHMETIC

#include <librapid/math/rapid_math.hpp>
#include <cstring> // For memset

namespace librapid
{
	namespace arithmetic
	{
		template<typename A, typename B, typename C,
			typename E,
			typename S_a, typename S_c,
			typename LAMBDA>
			LR_INLINE void array_op_scalar(A *__restrict src_a, B *__restrict src_b, C *__restrict src_c,
										   const basic_extent<E> &extent,
										   const basic_stride<S_a> &stride_a,
										   const basic_stride<S_c> &stride_c,
										   LAMBDA op)
		{
			// Counters
			lr_int idim = 0;
			lr_int ndim = extent.ndim();

			// Create pointers here to reduce function calls
			const auto *__restrict _extent = extent.get_extent_alt();
			const auto *__restrict _stride_a = stride_a.get_stride_alt();
			const auto *__restrict _stride_c = stride_c.get_stride_alt();

			// All strides are non-trivial
			lr_int mode = 1;

			// All strides trivial
			if (stride_a.is_trivial() && stride_c.is_trivial())
				mode = 0;

			// Reduce calculations by precalculating the size of the arrays
			const auto end = math::product(extent.get_extent(), extent.ndim());

			// The array index
			lr_int coord[LIBRAPID_MAX_DIMS]{};

			switch (mode)
			{
				case 0:
					{
						// Only use OpenMP if size is above a certain threshold
						// to improve speed for small arrays (overhead of multiple
						// threads makes it slower for small arrays)
						if (end > 100000)
						{
							long long e = (long long) end;
						#pragma omp parallel for shared(src_a, src_b, src_c, op, e) default(none) num_threads(4)
							for (long long i = 0; i < e; ++i)
								src_c[i] = op(src_a[i], *src_b);
						}
						else
						{
							for (lr_int i = 0; i < end; ++i)
								src_c[i] = op(src_a[i], *src_b);
						}
						break;
					}
				case 1:
					{
						do
						{
							*src_c = op(*src_a, *src_b);

							for (idim = 0; idim < ndim; ++idim)
							{
								if (++coord[idim] == _extent[idim])
								{
									coord[idim] = 0;
									src_a = src_a - (_extent[idim] - 1) * _stride_a[idim];
									src_c = src_c - (_extent[idim] - 1) * _stride_c[idim];
								}
								else
								{
									src_a = src_a + _stride_a[idim];
									src_c = src_c + _stride_c[idim];
									break;
								}
							}
						} while (idim < ndim);
						break;
					}
			}
		}
	}
}

#endif // NDARRAY_ARRAY_SCALAR_ARITHMETIC