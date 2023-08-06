# LEMMINGS

## Introducing Lemmings

Lemmings (lemmings-hpc) is an open-source code designed to simplify job scheduling on HPC clusters. It achieves this goal by offering the user a set of functionalities that does not require a priori knowledge on how to interact with a job sheduler. The emphasize can then be  placed on the workflow management. Portability of these workflows between different machines and machine environments will be ensured through lemmings.


**Two aspects** have to be clearly **distinguished** within lemmings:

- The interaction with the job sheduler 
  - this part is taken care of **by lemmings**
  - requires basic information from the user about the environment (see *Machine* section below)
- The workflow
  - this part is taken care of **by the user**: lemmings needs to know what to do
  - lemmings offers a framework in which this **has to be** **defined** (see *Workflow* section below)



The usage of lemmings can be extremely versatile with some examples

- chained runs
- chained runs with intermediate mesh refinements
- chained runs with changes of settings based on intermediate (postprocessed) solutions
- chained runs with conditional evolution
- ...

While originally developed within the context of Computational Fluid Dynamics (CFD) applications, in its construction, lemmings is not limited to this.


***To avoid infinite loops lemmings requires the user to specify a maximum allowed CPU hours to be consumed.***


**Note: The use of lemmings can best be understood in conjunction with the provided examples in the `/example/` directory on the associated repository `https://gitlab.com/cerfacs/lemmings`. Note as well that individual workflows might require additional python and / or non-python packages to be installed.**


## Install Lemmings

Lemmings is open-source and can be pip-installed :

```bash
pip install lemmings-hpc
```

We highly recommend to consider using a virtual environment.

In case you whish to install lemmings and its dependencies through wheels just follow the procedure under the section [How can I install something on an machine without internet?](https://cerfacs.fr/coop/python-faq).

## Machine
Lemmings requires basic information of the environment (job sheduler) it's being used in. This is specified in the form of a `{machine}.yml` file which we will simply call `machine.yml`.  After its definition, for lemmings to access this information an environment variable  `LEMMINGS_MACHINE`  must be defined and can be done with the following command:

```bash
export LEMMINGS_MACHINE='absolute_path_to_your_machine.yml'
```

Once defined, **the machine.yml file can be changed at any moment**. The only thing that has to be fixed at least once is the above environment variable.  The `machine.yml` file can be edited, for instance, as follow:

```bash
 vim $LEMMINGS_MACHINE
```

Examples of `machine.yml`  files can be found in `lemmings/src/lemmings/chain/machine_template/` which could already be suitable for your environment.  If it's not the case, no worries, you can easily create your own. **It is adviced to locate your machine.yml file somewhere outside of lemmings.**

### Create your Machine configuration {machine}.yml

A `machine.yml ` file, as shown below, contains two main groups 

```yaml
commands:
  submit: sbatch
  cancel: scancel
  get_cpu_time: sacct -j -LEMMING-JOBID- --format=Elapsed -n
  dependency: "--dependency=afterany:"
queues:
  debug:      #--> user defined name
    wall_time: '00:20:00'
    core_nb: 24    # core_nb = nodes*ntaks-per-node !!!
    header: |
            #!/bin/bash
            #SBATCH --partition debug
            #SBATCH --nodes=1
            #SBATCH --ntasks-per-node=24
            #SBATCH --job-name -LEMMING-JOB_NAME-
            #SBATCH --time=-LEMMING-WALL-TIME-
  
            -EXEC-
  debug_pj:   #--> user defined name
    wall_time: '00:02:00'
    header: |
           	#!/bin/bash
            #SBATCH --partition debug
            #SBATCH --nodes=1
            #SBATCH --ntasks-per-node=24
            #SBATCH --job-name -LEMMING-POSTJOB_NAME-
            #SBATCH --time=-LEMMING-WALL-TIME-

            -EXEC_PJ-
```
- commands: 

  - groups a basic set of commands to interact with the job sheduler 

- queues:

  - groups information on the queues that the user whished to use **and** exist on the cluster

  - The **wall_time** parameter is the wall clock time limit of the machine queue. It could be in **HH:MM:SS** format or a **Float** in seconds. 

  - The **core\_nb** parameter represents the number of cores to be used. Be careful, sometimes in the batch you use directly **core_nb**, sometimes you have to use "node number" * "ntasks-per-node". In any case, the core number will **ONLY** be taken via the  **core_nb** parameter and **NEVER** in the BATCH parameters.

  - The `machine.yml` requires at least two queues : `job` and `pjob`. This is simply a consequence of the working strategy of lemmings.  A `job`  queue is indicated by the  `-EXEC-` keyword at the end of the header whereas `-EXEC_PJ-`  indicates a  `pjob` queue. These two strings will be replaced by the associated executable information specified in the `workflow.yml` file as exemplified below. 

    ```yaml
    # associated with -EXEC-
    exec: |
          source "path/to/virtualenv/bin/activate"
          module load avbp
          mpirun -np $SLURM_NPROCS path/to/exec
    # associated with -EXEC_PJ-
    exec_pj: |
          source "path/to/virtualenv/bin/activate"
    ```

The user can define as many queues as wished (with the required information), e.g. a queue called *prod_long* which has a wall_time of 24h, a *prod_short* with wall_time of 5h, etc., as longs as the value does not exceed the maximum limit set by the machine on the specific partition. Moreover, multiple queues can be associated with the same partition.  *The `machine.yml` should  be seen as a list of options, or better, option pairs given the job / pjob link, from which the user can select in the workflow definition.*



## Workflow

***Lemmings is the base that permits the execution of workflows but all the mecanisms of lemmings are independant of the workflow used.  Indeed, workflows are customizable whereas lemmings is not.***

The workflow is what the user would like to achieve through lemmings, be it a simple chained run, a chained run with mesh refinement or whatever floats your boat.  Nevertheless, the workflow has to **follow the lemmings rules.**

A Workflow configures the scheme your run will follow, from a simple recursivity, to a mesh adaptation, a postprocessing operation, or customized operations. A Workflow is set up by two files :

- `{workflow_name}.py` : Python script of the scheme.
- `{workflow_name}.yml` : Yaml registering specific properties of your run' Workflow. **This file must be located in your RUN directory.**


<!-- You can find available Workflows defined in python scripts  in `lemmings/src/lemmings/chain/workflows` along with yaml examples or in the ` example/barbatruc` folder.  If the Workflow you need is not available, it can be defined as described further below. -->


In a similar way to the  Machine setup, an environment variable, `LEMMINGS_WORKFLOW` , can be defined to locate existing Workflows:

```bash
export LEMMINGS_WORKFLOW=/absolute_path_to_workflows_folder/
```
<!-- The following command shows the different Workflows available in the `LEMMINGS_WORKFLOW ` associated folder :

```bash
lemmings info workflows
```
You can display informations on a specific Workflow stored in the  `LEMMINGS_WORKFLOW ` folder :

```bash
lemmings info {workflow_name}
​``` -->

Note: 
- unlike the definition of a Machine environment variable, the workflow related environment variable is not a requirement, in which case the `{workflow_name}.py`  file should be located in the run folder. It is however adviced to centralise workflows instead of  resorting to endless copy - pasting when running from different folders. 
- be careful in the naming: if a workflow has the same `{workflow_name}.py`  name in both the local directory and in the  `$LEMMINS_WORKFLOW` location , the local workflow will be prioritized.


### Create your Workflow 

**NOTE: the workflow configuration file (.yml) and  script (.py) MUST have the same prefix!!!**

#### The configuration {workflow_name}.yml

Every workflow requires a configuration file. This file will be completed by the end user of lemmings. The number of parameters/informations required is workflow dependent, so make sure you know them or contact your 'garant'. 

<!-- You can create a default configuration file (*if the workflow permits it*) using the command: 

​```bash
lemmings init {workflow_name}
​``` -->

There are 5 mandatory parameters that have to be present in each configuration file:

- **exec** : Here, write what you want to put in your Batch file instead of the "-EXEC-" string  from the {machine}.yml. 
<!-- You can use the `lemmings info machine` command to understand the construction of the Batch file. -->

- **exec_pj**: the same as `exec` but for the post-job queue. You may just need to source your virtual environment to execute lemmings post-job

- **job\_queue/pjob\_queue**: The name of the queue you want to use for the Job/Post-job of lemmings. Queues are presented in the configuration file. 
<!-- You can use the `lemmings info machine` command to see it. -->
- **cpu_limit** : The maximum CPU [hours] that the lemmings chain can use.

The next one is not mandatory but can be used by lemmings:

- **job_prefix**: Lemmings auto generates a chain name and directory with the template : CVCVNN (e.g. JAZE53). If this parameter is present, a prefix will be added before the auto generated chain name (e.g. myprefix_JAZE53). **The logfile (.log) associated with your run will be located in here upon completion.**

<!-- - **percentage_of\_tgt**: Percentage of the target dtsum that is acceptable to stop lemmings. For exemple, if "simulation\_end\_time"=0.10s and the "percentage\_of\_tgt"=10 [%], if at the end of the loop the "dtsum"= 0.09 lemmings stops and considers the condition\_tgt to be reached. **This parameter was added to avoid a complete run to be restarted if we're very close to our final target time in which case continuing a run might end up with a large waste of computational resources.** 

- **solution\_writing_time**: Time to substract from the queue wall time. It corresponds to the desired writing time. For example, if your *wall\_clock\_time* is 12:00:00 and *solution_writing\_time*=00:30:00, simulation will stop at 11:30:00. If this key is not present, **by default the *solution_writing_time* is 00:15:00.**  -->

#### The script  {workflow_name}.py

The workflow is defined through a class called *LemmingJob* and sets the framework that must be followed by the user.  The structure is represented below.

                 Prior to job  +---------+             Prepare run
                     +--------->SPAWN JOB+---------------------+
                     |         +------^--+                     |
                     |                |                      +-v------+
                   True               |                      |POST JOB|
    +-----+          |                |                      +--------+
    |START+--->Check on start         |                          v
    +-----+          |                +---------------False-Check on end
                   False            Prior to new iteration       +
                     |                                         True
                     |                                           |
                     |                                           |
                     |           +----+                          |
                     +---------->|EXIT|<-------------------------+
               Abort on start    +----+                After end job

For an actual example of a `workflow.py` definition, please refer to the `example/barbatruc`  directory. The docs do also provide the user with further information on its definition and strict structure. 


## Launch lemmings

In your RUN directory, you **need**   the {workflow_name}.yml file.  When it is correctly filled, launch Lemmings from your RUN directory  with: 

```
lemmings run {workflow_name}
```
You can cancel a Lemmings run if necessary, from within the directory lemmings was launched with:

```
lemmings kill
```



## Lemmings commands

A list of useful commands are given below. 

| Command                       | Description                                                                                          |
|-------------------------------|------------------------------------------------------------------------------------------------------|
| lemmings-hpc --help               | Show all the commands                                                                                |
| lemmings-hpc clean                | Clean lemmings generated run files in current folder
| lemmings-hpc run --help           | Show the help for the 'run' command                                                                  |
| lemmings-hpc run {workflow_name}  | Launch the workflow in the current directory                                                         |
| lemmings-hpc status               | Show the status of the last lemmings chain                                                        |
| lemmings-hpc kill                 | Kill the current job and pjob of lemmings. You must be located in the  directory from where lemmings was launched.                                                                |
| lemmings-hpc safestop             | Finish properly the current loop of the lemmings chain and then stop.                               |

<!-- | lemmings info machine         | Show the machine configuration                                                                       |
| lemmings info workflows       | Show all the available workflows                                                                     |
| lemmings info {workflow_name} | Show the doctoring of the workflow                                                                   | -->
<!-- | lemmings init {workflow_name} | Create a default {workflow}.yml in the current directory<br>(only if the template exist in lemmings) | -->


## Extras
Additional information on lemmings can be found on the [COOP blog](https://cerfacs.fr/coop/). Type in the keyword "lemmings" in the search bar to get a list of different posts that could be helpful to you.

## Acknowledgement

Lemmings is a service created in the [EXCELLERAT Center Of Excellence](https://www.excellerat.eu/wp/) and is continued as part of the [COEC Center Of Excellence](https://coec-project.eu/). Both projects are funded by the European community. 
<!-- Its existence is the result of many discussions and interactions within the COOP group at Cerfacs. -->

![logo](https://www.excellerat.eu/wp-content/uploads/2020/04/excellerat_logo.png)

![logo](https://www.hpccoe.eu/wp-content/uploads/2020/10/cnmlcLiO_400x400-e1604915314500-300x187.jpg)
