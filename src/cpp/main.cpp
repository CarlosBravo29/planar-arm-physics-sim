#include <iostream>
#include <cmath>

using namespace std;

void calc_pos(int l1, int a1, int l2, int a2){    
    double x1 = 0.0, y1 = 0.0;
    double ar1 = 0.0, ar2 = 0.0;

    ar1 = a1 * M_PI / 180.0;
    ar2 = a2 * M_PI / 180.0;

    x1 = l1 * cos(ar1);
    y1 = l1 * sin(ar1);

    cout << "x1: " << x1 << "\ny1: " << y1 << endl;

}

int main(){
    int l1 = 0, l2 = 0;
    int a1 = 0, a2 = 0;

    cout << "L1: ";
    cin >> l1;
    cout << "angle 1: ";
    cin >> a1;

    calc_pos(l1, a1, l2, a2);

    return 0;
}