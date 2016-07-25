package grabber;

import org.apache.commons.io.FileUtils;
import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by Nikita on 03.07.16.
 */
public class Grabber {

    public static void main(String[] args) throws InterruptedException {
        Grabber grabber = new Grabber();
        String outPath = "/Volumes/Media/Documents/Git/MachineLearning/out/news/";
        grabber.walk(1, 23936, "news", outPath);
    }

    public MyDocument extract(String url, int id) {

        Document document = getDocument(url);
        if (document != null) {
            String title = document.getElementsByTag("h3").first().ownText();
            String date = document.getElementsByClass("reader_article_dateline__date").first().ownText();
            List<String> tags = getTags(document);
            String text = getText(document) + getAttachedText(document);

            return new MyDocument(Integer.toString(id) ,title, date, tags, text);
        }

        return null;
    }

    public void walk(int docIDStart, int docIDEnd, String citePart, String outPath) throws InterruptedException {
        for (int i = docIDStart; i <= docIDEnd; i++) {
            MyDocument doc = extract("http://government.ru/" + citePart + "/"+ i +"/?ajax=reader", i);
            if (doc != null) {
                MyDocumentWriter.write(doc, outPath);
            }
            Thread.sleep(1000);
        }
    }

    public Document getDocument(String url) {
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

    private String getAttachedText(Document doc) {
        String text = "";
        try {
            Element link = doc.getElementsByClass("entry_file_link").first();
            String href = link.attr("href");
            href = "http://government.ru/" + href;
            URL u = new URL(href);
            if (isPDF(href)) {
                File file = new File("/Volumes/Media/Documents/Git/MachineLearning/src/main/resources/tmp.pdf");
                FileUtils.copyURLToFile(u, file);
                text = MyPDFParser.parse(file.getAbsolutePath());
                FileUtils.forceDelete(file);
            } else {
                File file = new File("/Volumes/Media/Documents/Git/MachineLearning/src/main/resources/tmp.doc");
                FileUtils.copyURLToFile(u, file);
                text = WordFileParser.parse(file.getAbsolutePath());
                FileUtils.forceDelete(file);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (NullPointerException e) {
            e.printStackTrace();
        }
        return text;
    }

    private boolean isPDF (String source) {
        if (source.endsWith(".pdf")) {
            return true;
        } else {
            return false;
        }
    }



}
