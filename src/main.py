# -*- coding: utf-8 -*-
from math import pi, sin, radians, sqrt


def select_metric(kilometers):
    if kilometers >= 1:
        return kilometers, 'km'

    if kilometers * 1000 >= 1:
        return kilometers * 1000, 'm'

    if kilometers * 100000 >= 1:
        return kilometers * 100000, 'cm'

    return kilometers * 1000000, 'mm'


def km_to_mile(km):
    return km * 0.621371192


def mile_to_km(mile):
    return mile * 1.609344


def calculate_chord(radius, arc_degrees):
    """
    Please see the wikipedia link for more information on how this works.
    https://en.wikipedia.org/wiki/Chord_(geometry)
    """

    # Calculate the arc_degrees in radians.
    # We need this because sin() expects it.
    arc_radians = radians(arc_degrees)

    # Calculate the chord.
    return radius * (2 * sin(arc_radians / 2))  # km


def calculate_half_chord(radius, arc_degrees):
    """
    Convenience function.
    I forgot to divide by 2 at some point, and ended up with your 800 meter figure.
    This function makes it harder to repeat that mistake.
    """
    return calculate_chord(radius, arc_degrees) / 2  # km


def calculate_sagitta(radius, half_chord):
    """
    Please see the wikipedia link for more information on how this works.
    https://en.wikipedia.org/wiki/Sagitta_(geometry)
    """

    # There are two possible results of this formula, corresponding to both sides of the base of the arc.
    # This will return both sides. The smaller one is the one we want to use.

    squared = sqrt((radius ** 2) - (half_chord ** 2))
    return min(radius + squared, radius - squared)  # km


def calculate_arc_degrees(viewing_distance, circumference):
    """
    Calculate how many degrees an arc of the given length would cover of the circle.
    http://www.regentsprep.org/regents/math/geometry/gp15/circlearcs.htm
    """
    return (viewing_distance / circumference) * 360  # degrees

def display_results(viewing_distance, arc_degrees, sagitta):

    print('### Viewing distance:')
    print('%0.2f miles' % km_to_mile(viewing_distance))
    print()
    print('%0.2f %s' % select_metric(viewing_distance))
    print()

    print('### Arc:')
    print('%0.2f degrees' % arc_degrees)
    print()

    print("### Covered by curvature:")
    print('%0.2f miles' % km_to_mile(sagitta))
    print()
    print('%0.2f %s' % select_metric(sagitta))
    
    print()
    print('-----')
    print()

def main():
    # Earth's dimensions.
    circumference = 40000  # km
    diameter = circumference / pi  # km
    radius = diameter / 2  # km


    # Show the viewing distances of 10, 20, ... 60 miles,
    # and how much of the earth's curvature will get in the way.
    for viewing_distance in (10, 20, 30, 40, 50, 60, 125):

        # I'll be using SI units, so I'm going to have to convert the miles to kilometers.
        viewing_distance = mile_to_km(viewing_distance)  # km

        # The distance in degrees.
        arc_degrees = calculate_arc_degrees(viewing_distance, circumference)

        # Calculate the half chord and the sagitta.
        # Note: if you forget to divide the chord by 2, like I just did,
        # you'll end up with the 800 meter (0.5 mile) figure.
        half_chord = calculate_half_chord(radius, arc_degrees)  # km
        sagitta = calculate_sagitta(radius, half_chord)  # km

        # Display results.
        display_results(viewing_distance, arc_degrees, sagitta)

if __name__ == '__main__':
    main()
