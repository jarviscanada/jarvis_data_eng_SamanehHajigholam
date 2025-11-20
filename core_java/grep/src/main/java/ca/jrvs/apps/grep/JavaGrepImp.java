package ca.jrvs.apps.grep;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.apache.log4j.BasicConfigurator;

public class JavaGrepImp implements JavaGrep{

  final Logger logger = LoggerFactory.getLogger(JavaGrepImp.class);

  private String regex;
  private String rootPath;
  private String outFile;

  @Override
  public String getRegex() {
    return regex;
  }

  @Override
  public void setRegex(String regex) {
    this.regex = regex;
  }

  @Override
  public String getRootPath() {
    return rootPath;
  }

  @Override
  public void setRootPath(String rootPath) {
    this.rootPath = rootPath;
  }

  @Override
  public String getOutFile() {
    return outFile;
  }

  @Override
  public void setOutFile(String outFile) {
    this.outFile = outFile;
  }

  @Override
  public void process() throws IOException {
    List<String> matchedLines = new ArrayList<>();
    for (File file : listFiles(rootPath)) {
      for (String line : readLines(file)) {
        if (containsPattern(line)){
          matchedLines.add(line);
        }
      }
    }
    writeToFile(matchedLines);
  }

  @Override
  public List<File> listFiles(String rootDir) {
    List<File> filesList = new ArrayList<>();
    File root = new File(rootDir);

    if (!root.isDirectory()){
      throw new IllegalArgumentException(rootDir+" is not a directory");
    }

    File[] files = root.listFiles();
    if (files != null) {
      for (File file : files) {
        if (file.isFile()) {
          filesList.add(file);
        } else if (file.isDirectory()) {
          // recursion
          filesList.addAll(listFiles(file.getAbsolutePath()));
        }
      }
    }

    return filesList;
  }

  @Override
  public List<String> readLines(File inputFile) {
    List<String> lines = new ArrayList<>();
    try (BufferedReader reader = new BufferedReader(new FileReader(inputFile))){
      String line;
      while ((line = reader.readLine()) != null) {
        lines.add(line);
      }
    } catch (IOException e) {
      logger.error("Failed to read file: " + inputFile.getAbsolutePath(), e);
    }
    return lines;
  }

  @Override
  public boolean containsPattern(String line) {
    return Pattern.compile(regex).matcher(line).find();
  }

  @Override
  public void writeToFile(List<String> lines) throws IOException {
    File out = new File(outFile);

    try (BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(out), StandardCharsets.UTF_8))) {
      for (String line : lines) {
        writer.write(line);
        writer.newLine();
      }
    } catch (IOException e) {
      logger.error("Failed to write to: " + outFile, e);
      throw e;
    }
  }

  public static void main(String[] args) {
    if (args.length !=3){
      throw new IllegalArgumentException("USAGE: JavaGrep regex rootPath outFile");
    }

    //Use default logger config
    BasicConfigurator.configure();

    JavaGrepImp javaGrepImp = new JavaGrepImp();
    javaGrepImp.setRegex(args[0]);
    javaGrepImp.setRootPath(args[1]);
    javaGrepImp.setOutFile(args[2]);

    try {
      javaGrepImp.process();
    } catch (Exception ex) {
      javaGrepImp.logger.error("Error: Unable to process", ex);
    }
  }
}
