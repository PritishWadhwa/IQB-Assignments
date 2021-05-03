#include <iostream>
#include <algorithm>
#include <string>

using namespace std;

string convert(string s)
{
    string ans = "";
    for (int i = 0; i < s.length(); i++)
    {
        if (s[i] == 'A')
        {
            ans += 'T';
        }
        else if (s[i] == 'T')
        {
            ans += 'A';
        }
        else if (s[i] == 'G')
        {
            ans += 'C';
        }
        else
        {
            ans += 'G';
        }
    }
    reverse(ans.begin(), ans.end());
    return ans;
}

int main()
{
    string s;
    cin >> s;
    int t;
    cin >> t;
    if (t == 1)
    {
        string converted = convert(s);
        cout << s << endl
             << converted << endl;
    }
    else
    {
        cout << s.length();
    }
    return 0;
}
