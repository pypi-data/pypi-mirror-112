import numpy
from numpy import ndarray


def create(use_numba: bool, zero=0.0):
    """Creates a calculator object with the given options.

    Parameters
    ----------
    use_numba:
        If True, the numba package is used to speed up the
        returned object's calculations. In this case the
        calculations happen with 64 bit floating point numbers.
    zero:
        The constant used to initialize new arrays.
        Useful for the sympy package to initialize arrays of
        Integer objects.
    """
    # a substitute for numba's jit decorator that does nothing
    def optional_jit(*args, **kwargs):
        return lambda func: func

    # create substitutions for numba's types if the package is not used
    class dummy_numba_type:
        def __call__(self, *args):
            return self

        def __getitem__(self, *args):
            return self
    float64 = dummy_numba_type()
    int64 = dummy_numba_type()
    # import numba if requested
    if use_numba:
        import numba
        optional_jit = numba.jit
        int64 = numba.int64
        float64 = numba.float64

    # create functions for the class
    @optional_jit(float64[:](float64[:]), nopython=True)
    def partition_functions(weights: ndarray) -> ndarray:
        """Partition functions for many input set sizes.

        The result is a 1D array, where the i-th element is the
        partition function for an input set of size i.
        The 0th element will be 1.
        The returned array will have the same size as the 'weights' parameter.

        Parameters
        ----------
        weights:
            The i-th element gives the weight of subset size i.
        """
        assert(weights.size > 0)
        N = weights.size - 1
        result = numpy.full(N + 1, zero)
        result[0] = 1
        for k in range(1, N + 1):
            for n in range(k, N + 1):
                result[n] += weights[k] * result[n - k]
        return result

    @optional_jit(float64[:](float64[:], float64[:], int64), nopython=True)
    def partition_functions_multiplicity(
            weights: ndarray,
            part_functs: ndarray,
            subset_size: int) -> ndarray:
        """Partition functions for many input set sizes with multiplicities.

        The result is a 1D array, where the i-th element is the
        partition function for an input set of size i, but
        each summand is multiplied with the number of subsets
        in the corresponding partition having size 'subset_size'.
        The returned array will have the same size as the 'weights' parameter.

        Parameters
        ----------
        weights:
            The i-th element gives the weight of subset size i.
        part_functs:
            The result of the get_partition_functions function.
        subset_size:
            The target subset size to calculate multiplicities.
        """
        assert(weights.size > 0)
        assert(weights.size == part_functs.size)
        assert(0 < subset_size and subset_size < weights.size)
        N = weights.size - 1
        result = numpy.full(N + 1, zero)
        for n in range(subset_size, N + 1):
            result[n] = weights[subset_size] * \
                (result[n - subset_size] + part_functs[n - subset_size])
        return result

    @optional_jit(float64[:](float64[:], float64[:]), nopython=True)
    def subset_quantity_expectation_values(
            weights: ndarray,
            input_size_pmf: ndarray) -> ndarray:
        """Expectation value of number of subsets with given sizes.

        The result is a 1D array, where the i-th element is the
        expectation value of the number of subsets in the partition
        having size i.
        The returned array will have the same size as the 'weights' parameter.

        Parameters
        ----------
        weights:
            The i-th element gives the weight of subset size i.
        input_size_pmf:
            The probability mass function of the input set size.
            The i-th element gives the probability that the size of
            the input set is i.
            The elements of the array should sum up to 1.
            Must have the same size as 'weights'.
        """
        assert(weights.size > 0)
        assert(weights.size == input_size_pmf.size)
        N = weights.size - 1
        result = numpy.full(N + 1, zero)
        part_functs = partition_functions(weights)
        for k in range(1, N + 1):
            part_functs_mul = partition_functions_multiplicity(
                weights, part_functs, k)
            for n in range(1, N + 1):
                result[k] += part_functs_mul[n] / \
                    part_functs[n] * input_size_pmf[n]
        return result

    @optional_jit(float64[:](float64[:], int64), nopython=True)
    def partition_functions_exclude(
            weights: ndarray,
            subset_size: int) -> ndarray:
        """Partition functions for many input set sizes excluding a subset size.

        The result is a 1D array, where the i-th element is the
        partition function for an input set of size i, but summands which
        correspond to partitions having a subset of size 'subset_size'
        will be excluded from the sum.
        The returned array will have the same size as the 'weights' parameter.

        Parameters
        ----------
        weights:
            The i-th element gives the weight of subset size i.
        subset_size:
            The subset size to exclude from the sum.
        """
        assert(weights.size > 0)
        assert(subset_size > 0 and subset_size < weights.size)
        N = weights.size - 1
        result = numpy.full(N + 1, zero)
        result[0] = 1
        for k in range(1, N + 1):
            if(k != subset_size):
                for n in range(k, N + 1):
                    result[n] += weights[k] * result[n - k]
        return result

    @optional_jit(float64[:](float64[:], float64[:], int64), nopython=True)
    def subset_number_pmf_for_size(
            weights: ndarray,
            input_size_pmf: ndarray,
            subset_size: int) -> ndarray:
        """Probability mass function of the number of subsets with given size.

        The result is a 1D array, where the i-th element is the
        probability that the number of the subsets with size 'subset_size'
        will be exactly i.
        The returned array will have the same size as the 'weights' parameter.

        Parameters
        ----------
        weights:
            The i-th element gives the weight of subset size i.
        input_size_pmf:
            The probability mass function of the input set size.
            The i-th element gives the probability that the size of
            the input set is i.
            The elements of the array should sum up to 1.
            Must have the same size as 'weights'.
        subset_size:
            The subset size under investigation.
        """
        assert(weights.size > 0)
        assert(weights.size == input_size_pmf.size)
        assert(subset_size > 0 and subset_size < weights.size)
        N = weights.size - 1
        part_functs = partition_functions(weights)
        part_functs_exc = partition_functions_exclude(weights, subset_size)
        result = numpy.full(N + 1, zero)
        for n in range(0, N + 1):
            exponent = 1
            for k in range(0, n // subset_size + 1):
                result[k] += input_size_pmf[n] * exponent * \
                    part_functs_exc[n - k * subset_size] / part_functs[n]
                exponent *= weights[subset_size]
        return result

    # put the created functions into a class and return them
    class SetPartitionCalculator:
        get_partition_functions = staticmethod(partition_functions)
        get_partition_functions_multiplicity = staticmethod(
            partition_functions_multiplicity)
        get_subset_quantity_expectation_values = staticmethod(
            subset_quantity_expectation_values)
        get_partition_functions_exclude = staticmethod(
            partition_functions_exclude)
        get_subset_number_pmf_for_size = staticmethod(
            subset_number_pmf_for_size)
    return SetPartitionCalculator()


def for_sympy():
    """Creates a calculator object for sympy.

    The resulting calculator can be used with the sympy package.
    Example:
        >>> calc = calculator.for_sympy()
        >>> w0, w1, w2 = sympy.symbols("w0 w1 w2")
        >>> calc.get_partition_functions(numpy.array([w0, w1, w2]))
    """
    from sympy import Integer
    return create(False, Integer(0))


def for_numba():
    """Creates a calculator object with compiled functions.

    The resulting calculator works with 64 bit floating point numbers.
    Example:
        >>> calc = calculator.for_numba()
        >>> calc.get_partition_functions(numpy.array([0.0, 1.0, 1.0]))
    """
    return create(True)
