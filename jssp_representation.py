# Representation of the data in the input files

# Job class to save the information related to each Job processed
class Job:
  def __init__(self, processing_times, sequence):
    self.processing_times = processing_times
    self.sequence = sequence

  def __str__(self):
    return f"Processing Times: {self.processing_times}\nSequence: {self.sequence}"

  def get_output_format(self):
    return [
      f"(Machine {machine}, Processing Time {self.processing_times[machine - 1]})"
      for machine in self.sequence
    ]

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

# Method to create Job objects
def create_job_objects(num_jobs, processing_times, job_sequences):
  jobs = []
  for i in range(num_jobs):
    job = Job(processing_times[i], job_sequences[i])
    jobs.append(job)
  return jobs

# Print method
def print_output(jobs):
  for i, job in enumerate(jobs, start=1):
    print(f"Job {i}: {' '.join(job.get_output_format())}")

# Main program
if __name__ == "__main__":
  file_path = "resources/la01.txt"  # Path to your input file
  num_jobs, num_machines, optimal_makespan, processing_times, job_sequences = read_input_file(file_path)

  jobs = create_job_objects(num_jobs, processing_times, job_sequences)

  print(f"Number of Jobs: {num_jobs}")
  print(f"Number of Machines: {num_machines}")

  if optimal_makespan is not None:
    print(f"Optimal Makespan: {optimal_makespan}")

  print("\nOutput in the specified format:")
  print_output(jobs)
