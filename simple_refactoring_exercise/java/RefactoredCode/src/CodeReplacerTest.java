import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

public class CodeReplacerTest extends TestCase {
    public CodeReplacerTest(String testName) {
        super(testName);
    }

    public void testTemplateLoadedProperly() {
        try {
            CodeReplacer replacer = new CodeReplacer();
            String templateString = replacer.readTemplate();
            assertEquals("xxx%CODE%yyy%ALTCODE%zzz\n", templateString);
        } catch (Exception ex) {
            fail("No exception expected, but saw:" + ex);
        }
    }

    public void testSubstitution() {
        try {
            String trackingId = "01234567";
            CodeReplacer replacer = new CodeReplacer();
            String substitutedString = replacer.substitute(trackingId);
            assertEquals("xxx01234567yyy01234-567zzz\n", substitutedString);
        } catch (Exception ex) {
            fail("testSubstitution exception - " + ex);
        }

    }

    public static Test suite() {
        return new TestSuite(CodeReplacerTest.class);
    }

    static public void main(String args[]) {
        junit.textui.TestRunner.run(suite());

    }

}