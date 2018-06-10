import java.util.*;
import java.io.*;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class Twitter {	

	public static void main(String[] args) throws Exception 
	{
		JSONParser parser = new JSONParser();
		int no_clusters;
		File initialSeeds;
		String inseedFile, inputFile,outputFile;
		Scanner sci=new Scanner(System.in);
		Scanner scs=new Scanner(System.in);
		
		System.out.println("Enter the number of clusters:");
		no_clusters=sci.nextInt();
		
		System.out.println("Enter the name of Initial seeds file:");
		inseedFile=scs.nextLine();
		
		System.out.println("Enter the input tweets filename:");
		inputFile=scs.nextLine();
		
		System.out.println("Enter the output filename:");
		outputFile=scs.nextLine();
		outputFile=outputFile+".txt";
		
		initialSeeds = new File(inseedFile);
		File input = new File(inputFile);
		File output = new File(outputFile);
		
		Scanner is = new Scanner(initialSeeds);
		ArrayList<ArrayList<Tweets>> clusters = new ArrayList<>();
		
		while(is.hasNextLine()) 
		{
			ArrayList<Tweets> temp = new ArrayList<>();
			temp.add(new Tweets(is.nextLine()));
			clusters.add(temp);
		}
		Scanner inTweet = new Scanner(input); 
		ArrayList<Tweets> tweetsList = new ArrayList<>();
		
		try 
		{
			while(inTweet.hasNextLine()) 
			{
				JSONObject obj = (JSONObject) parser.parse(inTweet.nextLine());
				tweetsList.add(new Tweets(Long.toString((Long) obj.get("id")), (String) obj.get("text")));
			}
		} 
		catch(ParseException e) 
		{
			e.printStackTrace();
		}
		
		for(Tweets t : tweetsList)
			t.Tweet = t.Tweet.replaceAll("\\n"," ");
		
		for(ArrayList<Tweets> s : clusters) 
		{
			if(s.get(0).id.charAt(s.get(0).id.length() - 1) == ',')
				s.get(0).id = s.get(0).id.substring(0,s.get(0).id.length() - 1);
			
			for(Tweets j : tweetsList) 
			{
				if(s.get(0).id.compareTo(j.id) == 0) {
					s.get(0).addString(j.Tweet);
					break;
				}
			}
		}
		
		double dist,mindist;
		ArrayList<Tweets> minimumClus = new ArrayList<>();
		for(int i = 0; i < 25; i++) 
		{
			for(Tweets t : tweetsList) 
			{
				mindist = Double.MAX_VALUE;
				for(ArrayList<Tweets> c : clusters) 
				{
					dist = t.genDist(c.get(0).Tweet);
					if(dist < mindist) 
					{
						t.dist = dist;
						mindist = dist;
						minimumClus = c;
					}
				}
				minimumClus.add(t);
			}
			if(i == 24)
				break;
			
			ArrayList<ArrayList<Tweets>> tempClusters = new ArrayList<>();
			Tweets tempTweet = null;
			for(ArrayList<Tweets> c : clusters) 
			{
				mindist = Integer.MAX_VALUE;
				Iterator<Tweets> it = c.iterator();
				it.next();
				while(it.hasNext()) 
				{
					Tweets t = it.next();
					if(t.dist < mindist) 
					{
						mindist = t.dist;
						tempTweet = t;
					}
				}
				
				ArrayList<Tweets> tempList = new ArrayList<>();
				if(tempTweet != null)
					tempList.add(new Tweets(tempTweet.id, tempTweet.Tweet));
				else 
					tempList.add(c.get(0));
				tempClusters.add(tempList);
			}
			clusters = tempClusters;
		}
		
		int i = 1;
		FileWriter fW = new FileWriter(output);
		PrintWriter pW = new PrintWriter(fW);
		for(ArrayList<Tweets> c : clusters) 
		{
			pW.println("------Cluster " + i + "-------- ");
			Iterator<Tweets> it1 = c.iterator();
			it1.next();
			while(it1.hasNext()) 
			{
				Tweets t = it1.next();
				pW.println(t.id + " ");
			}
			pW.println();
			i++;
		}
		
		String sse="SSE is " + calcSSE(clusters);
		pW.write(sse);
		pW.close();
		System.out.println("SSE is " + calcSSE(clusters)); 
	}
	
	public static double calcSSE(ArrayList<ArrayList<Tweets>> clusters) 
	{
		double SSE = 0.0;
		for(ArrayList<Tweets> c : clusters) 
		{
			Tweets t = c.get(0);
			for(Tweets x : c)
				SSE += Math.pow(x.genDist(t.Tweet), 2); 
		}
		return SSE;
	}
}
