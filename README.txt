1. A List of files contained for structured data:
1).txt
Data\training.txt--40 names
Data\training_DOB.txt--40 DOB corresponding to training.txt
Data\testing.txt--10 names
Data\testing_DOB.txt-10 DOB corresponding to testing.txt
Data\output.txt Freebase query results for Data\testing.txt

2).py
freebase.py: Contains all functions and execution process.


2. A high level description:
We don't use any training data for our task.

1. Construct Search Query and use Freebase search API to get the mid, using name as the keyword.
2. We only pick the first one of the returned MIDs, because, by observation, we found that the other mids
   are for other related person.
3. Based on the mid, use freebase MQL read API to get the date_of_birth.

Return the first record [name,data_of_birth].

3. How to run the code:

   run freebase.py directly. (>python freebase.py)

   **please note that if you use different file names other than the ones we listed above, please change the parameters
   of the functions accordingly.



4. Accuracy: