package ca.jrvs.apps.practice;


import java.util.regex.Pattern;

public class RegexExcImp implements RegexExc {

  // If you use the same regex many times, compile it only once:so, this is more efficient(regex compilation is expensive.)
//  private static final Pattern EMPTY_LINE_PATTERN = Pattern.compile("^\\s*$");
//  @Override
//  public boolean isEmptyLine(String line) {
//    return EMPTY_LINE_PATTERN.matcher(line).matches();
//  }

  @Override
  public boolean matchJpeg(String filename) {
    return Pattern.compile("(?i)^.+\\.(jpg|jpeg)$").matcher(filename).matches();
  }

  @Override
  public boolean matchIp(String ip) {
    // Pattern.matches(regex, input) is a shortcut -> It compiles the regex every time you call it.
    return Pattern.matches("^(\\d{1,3}\\.){3}\\d{1,3}$", ip);
  }

  @Override
  public boolean isEmptyLine(String line) {
    return Pattern.matches("^\\s*$", line);
  }

  public static void main(String[] args) {

    RegexExc regex = new RegexExcImp();

    System.out.println("JPEG TESTS");
    System.out.println(regex.matchJpeg("photo.jpg"));       // true
    System.out.println(regex.matchJpeg("image.jpeg"));      // true
    System.out.println(regex.matchJpeg("test.JPG"));        // true
    System.out.println(regex.matchJpeg("file.png"));        // false

    System.out.println("IP TESTS");
    System.out.println(regex.matchIp("192.168.0.1"));       // true
    System.out.println(regex.matchIp("10.0.0.255"));        // true
    System.out.println(regex.matchIp("256.1.1.1"));         // false
    System.out.println(regex.matchIp("abc.def"));           // false

    System.out.println("EMPTY LINE TESTS");
    System.out.println(regex.isEmptyLine(""));              // true
    System.out.println(regex.isEmptyLine("   "));           // true
    System.out.println(regex.isEmptyLine("\t\t"));          // true
    System.out.println(regex.isEmptyLine("hello"));         // false
  }
}