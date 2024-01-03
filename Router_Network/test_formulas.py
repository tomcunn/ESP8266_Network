import Navigation
import pytest

# Test the distance formula
point1 = ((10,10))
point2 = ((20,20))

point3 = ((-10,-10))
point4 = ((-20,-20))

distance = Navigation.ComputeDistance(point1,point2)
print(distance)

def test_distance():
    # Positive Points
    assert  Navigation.ComputeDistance(point1,point2) == pytest.approx(14.1, 0.01)

def test_distance2():
    # Inverted Positive Points
    assert  Navigation.ComputeDistance(point2,point1) == pytest.approx(14.1, 0.01)

def test_distance3():
    # Negative Points
    assert  Navigation.ComputeDistance(point3,point4) == pytest.approx(14.1, 0.01)

def test_distance4():
    # Inverted Negative Points
    assert  Navigation.ComputeDistance(point4,point3) == pytest.approx(14.1, 0.01)



def test_turn_direction():
    # Basic Left Turn
    CurrentHeading = 270
    DesiredHeading = 180
    assert Navigation.ComputeTurnDirection(CurrentHeading,DesiredHeading) == "Left"


def test_turn_direction2():
    # Basic Right Turn
    CurrentHeading = 180
    DesiredHeading = 270
    assert Navigation.ComputeTurnDirection(CurrentHeading,DesiredHeading) == "Right"


def test_turn_direction3():
    # Crossing 360 to the left
    CurrentHeading = 10
    DesiredHeading = 290
    assert Navigation.ComputeTurnDirection(CurrentHeading,DesiredHeading) == "Left"


def test_turn_direction4():
    # Crossing 360 to the right
    CurrentHeading = 290
    DesiredHeading = 10
    assert Navigation.ComputeTurnDirection(CurrentHeading,DesiredHeading) == "Right"


def test_turn_direction5():
    # Large Left Turn
    CurrentHeading = 170
    DesiredHeading = 10
    assert Navigation.ComputeTurnDirection(CurrentHeading,DesiredHeading) == "Left"


def test_turn_direction6():
    # Large Right Turn
    CurrentHeading = 190
    DesiredHeading = 350
    assert Navigation.ComputeTurnDirection(CurrentHeading,DesiredHeading) == "Right"

def test_heading1():
    # Driving straight East
    CurrentPoint = ((10,0))
    PreviousPoint = ((0,0))
    assert Navigation.ComputeHeading(CurrentPoint,PreviousPoint) == pytest.approx(90, 0.1)

def test_heading2():
    # Driving straight West
    CurrentPoint = ((-10,0))
    PreviousPoint = ((0,0))
    assert Navigation.ComputeHeading(CurrentPoint,PreviousPoint) == pytest.approx(270, 0.1)

def test_heading3():
    # Driving straight North
    CurrentPoint = ((0,10))
    PreviousPoint = ((0,0))
    assert Navigation.ComputeHeading(CurrentPoint,PreviousPoint) == pytest.approx(0, 0.1)

def test_heading3():
    # Driving straight NorthWest
    CurrentPoint = ((-1,10))
    PreviousPoint = ((0,0))
    assert Navigation.ComputeHeading(CurrentPoint,PreviousPoint) == pytest.approx(350, 0.2)