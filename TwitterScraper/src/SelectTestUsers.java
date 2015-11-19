import java.io.BufferedReader;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;

/**
 * This class extracts the from twitter the current followers and put them in a file 
 * along with the followers from our dataset
 *
 */
public class SelectTestUsers {

	public static int MIN_LIM = 10;
	public static int MAX_LIM = 200;
	public static int skip_count = 4000000;
	public static int test_users_over = 837;
	/**
	 * Input file of the format
	 * User1 Following1 Following2 Following3 ..
	 * User2 Following1 Following2 Following3 ..
	 * 
	 * Output file of the format:
	 * User1 numberfollowing Following1 Following2 Following3.. newnumberfollowing Following4 Following5 Following6..  
	 */
	public static void main(String[] args) {
		try {
			BufferedReader reader = new BufferedReader(new FileReader("D:\\study\\machine learning\\project\\adj"));
			OutputStreamWriter writer = new OutputStreamWriter(new FileOutputStream("D:\\study\\machine learning\\project\\TestUsers.txt", true));

			Random random = new Random();
			ArrayList<Integer> rand = new ArrayList<Integer>(10000);

			while(rand.size() <= 25000) {
				int nextInt = random.nextInt(35000000 - skip_count) + skip_count + 1;
				if(!rand.contains(nextInt)) 
					rand.add(nextInt);
			}

			Collections.sort(rand);

			int rand_index = 0;
			int line_number = 0;
			int test_users = test_users_over;

			String line;
			while((line = reader.readLine()) != null && ++line_number <= skip_count);
			
			System.out.println(skip_count + " lines skipped");
			
			while((line = reader.readLine()) != null && test_users <= 5000) {
				if(++line_number%500000 == 0) {
					System.out.println("Reading line:" + line_number + "\t rand_index:"+rand_index+"\t test_users:"+test_users);
				}

				if(line_number != rand.get(rand_index))
					continue;

				rand_index++;
				
				String[] lineParts = line.split("\t");
				if (lineParts.length >= (MIN_LIM + 1) && lineParts.length <= (MAX_LIM + 1)) {
					ArrayList<String> current_friends = new ArrayList<String>(500);
					DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
					DocumentBuilder db = dbf.newDocumentBuilder();
					Document doc;
					Thread.sleep(24000);
					try {
						doc = db.parse("http://api.twitter.com/1/friends/ids/"+lineParts[0]+".xml");
					}
					catch (IOException e) {
						System.err.println("http://api.twitter.com/1/friends/ids/"+lineParts[0]+".xml" + " not found");
						continue;
					}
					NodeList idNodes = doc.getElementsByTagName("id");
					for(int i = 0; i < idNodes.getLength(); i++) {
						current_friends.add(idNodes.item(i).getTextContent());
					}

					writer.write(lineParts[0] + "\t" + (lineParts.length-1) + "\t" + 
							line.substring(line.indexOf("\t")+1) + "\t" + 
							current_friends.size() + "\t" + join(current_friends) + "\n");
					writer.flush();

					test_users++;
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private static String join(ArrayList<String> current_friends) {
		if(current_friends == null || current_friends.size() == 0)
			return "";
		String str = current_friends.get(0);
		for (int i = 1; i < current_friends.size(); i++) {
			str += "\t" + current_friends.get(i);
		}
		return str;
	}
}
