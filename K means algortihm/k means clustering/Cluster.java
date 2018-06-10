

import java.util.*;

public class Cluster 
{
	
    public List<Point>points=new ArrayList();
    public Point centre;
    public int id;

    public Cluster(int id) 
    {
        this.id = id;
    }

    public List getPoints() 
    {
        return points;
    }
	
    public void addPoint(Point point) 
    {
        points.add(point);
    }

    public void setPoints(List points) 
    {
        this.points = points;
    }

    public Point getCentre() 
    {
        return centre;
    }

    public void setCentre(Point centre) 
    {
        this.centre = centre;
    }

    public int getId() 
    {
        return id;
    }
    public void clear()
    {
    	points.clear();
    }
	
}