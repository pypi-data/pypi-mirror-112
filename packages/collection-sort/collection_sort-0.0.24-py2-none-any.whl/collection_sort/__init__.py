def quicksort(the_list, start, end):
    '''
    Parameters
    ----------
    the_list:
    start
    end
    Returns
    -------
    '''
    if start < end:
        m, n = start, end
        base = the_list[m]
        while m < n:
            while (m < n) and (the_list[n] >= base):
                n = n-1
            the_list[m]=the_list[n]
            while (m < n) and (the_list[m] <= base):
                m = m+1
            the_list[n] = the_list[m]
        the_list[m] = base
        quicksort(the_list, start, m-1)
        quicksort(the_list, n+1, end)
    return the_list
