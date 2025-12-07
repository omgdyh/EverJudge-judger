#include <iostream>
#include <string>
#include <windows.system.h>
#include <chrono>
#include <fstream>
#include <future>
#include <initializer_list>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

std::string get_string(std::initializer_list<std::string> multis) {
    std::string res = "";
    for (auto __s : multis) {
        res += __s;
    }
    return res;
}

int main(int argv, const char * args[]) {
    if (argv != 3) {
        std::cout << "invalid input." << std::endl;
        return -1;
    }
    
    std::string submission = args[1], contest = args[2];

    int __split_pos = submission.find("+");

    std::string problem = submission.substr(0, __split_pos);
    std::string id = submission.substr(__split_pos + 1, submission.size() - __split_pos + 1);

    std::string data = get_string({".\\contest\\", contest, "\\data\\", problem, "\\"});
    std::string file = get_string({".\\contest\\", contest, "\\source\\", submission});
    std::string result = get_string({".\\contest\\", contest, "\\result\\"});

    std::ifstream _readx(get_string({".\\contest\\", contest, "\\result.json"}).c_str());
    json R;
    _readx >> R;
    _readx.close();

    std::string complie = get_string({"g++ ", file, ".cpp -std=c++14 -Wall -O0 -o ", file, ".exe"});
    if (std::system(complie.c_str()) == 1) {
        R[id]["complie"] = false;
        R[id]["total"] = "CE";
        
        std::ofstream _out(get_string({".\\contest\\", contest, "\\result.json"}));
        _out << std::setw(4) << R;
        _out.close();

        return -1;
    }
    R[id]["complie"] = true;

    std::string mkd = get_string({"mkdir ", result, id});
    if (system(mkd.c_str())) {
        return -1;
    }
    json I;
    std::ifstream _read(get_string({data, ".json"}).c_str());
    I << _read;
    _read.close();

    bool AC = true, WA = false, TLE = false;

    int test_cases = I["test_cases"].get<int>(), time_limit = I["time_limit"].get<int>();

    std::cout << "[JUDGE] test cases: " << test_cases << ", time limit: " << time_limit << " (ms)" << std::endl;

    for (int i = 1; i <= test_cases; i++) {
        std::string run = get_string({file, ".exe < ", data, std::to_string(i), ".in > ", result, id, "\\", std::to_string(i), ".out"});
        std::string fc = get_string({"fc ", data, std::to_string(i), ".ans ", result, id, "\\", std::to_string(i), ".out"});
        
        std::future<void> task = std::async(run_task, run);
        std::future_status status = task.wait_for(std::chrono::milliseconds(time_limit));
        do {
            if (status == std::future_status::timeout) {
                R[id][std::to_string(i)] = "TLE";
                TLE = true;
                AC = false;
                break;
            }
            if (status == std::future_status::ready) {
                if (system(fc.c_str())) {
                    R[id][std::to_string(i)] = "WA";
                    AC = false;
                    WA = true;
                } else {
                    R[id][std::to_string(i)] = "AC";
                }
                break;
            }
        } while (status != std::future_status::ready);
    } if (WA == 1) {
        R[id]["total"] = "WA";
    } if (TLE == 1) {
        R[id]["total"] = "TLE";
    } if (AC == 1) {
        R[id]["total"] = "AC";
    }
    std::ofstream _out(get_string({".\\contest\\", contest, "\\result.json"}).c_str());
    _out << std::setw(4) << R;
    _out.close();
    return 0;
}