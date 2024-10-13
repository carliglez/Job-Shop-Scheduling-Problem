# Solves JSSP instances following the Shortest Processing Time (SPT) rule

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

def spt_dispatching_rule(jobs, machines):
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
        processing_time = job.processing_times[machine_index]
        current_machine = machines[machine_index]

        # Find the next available time for the current operation
        start_time = max(current_machine.current_time, current_machine.end_times.get(job.id, 0))

        # Check for overlaps with the same job on other machines
        overlaps = any(
          start_time < other_machine.end_times.get(job.id, 0)
          for other_machine in machines
          if other_machine != current_machine
        )

        # If there is an overlap, adjust the start time to the end time of the other machines
        if overlaps:
          start_time = max(other_machine.end_times.get(job.id, 0) for other_machine in machines)

        # Update the end time for the current job on the current machine
        current_machine.end_times[job.id] = start_time + processing_time

        end_time = start_time + processing_time
        current_machine.current_time = end_time
        schedule.append([start_time, end_time, job.id, machine_index + 1])

        job.processing_times[machine_index] = float('inf')
        job.sequence.pop(0)

  return schedule

# Main program
if __name__ == "__main__":
  file_path = 'resources/la01.txt'  # Path to your input file
  num_jobs, num_machines, optimal_makespan, jobs_data, sequences_data = read_input_file(file_path)

  jobs = [Job(i + 1, jobs_data[i], sequences_data[i]) for i in range(num_jobs)]
  machines = [Machine() for _ in range(num_machines)]

  schedule = spt_dispatching_rule(jobs, machines)

  # Calculate makespan
  makespan = max(entry[1] for entry in schedule)
  
  print("Optimal Makespan:", optimal_makespan)
  print("Resulting Makespan:", makespan)
  print("Schedule:")
  for entry in schedule:
    print(entry)
