#include <iostream>
using namespace std;

char square[10] = {'0','1','2','3','4','5','6','7','8','9'};

int checkwin();
void board();

int main()
{
    int player = 1, choice, gameState; 
    char mark;

    do
    {
        board();
        player = (player % 2) ? 1 : 2;

        cout << "Player " << player << ", Enter a number: ";
        cin >> choice;

        mark = (player == 1) ? 'X' : 'O';

        if (choice >= 1 && choice <= 9 && square[choice] == '0' + choice)
            square[choice] = mark;
        else
        {
            cout << "Invalid move. Try again." << endl;
            continue;
        }

        gameState = checkwin();

        if (gameState == 1)
            cout << "---> \aPlayer " << player << " wins!";
        else if (gameState == 0)
            cout << "---> \aGame draw";
        else
            player++;

    } while (gameState == -1);

    cin.ignore();
    cin.get();
    return 0;
}

int checkwin()
{
    for (int i = 1; i <= 9; i += 3)
        if (square[i] == square[i + 1] && square[i + 1] == square[i + 2])
            return 1; 

    for (int i = 1; i <= 3; ++i)
        if (square[i] == square[i + 3] && square[i + 3] == square[i + 6])
            return 1; 

    if (square[1] == square[5] && square[5] == square[9])
        return 1; 

    if (square[3] == square[5] && square[5] == square[7])
        return 1; 

    for (int i = 1; i <= 9; ++i)
        if (square[i] == '0' + i)
            return -1;

    return 0;
}

void board()
{
    cout << "Tic Tac Toe Game";

    cout << "Player 1-'X'  -  Player 2-'O'" << endl << endl;
    cout << "     |     |     " << endl;

    for (int i = 1; i <= 9; i += 3)
        cout << "  " << square[i] << "  |  " << square[i + 1] << "  |  " << square[i + 2] << endl
             << "_____|_____|_____" << endl;

    cout << "     |     |     " << endl << endl;
}
