import itertools
import math
import numpy
from typing import List


class randomnessTests():
    def __init__(self, data_array: List[float]):
        self.data = data_array
        if(data_array == None or len(data_array) < 2):
            raise Exception('Array too short. Please use a bigger array')

    def __accumulate_array(self, array):
        cumulative_array = []
        cumulative_array.append(array[0])

        for i in range(1, len(array)):
            cumulative_array.append(array[i] + cumulative_array[i-1])
        return cumulative_array

    def __kolmogorov_smirnov(self, observed_frequency: List[int], expected_probability: List[float]):

        observed_frequency_total = sum(observed_frequency)
        observed_probability = [f / observed_frequency_total for f in observed_frequency]

        observed_cumulative_probability = self.__accumulate_array(observed_probability)
        expected_cumulative_probability = self.__accumulate_array(expected_probability)

        kolmogorov_smirnov_5percent = 1.36/numpy.sqrt(sum(observed_frequency))
        kolmogorov_smirnov_calculated = max([abs(expected_cumulative_probability[i] - observed_cumulative_probability[i]) for i in range(len(observed_cumulative_probability))])

        return (kolmogorov_smirnov_calculated < kolmogorov_smirnov_5percent)


    def uniformity_test(self):
        data_array = self.data.copy()
        if(data_array) == None:
            return

        return self.__kolmogorov_smirnov(numpy.histogram(a=data_array, range=[0,1])[0], [1/10 for i in range(1, 11)])


    def runs_test(self):
        data_array = self.data.copy()
        if(data_array) == None:
            return

        def compute_runs(data_array, ascending = True):
            if(len(data_array) < 2): return
            
            runs = []
            run_count = 1
            index = 1

            while True:
                if( (ascending and data_array[index] > data_array[index-1]) or (not ascending and data_array[index] < data_array[index-1]) ): 
                    run_count = run_count + 1

                else:
                    runs.append(run_count)
                    run_count = 1
                    index = index + 1
                    
                index = index + 1
                if(index >= len(data_array)):
                    if(run_count > 1): runs.append(run_count)
                    break

            return runs

        ascending_runs = compute_runs(data_array)
        descending_runs = compute_runs(data_array, False)

        num_ascending_runs = [n for n in range(1, max(ascending_runs) + 1)]
        num_descending_runs = [n for n in range(1, max(descending_runs) + 1)]

        observed_frequency_ascending = [ascending_runs.count(n) for n in num_ascending_runs]
        observed_frequency_descending = [descending_runs.count(n) for n in num_descending_runs]

        expected_probability_ascending = [n/math.factorial(n + 1) for n in num_ascending_runs]
        expected_probability_descending = [n/math.factorial(n + 1) for n in num_descending_runs]
        
        
        return self.__kolmogorov_smirnov(observed_frequency_ascending, expected_probability_ascending) and self.__kolmogorov_smirnov(observed_frequency_descending, expected_probability_descending)


    def gap_test(self, num_decimal_places: int = 1):
        data_array = self.data.copy()
        if(data_array) == None:
            return

        if(num_decimal_places < 1): num_decimal_places = 1

        digits = []
        for n in data_array:
            digits_str = str(n).replace('.', '')
            if(len(digits_str) < (num_decimal_places + 1)):
                digits.append(0)
            else:
                digits.append(int(digits_str[num_decimal_places]))
        

        gap_dict = {'0':[], '1':[], '2':[], '3':[], '4':[],
                    '5':[], '6':[], '7':[], '8':[], '9':[]}

        gap_count = [0] * 10

        for n in range(len(digits)):
            for i in range(10):
                if(i != digits[n]):
                    gap_count[i] = gap_count[i] + 1

            key = str(digits[n])
            gap_dict[key] = gap_dict[key] + [gap_count[digits[n]]]
            gap_count[digits[n]] = 0

            # se for o ultimo numero, adiciona os valores dos intervalos
            if(n == len(digits)-1):
                for i in range(10):
                    gap_dict[str(i)] = gap_dict[str(i)] + [gap_count[i]]


        def compute_gaps(digit):
            intervals = [i for i in range(max(gap_dict[str(digit)]) + 1)]

            observed_frequency = []
            expected_probability = []

            for n in intervals:
                observed_frequency.append(gap_dict[str(digit)].count(n))
                expected_probability.append(pow(0.9, n)*0.1) 

            return self.__kolmogorov_smirnov(observed_frequency, expected_probability)

        results = []
        for i in range(10):
            results.append(compute_gaps(i))
        
        return all(results)


    def permutations_test(self, interval_size = 3):
        data_array = self.data.copy()
        if(data_array) == None:
            return

        def compute_permutations(data: list, interval_size):
            data2 = data
            while(len(data2) % interval_size != 0):
                data2.remove(data2[-1])

            intervals = numpy.split(numpy.array(data2), int(len(data2) / interval_size))
            
            p = itertools.permutations(intervals[0], interval_size)

            permutations_count = [0] * len(list(p))

            for i in range(len(intervals)):
                p = itertools.permutations(intervals[i], interval_size)
                function_index = 0
                for s in list(p):
                    if( all([s[j] < s[j+1] for j in range(len(s)-1)]) ):
                        permutations_count[function_index] = permutations_count[function_index] + 1
                        break

                    function_index = function_index + 1

            return permutations_count

        observed_frequency = compute_permutations(data_array, interval_size)
        expected_probability = [(1/math.factorial(interval_size))] * len(observed_frequency)
        

        return self.__kolmogorov_smirnov(observed_frequency, expected_probability)

