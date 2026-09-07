# SCITAS Guide

SCITAS provides EPFL computing resources for work that is too large, too slow, or simply more convenient to run on a shared computing cluster. The main difference from using your own computer is that you do not start a long computation directly after connecting. You first connect to a **login node**, prepare your files, and then ask **Slurm** to run the computation on one or more **compute nodes**.

This separation is the central idea behind using SCITAS. The login node is the place from which you organize and submit work. Slurm is the process, named **scheduler**, that decides when and where that work runs. Note that, because the cluster is shared, a submitted job may wait in a queue before resources become available.

For this course, the usual resources are:

- **Jed** for CPU computations. Student jobs run through the `academic` partition.
- **Izar** for GPU computations and courses that require GPUs.

Kuma is the research GPU cluster and is not available to student or course accounts.

> This guide deliberately covers only the workflow needed for typical course analyses. The [full SCITAS documentation](https://scitas-doc.epfl.ch/) remains the reference for advanced usage.

## Connecting to SCITAS

Before connecting, you need a valid GASPAR account and access to SCITAS for the course. Access should normally have been granted before the first class. If your SCITAS access does not work, contact [fabrice.nemo@epfl.ch](mailto:fabrice.nemo@epfl.ch). Your computer must also be on the EPFL network, or connected to the [EPFL VPN](https://www.epfl.ch/campus/services/en/it-services/network-services/remote-intranet-access/).

On macOS and Linux, SSH is already available from a terminal. For Windows users, SCITAS recommends Git Bash or Windows Subsystem for Linux (WSL). Open a terminal and connect with:

```bash
ssh username@cluster.hpc.epfl.ch
```

Replace `username` with your GASPAR username and `cluster` with the cluster you want. For example:

```bash
ssh alice@jed.hpc.epfl.ch
```

or

```bash
ssh bob@izar.hpc.epfl.ch
```

The first login may ask you to confirm the identity of the remote host, do confirm it. Once logged in, your terminal is running commands on a SCITAS login node rather than on your laptop. See the [SCITAS connection documentation](https://scitas-doc.epfl.ch/user-guide/using-clusters/connecting-to-the-clusters/) if you need more details.

A few shell commands are enough for most sessions:

```bash
pwd                              # show the current directory
ls                               # list files
cd path/to/folder                # move to another directory
mkdir new_folder                 # create a directory
nohup command > output.log 2>&1 & # keep a non-compute command running after logout
```

`nohup` is useful when a non-compute command should continue after an SSH session disconnects. Long computations should still be submitted through Slurm.

Use the login node to inspect files, edit small scripts, organize your project, and submit jobs. Computation itself should be sent through Slurm rather than run as a long process on the login node.

## From a command to a Slurm job

On your own computer, running an analysis may be as simple as typing a command such as `python analysis.py`. On SCITAS, the same command is normally placed inside a small **job script**. The script tells Slurm both what to run and how many resources the calculation needs.

For a simple CPU job on Jed, a minimal script can look like this:

```bash
#!/bin/bash -l

#SBATCH --job-name=homework
#SBATCH --partition=academic
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:30:00
#SBATCH --mem=4G

source .venv/bin/activate
python analysis.py
```

Save it as, for example, `job.sh`. The final two lines are only an example. Adjust the virtual-environment path if needed, and replace the Python command with the command required for your homework.

The `#SBATCH` lines describe the resources reserved for the job. `--nodes` sets the number of compute nodes, `--ntasks` the number of processes, `--cpus-per-task` the CPU cores available to each process, `--time` the maximum wall time, and `--mem` the requested memory. Here, the job uses one node, one task, one CPU core, at most 30 minutes of computation time, and 4 GB of memory. These values should be realistic. Requesting much more time or memory than necessary can make a job harder to schedule and may increase the time spent waiting in the queue. See the [SCITAS Slurm documentation](https://scitas-doc.epfl.ch/user-guide/using-clusters/running-jobs/) for more options.

The `academic` partition is required for student CPU jobs on Jed. Its current limits allow up to 7 days and 8 nodes per job. On Izar, request GPUs with, for example, #SBATCH --gres=gpu:1. One GPU is normally sufficient for course work. Most Izar compute nodes have 2 GPUs; the gpu-xl nodes have 4 GPUs each. Standard Izar jobs can run for up to 3 days and use up to 8 nodes, while the long QoS allows up to 7 days. See the [SCITAS QoS and partition documentation](https://scitas-doc.epfl.ch/user-guide/using-clusters/slurm-qos-partitions/) for the current limits.

Use GPU resources sparingly. Prefer Jed for development, preprocessing, testing, and any work that does not require a GPU. Use Izar when the computation actually benefits from GPU acceleration.

## Submitting and following a job

Once the script is ready, submit it from the directory containing the files needed by the analysis:

```bash
sbatch job.sh
```

Slurm replies with a job identifier:

```text
Submitted batch job 1234567
```

It identifies the job while it is queued or running. Check the job shortly after submission, since many configuration or runtime errors appear as soon as the job starts.

To see your jobs, use:

```bash
squeue
```

You can also inspect a specific job with:

```bash
squeue -j 1234567
```

A job marked `PD` is pending and waiting for resources. A job marked `R` is running. Waiting after submission is expected on a shared cluster. If you submitted the wrong script or no longer need a job, cancel it with:

```bash
scancel 1234567
```

Unless you configure another output file or working directory, Slurm normally writes the program output in the directory from which you ran `sbatch`, using a file named after the job ID, for example:

```text
slurm-1234567.out
```

You can inspect it with commands such as:

```bash
less slurm-1234567.out
```

or

```bash
cat slurm-1234567.out
```

When a job does not behave as expected, this output file is usually the first place to look. It is often useful to check in the first minute after the job submission, to verify that everything is running smoothly and not waste computation time. 

## Managing project files and transferring data

For source code and scripts, use Git when possible. Make changes either on your own computer or from the SSH terminal, then use commits and `push` or `pull` as needed to keep the project synchronized. This gives you a clear history of changes and avoids using file-transfer commands as the main way to manage source code. You can also directly connect to the cluster using VSCode and the SSH extension (see the [SCITAS VSCode documentation](https://scitas-doc.epfl.ch/advanced-guide/using-vscode/) for more info.).

For public datasets, prefer keeping a script in Git that downloads and preprocesses the data. Run this script wherever the dataset is needed, so that the data can be rebuilt from its public sources and reproduced by others. For results or other files that do not belong in Git, transfer them directly between your computer and the cluster over SSH. `rsync` is useful because it can resume interrupted transfers and avoids copying unchanged data again. See the [SCITAS data-transfer documentation](https://scitas-doc.epfl.ch/user-guide/data-management/transferring-data/) for more options.

Run transfer commands from **your own computer**, not from the SCITAS login node. To send a project folder to Jed:

```bash
rsync -azP ./project/ <username>@jed.hpc.epfl.ch:/home/<username>/project/
```

To retrieve results from SCITAS:

```bash
rsync -azP <username>@jed.hpc.epfl.ch:/scratch/<username>/project/results/ ./results/
```

Replace `jed` with the cluster used by the course when necessary. As with SSH, direct transfers require access to the EPFL network or VPN.

For a simple copy, `scp` is also available:

```bash
scp file.txt <username>@jed.hpc.epfl.ch:/home/<username>/
```

Use `scp -r` when copying a directory. A graphical file-transfer application such as FileZilla or WinSCP can also be used when appropriate.

## Choosing where data should be stored

The cluster exposes several file systems, but most course work only needs two of them. See the [SCITAS file-system documentation](https://scitas-doc.epfl.ch/user-guide/data-management/how-to-use-filesystems/) for the full details.

Your **home directory**, `/home/<username>`, is the safe place for source code, scripts, small input files, and material that should persist. It has a default quota of 100 GB and is backed up.

Your **scratch directory**, `/scratch/<username>`, is designed for data that a running computation reads and writes intensively. You can refer to it through the environment variable `$SCRATCH`. Scratch is faster for this type of work, but it is temporary storage. It is not backed up, files older than 30 days are automatically removed, and additional cleanup may occur when the file system becomes too full.

There is one more detail that matters when moving between clusters: scratch storage is **cluster-specific**. A file placed in scratch on Jed is not automatically available in scratch on Izar. Course access is temporary and is revoked when the course period ends, so download the final work you want to keep before your access ends.

A practical default is therefore to keep the durable copy of your project in home, use scratch for larger temporary inputs and outputs while the job runs, then move the results you want to keep back to home or to your own computer.

For example, you can prepare a scratch directory with:

```bash
mkdir -p $SCRATCH/homework1
```

and copy a project into it with:

```bash
rsync -a ~/homework1/ $SCRATCH/homework1/
```

From there, move into the directory and submit the job as usual:

```bash
cd $SCRATCH/homework1
sbatch job.sh
```

Once the computation is complete, copy important results out of scratch rather than leaving the only copy there.

## Minimal command reference

| Goal | Command |
|---|---|
| Connect to Jed | `ssh username@jed.hpc.epfl.ch` |
| Connect to Izar | `ssh username@izar.hpc.epfl.ch` |
| Show current directory | `pwd` |
| List files | `ls` |
| Go to a directory | `cd <directory>` |
| Keep a non-compute command running after logout | `nohup command > output.log 2>&1 &` |
| Submit a job | `sbatch job.sh` |
| See your jobs | `squeue` |
| Inspect one job | `squeue -j <jobid>` |
| Cancel a job | `scancel <jobid>` |
| Go to temporary compute storage | `cd $SCRATCH` |
| Copy local files to SCITAS | `rsync -azP <local> <username>@<cluster>.hpc.epfl.ch:<remote>` |
| Copy SCITAS files to your computer | `rsync -azP <username>@<cluster>.hpc.epfl.ch:<remote> <local>` |
