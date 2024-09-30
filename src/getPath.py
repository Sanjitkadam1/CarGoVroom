import time as t
import RPi.GPIO as PIN # type: ignore
import sys
import numpy as np 
import matplotlib.pyplot as plt
import reeds_shepp

start = (float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
final = (float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]))

rho = 400

path = reeds_shepp.path_sample(start, final, rho, step=20)

print(path)