#!/bin/bash

tolerance=0.00001

check_value () {
        args="$*"
        truth=${args%% *}
        command=${args#* }
        value=`$command`
        test=`python -c "print(abs(($value) - ($truth)) > $tolerance)"`
        if [ "$test" = "True" ]; 
        then
                echo "FAILED: $command != $truth"
                exit 1
        fi
}

if [ $# != 2 ]
then
        echo "USAGE: $0 ORACLE_EXECUTABLE POOL_CSV"
        exit 1
fi

check_value -1.540185 $1 $2 44 85 96 50
check_value -0.686360 $1 $2 23 28 99 60
check_value -0.804072 $1 $2 88 54 99
check_value -0.574731 $1 $2 91 7
check_value -2.778622 $1 $2 16 83 14
check_value -0.764271 $1 $2 7 77
check_value -1.390867 $1 $2 45 40 86 52 47
check_value 0.000000 $1 $2 67
check_value -0.535762 $1 $2 7 55 65 81 85
check_value -0.289360 $1 $2 52 28 99 72
check_value -0.966293 $1 $2 58 39
check_value -2.331134 $1 $2 74 33 22 23 49
check_value -0.580207 $1 $2 1 28 0 83
check_value 0.498469 $1 $2 3 78 92 43 3
check_value -1.316426 $1 $2 21 77 28
check_value -0.345373 $1 $2 93 48 38 60
check_value -0.441042 $1 $2 31 33 47
check_value 0.000000 $1 $2 52
check_value -1.816164 $1 $2 73 64 90 48
check_value -2.034547 $1 $2 62 99 16
check_value -1.716216 $1 $2 4 54 66 50
check_value -0.495326 $1 $2 27 28 40
check_value -0.706289 $1 $2 63 17
check_value -2.562272 $1 $2 28 16 57
check_value -0.193106 $1 $2 60 18 3
check_value -1.205585 $1 $2 54 36 75 37 58
check_value -0.308294 $1 $2 40 15 41
check_value 0.000000 $1 $2 9
check_value 0.000000 $1 $2 38
check_value -1.863203 $1 $2 62 79
check_value -1.026490 $1 $2 89 90 3 54
check_value -0.339986 $1 $2 73 94 66 11 35
check_value -0.171573 $1 $2 18 67 57 47
check_value 0.000000 $1 $2 27
check_value -0.121005 $1 $2 68 84 30 10 93
check_value -0.529871 $1 $2 6 60
check_value -1.585704 $1 $2 39 49
check_value -0.993432 $1 $2 20 34
check_value 0.000000 $1 $2 62
check_value -1.255240 $1 $2 48 6 26 33 49
check_value 0.000000 $1 $2 51
check_value 0.093236 $1 $2 4 46 96 97
check_value -0.614456 $1 $2 94 96 86
check_value -1.906572 $1 $2 81 14 26 63
check_value 0.000000 $1 $2 53
check_value -0.792729 $1 $2 80 96 24 42 45
check_value -0.304749 $1 $2 83 71 60 45
check_value -0.353839 $1 $2 97 5
check_value -0.578013 $1 $2 99 57 36 7 65
check_value -0.309027 $1 $2 17 4
check_value -0.396769 $1 $2 55 72
check_value -0.441295 $1 $2 27 80 50
check_value -1.847373 $1 $2 57 93 54
check_value -0.329613 $1 $2 84 36 2 15 50
check_value -1.198640 $1 $2 53 38 50
check_value -1.119565 $1 $2 9 6 94 83 68
check_value -1.048818 $1 $2 77 34 23 96 58
check_value -0.448773 $1 $2 68 49 1 77
check_value -0.988085 $1 $2 12 33 21 80
check_value -0.530394 $1 $2 78 82
check_value -0.432782 $1 $2 96 72
check_value 0.000000 $1 $2 20
check_value -0.502733 $1 $2 52 36 41
check_value -0.126644 $1 $2 28 77 26 80
check_value -1.690352 $1 $2 10 4 98
check_value -0.839811 $1 $2 6 75 60 96 53
check_value 0.000000 $1 $2 96
check_value -2.233617 $1 $2 68 64 90 22
check_value -1.806873 $1 $2 86 48 90 96 95
check_value -0.595476 $1 $2 24 88 71 83
check_value -1.506266 $1 $2 99 39 80 16 93
check_value -0.382470 $1 $2 26 25 16 38 53
check_value -1.267494 $1 $2 51 85 7 70
check_value -0.602095 $1 $2 68 74 85
check_value -0.760066 $1 $2 42 80
check_value -0.685259 $1 $2 9 24
check_value -1.386578 $1 $2 2 80
check_value -0.699484 $1 $2 25 23 89
check_value -0.008764 $1 $2 69 30 81
check_value -0.357059 $1 $2 33 5
check_value 0.000000 $1 $2 16
check_value -0.951481 $1 $2 51 84
check_value 0.000000 $1 $2 19
check_value -1.141832 $1 $2 57 83
check_value 0.000000 $1 $2 67
check_value -1.401055 $1 $2 29 85 68 8 68
check_value -0.505163 $1 $2 73 51
check_value -0.596623 $1 $2 60 17
check_value -0.375052 $1 $2 36 89
check_value -0.204157 $1 $2 27 30 72 8
check_value -0.625461 $1 $2 79 79 62 75 13
check_value -1.034943 $1 $2 75 42 18 86
check_value -0.404619 $1 $2 74 57 24 43 76
check_value -0.773089 $1 $2 0 84 47 89
check_value -1.153847 $1 $2 17 64
check_value -1.230127 $1 $2 98 40 62
check_value -1.298639 $1 $2 73 45
check_value -0.937718 $1 $2 34 74 44 35 61
check_value -0.829532 $1 $2 72 68 3 76
check_value 0.000000 $1 $2 53
check_value -0.483144 $1 $2 92 99 36 25
check_value -0.461515 $1 $2 70 51 69
check_value 0.310422 $1 $2 94 84 29 56 13
check_value -2.484913 $1 $2 63 42 70
check_value -2.742661 $1 $2 18 73 63
check_value -0.973113 $1 $2 0 73 85 2
check_value -0.410446 $1 $2 27 94
check_value -0.645882 $1 $2 75 89 74 49
check_value -0.473079 $1 $2 31 77
check_value -1.573140 $1 $2 79 99 31 79 57
check_value -0.127126 $1 $2 3 49 70
check_value -0.445552 $1 $2 78 30 25 73
check_value -0.903638 $1 $2 75 96 71 85
check_value -0.918254 $1 $2 31 5 77 46
check_value -0.457481 $1 $2 98 0
check_value -1.679164 $1 $2 93 71 23
check_value -0.202952 $1 $2 78 3 93 98
check_value -0.954705 $1 $2 46 21 62 53
check_value -0.227417 $1 $2 16 95 22 18 13
check_value -0.494930 $1 $2 10 22 54 18 95
check_value -0.117711 $1 $2 58 67 58 45 30
check_value -1.226799 $1 $2 31 54 98 57 40
check_value -1.909804 $1 $2 10 41 99
check_value -1.500933 $1 $2 2 70 27 4
check_value -1.733821 $1 $2 64 88
check_value 0.000000 $1 $2 15
check_value -0.170095 $1 $2 49 77 20 57 91
check_value -1.408114 $1 $2 76 24
check_value -0.582103 $1 $2 45 6 15 35 86
check_value -0.744103 $1 $2 78 95 20 2 27
check_value -0.826942 $1 $2 32 13 97 6 45
check_value -0.512170 $1 $2 56 26 0
check_value -0.875839 $1 $2 22 95 90 7
check_value -1.423249 $1 $2 9 63 16 91 65
check_value -1.329462 $1 $2 84 8 81 91
check_value -1.100356 $1 $2 82 77 73
check_value -1.881354 $1 $2 40 6 64
check_value 0.266685 $1 $2 14 29
check_value -0.672343 $1 $2 67 41 75 90
check_value -1.232230 $1 $2 58 19
check_value 0.000000 $1 $2 70
check_value 0.000000 $1 $2 24
check_value -0.852881 $1 $2 5 73 3
check_value 0.000000 $1 $2 89
check_value -1.661199 $1 $2 74 16 27
check_value -0.646144 $1 $2 10 74 35 41 80
check_value -0.672595 $1 $2 60 15
check_value 0.000000 $1 $2 83
check_value -0.506599 $1 $2 88 56 91 6
check_value 0.000000 $1 $2 80
check_value 0.251994 $1 $2 52 39 9 62 3
check_value -1.553005 $1 $2 2 95 38
check_value -0.757111 $1 $2 46 91 22
check_value -0.959014 $1 $2 14 31
check_value -0.463559 $1 $2 48 22 56
check_value -0.087883 $1 $2 8 56
check_value 0.027824 $1 $2 7 53 22
check_value -0.993645 $1 $2 75 92 29 27
check_value 0.000000 $1 $2 42
check_value 0.000000 $1 $2 0
check_value 0.000000 $1 $2 10
check_value -1.939718 $1 $2 75 38 2 2
check_value 0.250948 $1 $2 91 45
check_value -0.149107 $1 $2 54 47
check_value -1.073117 $1 $2 94 98 72 31 73
check_value -0.512520 $1 $2 9 37 52
check_value -2.447872 $1 $2 21 16
check_value -0.190237 $1 $2 89 94
check_value -1.716160 $1 $2 52 63 55
check_value -1.366671 $1 $2 88 13 63 65 2
check_value -0.917455 $1 $2 71 46 65 96
check_value -0.189331 $1 $2 4 33 63 19
check_value 0.017933 $1 $2 66 4
check_value -0.917247 $1 $2 88 64 75 51 34
check_value 0.391372 $1 $2 10 17 77 11
check_value -0.166328 $1 $2 11 97 91 19 51
check_value -1.058399 $1 $2 92 98 61
check_value -1.199834 $1 $2 23 35 75 3 7
check_value -0.888737 $1 $2 85 5 26 52 89
check_value 0.000000 $1 $2 23
check_value -0.878043 $1 $2 55 37 24 91
check_value 0.000000 $1 $2 79
check_value -0.857306 $1 $2 92 4 30
check_value -3.648730 $1 $2 65 52
check_value -0.718650 $1 $2 73 70
check_value -1.021371 $1 $2 78 14 57 8 47
check_value -0.110682 $1 $2 22 59
check_value 0.000000 $1 $2 40
check_value 0.000000 $1 $2 30
check_value 0.000000 $1 $2 77
check_value -1.031407 $1 $2 42 77 5 60
check_value -0.351246 $1 $2 46 52
check_value -0.979069 $1 $2 70 49 14
check_value -0.554876 $1 $2 24 34
check_value 0.000000 $1 $2 3
check_value -0.284933 $1 $2 95 72
check_value -1.167116 $1 $2 50 96 37 56 54
check_value 0.372470 $1 $2 9 29 15 15
check_value -0.604709 $1 $2 79 87 3 60
check_value -0.619494 $1 $2 38 75 0 5

echo "ALL TESTS PASSED"
