import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

/**
 * Replace %CODE% with requested id, and
 * replace %ALTCODE% w/"dashed" version of id.
 */
public class CodeReplacer {

    private static String CODE = "%CODE%";
    private static String ALTCODE = "%ALTCODE%";
    private static String DASHED = "-";

    protected String readTemplate() throws IOException {
        BufferedReader bufferReader = null;
        try {
            StringBuffer stringBuffer = new StringBuffer();

            // Read file from resources folder

            bufferReader = new BufferedReader(new FileReader(new File("./Resources/template.html")));
            String line;
            while (((line = bufferReader.readLine()) != null)) {
                stringBuffer.append(line);
                stringBuffer.append("\n");
            }
            return stringBuffer.toString();
        }catch(IOException e){
            System.out.println("Template file not found.");
            throw  e;
        }finally {
            if (null != bufferReader) {
                bufferReader.close();
            }
        }
    }


    /**
     * @param reqId java.lang.String
     * @throws java.io.IOException The exception description.
     */
    protected String substitute(String reqId) throws Exception {
        try {
            String template = readTemplate();
            template = substituteForCode(template, reqId, CODE);
            return substituteForCode(template, reqId.substring(0, 5) + DASHED + reqId.substring(5, 8), ALTCODE);
        } catch (Exception e) {
            System.out.println("Error in substitute()");
            throw e;
        }
    }

    private String substituteForCode(String template, String reqId, String substitutablePattern) {
        int templateSplitBegin = template.indexOf(substitutablePattern);
        int templateSplitEnd = templateSplitBegin + substitutablePattern.length();
        String templatePartOne = template.substring(0, templateSplitBegin);
        String templatePartTwo = template.substring(templateSplitEnd, template.length());
        return templatePartOne + reqId + templatePartTwo;
    }
}


