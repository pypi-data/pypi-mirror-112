from numpy import power,exp,sqrt,pi,array
from sys import float_info as float_h

zero = 44e-15
inf = 1/zero


def limit(f,x,delta_x=zero):
    return f(x+delta_x)


def q_exp(u,q=1):
	power = lambda q_: 1/(1-q_)
	power = limit(power,q)
	q_exp_base = lambda q_: pow((1+u*(1-q_)),power)
	return limit(q_exp_base,q)


def radian(angle):
	return angle*(2*pi)/360


