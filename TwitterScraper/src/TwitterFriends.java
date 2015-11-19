import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;


public class TwitterFriends {

	public static void main(String[] args) {
		try {
			File file = new File(args[1]);
			BufferedReader reader = new BufferedReader(new FileReader(file));
			String line;
			while((line = reader.readLine()) != null) {
				Thread.sleep(24000);
				DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
				DocumentBuilder db = dbf.newDocumentBuilder();
				Document doc = db.parse("http://api.twitter.com/1/friends/ids/"+line+".xml");
				NodeList idNodes = doc.getElementsByTagName("id");
				for(int i = 0; i < idNodes.getLength(); i++) {
					System.out.println(idNodes.item(i).getTextContent());
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
