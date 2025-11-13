def num_cpus_choices():
    mem_size_base = 2
    mem_size_min_exponent = 0
    mem_size_max_exponent = 7
    return (
        (mem_size_base**exponent, mem_size_base**exponent)
        for exponent in range(
            mem_size_min_exponent,
            mem_size_max_exponent
        )
    )


def mem_size_choices():
    mem_size_base = 2
    mem_size_min_exponent = 2
    mem_size_max_exponent = 9
    return (
        (mem_size_base**exponent, mem_size_base**exponent)
        for exponent in range(
            mem_size_min_exponent,
            mem_size_max_exponent
        )
    )


def disk_size_choices():
    mem_size_base = 2
    mem_size_min_exponent = 3
    mem_size_max_exponent = 10
    return (
        (mem_size_base**exponent, mem_size_base**exponent)
        for exponent in range(
            mem_size_min_exponent,
            mem_size_max_exponent
        )
    )
