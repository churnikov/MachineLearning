package grabber;

import java.util.List;

/**
 * Created by Nikita on 04.07.16.
 */
public class MyDocument {
    private String urlID;
    private String title;
    private String date;
    private List<String> tags;
    private String text;

    public MyDocument(String urlID, String title, String date, List<String> tags, String text) {
        this.urlID = urlID;
        this.title = title;
        this.date = date;
        this.tags = tags;
        this.text = text;
    }

    public String getUrlID() {
        return urlID;
    }

    public String getTitle() {
        return title;
    }

    public String getDate() {
        return date;
    }

    public List<String> getTags() {
        return tags;
    }

    public String getText() {
        return text;
    }
}
