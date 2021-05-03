#include <iostream>
#include <math.h>
#include <vector>
#include <algorithm>
#include <set>
using namespace std;

bool checkAndPrint(vector<int> ans, vector<int> ansCopy, int sol[], int arr1[], int n1, int arr2[], int n2)
{
    sort(ans.begin(), ans.end());
    for (int i = 0; i < ans.size(); i++)
    {
        if (ans[i] != sol[i])
        {
            return false;
        }
    }
    for (int i = 0; i < n1; i++)
    {
        cout << arr1[i] << " ";
    }
    cout << endl;
    for (int i = 0; i < n2; i++)
    {
        cout << arr2[i] << " ";
    }
    cout << endl;
    for (int i : ansCopy)
    {
        cout << i << " ";
    }
    cout << endl;
    return true;
}

vector<int> solve(int arr1[], int n1, int arr2[], int n2)
{
    vector<int> ans;
    int i = 0, j = 0;
    while (i != n1 && j != n2)
    {
        if (arr1[i] == arr2[j])
        {
            ans.push_back(arr1[i]);
            i++;
            j++;
        }
        else if (arr1[i] < arr2[j])
        {
            ans.push_back(arr1[i]);
            arr2[j] -= arr1[i];
            i++;
        }
        else
        {
            ans.push_back(arr2[j]);
            arr1[i] -= arr2[j];
            j++;
        }
    }
    // if (ans.size() == 10)
    // {
    //     for (int i = 0; i < n1; i++)
    //     {
    //         cout << arr1[i] << " ";
    //     }
    //     cout << endl;
    //     for (int i = 0; i < n2; i++)
    //     {
    //         cout << arr2[i] << " ";
    //     }
    //     cout << endl;
    //     for (auto i : ans)
    //     {
    //         cout << i << " ";
    //     }
    //     cout << endl;
    // }
    return ans;
}

int ctr = 0, loop = 0;

void check(int arr1[], int n1, int arr2[], int n2, int sol[], int ansLen)
{
    do
    {
        do
        {
            loop++;
            int passArr1[5];
            for (int i = 0; i < 5; i++)
            {
                passArr1[i] = arr1[i];
            }
            int passArr2[6];
            for (int i = 0; i < 6; i++)
            {
                passArr2[i] = arr2[i];
            }
            vector<int> ans = solve(passArr1, 5, passArr2, 6);
            if (10 == ans.size())
            {
                if (checkAndPrint(ans, ans, sol, arr1, 5, arr2, 6))
                {
                    return;
                    // ctr++;
                    // cout << endl;
                }
            }
        } while (next_permutation(arr2, arr2 + 6));
    } while (next_permutation(arr1, arr1 + 5));
}

int main()
{
    int arr1[] = {4, 5, 7, 8, 12};
    int arr2[] = {3, 4, 4, 6, 9, 10};
    int sol[] = {1, 2, 3, 3, 4, 4, 4, 4, 5, 6};
    check(arr1, 5, arr2, 6, sol, 10);
    cout << ctr << " " << loop << endl;
    return 0;
}