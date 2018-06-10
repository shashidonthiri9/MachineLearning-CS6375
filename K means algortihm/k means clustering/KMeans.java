
import java.util.*;
import java.io.*;
import java.lang.*;

public class KMeans 
{ 

    static List<Point> datapoints=new ArrayList();
    static List<Cluster>clusters=new ArrayList();
    static boolean first=false;
    static boolean samecentre=false;
    
    public static void main(String[] args) 
    {
        int k;
        double x;
        double y;
        Point p;
        Cluster c;
        int i;
        Scanner s=new Scanner(System.in);
        String line="";
        String file;
        String []input=new String[3];
        BufferedReader br = null;
        
        System.out.println("Enter the input file name:");
        file=s.nextLine();
        
        System.out.println("Enter the number of clusters:");
        k=s.nextInt();
       
        try 
        {
            br = new BufferedReader(new FileReader(file));
            br.readLine();
            while ((line = br.readLine()) != null) 
            {
                input= line.split("\\s+");
                x=Double.parseDouble(input[1]);
                y=Double.parseDouble(input[2]);
                
                p=new Point(x,y,Integer.parseInt(input[0]));
                datapoints.add(p);
            }
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }
       
        for(i=1;i<=k;i++)
        {
          c=new Cluster(i);
          clusters.add(c);
        }
        
        for(i=0;i<k;i++)
        {
          clusters.get(i).addPoint(datapoints.get(i));
          clusters.get(i).setCentre(datapoints.get(i));
        }
        
        clusters=findClusters(k);
        first=true;
        for(int up=0;up<25;up++)
        {
           clusters =calClusterCentre(clusters);
           if(samecentre==true)
           {
        	   break;
           }
           else
           {
        	   for(int r=0;r<clusters.size();r++)
               {
            	   clusters.get(r).clear();
            	   
               }
        	   
        	  
        	   clusters=findClusters(k);
              
           }
           
           
        }
        
        printClusterPoints();
        
    }
    public static List<Cluster> findClusters(int k)
    {
        int i,j,shortest=0;
        double dist,prevdist=Double.MAX_VALUE;
        Point p;
        if(first==false)
        {
            for(i=k;i<datapoints.size();i++)
            {
                p=(Point) datapoints.get(i);
         
                for(j=0;j<k;j++)
                {
                    Cluster cc=clusters.get(j);
                    Point pp=cc.getCentre();
                    dist=distance(p,pp);
                    if(dist<prevdist)
                    {
                        prevdist=dist;
                        shortest=j;
                    }
            
                }
            clusters.get(shortest).addPoint(p);
            prevdist=Double.MAX_VALUE;
            }
        }
        else
        {
            for(i=0;i<datapoints.size();i++)
            {
                p=(Point) datapoints.get(i);
         
                for(j=0;j<k;j++)
                {
                    Cluster cc=clusters.get(j);
                    Point pp=cc.getCentre();
                    dist=distance(p,pp);
                    if(dist<prevdist)
                    {
                        prevdist=dist;
                        shortest=j;
                    }
            
                }
            clusters.get(shortest).addPoint(p);
            prevdist=Double.MAX_VALUE;
            }
        }
        
       return clusters;
    }
    
    public static double distance(Point p, Point centre) 
    {
       return Math.sqrt(Math.pow((centre.getY() - p.getY()), 2) + Math.pow((centre.getX() - p.getX()), 2));
    }
    
    public static List<Cluster> calClusterCentre(List<Cluster>clusters)
    {
        double avgx,avgy,sumx=0.0,sumy=0.0;
        int i,no_points;
        Point centre=new Point(0,0);
        samecentre=true;
       for(i=0;i<clusters.size();i++)
       {	
    	   	no_points=0;
    	   	sumx=0.0;
    	   	sumy=0.0;
            List<Point> cluspoints=clusters.get(i).getPoints();
            Point clus_centre=clusters.get(i).getCentre();
            for(Point point :cluspoints )
            {
                no_points+=1;
                sumx+=point.getX();
                sumy+=point.getY();
            }
            avgx=sumx/no_points;
            avgy=sumy/no_points;
            
            	samecentre=(clus_centre.getX()==avgx)&&(clus_centre.getY()==avgy)&& samecentre;
           
            centre.setX(avgx);
            centre.setY(avgy);
            clusters.get(i).setCentre(new Point(centre.getX(),centre.getY()));
       }
       
       return clusters;
    }
    public static void printClusterPoints()
    {
    	System.out.println("enter the output file name:");
    	Scanner s=new Scanner(System.in);
    	String filename=s.nextLine();
    	filename+=".txt";
    	File OutputFile = new File(filename);
        BufferedWriter bw =null;
        double sqerror=0.0;
        try
        {
        	bw = new BufferedWriter(new FileWriter(OutputFile));
        }
        catch(Exception e)
        {
        	e.printStackTrace();
        }

    	sqerror=calcaulateSqErr(clusters);
    	
        for(int z=0;z<clusters.size();z++)
        {
            List<Point> print=clusters.get(z).getPoints();
            String output=clusters.get(z).getId()+"  ";
            int mark=0;
            for(Point cluspoints : print)
            {
            	if(mark!=0)
            	output+= ","+cluspoints.getId();
            	else
            		output+= cluspoints.getId();	
            	
            	mark++;	
            }
          
            System.out.print(output+"\n");
            try 
            {
            	
            	bw.write(output+"\n");
			} 
            catch (IOException e) 
            {
				e.printStackTrace();
			}
         
        }
        
        System.out.println("Sum Of squared error:"+sqerror);
        
        try 
        {
			bw.write("Sum Of squared error: "+sqerror);
			bw.close();
		} 
        catch (IOException e) 
        {
		
			e.printStackTrace();
		}

    }
    public static double calcaulateSqErr(List<Cluster> cluster)
    {
    	int i;
    	double sqerror=0.0;
    	 for(i=0;i<clusters.size();i++)
         {	
      	   	
              List<Point> cluspoints=clusters.get(i).getPoints();
              Point clus_centre=clusters.get(i).getCentre();
              for(Point point :cluspoints )
              {
            	  sqerror+=sqError(point,clus_centre);   
              }
         }
    	 return sqerror;
}
    
  public static double sqError(Point p, Point centre) 
  {
    double res=Math.sqrt(Math.pow((centre.getY() - p.getY()), 2) + Math.pow((centre.getX() - p.getX()), 2));
    return Math.pow(res,2);
  }  
}   