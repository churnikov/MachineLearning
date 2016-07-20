package grabber;

import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by Nikita on 03.07.16.
 */
public class Grabber {

    public static void main(String[] args) throws InterruptedException {
        Grabber grabber = new Grabber();
        grabber.walk(23720, 23874);
    }

    public MyDocument extract(String url, int id) {

        Document document = getDocument(url);
        if (document != null) {
            String title = document.getElementsByTag("h3").first().ownText();
            String date = document.getElementsByClass("reader_article_dateline__date").first().ownText();
            List<String> tags = getTags(document);
            String text = getText(document);

            return new MyDocument(Integer.toString(id) ,title, date, tags, text);
        }

        return null;
    }

    public void walk(int docIDStart, int docIDEnd) throws InterruptedException {
        for (int i = docIDStart; i <= docIDEnd; i++) {
            MyDocument doc = extract("http://government.ru/docs/"+ i +"/?ajax=reader", i);
            if (doc != null) {
                MyDocumentWriter.write(doc, "/Volumes/Media/Documents/Git/MachineLearning/out/");
            }
            Thread.sleep(1000);
        }
    }

    private Document getDocument(String url) {
        Document document = null;
        try {

            Connection.Response resp = Jsoup.connect(url)
                    .userAgent("Mozilla")
                    .referrer("http://www.google.com")
                    .ignoreHttpErrors(true)
                    .execute();
            int status = resp.statusCode();
            if (status == 200) {
                Connection conn = Jsoup.connect(url)
                        .userAgent("Mozilla")
                        .referrer("http://www.google.com");
                document = conn.get();
                System.out.println("Received error code : " + status + " on url : " + url);
            } else {
                System.out.println("Received error code : " + status + " on url : " + url);
            }

        } catch (IOException e) {
            e.printStackTrace();
        } catch (NullPointerException e) {
            e.printStackTrace();
        }
        return document;
    }

    private List<String> getTags(Document doc) {
        List<String> tags = new ArrayList<String>();
        try {
            Elements elemTags = doc.getElementsByClass("reader_article_tags_list").first().getElementsByTag("a");
            for (Element tag : elemTags) {
                tags.add(tag.ownText());
            }
        } catch (NullPointerException e) {
            tags.add("notag");
            e.printStackTrace();
        }

        return tags;
    }

    private String getText(Document doc) {
        String mainText = "";
        Elements paragraps = doc.getElementsByClass("reader_article_body").first().getElementsByTag("p");
        for (Element par : paragraps) {
            mainText = mainText + "\n" + par.text();
        }
        return mainText;
    }

}
