class MyMath
{
public:
    /**
     * Determines whether line segment ab intersects line segment cd (common end point is intersection as well)
     * */
    static bool Intersect(Point a, Point b, Point c, Point d)
    {
        Point devnull1, devnull2;
        return FindIntersection(a, b, c, d, devnull1, devnull2) > 0;
    }
    /**
    * Returns wheter point p lies inside contour c (including border)
    * */
    static bool IsInside(Point p, Contour &c)
    {
        int i = 0;
        int sum = SumOfIntersections_(p, Point(i, std::numeric_limits<int>::max()), c);

        //in case of touching segment ray is moved a bit
        while (sum == -1)
            sum = SumOfIntersections_(p, Point(++i, std::numeric_limits<int>::max()), c);

        return sum % 2 == 1;
    }

    /**
     * Determinant of (a-o), (b-o)
     */
    static double Det(Point a, Point b, Point o)
    {
        return static_cast<double>(a.x - o.x) * (b.y - o.y) - static_cast<double>(b.x - o.x) * (a.y - o.y);
    }

    //TODO - use my
    /**
    * Returns number of intersections and writes to output variables their coordinates.
    * */
    int static FindIntersection(Point a, Point b, Point c, Point d, Point &intersection_1, Point &intersection_2)
    {
        Point r = b - a; //rather vector
        Point s = d - c; //rather vector

        double cross_product = r.Cross(s);
        if (cross_product == 0) //parallel
        {
            if ((c - a).Cross(r) == 0) //collinear
            {
                double t1 = (c - a).Dot(r) / static_cast<double>(r.Dot(r));
                double t2 = t1 + s.Dot(r) / static_cast<double>(r.Dot(r));
                if (t1 >= 0 && t1 <= 1) //interiors are intersecting (c betweeen ab)
                {
                    intersection_1 = c;
                    intersection_2 = b;
                    return 2;
                }
                if (t2 > 0 && t2 < 1) //interiors are intersecting (d between ab)
                {
                    intersection_1 = a;
                    intersection_2 = d;

                    return 2;
                }
            }
        }
        else
        {
            double t = (c - a).Cross(s) / static_cast<double>(cross_product);
            double u = (c - a).Cross(r) / static_cast<double>(cross_product);

            if (t >= 0 && t <= 1 && u >= 0 && u <= 1) //intersecting
            {
                Point n = c + s * u; //calculates intersection
                //NOTE: m and n should be same (except rounding errors)
                //Point m = a + r * t;
                //DEBUG_PRINT("========== check intersection: " << n.x << " " << n.y << " ?=? " << m.x << " " << m.y << std::endl)

                if (t > 0 && t < 1 && u > 0 && u < 1) //intersecting in interiors
                {
                    intersection_1 = n;
                    return 1;
                }
                //following are all "T" cases:
                else if (t == 0 && u > 0 && u < 1)
                {
                    intersection_1 = a;
                    return 1;
                }
                else if (t == 1 && u > 0 && u < 1)
                {
                    intersection_1 = b;
                    return 1;
                }
                else if (u == 0 && t > 0 && t < 1)
                {
                    intersection_1 = c;
                    return 1;
                }
                else if (u == 1 && t > 0 && t < 1)
                {
                    intersection_1 = d;
                    return 1;
                }
                //segments have common endpoint
                else
                {
                    intersection_1 = n;
                    return 1;
                }
            }
        }
        return 0;
    }

private:
    static int SumOfIntersections_(Point p, Point end, Contour &c)
    {
        Point int1, int2;
        int sum = 0;
        for (size_t i = 0; i < c.Size(); i++)
        {
            auto seg = c.GetSegment(i);
            int count = FindIntersection(p, end, seg.begin(), seg.end(), int1, int2);
            if (count == 1)
            {
                if (int1 == p) return 1; //point is on the border
                ++sum;
            }
            if (count == 2)
                return -1; //ray touches segment
            //ray touches vertex (e.g. two lines) -> the parity of sum stayes unchanged
        }
        return sum;
    }

    static int FindCollinearIntersection_(double u0, double u1, double v0, double v1, double out[2])
    {
        //no intersection
        if ((u1 < v0) || (u0 > v1))
            return 0;
        if (u1 > v0)
        {
            if (u0 < v1)
            {
                out[0] = (u0 < v0) ? v0 : u0;
                out[1] = (u1 > v1) ? v1 : u1;
                return 2;
            }
            else
            {
                // u0 == v1 ... common endpoint
                out[0] = u0;
                return 1;
            }
        }
        else
        {
            // u1 == v0 ... common endpoint
            out[0] = u1;
            return 1;
        }
    }
};