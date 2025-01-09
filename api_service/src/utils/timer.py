import time

def timer(func):
    """A decorator to measure the time a function takes to execute."""
    
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        
        result = func(*args, **kwargs)  # Execute the function
        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the time difference
        print(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds.")
        return result  # Return the result of the function call

    return wrapper