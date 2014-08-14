import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;


public class WikiMatcher
{
    static String searchTerm1;
    static String searchTerm2;

    ArrayList <String>categoryList1 = new ArrayList<String>();
    ArrayList <String>categoryList2 = new ArrayList<String>();
   
   
    public static void main(String[] args) throws IOException
    {
        String[] category1=null;
        String[] category2=null;
        BufferedReader buffer1 = new BufferedReader(new InputStreamReader(System.in));
        System.out.println("Enter the 1st term");
        String searchTerm1 = buffer1.readLine();
        BufferedReader buffer2 = new BufferedReader(new InputStreamReader(System.in));
        System.out.println("Enter the 2nd term");
        String searchTerm2 = buffer2.readLine();
        System.out.println("Category Tree:" + searchTerm1);
        category1=getCategory(searchTerm1);
        for(int i=0;i<category1.length;i++)
            System.out.println(category1[i]);
        System.out.println("Category Tree:" + searchTerm2);
        category2 = getCategory(searchTerm2);
        for(int j=0;j<category2.length;j++)
            System.out.println(category2[j]);


    }

    public static String[] getCategory(String term)
    {
       
        ArrayList <String>categoryList = new ArrayList<String>();
        String tokens4[] = null;

try {
            URL wikiUrl = new URL("http://en.wikipedia.org/w/index.php?title="+term+"&action=edit");
            URLConnection wikiURLConnection=wikiUrl.openConnection();
            wikiURLConnection.connect();
            BufferedReader in = new BufferedReader(
new InputStreamReader(
wikiURLConnection.getInputStream()));
            String inputLine;
            while ((inputLine = in.readLine()) != null)
            {
                if(inputLine.startsWith("[[Category:"))
                {
                    categoryList.add(inputLine);
                }
                //if(inputLine.contains("#REDIRECT"))
                //{
                //    System.out.println("Page Redirected");
                //    System.exit(0);
                }
           
           
         
            in.close();
            String tokens1 = categoryList.toString().replaceAll("\\[","");
            String tokens2 = tokens1.replaceAll("\\]","");
            //System.out.println(tokens2);
            String tokens3 = tokens2.replaceAll("Category:","");
            //System.out.println(tokens3);
            tokens4 = tokens3.split(",");
            //for(int i=0;i<tokens4.length;i++)
                //System.out.println(tokens4[i]);
           //System.out.println(categoryList1);
            // TODO code application logic here
        } catch (MalformedURLException ex) {
            Logger.getLogger(WikiMatcher.class.getName()).log(Level.SEVERE, null, ex);
        }catch (IOException ex) {
            Logger.getLogger(WikiMatcher.class.getName()).log(Level.SEVERE, null, ex);
        }
return tokens4;
    }
}
