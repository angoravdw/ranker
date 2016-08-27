# Program Purpose
Simple "league rank" calculator to take in a file with match results and produce an output file with the team's rank,
sorted according to points and names where relevant.

The input format is assumed to be well formatted (in other words, no error checks are done on the format in the file). Here is
and example of the expected input format:

<pre>
Lions 3, Snakes 3
Tarantulas 1, FC Awesome 0
Lions 1, FC Awesome 1
Tarantulas 3, Snakes 1
Lions 4, Grouches 0
</pre>

As you can see, it contains the name of the team, followed by the points they scored in the match, followed by the name
of the next team and followed by the points they scored in the match. Each match result is placed in the next line in the
input file.

The resulting output will look as follows:
<pre>
1. Tarantulas, 6 pts
2. Lions, 5 pts
3. FC Awesome, 1 pt
3. Snakes, 1 pt
5. Grouches, 0 pts
</pre>

Teams that are equal in rank will be placed below each other alphabetically. It does not denote "better" performance if you
are second in line for the same rank.

The resulting output is also written to file for perusal afterward.


# Running The Program:

## Directly (OS-X or Linux)
### Prerequisites
- It is assumed that you are running a later version of either OS-X or Linux which comes with Python 2.7 installed.
- It is assumed that python pip is installed. If not, please run ```brew install python``` to get all python, pip and setup
 pacakages on OS-X, or ```apt-get -y install python-pip``` for Linux

### Setup
- Run ``` pip install -r requirements.txt ``` in the source folder. It is only needed for the automated tests.

### Running It
First, we assume that the input file is located at */tmp/match_results.txt*

To calculate the rank, you will therefore run the following command:
```python calculate_rank.py -f /tmp/match_results.txt```

The program will output the result to "rank_results.txt" and place it in the same source location as the input file.
Therefore, the resulting calculated rank will be found at */tmp/rank_results.txt*

### Testing It
Tests are run via python nose.
To run automated tests, ensure you are in the source folder root, then:
- ```nosetests tests/```


## Via Docker
### Prerequisites
To run the docker container you will need to install Docker first. Follow installs steps, for your particular OS, here:
https://docs.docker.com/engine/installation/

### Setup
- Create your docker image. Run this command from root:
``` docker build -t ranker .```

### Running It
First, we assume that the input file is located at */tmp/match_results.txt* on the host machine.

To run, start up a docker container using the pre-built image:
- ```docker run -it --name rank_container ranker bash```
The above command will start up a container with the "rank_container" name. This is only to make the steps following easier.

Next, copy the source file you need to the /tmp folder in the container. You will need to open up another
terminal since the previous command will attach your terminal to the container console.
- ```cp /tmp/match_results.txt rank_container:/tmp```

Now go back to the terminal connected to your container. Now you can run:
```python calculate_rank.py -f /tmp/match_results.txt``` **in the container.**

The program will output the result to "rank_results.txt" and place it in the same source location as the input file.
Therefore, the resulting calculated rank will be found at */tmp/rank_results.txt* **in the container**

### Testing It
To run, start up a docker container using the pre-built image:
- ```docker run -it ranker bash```
A name is not needed to run automated tests.

You will be attached to the container, then run:
- ```nosetests tests/```

To exit any container, simply type "Exit" in the terminal connected to the container. The containers will also stop.

### Additional Info:
If you change any source files, simply rebuild the container and repeat the steps. Alternatively, map your source code
to the same source location when you start your "disposable" container and any changes you make to your source code on
your host machine will also be on the container.

To do this:
- Ensure you are in the source folder root
- run ```ROOT=`pwd` ```
- run ```docker run -it -v ${ROOT}:/src ranker bash```
