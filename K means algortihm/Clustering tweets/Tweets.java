import java.util.*;
import java.io.*;

class Tweets {
	
	String id;
	String Tweet;
	double dist;
	Tweets(String id, String t) {
		this.id = id;
		Tweet = t;
		this.dist = Double.MAX_VALUE;
	}
	Tweets(String id) {
		this.id = id;
		Tweet = "";
	}
	public void addString(String s) {
		Tweet = s;
	}
	public double genDist(String s) {
		String[] s1 = Tweet.split(" ");
		String[] s2 = s.split(" ");
		Set<String> hs1 = new HashSet<>();
		Set<String> hs2 = new HashSet<>();
		for(String t : s1) 
			hs1.add(t);
		for(String t: s2) 
			hs2.add(t);
		int inc = 0;
		for(String t : hs1) {
			if(hs2.contains(t))
				inc++;
		}
		int uc = hs1.size() + hs2.size() - inc;
		return (1.0 - (((double) inc)/uc));
	}
}