#include <iostream>
#include <fstream>

struct fullfile {
    std::ifstream p;
    fullfile () {}
    fullfile (char * path) {p = std::ifstream(path);}
    
    int next_character() {
        if (p.eof()) {
            return -1;
        }
        int x = (int)p.get();
        if (x == ' ' || x == '\n' || x == '\r') return next_character();
        return x;
    }
};

int main(int args, char * argv[]) {
    if (args != 3) {
        std::cout << "Invalid input." << std::endl;
        return -1;
    }
    char * path1 = argv[1];
    char * path2 = argv[2];
    auto f1 = fullfile(path1);
    auto f2 = fullfile(path2);

    while (true) {
        int c1 = f1.next_character();
        int c2 = f2.next_character();
        if (c1 != c2) {
            std::cout << 1 << std::endl;
            return 1;
        }
        if (c1 == c2 && c1 == -1) {
            std::cout << 0 << std::endl;
            return 0;
        }
    }
}