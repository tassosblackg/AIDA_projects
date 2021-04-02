# Execution

# TSP data generator

> $python3 tsp_data_genarator.py NumberOfRecords, start_index,end_index
>
>> NumberOfRecords is the total number of x,y points
>> & (start_index,end_index) is the range for the values of x,y

# Knapsack data generator
> $python3 knap_data.py NumberOfRecords, capacity_start_index,capacity_end_index
>
>>NumberOfRecords is the total number of object to add to the sack (#weights)
>>(capacity_start_index,capacity_end_index) take a capacity value between  a range

# !NOTE:

- start_index must be << from end_index
- make sure NumberOfRecords to be smaller from (end_index-start_index) in order to avoid many records with the same values
