from easy_trilateration.graph import *
from easy_trilateration.model import *
from scipy.optimize import least_squares


def rssi_to_distance(rssi, C=17, R=38):
    return 10 ** (-1 * (rssi + C) / R)


def easy_least_squares(crls, guess=(0, 0, 0)):
    result = least_squares(equations, guess, args=[crls])
    xf, yf, rf = result.x

    return Circle(Point(xf, yf), rf), result


def equations(guess, crls: [Circle]):
    eqs = []
    x, y, r = guess
    for circle in crls:
        eqs.append(((x - circle.center.x) ** 2 + (y - circle.center.y) ** 2 - (circle.radius - r) ** 2))
    return eqs


if __name__ == '__main__':
    circles = [Circle(Point(0, 0, ), rssi_to_distance(-72.5958)),
               Circle(Point(16.5, 0), rssi_to_distance(-73.3073)),
               Circle(Point(33, 0), rssi_to_distance(-73.2301)),
               Circle(Point(50, 0), rssi_to_distance(-77.1108)),
               Circle(Point(0, 50), rssi_to_distance(-77.1108)),
               Circle(Point(16.5, 50), rssi_to_distance(-73.3082)),
               Circle(Point(33, 50), rssi_to_distance(-73.231)),
               Circle(Point(50, 50), rssi_to_distance(-77.1113)),
               Circle(Point(0, 25), rssi_to_distance(-72.5948)),
               Circle(Point(50, 25), rssi_to_distance(-72.5948))]
    result_cirl, meta = easy_least_squares(circles)
    create_circle(result_cirl, target=True)
    draw([circles[0], circles[1], circles[2], circles[3], circles[4], circles[5], circles[6], circles[7],
          circles[8], circles[9]])
