import time
import randomnessTests
import pseudoRandomNumberGenerators as generators

def main():
    #t1 = time.time()
    #data = generators.glim3_generator(50000000, 2022)
    #t2 = time.time()

    #with open('numeros.txt', 'w') as file:
        #for d in data:
            #file.write(str(d) + '\n')


    #print('time lapsed: ', (t2-t1))

    #data = []
    t1 = time.time()
    data = generators.glim3_generator(50000000, 2022)
    t2 = time.time()

    print('time lapsed: ', (t2-t1))

    #with open('intervData.txt') as file:
        #for line in file:
            #data.append(float(line.replace(',', '.').replace('\n', '')))

    
    

    try:
        rt = randomnessTests.randomnessTests(data)
    except Exception as e:
        print(e)
        exit(-1)

    print('uniformity test: ', rt.uniformity_test(4))
    #print('runs test: ', rt.runs_test())
    #print('gap test: ', rt.gap_test())
    #print('permutations test: ', rt.permutations_test())


if __name__ == '__main__':
    main()