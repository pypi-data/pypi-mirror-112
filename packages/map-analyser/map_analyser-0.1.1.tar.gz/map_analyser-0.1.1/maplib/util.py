import numpy as np

from collections import namedtuple
from dataclasses import dataclass

# Coord = namedtuple('Coord', 'x y')
CoordsLists = namedtuple('CoordsLists', 'x y')

class ParseError(Exception):
    pass

@dataclass(order=True, frozen=True)
class Coord():
    x: int
    y: int

    def __add__(self, other):
        if type(other) is type(self):
            return Coord(self.x + other.x, self.y + other.y)
        else:
            return Coord(self.x + other, self.y + other)

    def __sub__(self, other):
        return Coord(self[0] - other[0], self[1] - other[1])

    def __iter__(self):
        yield self.x
        yield self.y

    def __mul__(self, scalar):
        return Coord(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return Coord(self.x * scalar, self.y * scalar)

    def __getitem__(self, index):
        if index == 'x' or index == 0:
            return self.x
        elif index == 'y' or index == 1:
            return self.y
        else:
            raise IndexError('Unknown index.')

    # def __init__(self, x, y):
    #     self.x = x
    #     self.y = y
    # def __setitem__(self, index, value):
    #     if index == 'x' or index == 0:
    #         self.x = value
    #     elif index == 'y' or index == 1:
    #         self.y = value
    #     else:
    #         raise IndexError('Unknown index.')
    #
    # def __hash__(self):
    #     return hash((self.x, self.y))
    #
    # def __lt__(self, other):
    #     return (self.x, self.y) < (other.x, other.y)
    #
    # def __eq__(self, other):
    #     return self.x == self.y and self.x == self.y

"""
void Polygon::Extract_Polygon_(const Object &o)
{
    switch (o.GetType())
    {
    case Object::Type::TEXT:
        throw AnalyserException("Text cannot be in map plan.");
    case Object::Type::POINT:
        //TODO:
        //Extract_Point_(o.coords[0], o.symbol)
        break;
    case Object::Type::PATH:
    {
        Contour c;
        for (size_t i = 0; i < o.coords.size(); i++)
        {
            auto p = Point(o.coords[i]);
            if(i == 0 || (c[c.Size()-1] != p && ! o.coords[i].IsCurveStart())) //prevents two same points in a row
                c.Add(p);
            if (o.coords[i].IsCurveStart())
            {
                if (i + 2 >= o.coords.size())
                    throw AnalyserException("Unended Bezier curve.");
                Aprox_Bezier_(c, o.coords[i], o.coords[i + 1], o.coords[i + 2], o.coords[i + 3]);
                i += 2;
            }
        }
        if (o.coords.back().IsClosePoint() || (c.Size() > 1 && c.front() == c.back()) )
        {
            if(c.Size() <= 2) break; //too short object
            
            c.Erase(--c.end()); //dont want closed curve start point twice
            c.SetClosed();
            
            if(c.front().Dist(c.back()) < RADIUS)//should avoid minor drawing inacuracies:
                c.Erase(--c.end());
        }
        else //line symbol
        {
            c.SetNotClosed();
        }
        
        contours_.push_back(std::move(c));
        break;
    }
    default:
        throw AnalyserException("This object type cannot be in map plan.");
    }
}
/*
Bezier curve is: https://en.wikipedia.org/wiki/B%C3%A9zier_curve
*/
void Polygon::Aprox_Bezier_(Contour &out, Point a, Point b, Point c, Point d)
{
    float this_step = STEP * Get_Radius_(a,b,c,d);
    if(this_step < 0.15) this_step = 0.15f;
    if(this_step > 0.3) this_step = 0.3f;
    for (float i = this_step; i < 1; i += this_step)
    {
        Point x = Get_Point_(a, b, i);
        Point y = Get_Point_(b, c, i);
        Point z = Get_Point_(c, d, i);

        Point m = Get_Point_(x, y, i);
        Point n = Get_Point_(y, z, i);

        out.Add(Get_Point_(m, n, i));
    }
}

double Polygon::Get_Radius_(Point a, Point b, Point c, Point d)
{
    auto avg = (a+b+c+d) * (1/4.0);
    double max =0;
    double dist;

    dist= a.Dist(avg);
    if(dist > max) max = dist;

    dist= b.Dist(avg);
    if(dist > max) max = dist;
    
    dist= c.Dist(avg);
    if(dist > max) max = dist;
    
    dist= d.Dist(avg);
    if(dist > max) max = dist;

    return max;
}
Point Polygon::Get_Point_(Point a, Point b, float percentage)
{
    return a + (b - a) * percentage;
}

void Polygon::BoundingBox(Point &min, Point &max)
{
    min.x = min.y = std::numeric_limits<int>::max();
    max.x = max.y = std::numeric_limits<int>::min();
    Point mintmp;
    Point maxtmp;
    for (size_t i = 0; i < Size(); i++)
    {
        contours_[i].BoundingBox(mintmp, maxtmp);
        if (mintmp.x < min.x)
            min.x = mintmp.x;
        if (maxtmp.x > max.x)
            max.x = maxtmp.x;
        if (mintmp.y < min.y)
            min.y = mintmp.y;
        if (maxtmp.y > max.y)
            max.y = maxtmp.y;
    }
}

void Contour::BoundingBox(Point &min, Point &max)
{
    min.x = min.y = std::numeric_limits<int>::max();
    max.x = max.y = std::numeric_limits<int>::min();
    Contour::iterator i = begin();
    while (i != end())
    {
        if (i->x < min.x)
            min.x = i->x;
        if (i->x > max.x)
            max.x = i->x;
        if (i->y < min.y)
            min.y = i->y;
        if (i->y > max.y)
            max.y = i->y;
        ++i;
    }
}

bool Contour::Counterclockwise()
{
	if (computedCC_)
		return CC_;
	else computedCC_ = true;

	double sum = 0.0; //Sum over the edges  (https://en.wikipedia.org/wiki/Shoelace_formula)
	for (size_t i = 0; i < Size(); i++)
    {
        Segment s = GetSegment(i);
        sum += static_cast<double>(s.end().x + s.begin().x)*static_cast<double>( s.begin().y - s.end().y);
    }

	CC_ = sum >= 0.0;
    return CC_;
}
"""
