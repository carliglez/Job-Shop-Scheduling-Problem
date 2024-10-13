# Job-Shop Scheduling Problem (JSSP) Solver

This Python project addresses the **Job-Shop Scheduling Problem (JSSP)**, a complex optimization challenge widely recognized in production and manufacturing environments. The JSSP involves scheduling a set of jobs across multiple machines, where each job comprises various operations that must be performed in a specific sequence. Each operation has a fixed duration and must monopolize a particular machine during its processing time.

The primary goal of the JSSP is to **minimize the makespan**, which represents the total time required to complete all jobs. This project explores various formulations and methodologies to tackle the JSSP, aiming to optimize scheduling and resource allocation.

## Organization of the Data in the Input Files

The input files for the JSSP solver follow a specific structure:

1. **Number of Jobs and Machines**:
   - The first line contains an integer representing the number of jobs.
   - The second line contains an integer representing the number of machines.

2. **Optimal Makespan (Optional)**:
   - The third line may contain an integer representing the optimal makespan, if available.

3. **Job Processing Times**:
   - The next `num_jobs` lines provide the processing times for each job, with each line containing `num_machines` integers, representing the time each job takes on each machine.

4. **Job Sequences**:
   - The following `num_jobs` lines represent the sequence in which each job must be processed on the machines. Each line contains `num_machines` integers indicating the order of the machines for each job.

## Implemented Methods

### Shortest Processing Time (SPT)

The **Shortest Processing Time (SPT)** rule prioritizes jobs with the shortest remaining processing time on their next machine. Although the optimal makespan could not be achieved for all test instances, approximations were made for some cases, such as the `la05` and `mt06` input files. It's important to note that some input instances lack an optimal makespan value for comparison.

The code includes a version of the SPT that provides a **Gantt chart** to visually represent the resulting job schedules. This Gantt chart allows users to easily visualize how jobs are distributed across machines, providing a clear representation of the results.

### Shifting Bottleneck Heuristic

The **Shifting Bottleneck Heuristic** is also implemented as a simplified version of the approach described on [Wikipedia](https://en.wikipedia.org/wiki/Shifting_bottleneck_heuristic). A **Gantt chart** is included to visually represent the scheduling results for clarity.

Below is a detailed breakdown of how the code corresponds to the steps of the heuristic:

1. **Make graph**:
   The graph creation is not explicitly implemented in the code. Instead, the focus is on updating the schedule dynamically based on the heuristic.
    
2. **Determine starting makespan**:
   The initial makespan is calculated dynamically as the algorithm progresses, and it is updated with each iteration.
    
3. **Determine optimal sequence for the bottleneck machine**:
   The code identifies the bottleneck machine by finding the machine with the minimum completion time. Jobs are then scheduled on that machine based on the predefined job sequences.

4. **Perform an iteration**:
   The iteration schedules jobs on the bottleneck machine based on the optimal sequence, and this process is repeated until all jobs are assigned.

5. **Solve lowest maximum lateness problem**:
   The focus of the implementation is on minimizing the **makespan** rather than the maximum lateness, as the Shifting Bottleneck Heuristic aims to minimize job completion times.

6. **Include optimal sequence in the graph**:
   Although no explicit graph is created, the schedule is dynamically updated with the optimal sequence for each job on the bottleneck machine.

7. **Determine optimal sequences for remaining machines**:
   The order of execution is respected for each job, ensuring the correct scheduling of operations on every machine in sequence.

8. **Perform further iterations**:
   Iterations continue, dynamically updating the job schedules and makespan until all jobs are scheduled.

9. **Conduct iterations until all machines are accounted for**:
   The algorithm iterates until all jobs are scheduled on all machines.

10. **Draw out the final graph**:
    The code includes a **Gantt chart** that visually represents the final schedule of jobs across different machines, as in the SPT version.

11. **Determine final makespan**:
    The final makespan is updated dynamically throughout the process and is printed at the end of the execution.

Although the code does not explicitly follow every step described in Wikipedia, it captures the essence of the **Shifting Bottleneck Heuristic** by iteratively scheduling jobs on bottleneck machines and adjusting the schedule to minimize the overall makespan.

## Conclusion

This project provides various heuristics and approaches to solve the Job-Shop Scheduling Problem using Python. While optimal solutions were not obtained for all instances, significant approximations were made using SPT and the Shifting Bottleneck Heuristic, providing valuable insights into the complexities of the problem.

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
