# Solves JSSP instances following an implementation of the Shifting Bottleneck Heuristic. Includes a Gantt chart

import matplotlib.pyplot as plt

# Job class to save the information related to each Job processed
class Job:
  def __init__(self, id, processing_times, sequence):
    self.id = id
    self.processing_times = processing_times
    self.sequence = sequence

# Machine class to save information related to each Machine processed
class Machine:
  def __init__(self):
    self.current_time = 0
    self.end_times = {}  # Dictionary to store end times for each job

# Method to read input files
def read_input_file(file_path):
  with open(file_path, 'r') as file:
    # Read the first two lines
    num_jobs = int(file.readline().strip())
    num_machines = int(file.readline().strip())

    # Read the third line
    third_line = file.readline().strip()

    # Check if the third line is a simple integer (optimal makespan)
    optimal_makespan = int(third_line) if third_line.isdigit() else None

    # If the third line is not an integer, treat it as the first line of job processing times
    if optimal_makespan is None:
      processing_times = [list(map(int, third_line.split()))]
    else:
      processing_times = []

    # Read the remaining job processing times
    processing_times.extend([list(map(int, file.readline().split())) for _ in range(num_jobs - len(processing_times))])

    # Read job sequences
    job_sequences = [list(map(int, file.readline().split())) for _ in range(num_jobs)]

  return num_jobs, num_machines, optimal_makespan, processing_times, job_sequences

# Method to determine optimal sequence for the bottleneck machine
def shifting_bottleneck_heuristic(jobs, machines):
  schedule = []

  # Initialize current_time and end_times for each machine
  for machine in machines:
    machine.current_time = 0
    machine.end_times = {}

  # Continue looping as long as there is at least one job with pending operations (i.e., while there is a job whose sequence is not empty)
  while any(any(job.sequence) for job in jobs):
    for job in jobs:
      if job.sequence:
        machine_index = job.sequence[0] - 1
        current_machine = machines[machine_index]

        # Find the next available time for the current operation
        min_completion_time = min(machines[machine_index].end_times.get(job.id, 0) for job in jobs if job.sequence)
        eligible_jobs = [job for job in jobs if job.sequence and current_machine.end_times.get(job.id, 0) == min_completion_time]

        # Sort eligible jobs based on the job sequence
        eligible_jobs.sort(key=lambda x: x.sequence.index(machine_index + 1) if machine_index + 1 in x.sequence else float('inf'))

        selected_job = eligible_jobs[0]

        # Schedule the selected job on the current machine
        start_time = max(current_machine.current_time, current_machine.end_times.get(selected_job.id, 0))

        # Check for overlaps with the same job on other machines
        overlaps = any(
          start_time < other_machine.end_times.get(selected_job.id, 0)
          for other_machine in machines
          if other_machine != current_machine
        )

        # If there is an overlap, adjust the start time to the end time of the other machines
        if overlaps:
          start_time = max(other_machine.end_times.get(selected_job.id, 0) for other_machine in machines)

        processing_time = selected_job.processing_times[machine_index]
        end_time = start_time + processing_time

        current_machine.end_times[selected_job.id] = end_time
        current_machine.current_time = end_time

        schedule.append([start_time, end_time, selected_job.id, machine_index + 1])

        selected_job.processing_times[machine_index] = float('inf')
        selected_job.sequence.pop(0)

  return schedule

# Method to generate the Gantt Chart
def plot_gantt_chart(schedule, num_machines, makespan):
    # Define a list of colors for the jobs
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

    # Ensure that there are enough colors for the jobs
    while len(colors) < max(entry[2] for entry in schedule):
        colors.extend(colors)

    legend_labels = {}

    for machine_index in range(num_machines):
        machine_schedule = [item for item in schedule if item[3] == machine_index + 1]
        for entry in machine_schedule:
            start_time, end_time, job_id, _ = entry

            if job_id not in legend_labels:
                # Use colors cyclically if there are more jobs than colors
                legend_labels[job_id] = colors[(job_id - 1) % len(colors)]

            plt.barh(machine_index, end_time - start_time, left=start_time, color=legend_labels[job_id], edgecolor='black')

    plt.yticks(range(num_machines), [f'Machine {i+1}' for i in range(num_machines)])
    plt.xlabel('Time')
    plt.title('Gantt Chart - Shifting Bottleneck Heuristic')

    # Add legend outside the plot
    sorted_legend = sorted(legend_labels.keys())
    plt.legend([plt.Rectangle((0, 0), 1, 1, fc=legend_labels[label], edgecolor='black') for label in sorted_legend],
               [f'Job {label}' for label in sorted_legend], loc='center left', bbox_to_anchor=(1, 0.5))

    # Highlight makespan with a vertical line
    plt.axvline(x=makespan, color='r', linestyle='--', linewidth=2, label=f'Makespan: {makespan}')

    # Set a larger figure size
    plt.gcf().set_size_inches(12, 6)

    plt.show()

# Main program
if __name__ == "__main__":
    file_path = 'resources/la01.txt'  # Path to your input file
    num_jobs, num_machines, optimal_makespan, jobs_data, sequences_data = read_input_file(file_path)

    jobs = [Job(i + 1, jobs_data[i], sequences_data[i]) for i in range(num_jobs)]
    machines = [Machine() for _ in range(num_machines)]

    schedule = shifting_bottleneck_heuristic(jobs, machines)

    # Calculate makespan
    makespan = max(entry[1] for entry in schedule)

    print("Optimal Makespan:", optimal_makespan)
    print("Resulting Makespan:", makespan)
    print("Schedule:")
    for entry in schedule:
      print(entry)

    plot_gantt_chart(schedule, num_machines, makespan)
