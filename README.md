# Web Server
This is Team 2's web server repository.

## Installation
We require that you use miniconda. This loads in the basic software and tools we
will be using in our pipeline. To use our environment, type in
```console
user@biosci:Team2-WebServer$ export PATH=$PATH:/home/projects/team-b/miniconda3/condabin
```
If this is your first time using conda, type in
```console
user@biosci:Team2-WebServer$ conda init bash
```

Then type in
```console
user@biosci:Team2-WebServer$ conda activate team-2-conda
```

## Execution
We will be calling a file called *backbone.py* in each directory of the 4
other steps of the pipeline. This ensures that a single file is running all of the
code within a single pipeline step and centralizing the outputs. TODO: can we access
these scripts if they are in different directories?

When a job is launched, each pipeline step's page will be created and will display
a standby message. These pages will be filled with results as soon as they are 
available.

At the start, we will be checking if certain *tools* or *inputs* are present before
the scripts are run.

## Frameworks & Packages Used
- Django
- Celery (TODO: look for alternatives (celery not too good with
  errors or nonrepetitive tasks)? async.io, etc.)
- SQLite

## Data Usage
TODO: how will it be organized? how will we maintain it? how do we use SQLite? 
