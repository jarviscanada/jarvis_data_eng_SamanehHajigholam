package ca.jrvs.apps.grep;

import java.io.File;
import java.io.IOException;
import java.util.List;

public interface JavaGrep {

  /**
   * Top level search workflow
   * @throws IOException
   */
  void process() throws IOException;

  /**
   * Traverse a given directory and return all files
   * @param rootDir input directory
   * @return files under the rootDir
   */
  List<File> listFiles(String rootDir);

  /**
   * Read a file and return all the lines
   *
   * FileReader: A class for reading characters from a file. It uses the system's default
   * character encoding, which may cause issues if the file uses a different encoding.
   *
   * BufferedReader: A wrapper around another Reader (such as FileReader) that improves performance
   * by buffering input(). It provides useful methods like readLine(), allowing efficient line-by-line reading.
   *
   * Character Encoding: Determines how characters are represented as bytes in a file. Using the
   * wrong encoding can lead to corrupted text. FileReader does not let you choose the encoding,
   * so for reliable encoding (e.g., UTF-8), it is better to use InputStreamReader with an
   * explicit charset.
   * @param inputFile
   * @return lines
   * @throws IllegalArgumentException if a given inputFile is not a file
   */
  List<String> readLines(File inputFile);

  /**
   * check if a line contains the regex patter (passed by the user)
   * @param line input string
   * @return true if there is a match
   */
  boolean containsPattern(String line);

  /**
   * Write lines to a file
   * FileOutputStream: A byte stream class used to write raw bytes to a file. It creates or
   * overwrites the target file and is the lowest-level stream in this writing process. Because it
   * works with bytes, it does not handle character encoding directly.
   *
   * OutputStreamWriter: A bridge between byte streams and character streams. It wraps a
   * FileOutputStream and converts characters into bytes using a specific character
   * encoding (e.g., UTF-8). This ensures that text is written correctly based on the chosen encoding.
   *
   * BufferedWriter: A wrapper that adds buffering to character output. Instead of writing each
   * character to the file immediately, it stores them in an internal buffer to improve performance.
   * It also provides convenient methods like write() and newLine() for writing text efficiently.
   * @param lines matched line
   * @throws IOException if write failed
   */
  void writeToFile(List<String> lines) throws IOException;

  String getRootPath();

  void setRootPath(String rootPath);

  String getRegex();

  void setRegex(String regex);

  String getOutFile();

  void setOutFile(String outFile);

}
