# EverJudge 测评器
使用C++编写Windows操作系统下的文件测评器

*引用了nlohmann::json*


文件格式如下
- contest
  - example
    - data
      - A
        - x.in
        - x.ans
        - .json
      - B
        - x.in
        - x.ans
        - .json
    - source
      - 1
        - A+1.cpp
        - A+1.exe (complied)
    - result
        - 1
          x.ans
    result.json

调用方式:

    judge <contest_name> <file_name>

其中
- file_name 格式为 **problem**+**submission**.cpp
- contest_name 为比赛名称， 样例中为**example**
