# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # <center>Introduction to Quantitative Biology(BIO213-IQB)</center>
# ## <center>Assignment 1</center>
# <h5><div style="text-align: right">Efforts By: Pritish Wadhwa (2019440)</div></h5>
# <hr>

# %%
# importing the required libraries
import numpy as np
import math


# %%
# the given DNA Sequences
dnaSeq1 = "ATCAGAGTA"
dnaSeq2 = "TTCAGTA"


# %%
# calculating the number of rows and columns for the DP table
rows = len(dnaSeq1) + 1
cols = len(dnaSeq2) + 1


# %%
# initilaizing the original match, gap and mismatch scores
matchPenalty = 2
mismatchPenalty = -1
gapPenalty = -1


# %%
# initializing the DP matrix with 0's
dpMatrix = np.zeros((rows, cols), dtype=np.int)


# %%
# creating a visited matrix for backtracking
visited = np.zeros((rows, cols), dtype=np.int)


# %%
# function to check whether a cell is valid as the last cell or not(while generating for local alignment)
def isValid(i, j):
    if i == 0:
        if dpMatrix[i][j-1] + gapPenalty != dpMatrix[i][j]:
            return True
        else:
            return False
    elif j == 0:
        if dpMatrix[i-1][j] + gapPenalty != dpMatrix[i][j]:
            return True
        else:
            return False
    else:
        if (dpMatrix[i-1][j] + gapPenalty != dpMatrix[i][j]) and (dpMatrix[i][j-1] + gapPenalty != dpMatrix[i][j]) and (dpMatrix[i-1][j-1] + mismatchPenalty != dpMatrix[i][j]):
            return True
        else:
            return False


# %%
# function to calculate scores of the 2 sequences depending upon the scoring scheme
def calculateScore(seq1, seq2):
    score = 0
    for i in range(len(seq1)):
        if seq1[i] == ' ':
            continue
        elif seq1[i] == seq2[i]:
            score += matchPenalty
        elif seq1[i] != seq2[i]:
            if seq1[i] == '-' or seq2[i] == '-':
                score += gapPenalty
            else:
                score += mismatchPenalty
    return score


# %%
# the function to print the sequences along with their matching sequences
def printSequences(seq1, seq2):
    seq1 = seq1.replace("", " ")
    seq2 = seq2.replace("", " ")
    seq1 = seq1[1: -1]
    seq2 = seq2[1: -1]
    score = calculateScore(seq1, seq2)
    print(seq1)
    for i in range(len(seq1)):
        if seq1[i] == ' ' or seq1[i] != seq2[i] or seq1[i] == seq2[i] == '-':
            print(' ', end='')
        elif seq1[i] == seq2[i]:
            print('|', end='')
    print()
    print(seq2)
    print("The alignment score for the above sequences with given penalties is: " + str(score))
    print()


# %%
# function to print the dp matrix
def printMatrix():
    column0 = '0' + dnaSeq2
    row0 = '0' + dnaSeq1
    for i in range(rows + 1):
        for j in range(cols + 1):
            if i == 0 and j == 0:
                print('X', end='\t')
            elif i == 0:
                print(column0[j-1], end='\t')
            elif j == 0:
                print(row0[i-1], end='\t')
            else:
                print(dpMatrix[i-1][j-1], end="\t")
        print()


# %%
# function to generate the global alignments of the given 2 sequences
def globalAlignment(rows, cols, seq1, seq2):
    for i in range(1, rows):
        for j in range(1, cols):
            if seq1[i-1] == seq2[j-1]:
                dpMatrix[i][j] = dpMatrix[i-1][j-1] + matchPenalty
            else:
                dpMatrix[i][j] = max(dpMatrix[i-1][j-1] + mismatchPenalty,
                                     dpMatrix[i-1][j] + gapPenalty, dpMatrix[i][j-1] + gapPenalty)


# %%
# function to generate the local alignments of the given 2 sequences
# It returns a list of positions where the dp matrix has the max value
def localAlignment(rows, cols, seq1, seq2):
    maxVal = -math.inf
    l = []
    for i in range(0, rows):
        for j in range(0, cols):
            if i == 0 or j == 0:
                dpMatrix[i][j] = 0
            elif seq1[i-1] == seq2[j-1]:
                dpMatrix[i][j] = dpMatrix[i-1][j-1] + matchPenalty
            else:
                dpMatrix[i][j] = max(0, dpMatrix[i-1][j-1] + mismatchPenalty,
                                     dpMatrix[i-1][j] + gapPenalty, dpMatrix[i][j-1] + gapPenalty)
            if dpMatrix[i][j] >= maxVal:
                maxVal = dpMatrix[i][j]
    for i in range(0, rows):
        for j in range(0, cols):
            if dpMatrix[i][j] == maxVal:
                l.append((i, j))
    return l


# %%
# function to generate sequences in both global and local alignment scenarios
def generateSequences(i, j, seq1, seq2, ans1, ans2):
    if (i == 0 and j == 0) or (dpMatrix[i][j] == 0 and isValid(i, j)):
        ans1 = ans1[::-1]
        ans2 = ans2[::-1]
        printSequences(ans1, ans2)
        return
    elif dpMatrix[i][j] == 0:
        ans1 = ans1[::-1]
        ans2 = ans2[::-1]
        printSequences(ans1, ans2)
        ans1 = ans1[::-1]
        ans2 = ans2[::-1]
    elif i < 0 or j < 0 or visited[i][j] == 1:
        return
    visited[i][j] = 1
    flag = 0
    if seq1[i-1] == seq2[j-1]:
        flag = 1
        generateSequences(i-1, j-1, seq1, seq2, ans1 +
                          seq1[i-1], ans2 + seq2[j-1])
    if dpMatrix[i][j] == dpMatrix[i-1][j-1] + mismatchPenalty:
        flag = 1
        generateSequences(i-1, j-1, seq1, seq2, ans1 +
                          seq1[i-1], ans2 + seq2[j-1])
    if dpMatrix[i][j] == dpMatrix[i-1][j] + gapPenalty:
        flag = 1
        generateSequences(i-1, j, seq1, seq2, ans1 + seq1[i-1], ans2 + '-')
    if dpMatrix[i][j] == dpMatrix[i][j-1] + gapPenalty:
        flag = 1
        generateSequences(i, j-1, seq1, seq2, ans1 + '-', ans2 + seq2[j-1])
    if flag == 0:
        generateSequences(i-1, j-1, seq1, seq2, ans1 + '-', ans2 + '-')
    visited[i][j] = 0

# %% [markdown]
# ## Question 1)
# <hr>


# %%
# initializing the 0th row and 0th column in DP matrix for global Alignment
for i in range(rows):
    dpMatrix[i][0] = -1 * i
for j in range(cols):
    dpMatrix[0][j] = -1 * j


# %%
globalAlignment(rows, cols, dnaSeq1, dnaSeq2)

# %% [markdown]
# ### 1-a)
# The generated dynamic programming matrix:

# %%
printMatrix()

# %% [markdown]
# ### 1-b)
# <div style="text-align:justify">Yes, There are more than 1 optimal alingments for the given pair of DNA Sequences. This occurs because, the highest possible alignment score for the given pair of sequences is possible in more than 1 way</div>
# %% [markdown]
# ### 1-c)
# The global allignments with their scores are:

# %%
generateSequences(rows - 1, cols - 1, dnaSeq1, dnaSeq2, "", "")

# %% [markdown]
# ## Question 2)
# <hr>

# %%
l = localAlignment(rows, cols, dnaSeq1, dnaSeq2)

# %% [markdown]
# ### 2-a)
# The generated dynamic programming matrix:

# %%
printMatrix()

# %% [markdown]
# ### 2-b)
# The local allignments with their scores are:

# %%
for i in l:
    generateSequences(i[0], i[1], dnaSeq1, dnaSeq2, "", "")

# %% [markdown]
# ## Question 3)
# <hr>
# <div style="text-align:justify">The changes required in the program to perform local alignment rather then global alignment are:
# <ul>
# <li>For the global alignment, the entries of the 0<sup>th</sup> row and column were initialised with 0, -1, -2 and so on, whereas in the local aligment, the entries of the 0<sup>th</sup> row and column were initialised by 0.</li>
# <li>For the other entries, in the dp matrix of the global alignmnet, -ve values are possible but that is not the case for the dp matrix of local alignment. There the entries can only be a whole number.</li>
# <li>The above points are valid because while in the global alignment, while filling the table, only the maximum value of the adjoining cells with the added penalties are considered, whereas in the local alignment, while filling the table, the maximum of the adoining cells with added penalties, and 0 is considered.</li>
# <li>While reconstructing the sequence, in the global alignment, the maximum value is always at the last cell of the matrix, where as the maximum value in the local alignment can be anywhere in the matrix, not necessarily at the very end.</li>
# <li>In global alignment, while only one cell can accomodate the maximum value, whereas in local alignment, the maximum value can present in multiple cells.</li>
# <li>In the global alignment, the base case is reached when you are at the (0,0)<sup>th</sup> cell, whereas in local alignment, the base case is reached when, you can't move anywhere from the current cell, and the current cell has the value 0 in it.</li>
# <li>Another case that can be considered for local alignment is that if a value of 0 is reached while generating the sequence, at that instant, the generated sequence is also optimally aligned, but the function can not return from there as it is not the ultimate base case.</li>
# </ul></div>
# %% [markdown]
# ## Question 4)
# <hr>

# %%
# updated scores for the last question
matchPenalty = 2
mismatchPenalty = -1
gapPenalty = -2

# %% [markdown]
# ### Global Alignment

# %%
# initializing dp matrix for global alignment
for i in range(rows):
    dpMatrix[i][0] = -1 * i
for j in range(cols):
    dpMatrix[0][j] = -1 * j
globalAlignment(rows, cols, dnaSeq1, dnaSeq2)

# %% [markdown]
# #### Generated Dynamic Programming Matrix:

# %%
printMatrix()

# %% [markdown]
# #### Optimally Aligned Sequences:

# %%
generateSequences(rows - 1, cols - 1, dnaSeq1, dnaSeq2, "", "")

# %% [markdown]
# <div style="text-align:justify">
# <ul>
# <li>After updatind the scoring scheme, even though the generated sequence didn't change, the corresponding score did change.</li>
# <li>This was because, as in global alignments, there has to the complete involvement of both the subsequences.</li>
# <li>Since the difference in the 2 strings is of 2 characters, there has to be atleast 2 gaps to be inserted.</li>
# <li>Now since the gap penalty is made more negative, thus, the DP Matrix changes.</li>
# <li>Since the difference in the new values was not that much significant for the given sequences when being considered for global alignment, we get the same old alignments but a different score for each</li>
# </ul>
# </div>
# %% [markdown]
# ### Local Alignment

# %%
l = localAlignment(rows, cols, dnaSeq1, dnaSeq2)

# %% [markdown]
# #### Generated Dynamic Programming Matrix:

# %%
printMatrix()

# %% [markdown]
# #### Optimally Aligned Sequences:

# %%
for i in l:
    generateSequences(i[0], i[1], dnaSeq1, dnaSeq2, "", "")

# %% [markdown]
# <div style="text-align:justify">
# <ul>
# <li>After updatind the scoring scheme, the generated sequences changed and the corresponding score did change.</li>
# <li>This was because, as in local alignment, unlike global one, there is no need for complete involvement of both the subsequences.</li>
# <li>Now since the gap penalty is made more negative, thus, the DP Matrix changes.</li>
# <li>Since the difference in the new values was significant for the given sequences when being considered for local alignment, we get three more sequences, along with the ones we got with the previos scoring scheme.</li>
# </ul>
# </div>
