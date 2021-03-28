## Example Execution

If the directory structure is correct and all required dependencies are installed, the output of a successful execution of the script looks something
like this:

```shell
Ensuring result directory "/home/result" exists...Done.
Filtered 31 oscar information entries from "/home/data/the_oscar_award.csv".
Read 6820 movie information entries from "/home/data/movies.csv".
Matched 31 movies with awards.
Wrote result of data processing to file "/home/result/awarded_movies.csv".
Saved plot of processed data to file "/home/result/awarded_movies_visualization.png".
```

## Running with Docker

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

### Option A: Execute Container With Provided Defaults (Recommended)

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

### Option B: Interactively Run Container and Execute Script Oneself

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

### Retrieve Result Directory From Container

In order to copy the results from the exited container to the host, run the following command (don't forget the dot `.` at the end):

```shell
docker cp awarded_movies_container:/home/result .
```

This command copies the whole directory tree `/usr/src/app/result` into the current working directory (the experiment root), overwriting files that
already exist in `./result` with the same filename.

### Delete the Container (optional)

In order to keep the system clean and tidy, one might not want to keep containers that are not actively used anymore. This can be achieved with the
following command:

```shell
docker container rm awarded_movies_container
```

### Delete the Image (optional)

Similar to the deletion of the container, it could be preferable to remove the image from which the container was created. The following instruction
accomplishes this:

```shell
docker image rm awarded_movies:latest
```

_**Note:** In order to safely delete the image, you should first remove the container._