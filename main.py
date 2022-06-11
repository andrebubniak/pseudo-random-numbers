import randomnessTests
import pseudoRandomNumberGenerators as generators

def main():
    data = generators.glim3_generator(10, 2022)
    try:
        rt = randomnessTests.randomnessTests(data)
    except Exception as e:
        print(e)
        exit(-1)

    print('uniformity test: ', rt.uniformity_test())
    print('runs test: ', rt.runs_test())
    print('gap test: ', rt.gap_test())
    print('permutations test: ', rt.permutations_test())


if __name__ == '__main__':
    main()