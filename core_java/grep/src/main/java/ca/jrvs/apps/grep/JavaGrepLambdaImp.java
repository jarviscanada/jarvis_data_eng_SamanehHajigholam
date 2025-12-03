package ca.jrvs.apps.grep;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class JavaGrepLambdaImp extends JavaGrepImp {

  public static void main(String[] args) {
    if (args.length != 3) {
      throw new IllegalArgumentException("USAGE: JavaGrepLambdaImp regex rootPath outFile");
    }

    JavaGrepLambdaImp grepLambda = new JavaGrepLambdaImp();
    grepLambda.setRegex(args[0]);
    grepLambda.setRootPath(args[1]);
    grepLambda.setOutFile(args[2]);

    try {
      // calling the process in the parent class
      grepLambda.process();
    } catch (Exception ex) {
      grepLambda.logger.error("Error: Unable to process", ex);
    }
  }

  /**
   * Implement using lambda and stream APIs
   * @param inputFile
   * @return
   */
  @Override
  public List<String> readLines(File inputFile) {
    if (!inputFile.isFile()) {
      throw new IllegalArgumentException(inputFile + " is not a file");
    }

    try(BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(inputFile), StandardCharsets.UTF_8))) {
      return reader.lines().collect(Collectors.toList());
    } catch (IOException e) {
      logger.error("Failed to read file: " + inputFile.getAbsolutePath(), e);
      return Collections.emptyList();
    }
  }

  /**
   * Implement using lambda and stream APIs
   * @param rootDir input directory
   * @return
   */
  @Override
  public List<File> listFiles(String rootDir) {
    File root = new File(rootDir);

    if(!root.isDirectory()) {
      throw new IllegalArgumentException(rootDir + " is not a directory");
    }

    File[] files = root.listFiles();
    if (files == null) {
      return Collections.emptyList();
      //return List.of(); for Java9 and higher
    }
    return Stream.of(files).flatMap(file -> {
      if (file.isDirectory()) {
        return listFiles(file.getAbsolutePath()).stream(); // when we reach a directory, listFiles returns list of files, but we need to return stream as flatMap requires a Stream<File>
      } else {
        return Stream.of(file);
      }
    }).collect(Collectors.toList());
  }
}
