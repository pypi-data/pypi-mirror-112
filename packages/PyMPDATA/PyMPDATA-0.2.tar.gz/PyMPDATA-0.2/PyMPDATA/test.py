if __name__ == '__main__':
    import numba
    @numba.njit()
    def fun():
        return None(*None, (None if None else None))
    fun()
