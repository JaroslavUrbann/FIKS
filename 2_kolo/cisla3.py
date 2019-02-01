# A Dynamic Programming solution for subset sum problem
# Returns true if there is a subset of
# set[] with sun equal to given sum
import fileinput

# Returns true if there is a subset of set[]
# with sun equal to given sum
def isSubsetSum(set, n, sum):
    # The value of subset[i][j] will be
    # true if there is a
    # subset of set[0..j-1] with sum equal to i
    subset = ([[False for i in range(sum + 1)]
               for i in range(n + 1)])

    # If sum is 0, then answer is true
    for i in range(n + 1):
        subset[i][0] = True

        # If sum is not 0 and set is empty,
        # then answer is false
        for i in range(1, sum + 1):
            subset[0][i] = False

        # Fill the subset table in botton up manner
        for i in range(1, n + 1):
            for j in range(1, sum + 1):
                if j < set[i - 1]:
                    subset[i][j] = subset[i - 1][j]
                if j >= set[i - 1]:
                    subset[i][j] = (subset[i - 1][j] or
                                    subset[i - 1][j - set[i - 1]])

                    # uncomment this code to print table
        # for i in range(n+1):
        # for j in range(sum+1):
        #     print (subset[i][j],end=" ")
        # print()
    return subset[n][sum]


# Driver program to test above function
if __name__ == '__main__':
    inp = fileinput.input()
    lines = int(inp.readline())
    for i in range(lines):
        line = list(map(int, inp.readline().split(" ")))
        target = line[0]
        set = line[2:]
        # target = 8
        # set = [4, 7, 5, 2]
        b = (sum(set) - target) / 2
        a = target + b
        n = len(set)
        if int(a) != a:
            print("NELZE")
        elif isSubsetSum(set, n, int(a)):
            print("LZE")
        else:
            print("NELZE")

    # This code is contributed by
# sahil shelangia.