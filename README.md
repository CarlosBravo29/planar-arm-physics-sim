# 3 DOF planar arm kinematics and dynamics simulation

![Project Status: In Development](https://img.shields.io/badge/STATUS-WIP-blue)




## Direct Kinematic Model

$$T^0_3=\begin{bmatrix} \cos(\theta_1+\theta_2+\theta_3) & -\sin(\theta_1+\theta_2+\theta_3) & 0 & a_1\cos(\theta_1)+a_2\cos(\theta_1+\theta_2)+a_3\cos(\theta_1+\theta_2+\theta_3) \\ \sin(\theta_1+\theta_2+\theta_3) & \cos(\theta_1+\theta_2+\theta_3) & 0 & a_1\sin(\theta_1)+a_2\sin(\theta_1+\theta_2)+a_3\sin(\theta_1+\theta_2+\theta_3) \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

$x = a_1\cos(\theta_1)+a_2\cos(\theta_1+\theta_2)+a_3\cos(\theta_1+\theta_2+\theta_3)$

$y = a_1\sin(\theta_1)+a_2\sin(\theta_1+\theta_2)+a_3\sin(\theta_1+\theta_2+\theta_3)$


## Tech Stack

![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)