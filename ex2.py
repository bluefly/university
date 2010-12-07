import math
import mpmath
import sys

def usage():
    print "%s <precision, e.g. 10**-2> <value of function to compute> <highest Taylor degree to try>" % __file__
    sys.exit(1)

def main():
    func = lambda x: mpmath.exp(mpmath.power(x, 2))
    precision = sys.argv[1].split('**')
    precision = math.pow(int(precision[0]), int(precision[1]))
    x = mpmath.mpf(float(sys.argv[2]))

    print "expected value = %f" % mpmath.quad(func, [0, x])
    print "precision = %f" % precision
    print "x = %f" % x
    print "max Taylor degree to try = %s" % sys.argv[3]
    print ""

    upperbound = int(sys.argv[3])
    lowerbound = 0
    lowestn = 0

    # find the degree logarithmically, this is usually faster than trying 0..n
    while lowerbound < upperbound:
        n = (lowerbound + upperbound) / 2

        # estimate the remainder
        diff = mpmath.diff(func, x, n)
        rn = diff / mpmath.factorial(n + 1)
        rn = rn * mpmath.power(x, n + 1)

        # is it good enough?
        if rn < precision:
            upperbound = n
            lowestn = n
        else:
            lowerbound = n + 1

    if lowestn:
        print "lowest Taylor degree needed = %d" % lowestn
        coefficients = []

        # find the coefficients of our Taylor polynomial
        for k in reversed(range(lowestn + 1)):
            if k > 0:
                coefficients.append(mpmath.diff(func, 0, k - 1) / mpmath.factorial(k))

        # compute the value of the polynomial (add 0 for the free variable, the value of the indefinite integral at 0)
        p = mpmath.polyval(coefficients + [0], x)
        print "computed value = %f" % p
    else:
        print "max n is too low"

if __name__ == "__main__":
    if len(sys.argv) < 4:
        usage()

    main()
