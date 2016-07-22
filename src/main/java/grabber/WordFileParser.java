package grabber;

import org.apache.poi.hwpf.HWPFDocument;
import org.apache.poi.hwpf.extractor.WordExtractor;

import java.io.File;
import java.io.FileInputStream;

/**
 * Created by Nikita on 22.07.16.
 */
public class WordFileParser {
    public static String parse(String path){
        File file = null;
        WordExtractor extractor = null;
        String text = "";
        try
        {

            file = new File(path);
            FileInputStream fis = new FileInputStream(file.getAbsolutePath());
            HWPFDocument document = new HWPFDocument(fis);
            extractor = new WordExtractor(document);
            String[] fileData = extractor.getParagraphText();
            for (int i = 0; i < fileData.length; i++)
            {
                if (fileData[i] != null)
                    text = text + fileData[i];
            }
        }
        catch (Exception exep)
        {
            exep.printStackTrace();
        }
        return text;
    }
}
