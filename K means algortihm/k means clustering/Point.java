

import java.util.*;

public class Point 
{
    private double x = 0;
    private double y = 0;
    private int cno = 0;
    private int id=-1;
    
    
    public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public Point(double x, double y)
    {
        this.setX(x);
        this.setY(y);
    }
    
	public Point(double x, double y,int id)
    {
        this.setX(x);
        this.setY(y);
        this.id = id;
    }
	
    public void setX(double x) 
    {
        this.x = x;
    }
    
    public double getX() 
    {
        return this.x;
    }
    
    public void setY(double y) 
    {
        this.y = y;
    }
    
    public double getY() 
    {
        return this.y;
    }
    
    public void setCNo(int n) 
    {
        this.cno = n;
    }
    
    public int getCNo() {
        return this.cno;
    }
    
}