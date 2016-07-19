package grabber;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

/**
 * Created by Nikita on 10.07.16.
 */
public class MyDocumentWriter {
    public static void write(MyDocument doc, String dir) {
        try {

            File file = new File(dir + doc.getUrlID() + ".txt");
            if (!file.exists()) {
                file.createNewFile();
            }

            FileWriter fw = new FileWriter(file.getAbsoluteFile());
            BufferedWriter bw = new BufferedWriter(fw);
            bw.write("<document>");
            bw.write("<title>" + doc.getTitle() + "</title>\n");
            bw.write("<tags>\n");
            for (String tag : doc.getTags()) {
                bw.write("<tag>" + tag + "</tag>\n");
            }
            bw.write("</tags>\n");
            bw.write("<text>" + doc.getText() + "\n</text>\n");
            bw.write("</document>");

            bw.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
