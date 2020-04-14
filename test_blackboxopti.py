import blackbox as bb


def fun(par):
    return par[0]**2 + par[1]**2 # dummy 2D example


def main():
    bb.search(f=fun,  # given function
              box=[[-10., 10.], [-10., 10.]],  # range of values for each parameter (2D case)
              n=20,  # number of function calls on initial stage (global search)
              m=20,  # number of function calls on subsequent stage (local search)
              batch=4,  # number of calls that will be evaluated in parallel
              resfile='output.csv')  # text file where results will be saved


if __name__ == '__main__':
    main()