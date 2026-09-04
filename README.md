# 3 DOF planar arm kinematics and dynamics simulation

![Project Status: In Development](https://img.shields.io/badge/STATUS-WIP-blue)

## Direct Kinematic Model

| | $\theta_i$ | $d_i$ | $a_i$ | $\alpha_i$ |
| --- | --- | --- | --- | --- |
| 1 | $\theta_1$ | 0 | $a_1$ | 0 |
| 2 | $\theta_2$ | 0 | $a_2$ | 0 |
| 3 | $\theta_3$ | 0 | $a_3$ | 0 |

$x = a_1\cos(\theta_1)+a_2\cos(\theta_1+\theta_2)+a_3\cos(\theta_1+\theta_2+\theta_3)$

$y = a_1\sin(\theta_1)+a_2\sin(\theta_1+\theta_2)+a_3\sin(\theta_1+\theta_2+\theta_3)$


## Tech Stack

![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
