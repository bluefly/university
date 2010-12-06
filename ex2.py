import math
import mpmath
import sys

def usage():
    print "%s <precision, e.g. 10^-2> <value of function to compute> <highest Taylor degree to try>" % __file__
    sys.exit(1)

def derivative(f):
    def df(x, h=0.1e-5):
        return (f(x+h/2) - f(x-h/2)) / h

    return df

def main():
    func = lambda x: mpmath.exp(mpmath.power(x, 2))
    precision = sys.argv[1].split('^')
    print precision
    precision = math.pow(int(precision[0]), int(precision[1]))
    x = mpmath.mpf(float(sys.argv[2]))

    print "expected value = %f" % mpmath.quad(func, [0, x])
    print "precision = %f" % precision
    print "x = %f" % x
    print "max Taylor degree = %s" % sys.argv[3]
    print ""

    upperbound = int(sys.argv[3])
    lowerbound = 0
    lowestn = 0

    while lowerbound < upperbound:
        n = (lowerbound + upperbound) / 2
        #for n in range(int(sys.argv[3])):
        #print "trying n = %d " % n
        diff = mpmath.diff(func, x, n)
        rn = diff / mpmath.factorial(n + 1)
        rn = rn * mpmath.power(x, n + 1)

        if rn < precision:
            upperbound = n
            lowestn = n
        else:
            lowerbound = n + 1

    if lowestn:
        print "lowest Taylor degree needed = %d" % lowestn
        coefficients = []

        for k in reversed(range(lowestn + 1)):
            if k > 0:
                coefficients.append(mpmath.diff(func, 0, k - 1) / mpmath.factorial(k))

        p = mpmath.polyval(coefficients + [0], x)
        print "computed value = %f" % p
    else:
        print "max n is too low"

if __name__ == "__main__":
    if len(sys.argv) < 4:
        usage()

    main()
