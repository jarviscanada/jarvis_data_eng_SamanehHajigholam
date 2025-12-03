# Introduction

The Java Grep App is a command-line application that mimics the Linux `grep` command. It recursively searches for a user-provided regex pattern in all files under a specified directory and 
outputs matched lines to a file. The project demonstrates **Core Java, Maven, Streams & Lambdas, logging with SLF4J/Log4j**, and **Docker** for deployment. Two implementations exist: a classic Java 
version (`JavaGrepImp`) and a lambda/stream-based version (`JavaGrepLambdaImp`) for modern Java practices.

# Quick Start

## Compile & Package
```bash
# In the Project Root
mvn clean package
```

## Run Java App
### Option 1 - Using Fat JAR

```bash
java -jar target/grep-1.0-SNAPSHOT.jar "PATTERN" /path/to/input /path/to/output.txt
```

Example:

```bash
java -jar target/grep-1.0-SNAPSHOT.jar ".*Romeo.*Juliet.*" ./data ./out/grep.txt
```

### Option 2 - Using Docker

```bash
docker run --rm \
-v $(pwd)/data:/data -v $(pwd)/out:/out \
samaneh7272/grep ".*Romeo.*Juliet.*" /data /out/grep.txt
```

# Implemenation
## Pseudocode
```bash
matchedLines = []
for file in listFilesRecursively(rootDir)
  for line in readLines(file)
      if containsPattern(line)
        matchedLines.add(line)
writeToFile(matchedLines)
```

## Performance Issue
When reading very large files (handling of huge datasets), the original implementation using `List<String>` caused `OutOfMemoryError`, because it tried to load the entire file into memory at once.

**Root Cause:**

- `List<String> lines = readLines(file)` collects all lines before processing.

- Large files exceed the JVM heap, especially with small memory limits (`-Xms5m -Xmx5m`).

Solution:

1. Use `BufferedReader` + Streams to read files **line by line**.

2. Return a lazy `Stream<String>` instead of a `List<String>`.

3. Compile regex once and reuse it in `containsPattern()` to improve performance.

4. Write matched lines immediately to the output file instead of storing them in memory.


# Test
- Run grep with known patterns (e.g., `Romeo.*Juliet`)

- Compare the output with Linux `egrep` results manually

- Verified both classic and lambda-based implementations

- Tested small and large files to ensure no memory errors occur

# Deployment

- Dockerized for easier distribution

- Dockerfile uses lightweight `eclipse-temurin:8-jdk-alpine` and copies the fat JAR

  - Running the app manually (`java -cp ...`) originally caused `ClassNotFoundException` for SLF4J/Log4j because dependencies were external.

  - Solved by building a **Fat/Uber JAR** with Maven Shade plugin, which packages all dependencies into a single JAR.

  - Now you can run the app easily: `java -jar target/grep-1.0-SNAPSHOT.jar ".*Romeo.*Juliet.*" ./data ./out/grep.txt`

- Volume mounting allows mapping of local input/output directories

- Commands:

```bash
# Build the image
docker build -t samaneh7272/grep .
# Run the container
docker run --rm -v `pwd`/data:/data -v `pwd`/log:/log samaneh7272/grep ".*Romeo.*Juliet.*" /data /log/grep.out
# Push the image to DockerHub
docker push samaneh7272/grep
```

# Improvement
- Stream-based processing for huge files (lazy reading via `BufferedReader` + `Stream`)
- Use -Xms and -Xmx JVM flags for heap control.
- Automated unit and integration testing