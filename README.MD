# Examining the Progression of the Revenue of Oscar “Best Picture” Winners and Their IMDb User Score From 1986 to 2016

This experiment serves the purpose of investigating how the gross revenue (USA) and the IMDb user score of movies that were awarded with an Oscar in
the category "Best Picture" have evolved and fluctuated over the last three decades - more specifically, from 1986 to 2016. from 1986 until 2016.

## Description

...

## Data Sources

...

## Data Flow

![Data Flow Diagram](documentation/data_flow/data_flow.png)

## Directory and File Structure

The listing below illustrates the directory structure of the experiment, along with its most important files.

```shell
.
├── data
│   ├── movies.csv
│   └── the_oscar_award.csv
├── documentation
│   └── data_flow
│       ├── data_flow.pdf
│       └── data_flow.png
├── result
│   ├── awarded_movies.csv
│   └── awarded_movies_visualization.png
├── src
│   ├── awarded_movie.py
│   ├── main.py
│   ├── movie.py
│   └── oscar_info.py
├── Dockerfile
└── requirements.txt
```

* `data`: raw data sets that are processed
    * `movies.csv`: 6820 movies from 1986 until 2016 with attributes such as budget, genre, gross revenue, IMDb user score; data was scraped from IMDb
    * `the_oscar_award.csv`: records of past Oscar winners and nominees between 1927 and 2018; data was scraped from the official Academy Awards
      search site
* `documentation`: files that provide additional information about the experiment (might overlap with information presented in this `README`)
* `result`: represents the result ("output") of the experiment
    * `awarded_movies.csv`:
    * `awarded_movies_visualization.png`:
* `src`: Python source files that make up the experiment
    * `main.py`: bundles input data parsing, processing and exporting of results
    * `awarded_movie.py`, `movie.py`, `oscar_info.py`: model classes that are Python representations of data rows from `awarded_movies.csv`,
      movies.csv` and `the_oscar_award.csv`, respectively
* `Dockerfile`: a text document with commands Docker can read and build an image from
* `requirements.txt`: a file listing the Python dependencies of the script that can be installed using `pip`

## Running the Experiment

### Local Python Interpreter

This experiment was conceived using Python `3.7`. Any higher, backwards-compatible version and most probably `3.6` will also work without any
problems.

#### Preparing a Virtual Environment (optional)

If you do not want to pollute your global Python installation with the dependencies of the main script, you can create a virtual environment that is
local to the experiment directory.

_**Note:** In the following, `python37` is used to denote the executable of your installation of Python and could, for instance, be replaced by the
absolute path to the executable of Python `3.8`. The same goes for commands like `pip37` or `virtualenv37`._

In case you don't have the `virtualenv` module installed or if you are not sure, enter the following command:

```shell
pip37 install virtualenv
```

Next, you can create a directory within the experiment's root folder that will contain the virtual environment. Following common conventions, **venv**
or **.venv** (if the folder should be hidden) are good choices for the folder's name:

```shell
virtualenv37 venv
```

Alternatively, if you cannot find the location of your `virtualenv` and the correct version is not in the `PATH`, you can also use:

```shell
python37 -m virtualenv venv
```

Above command(s) create a virtual environment containing, amongst others, a copy of the Python interpreter and the standard library.

In order to use the virtual environment, you need to activate it. The following table depicts how to activate it, depending on your operating system
and shell environment:

| Environment        | Command                         |
|--------------------|---------------------------------|
| Windows CMD        | `venv\Scripts\activate.bat`     |
| Windows PowerShell | `.\venv\Scripts\activate.ps1`   |
| Unix/MacOS bash    | `source venv/bin/activate`      |
| Unix/MacOS csh     | `source venv/bin/activate.csh`  |
| Unix/MacOS fish    | `source venv/bin/activate.fish` |

After activating the virtual environment, your shell's prompt should be prefixed with `(venv)` and running `python`, `pip`and the like will execute
the particular version of the Python interpreter the virtual environment is based on.

In order to finalize the virtual environment setup, the required dependencies need to be installed:

```shell
pip install -r requirements.txt
```

_**Note:** When you are done with the experiment and want to exit the virtual environment, simply type `deactivate` (this command is registered upon
activating the virtual environment) or - if that should fail - close the shell._

#### Executing the Experiment

The experiment is run by simply invoking the main script:

```shell
python src/main.py
```

### Docker

If you don't have Python installed on your machine or do not want to install another version (if yours should not work), you can also run the
experiment in a Docker container.

First, you need to build the image based on the provided `Dockerfile`. This can be achieved with the following command (don't forget the dot `.` at
the end):

```shell
docker build -t awarded_movies:latest .
```

The command above creates a Docker **image** with the name **awarded_movies:latest** which contains the `data` directory, the `src` directory as well
as the `requirements.txt` file.

Upon building the image, the correct version of Python (`3.7`) is installed, along with all the modules the script depends on, as specified in
the `requirements.txt`.

_**Note:** If you perform modifications to the source code and want to build them into an image without overwriting the original one, you can change
the tag `latest` to any other distinguishable identifier of your choice_

There are two possibilities to execute the image as a container. They both achieve the same, but based on individual preferences, one might be chosen
over the other.

#### Option A: Executing the Container With the Provided Defaults (Recommended)

This method is recommended for its simplicity.

Run the previously built image as a **container** with the name **awarded_movies_container**:

```shell
docker run --name awarded_movies_container awarded_movies:latest
```

The instruction starts up the container with the specified name and immediately executes the main script. After execution, the container exits
automatically.

_**Note:** In order to start the container another time after exiting, the `start` command is required instead of `run`:_

```shell
docker start -a awarded_movies_container
```

_(The `-a` flag, a shorthand for `--attach`, is required to start the container in the foreground, just like when running it with `docker run`.)_

#### Option B: Interactively Running the Container and Executing the Script Oneself

For the curious-minded people who prefer doing most of the work themselves, there is of course the possibility to interactively start the container
with shell-access to it:

```shell
docker run --name awarded_movies_container -it awarded_movies /bin/bash
```

_(The `-it` flags, a shorthand for `--interactive --tty`, allocate an interactive terminal session into the container, with `bash` as the shell)_

After starting the terminal session, the experiment can be run by invoking it using Python:

```shell
python ./src/main.py
```

_(If you prefer absolute paths, you may also call `python /home/src/main.py`.)_

Finally, you can exit the container with `CTRL+D` or `exit`.

_**Note:** In order to start the container another time after exiting, the `start` command is required instead of `run`:_

```shell
docker start -i awarded_movies_container
```

_(The `-i` flag, a shorthand for `--interactive`, is required to start the container interactively, with the terminal allocated when running it
with `docker run -it`.)_

#### Retrieve Result Directory From Container

In order to copy the results from the exited container to the host, run the following command (don't forget the dot `.` at the end):

```shell
docker cp awarded_movies_container:/home/result .
```

This command copies the whole directory tree `/usr/src/app/result` into the current working directory (the experiment root), overwriting files that
already exist in `./result` with the same filename.

#### Delete the Container (Optional)

In order to keep the system clean and tidy, one might not want to keep containers that are not actively used anymore. This can be achieved with the
following command:

```shell
docker container rm awarded_movies_container
```

#### Delete the Image (Optional)

Similar to the deletion of the container, it could be preferable to remove the image from which the container was created. The following instruction
accomplishes this:

```shell
docker image rm awarded_movies:latest
```

_**Note:** In order to safely delete the image, you should first remove the container._

### Example Log Output

If the directory structure is correct and installing the required dependencies (or building and starting the Docker container) went well, then the
output of a successful execution of the script looks something like this (this output is taken from an execution via Docker):

```shell
Ensuring result directory "/home/result" exists...Done.
Filtered 31 oscar information entries from "/home/data/the_oscar_award.csv".
Read 6820 movie information entries from "/home/data/movies.csv".
Matched 31 movies with awards.
Wrote result of data processing to file "/home/result/awarded_movies.csv".
Saved plot of processed data to file "/home/result/awarded_movies_visualization.png".
```